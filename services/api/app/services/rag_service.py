from fastapi import HTTPException, Request
from app.core.timing import track_timing
from app.core.tokens import count_tokens, track_tokens
from app.embeddings.factory import get_embedding_client
from app.embeddings.service import EmbeddingService
from app.embeddings.schemas import SimilarityResult
from app.llm.runner import run_llm_async
from app.core.config import settings

DEBUG = settings.DEBUG_MODE
MAX_PROMPT_TOKENS = 8000  # restriction for prompt tokens


class RAGService:
    SYSTEM_PROMPT = """
    Ты — AI-ассистент, который отвечает ТОЛЬКО на основе предоставленного контекста.
    Если ответа нет в контексте — ответь: "Информация не найдена в документах".
    Не используй внешние знания.
    """.strip()

    def __init__(self, embedding_provider: str = "gemini", top_k: int = 5):
        client = get_embedding_client(embedding_provider)
        self.embedding_service = EmbeddingService(client)
        self.top_k = top_k

    async def answer(
        self,
        question: str,
        llm_client,
        gen_config: dict,
        timeout: float = 30.0,
        request: Request | None = None,
    ):
        # 1️⃣ Semantic search
        if request:
            with track_timing(request, "vector_search"):
                top_chunks: list[SimilarityResult] = (
                    await self.embedding_service.most_similar(
                        query=question,
                        top_k=self.top_k,
                        request=request,
                    )
                )
        else:
            top_chunks = await self.embedding_service.most_similar(
                query=question,
                top_k=self.top_k,
                request=None,
            )

        if DEBUG:
            print(f"[DEBUG] Retrieved {len(top_chunks)} chunks")

        if not top_chunks:
            raise HTTPException(status_code=404, detail="Information not found in docs")

        # 2️⃣ Extractive filtering: leave only the chunks where keywords occur
        keywords = [w.lower() for w in question.split() if len(w) > 2]
        filtered_chunks = [
            c for c in top_chunks
            if any(k in c.document.lower() for k in keywords)
        ]
        if DEBUG:
            print(f"[DEBUG] Filtered to {len(filtered_chunks)} "
                  "chunks after keyword filter")

        if not filtered_chunks:
            filtered_chunks = top_chunks[:self.top_k]  # fallback on top-k

        # 3️⃣ Build token-limited context
        context = []
        context_tokens = 0
        for i, c in enumerate(filtered_chunks):
            chunk_text = f"[{i+1}] {c.document}"
            t = count_tokens(chunk_text)
            if context_tokens + t > MAX_PROMPT_TOKENS:
                break
            context.append(chunk_text)
            context_tokens += t

        prompt_context = "\n\n".join(context)

        prompt = f"""CONTEXT:
        {prompt_context}

        QUESTION:
        {question}
        """

        # 4️⃣ LLM call
        if request:
            with track_timing(request, "llm_call"):
                with track_tokens(request, "rag_prompt", prompt):
                    response = await run_llm_async(
                        prompt=prompt,
                        gen_config=gen_config,
                        client=llm_client,
                        instruction=[self.SYSTEM_PROMPT],
                        timeout=timeout,
                    )

                # фиксируем usage
                usage = (response.meta or {}).get("raw", {}).get("usage", {})
                if usage:
                    request.state.tokens["prompt_tokens"] = (
                        request.state.tokens.get("prompt_tokens", 0)
                        + usage.get("prompt_tokens", 0)
                    )
                    request.state.tokens["completion_tokens"] = (
                        request.state.tokens.get("completion_tokens", 0)
                        + usage.get("completion_tokens", 0)
                    )
                    request.state.tokens["total_tokens"] = (
                        request.state.tokens.get("total_tokens", 0)
                        + usage.get("total_tokens", 0)
                    )
        else:
            response = await run_llm_async(
                prompt=prompt,
                gen_config=gen_config,
                client=llm_client,
                instruction=[self.SYSTEM_PROMPT],
                timeout=timeout,
            )

        # 5️⃣ Return
        return {
            "answer": response.result.text,
            "sources": [
                {"index": i + 1, "text": c.document, "score": c.score}
                for i, c in enumerate(filtered_chunks)
            ],
            "meta": response.meta,
        }
