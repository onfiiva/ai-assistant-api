import traceback
from fastapi import APIRouter, HTTPException, Depends, Request

from app.dependencies.rate_limit import rate_limit_dependency
from app.dependencies.security import security_dependency
from app.dependencies.auth import auth_dependency
from app.models.user import UserContext

from app.llm.adapters.base.http_client import BaseHTTPClient
from app.core.config import settings


router = APIRouter(
    prefix="/lmstudio",
    tags=["LMStudio"],
    dependencies=[Depends(auth_dependency)]
)

def get_lmstudio_client():
    return BaseHTTPClient(
        base_url=settings.LMSTUDIO_BASE_URL,
        api_key=settings.LMSTUDIO_API_KEY
    )


@router.get("/models")
async def list_models(
    user: UserContext = Depends(auth_dependency),
    client: BaseHTTPClient = Depends(get_lmstudio_client)
):
    try:
        response = await client._get(
            "/v1/models",
            timeout=30.0
        )
        return response.json()

    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Failed to fetch models")


@router.get("/models/{model_id}")
async def get_model_info(
    model_id: str,
    user: UserContext = Depends(auth_dependency),
    client: BaseHTTPClient = Depends(get_lmstudio_client)
):
    try:
        response = await client._get(
            f"/v1/models/{model_id}",
            timeout=30.0
        )
        return response.json()

    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Failed to fetch model info")


@router.post("/chat/completions")
async def chat_completions(
    payload: dict,
    user: UserContext = Depends(auth_dependency),
    client: BaseHTTPClient = Depends(get_lmstudio_client)
):
    try:
        response = await client._post(
            "/v1/chat/completions",
            json_payload=payload,
            timeout=180.0
        )

        return response.json()

    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Chat completion failed")


@router.post("/completions")
async def text_completions(
    payload: dict,
    user: UserContext = Depends(auth_dependency),
    client: BaseHTTPClient = Depends(get_lmstudio_client)
):
    try:
        response = await client._post(
            "/v1/completions",
            json_payload=payload,
            timeout=180.0
        )

        return response.json()

    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Completion failed")


@router.post("/embeddings")
async def embeddings(
    payload: dict,
    user: UserContext = Depends(auth_dependency),
    client: BaseHTTPClient = Depends(get_lmstudio_client)
):
    try:
        response = await client._post(
            "/v1/embeddings",
            json_payload=payload,
            timeout=60.0
        )

        return response.json()

    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Embedding failed")
