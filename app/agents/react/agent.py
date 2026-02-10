import re
from app.agents.memory.base import AgentMemory
from app.llm.runner import run_llm
from app.llm.factory import LLMClientFactory
from app.agents.schemas import AgentStep, ActionType
from app.agents.actions import execute_action
from app.core.logging import logger
from app.llm.config import DEFAULT_GEN_CONFIG


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

            logger.error(
                "RAW LLM RESPONSE (agent):\n%s",
                llm_response
            )

            parsed = self._parse(llm_response.result.text)

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

        Goal:
        {goal}

        History:
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
