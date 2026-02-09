from app.agents.memory.base import AgentMemory
from app.llm.runner import run_llm
from app.llm.factory import LLMClientFactory
from app.agents.schemas import AgentStep, ActionType
from app.agents.actions import execute_action
from app.core.logging import logger
from app.core.config import settings
from app.llm.config import DEFAULT_GEN_CONFIG


class ReActAgent:
    def __init__(self, memory: AgentMemory, max_steps: int = 2):
        self.max_steps = max_steps
        self.gen_config = DEFAULT_GEN_CONFIG
        self.memory = memory

        llm_factory = LLMClientFactory()
        self.llm_client = llm_factory.get(settings.DEFAULT_PROVIDER)

    def run(self, agent_id: str, goal: str) -> str:
        history = self.memory.load(agent_id)

        for step in range(self.max_steps):
            prompt = self._build_prompt(goal, history)

            logger.debug(f"Agent prompt:\n{prompt}")

            llm_response = run_llm(
                prompt=prompt,
                gen_config=self.gen_config,
                client=self.llm_client
            )

            parsed = self._parse(llm_response)

            logger.info(f"[STEP {step+1}] Thought: {parsed.thought}")
            logger.info(f"[STEP {step+1}] Action: {parsed.action}")

            if parsed.action == ActionType.FINISH:
                return parsed.action_input or ""

            observation = execute_action(
                parsed.action,
                parsed.action_input or ""
            )

            logger.info(f"[STEP {step+1}] Observation: {observation}")

            history.append({
                "thought": parsed.thought,
                "action": parsed.action,
                "observation": observation,
            })

            self.memory.save(agent_id, history)

        return "Agent stopped: max steps reached"

    def _build_prompt(self, goal: str, history: list) -> str:
        prompt = f"""
        You are a ReAct agent.

        Goal:
        {goal}

        You must respond ONLY in one of the formats:

        Thought: ...
        Action: search
        ActionInput: ...

        OR

        Thought: ...
        Final: ...

        History:
        """.strip()

        for h in history:
            prompt += f"""
        Thought: {h['thought']}
        Action: {h['action']}
        Observation: {h['observation']}
        """

        return prompt

    def _parse(self, text: str) -> AgentStep:
        if "Final:" in text:
            thought, final = text.split("Final:", 1)
            return AgentStep(
                thought=thought.replace("Thought:", "").strip(),
                action=ActionType.FINISH,
                action_input=final.strip(),
            )

        if "Action:" in text:
            lines = text.splitlines()
            thought = lines[0].replace("Thought:", "").strip()
            action = lines[1].replace("Action:", "").strip()
            action_input = lines[2].replace("ActionInput:", "").strip()

            return AgentStep(
                thought=thought,
                action=ActionType(action),
                action_input=action_input,
            )

        raise ValueError("Invalid agent response format")
