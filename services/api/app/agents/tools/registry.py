from typing import Dict
from .base import Tool
from app.agents.schemas import ActionType


class ToolRegistry:
    def __init__(self):
        self.tools: Dict[ActionType, Tool] = {}

    def register(self, tool: Tool):
        self.tools[tool.name] = tool

    def run(self, action: ActionType, input: str) -> str:
        if action not in self.tools:
            raise ValueError(f"Unknown tool: {action}")
        return self.tools[action].run(input)

    def list_tools(self):
        return list(self.tools.keys())


tool_registry = ToolRegistry()
