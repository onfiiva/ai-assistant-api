import traceback
from fastapi import APIRouter, HTTPException, Depends

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
