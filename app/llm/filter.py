import re
import unicodedata
from app.core.config import settings


class SystemCommandDetected(ValueError):
    pass


def normalize_prompt(text: str) -> str:
    # Unicode normalize
    text = unicodedata.normalize("NFKD", text)

    # Lowercase
    text = text.lower()

    # Remove zero-width and control chars
    text = re.sub(r"[\u200b-\u200f\uFEFF]", "", text)

    # Collapse spaces
    text = re.sub(r"\s+", " ", text)

    # Replace common leetspeak
    replacements = {
        "0": "o",
        "1": "i",
        "3": "e",
        "4": "a",
        "5": "s",
        "7": "t",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)

    return text.strip()


def detect_instruction_form(text: str) -> bool:
    for pattern in settings.INSTRUCTION_REGEX:
        if re.search(pattern, text):
            return True
    return False


def detect_role_override(text: str) -> bool:
    for pattern in settings.ROLE_OVERRIDE_REGEX:
        if re.search(pattern, text):
            return True
    return False


def detect_system_meta_request(text: str) -> bool:
    for pattern in settings.META_SYSTEM_REGEX:
        if re.search(pattern, text):
            return True
    return False


def system_command_risk_score(prompt: str) -> int:
    text = normalize_prompt(prompt)
    score = 0

    if detect_instruction_form(text):
        score += 2

    if detect_role_override(text):
        score += 3

    if detect_system_meta_request(text):
        score += 3

    # suspicious length (instructions are often long)
    if len(text.split()) > 80:
        score += 1

    return score


def filter_system_commands(prompt: str) -> str:
    score = system_command_risk_score(prompt)

    if score >= 3:
        raise SystemCommandDetected(
            f"Potential system command injection detected (risk_score={score})"
        )

    return prompt


def detect_instruction_attack(prompt: str) -> None:
    lowered = prompt.lower()

    for pattern in settings.INSTRUCTION_PATTERNS:
        if pattern in lowered:
            raise ValueError(
                f"Instruction injection detected: '{pattern}'"
            )


def detect_exfiltration_attempt(prompt: str) -> None:
    lowered = prompt.lower()
    for pattern in settings.EXFILTRATION_PATTERNS:
        if pattern in lowered:
            raise ValueError(
                f"Potential data exfiltration attempt: '{pattern}'"
            )


def refusal_response(reason: str):
    return {
        "status": "refused",
        "reason": reason,
        "answer": """
        I can’t help with this request,
        but I can explain related concepts safely.
        """,
        "confidence": "high"
    }


def validate_llm_output(output) -> bool:
    if not output:
        return False

    if isinstance(output, dict):
        text = output.get("answer") or output.get("text")
    else:
        text = str(output)

    if not text:
        return False

    if len(text) > settings.MAX_RESPONSE_LENGTH:
        return False

    lowered = text.lower()
    if any(f in lowered for f in settings.FORBIDDEN_LLM_OUTPUT):
        return False

    return True
