from .base import Tool
from app.agents.schemas import ActionType

class SummaryTool(Tool):
    name = ActionType.SUMMARY  # Добавим в ActionType

    def run(self, input: str) -> str:
        # Simplest mock-summary: pick first 50 letters
        return input[:50] + "..." if len(input) > 50 else input
