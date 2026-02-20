import json
from app.core.config import settings
from app.embeddings.factory import get_embedding_client
from .base import Tool
from app.agents.schemas import ActionType
from app.embeddings.service import EmbeddingService
from app.agents.tools.validation import VectorSearchArgs
from app.infra.db import qdrant
import asyncio


class VectorSearchAsyncTool(Tool):
    name = ActionType.VECTOR_SEARCH

    def __init__(self):
        embedding_client = get_embedding_client(settings.EMBEDDING_PROVIDER)
        self.embedding_service = EmbeddingService(embedding_client)
        self.use_qdrant = True

    async def run(self, args: dict) -> str:
        """
        args: dict, which will be validated via VectorSearchArgs
        """
        # --- Normalize args ---
        if isinstance(args, str):
            try:
                parsed = json.loads(args)

                if isinstance(parsed, dict):
                    args = parsed

                elif isinstance(parsed, list):
                    # объединяем список в одну строку
                    args = {
                        "query": " ".join(str(x) for x in parsed),
                        "top_k": 5
                    }

                else:
                    args = {"query": str(parsed), "top_k": 5}

            except json.JSONDecodeError:
                args = {"query": args, "top_k": 5}

        elif isinstance(args, list):
            args = {
                "query": " ".join(str(x) for x in args),
                "top_k": 5
            }

        elif not isinstance(args, dict):
            args = {"query": str(args), "top_k": 5}

        # default top_k
        args.setdefault("top_k", 5)

        # 1️⃣ Validate args
        validated_args = VectorSearchArgs(**args)

        # 2️⃣ Get embedding async (if service supports async, else run_in_executor)
        embedding = await asyncio.to_thread(
            self.embedding_service.embed,
            validated_args.query
        )

        # 3️⃣ Search in Qdrant
        if self.use_qdrant:
            results = await asyncio.to_thread(
                qdrant.search, query_vector=embedding, limit=validated_args.top_k
            )
            return "\n".join([
                f"{r['content']} (score: {r['score']:.3f})"
                for r in results
            ])
        else:
            # TODO: add async FAISS if needed
            raise NotImplementedError("FAISS async search not implemented yet")
