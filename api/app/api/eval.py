from fastapi import APIRouter, Body
from app.schemas.eval import EvalRequest
from app.services.chat_service import ChatService
from app.services.rag_service import RAGService
from app.llm.factory import LLMClientFactory
from app.llm.config import EVAL_GEN_CONFIG

router = APIRouter(prefix="/eval", tags=["Evaluation"])

chat_service = ChatService()


@router.post("/base")
async def eval_base(req: EvalRequest):

    result = await chat_service.chat(
        prompt=prompt,
        provider="qwen3vl",
        gen_config={**EVAL_GEN_CONFIG, "mode": "base"},
        instruction="",
        timeout=120,
        request=None
    )

    return result


@router.post("/finetuned")
async def eval_finetuned(req: EvalRequest):
    result = await chat_service.chat(
        prompt=req.prompt,
        provider="qwen3vl",
        gen_config={**EVAL_GEN_CONFIG, "mode": "lora"},
        instruction="",
        timeout=120,
        request=None
    )
    return result


@router.post("/rag")
async def eval_rag(req: EvalRequest):

    rag = RAGService(
        embedding_provider="gemini",
        top_k=5
    )

    llm_factory = LLMClientFactory()
    llm_client = llm_factory.get("qwen")

    result = await rag.answer(
        question=req.prompt,
        llm_client=llm_client,
        gen_config=EVAL_GEN_CONFIG,
        request=None
    )

    return result
