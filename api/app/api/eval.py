from fastapi import APIRouter
from app.services.chat_service import ChatService
from app.services.rag_service import RAGService
from app.llm.factory import LLMClientFactory
from app.llm.config import EVAL_GEN_CONFIG

router = APIRouter(prefix="/eval", tags=["Evaluation"])

chat_service = ChatService()


@router.post("/base")
async def eval_base(prompt: str):

    result = await chat_service.chat(
        prompt=prompt,
        provider="qwen",
        gen_config=EVAL_GEN_CONFIG,
        instruction="",
        timeout=30,
        request=None
    )

    return result


@router.post("/finetuned")
async def eval_finetuned(prompt: str):

    result = await chat_service.chat(
        prompt=prompt,
        provider="qwen",
        gen_config={**EVAL_GEN_CONFIG, "mode": "lora"},
        instruction="",
        timeout=30,
        request=None
    )

    return result


@router.post("/rag")
async def eval_rag(question: str):

    rag = RAGService(
        embedding_provider="gemini",
        top_k=5
    )

    llm_factory = LLMClientFactory()
    llm_client = llm_factory.get("qwen")

    result = await rag.answer(
        question=question,
        llm_client=llm_client,
        gen_config=EVAL_GEN_CONFIG,
        request=None
    )

    return result
