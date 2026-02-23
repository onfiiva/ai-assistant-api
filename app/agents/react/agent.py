import asyncio
import re
from app.agents.memory.summarize import summarize_history
from app.agents.memory.base import AgentMemory
from app.agents.state import AgentState
from app.llm.runner import run_llm_async
from app.llm.factory import LLMClientFactory
from app.agents.schemas import AgentStep, ActionType
from app.agents.actions import execute_action
from app.llm.config import DEFAULT_GEN_CONFIG
from app.core.logging import logger


class ReActAgent:
    def __init__(
        self,
        memory: AgentMemory,
        provider: str,
        max_steps: int = 10,
        generation_config: dict | None = None,
        tool_timeout: int = 5,
        planner_timeout: int = 120,
        max_cost: float | None = None,
    ):
        self.max_steps = max_steps
        self.memory = memory
        self.gen_config = generation_config or DEFAULT_GEN_CONFIG

        self.llm_client = LLMClientFactory().get(provider)

        self.tool_timeout = tool_timeout
        self.planner_timeout = planner_timeout
        self.max_cost = max_cost

    async def run(self, agent_id: str, goal: str) -> str:
        state = AgentState(
            agent_id=agent_id,
            goal=goal
        )

        state.memory_chunks = await self.memory.retrieve(
            agent_id,
            goal,
            k=3
        )

        while not state.finished and state.step < self.max_steps:

            state = await self.planner_node(state, timeout=self.planner_timeout)

            logger.debug(f"AGENT STATE: {state}")

            if state.finished:
                break

            logger.debug("AGENT CALLING TOOL")
            state = await self.tool_node(state, timeout=self.tool_timeout)

            logger.debug("AGENT CALLING MEMORY")
            state = await self.memory_node(state)

        final_text = state.final_answer or "Stopped"
        return {
            "text": final_text,
            "finish_reason": "finished" if state.finished else "stopped",
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
            "provider": "custom-llm"
        }

    def _build_prompt(self, goal: str, history: list, memory_chunks: list) -> str:

        memory_text = "\n".join(memory_chunks)

        history_lines = []

        for h in history:
            if "summary" in h:
                history_lines.append(f"Summary:{h['summary']}")
            else:
                history_lines.append(
                    f"Thought:{h['thought']}\n"
                    f"Action:{h['action']}\n"
                    f"Observation:{h['observation']}"
                )

        history_text = "\n".join(history_lines)

        prompt = f"""
        You are a ReAct agent.

        STRICT RULES:
        - Respond in PLAIN TEXT
        - DO NOT use markdown
        - DO NOT add explanations
        - DO NOT add extra lines
        - DO NOT repeat the goal
        - Output MUST match EXACTLY one of the formats below
        - Use ONLY one of the following actions:
            search, finish, vector_search, external_api
        - ONLY return ONE Thought/Action/ActionInput block at a time.
            Do NOT include additional Thought/Observation blocks in ActionInput.
        - Do NOT output Observation or multiple blocks.
        - If action is vector_search:
            ActionInput MUST be a valid JSON object:
            {{"query": "<string>", "top_k": <integer>}}

        FORMAT:
        Thought: <one line>
        Action: <action>
        ActionInput: <single input for this action>

        Relevant past memory:
        {memory_text}

        Goal:
        {goal}

        History:
        {history_text}
        """.strip()

        return prompt

    def _parse(self, text: str) -> AgentStep:
        text = text.strip()
        # try to find Thought/Action/ActionInput
        pattern = (r"Thought:\s*(.*?)\nAction:\s*(.+?)"
                   r"(?:\nActionInput:\s*(.*?))?(?:\nThought:|$)")
        match = re.search(pattern, text, re.DOTALL)
        if match:
            thought, raw_action, action_input = match.groups()
            clean_action = re.sub(
                r"ActionType\.?",
                "",
                raw_action,
                flags=re.IGNORECASE
            ).lower()
            if clean_action not in [a.value for a in ActionType]:
                clean_action = "finish"
            return AgentStep(
                thought=thought.strip(),
                action=ActionType(clean_action),
                action_input=(action_input or "").strip()
            )
        else:
            # if no pattern - final text
            return AgentStep(
                thought="Auto-final",
                action=ActionType.FINISH,
                action_input=text
            )

    def _compute_cost(self, usage: dict) -> float:
        # E.G. for OpenAI
        # TODO: move to conf
        prompt_cost_per_1k = 0.03
        completion_cost_per_1k = 0.06

        prompt_tokens = usage.prompt_tokens or 0
        completion_tokens = usage.completion_tokens or 0

        return (
            (prompt_tokens / 1000 * prompt_cost_per_1k)
            + (completion_tokens / 1000 * completion_cost_per_1k)
        )

    async def planner_node(self, state: AgentState, timeout: float = 80.0) -> AgentState:
        logger.debug("PLANNER CALLED")
        prompt = self._build_prompt(
            state.goal,
            state.history,
            state.memory_chunks
        )

        try:
            response = await asyncio.wait_for(
                run_llm_async(
                    prompt,
                    gen_config=self.gen_config,
                    client=self.llm_client,
                    timeout=timeout
                ),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            state.finished = True
            state.final_answer = "Stopped: timeout during planning"
            return state

        logger.debug(f"PLANNER Returned response: {response}")

        cost = self._compute_cost(response.usage)
        state.total_cost += cost

        parsed = self._parse(response.result.text)

        state.history.append({
                "thought": parsed.thought,
                "action": parsed.action,
                "observation": None,
            })
        logger.debug("PLANNER history append")

        if parsed.action == ActionType.FINISH:
            logger.debug("PLANNER FINISH")
            state.finished = True

            if parsed.action_input:
                state.final_answer = parsed.action_input
            else:
                # fallback — взять последнее observation
                if state.history and state.history[-1].get("observation"):
                    state.final_answer = state.history[-1]["observation"]
                else:
                    state.final_answer = "Finished"

            return state

        state.next_action = parsed

        return state

    async def executor_node(self, action_step: AgentStep, timeout: float) -> str:
        """Doing action and returns Observation"""
        logger.debug("EXECUTOR CALLED")
        try:
            logger.debug("EXECUTOR getting observation")
            observation = await asyncio.wait_for(
                execute_action(action_step.action, action_step.action_input or ""),
                timeout=timeout
            )
            logger.debug("EXECUTOR observation got")
        except asyncio.TimeoutError:
            observation = f"Stopped: timeout during {action_step.action.value}"
        return observation

    async def tool_node(self, state: AgentState, timeout: float = 5.0) -> AgentState:
        # TODO: add logic to tool choice
        logger.debug("TOOL CALLED")
        if not state.next_action:
            logger.debug("TOOL no action")
            return state
        parsed = state.next_action
        logger.debug("TOOL parsed")

        state.last_actions.append(parsed.action.value)
        state.last_actions = state.last_actions[-5:]
        logger.debug("TOOL last actions")

        if len(state.history) >= 3:
            last_three = state.history[-3:]
            if all(
                h["action"] == last_three[0]["action"] and
                h.get("observation") == last_three[0].get("observation")
                for h in last_three
            ):
                state.finished = True
                state.final_answer = "Stopped: repeated identical steps"
                return state

        logger.debug("TOOL calling executor node")
        observation = await self.executor_node(action_step=parsed, timeout=timeout)

        logger.debug("TOOL applying history observation")
        state.history[-1]["observation"] = observation
        state.step += 1

        return state

    async def memory_node(self, state: AgentState) -> AgentState:
        logger.debug("MEMORY CALLED")
        # Retrieval
        state.memory_chunks = await self.memory.retrieve(
            state.agent_id,
            state.goal,
            k=3
        )

        logger.debug(f"MEMORY chunks: {state.memory_chunks}")

        # Compression
        if len(state.history) > 6:
            summary = await summarize_history(
                self,
                history_chunk=state.history[:-3]
            )
            state.history = [
                {"summary": summary},
                *state.history[-3:]
            ]

        return state
