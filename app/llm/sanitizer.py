
from app.core.config import settings
from app.llm.filter import \
    detect_exfiltration_attempt, detect_instruction_attack, filter_system_commands


def sanitize_user_prompt(prompt: str) -> str:
    prompt = prompt.strip()

    if len(prompt) > settings.MAX_PROMPT_LENGTH:
        raise ValueError("Prompt too long")

    filter_system_commands(prompt)
    detect_instruction_attack(prompt)
    detect_exfiltration_attempt(prompt)

    return prompt
