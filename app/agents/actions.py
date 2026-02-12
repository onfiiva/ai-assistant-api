from app.agents.schemas import ActionType
from app.agents.tools.vector_search_async import VectorSearchTool

vector_search_tool = VectorSearchTool()


async def execute_action(action: ActionType, action_input: str) -> str:
    if action == ActionType.VECTOR_SEARCH:
        # action_input can be parsed as JSON {"query": "...", "top_k": 5}
        import json
        data = json.loads(action_input)
        return await vector_search_tool.run(data)
    # ... other actions
    return f"Executed {action} with input: {action_input}"
