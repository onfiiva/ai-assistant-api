import traceback
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel, Field
from typing import Optional, Dict

from app.dependencies.rate_limit import rate_limit_dependency
from app.dependencies.security import security_dependency
from app.dependencies.auth import auth_dependency
from app.llm.sanitizer import sanitize_user_prompt
from app.models.user import UserContext
from app.services.tts_service import TTSService
from app.schemas.tts import TTSResponse, TTSRequest

router = APIRouter(
    prefix="/tts",
    tags=["TTS"],
    dependencies=[
        dependencies=[Depends(auth_dependency)]
    ]
)

tts_service = TTSService()


@router.post("/", response_model=TTSResponse)
async def generate_tts(
    req: TTSRequest,
    request: Request,
    user: UserContext = Depends(auth_dependency)
):
    try:
        if not req.prompt.strip():
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")

        try:
            safe_prompt = sanitize_user_prompt(req.prompt)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid prompt: {str(e)}")

        # ===== Call TTS Service =====
        tts_output = await tts_service.generate(
            prompt=safe_prompt,
            speaker=req.speaker,
            language=req.language,
            gen_config=req.gen_config,
            request=request
        )

        return tts_output

    except HTTPException:
        raise

    except Exception:
        print("=== TTS endpoint error ===")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")
