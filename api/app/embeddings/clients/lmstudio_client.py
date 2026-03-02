from typing import Dict, Any, List, Optional

from .base.http_client import BaseHTTPClient
from .base.embedding_client import EmbeddingClient


class LMStudioEmbeddingClient(EmbeddingClient, BaseHTTPClient):

    def __init__(self, base_url: str, model: str, api_key: Optional[str] = None):
        BaseHTTPClient.__init__(self, base_url, api_key)
        self.model_name = model

    async def embed(self, texts: List[str]) -> Dict[str, Any]:

        payload = {
            "model": self.model_name,
            "input": texts
        }

        response = await self._post(
            "/v1/embeddings",
            payload,
            timeout=120.0
        )

        data = response.json()

        return {
            "embeddings": [d["embedding"] for d in data["data"]],
            "provider": "lmstudio",
            "usage": data.get("usage")
        }
