import re
from app.agents.memory import summarize
from app.agents.memory.base import AgentMemory
from app.agents.state import AgentState
from app.agents.tools.vector_search import VectorSearchTool
from app.llm.runner import run_llm_async
from app.llm.factory import LLMClientFactory
from app.agents.schemas import AgentStep, ActionType
from app.agents.actions import execute_action
from app.llm.config import DEFAULT_GEN_CONFIG

vector_search_tool = VectorSearchTool()


class ReActAgent:
    def __init__(
        self,
        memory: AgentMemory,
        provider: str,
        max_steps: int = 2,
        generation_config: dict | None = None,
    ):
        self.max_steps = max_steps
        self.memory = memory
        self.gen_config = generation_config or DEFAULT_GEN_CONFIG

        self.llm_client = LLMClientFactory().get(provider)

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

            state = await self.planner_node(state)

            if state.finished:
                break

            state = await self.tool_node(state)

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
        - You must perform at least 3 reasoning cycles
            (Thought + Action + Observation) before giving Final answer.

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
            r"Thought:\s*(.*?)\nAction:\s*(\w+)\nActionInput:\s*(.*)",
            text,
            re.DOTALL
        )
        if action_match:
            return AgentStep(
                thought=action_match.group(1).strip(),
                action=ActionType(action_match.group(2).strip()),
                action_input=action_match.group(3).strip(),
            )

        raise ValueError(
            f"Invalid agent response format:\n{text}"
        )

    async def planner_node(self, state: AgentState) -> AgentState:
        prompt = self._build_prompt(
            state.goal,
            state.history,
            state.memory_chunks
        )

        response = await run_llm_async(
            prompt,
            gen_config=self.gen_config,
            client=self.llm_client
        )

        parsed = self._parse(response.result.text)

        state.history.append({
            "thought": parsed.thought,
            "action": parsed.action,
        })

        if parsed.action == ActionType.FINISH:
            state.finished = True
            state.final_answer = parsed.action_input
        else:
            state.next_action = parsed

        return state

    async def tool_node(self, state: AgentState) -> AgentState:
        parsed = state.next_action

        observation = await execute_action(
            parsed.action,
            parsed.action_input or ""
        )

        state.history[-1]["observation"] = observation
        state.step += 1

        return state

    async def memory_node(self, state: AgentState) -> AgentState:
        # Retrieval
        state.memory_chunks = self.memory.retrieve(
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
