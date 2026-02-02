from fastapi import Request
from app.core.timing import track_timing
from app.embeddings.factory import get_embedding_client
from app.embeddings.service import EmbeddingService
from app.embeddings.schemas import SimilarityResult
from app.llm.runner import run_llm
from app.core.config import settings

DEBUG = settings.DEBUG_MODE


class RAGService:
    SYSTEM_PROMPT = """
    Ты — AI-ассистент, который отвечает ТОЛЬКО на основе предоставленного контекста.
    Если ответа нет в контексте — ответь: "Информация не найдена в документах".
    Не используй внешние знания.
    """.strip()

    def __init__(
        self,
        embedding_provider: str = "gemini",
        top_k: int = 5
    ):
        client = get_embedding_client(embedding_provider)
        self.embedding_service = EmbeddingService(client)
        self.top_k = top_k

    def embed_question(self, question: str) -> list[float]:
        """
        Turns user's question into vector embedding
        """
        if not question or not question.strip():
            raise ValueError("Question cannot be empty")

        embedding = self.embedding_client.embed(question)

        if not embedding:
            raise RuntimeError("Failed to compute embedding for question")

        return embedding

    async def answer(
        self,
        question: str,
        llm_client,
        gen_config: dict,
        timeout: float = 30.0,
        request: Request | None = None
    ):
        """
        1. Embed question
        2. Search top-k chunks
        3. Assemble prompt
        4. Call LLM
        5. Return answer + sources
        """
        # 1. Find top_k docs via EmbeddedService
        top_chunks: list[SimilarityResult] = await self.embedding_service.most_similar(
            query=question,
            top_k=self.top_k,
            request=request
        )

        # --- DEBUG LOGGING ---
        if DEBUG:
            print(f"[DEBUG] Retrieved {len(top_chunks)} chunks:")
            for i, c in enumerate(top_chunks):
                print(f"Chunk {i+1} (score={c.score:.4f}): {c.document[:200]}...")

        if not top_chunks:
            return {
                "answer": "Информация не найдена в документах",
                "sources": []
            }

        # Reranking top chunks if top_k ≥ 5
        if self.top_k >= 5:
            top_chunks = sorted(
                top_chunks,
                key=lambda x: x.score,
                reverse=True
            )[:self.top_k]

        # 2. Building prompt
        context = "\n\n".join(f"[{i+1}] {c.document}" for i, c in enumerate(top_chunks))
        prompt = f"CONTEXT:\n{context}\n\nQUESTION:\n{question}"

        # 3. Call LLM
        if request:
            with track_timing(request, "llm_ms"):
                response = run_llm(
                    prompt=prompt,
                    gen_config=gen_config,
                    client=llm_client,
                    instruction=[self.SYSTEM_PROMPT],
                    timeout=timeout
                )
        else:
            response = run_llm(
                prompt=prompt,
                gen_config=gen_config,
                client=llm_client,
                instruction=[self.SYSTEM_PROMPT],
                timeout=timeout
            )

        # 4. Returns answer + sources
        return {
            "answer": response,
            "sources": [
                {
                    "index": i+1,
                    "text": c.document,
                    "score": c.score
                }
                for i, c in enumerate(top_chunks)
            ]
        }
