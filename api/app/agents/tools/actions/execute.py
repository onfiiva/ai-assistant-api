import asyncio
import json
from app.agents.schemas import ActionType
from app.agents.tools.registry import tool_registry
from app.agents.tools.base import Tool


def execute_action(action: ActionType, action_input: str) -> str:
    """
    Universal call registered instruments.
    Async instruments execute via asyncio.run().
    """
    tool: Tool | None = tool_registry.get(action)
    if not tool:
        return f"No tool registered for action {action}"

    # Try parse input as JSON
    try:
        parsed_input = json.loads(action_input)
    except Exception:
        parsed_input = action_input  # if not JSON, stay str

    # if async tool
    if getattr(tool, "run", None) and asyncio.iscoroutinefunction(tool.run):
        return asyncio.run(tool.run(parsed_input))

    # sync tool
    if getattr(tool, "run", None):
        return tool.run(parsed_input)

    return f"Tool {tool.name} has no run() method"
