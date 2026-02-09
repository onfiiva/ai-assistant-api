from .base import Tool
from app.agents.schemas import ActionType


class SearchTool(Tool):
    name = ActionType.SEARCH

    def run(self, input: str) -> str:
        return f"Search results for: {input}"
