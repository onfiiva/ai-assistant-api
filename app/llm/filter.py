from app.core.config import settings


def filter_system_commands(prompt: str) -> str:
    """
    Checks whether there are no forbidden commands in the prompt
    If there is, throws ValueError
    """
    for cmd in settings.FORBIDDEN_COMMANDS:
        if cmd.lower() in prompt.lower():
            raise ValueError(f"Use of forbidden system command detected: '{cmd}'")
