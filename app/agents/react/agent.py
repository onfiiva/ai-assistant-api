import asyncio
import re
from app.agents.memory import summarize
from app.agents.memory.base import AgentMemory
from app.agents.state import AgentState
from app.llm.runner import run_llm_async
from app.llm.factory import LLMClientFactory
from app.agents.schemas import AgentStep, ActionType
from app.agents.actions import execute_action
from app.llm.config import DEFAULT_GEN_CONFIG


class ReActAgent:
    def __init__(
        self,
        memory: AgentMemory,
        provider: str,
        max_steps: int = 10,
        generation_config: dict | None = None,
        min_steps: int = 3,
        tool_timeout: int = 5,
        planner_timeout: int = 120,
        max_cost: float | None = None,
    ):
        if min_steps > max_steps:
            raise ValueError("min_reasoning_steps cannot exceed max_steps")
        self.max_steps = max_steps
        self.min_steps = min_steps
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

            if state.finished:
                break

            state = await self.tool_node(state, timeout=self.tool_timeout)

            state = await self.memory_node(state)

        return state.final_answer or "Stopped"

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

        FORMAT 1:
        Thought: <one line>
        Action: <action>
        ActionInput: <input>

        FORMAT 2:
        Thought: <one line>
        Final: <answer>

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

        # Final
        final_match = re.search(
            r"Thought:\s*(.*?)\nFinal:\s*(.*)",
            text,
            re.DOTALL
        )
        if final_match:
            return AgentStep(
                thought=final_match.group(1).strip(),
                action=ActionType.FINISH,
                action_input=final_match.group(2).strip(),
            )

        # Action
        action_match = re.search(
            r"Thought:\s*(.*?)\nAction:\s*(.+)\nActionInput:\s*(.*)",
            text,
            re.DOTALL
        )
        if action_match:
            raw_action = action_match.group(2).strip()

            clean_action = re.sub(
                r"ActionType\.?",
                "",
                raw_action,
                flags=re.IGNORECASE
            ).lower()

            if (
                clean_action not in ActionType.__members__.keys()
                and clean_action not in [a.value for a in ActionType]
            ):
                raise ValueError(f"Unknown action from LLM: {clean_action}")

            return AgentStep(
                thought=action_match.group(1).strip(),
                action=ActionType(clean_action),
                action_input=action_match.group(3).strip(),
            )

        raise ValueError(
            f"Invalid agent response format:\n{text}"
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

        cost = self._compute_cost(response.usage)
        state.total_cost += cost

        parsed = self._parse(response.result.text)

        state.history.append({
                "thought": parsed.thought,
                "action": parsed.action,
                "observation": None,
            })

        if parsed.action == ActionType.FINISH and state.step < self.min_steps:
            state.history.append({
                "thought": parsed.thought,
                "action": parsed.action,
                "observation": "Minimum reasoning steps not reached"
            })
            return state

        if parsed.action == ActionType.FINISH:
            state.finished = True
            state.final_answer = parsed.action_input
            return state

        state.next_action = parsed

        return state

    async def executor_node(self, action_step: AgentStep, timeout: float) -> str:
        """Doing action and returns Observation"""
        try:
            observation = await asyncio.wait_for(
                execute_action(action_step.action, action_step.action_input or ""),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            observation = f"Stopped: timeout during {action_step.action.value}"
        return observation

    async def tool_node(self, state: AgentState, timeout: float = 5.0) -> AgentState:
        if not state.next_action:
            return state
        parsed = state.next_action

        state.last_actions.append(parsed.action.value)
        state.last_actions = state.last_actions[-5:]

        if len(state.last_actions) >= 3:
            if len(set(state.last_actions[-3:])) == 1:
                state.finished = True
                state.final_answer = "Stopped: repeated action loop"
                return state

        observation = await self.executor_node(action_step=parsed, timeout=timeout)

        state.history[-1]["observation"] = observation
        state.step += 1

        return state

    async def memory_node(self, state: AgentState) -> AgentState:
        # Retrieval
        state.memory_chunks = await self.memory.retrieve(
            state.agent_id,
            state.goal,
            k=3
        )

        # Compression
        if len(state.history) > 6:
            summary = await summarize(
                state.history[:-3]
            )
            state.history = [
                {"summary": summary},
                *state.history[-3:]
            ]

        return state
