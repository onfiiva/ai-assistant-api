from .base import Tool
from app.agents.schemas import ActionType
import json


class ExternalAPITool(Tool):
    name = ActionType.EXTERNAL_API

    def run(self, input: str) -> str:
        # Mock call external API
        response = {"query": input, "result": f"Response for '{input}'"}
        return json.dumps(response)
