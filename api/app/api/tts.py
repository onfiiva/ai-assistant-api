import traceback
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import StreamingResponse

from app.dependencies.auth import auth_dependency
from app.llm.sanitizer import sanitize_user_prompt
from app.models.user import UserContext
from app.services.tts_service import TTSService
from app.schemas.tts import TTSRequest

router = APIRouter(
    prefix="/tts",
    tags=["TTS"],
    dependencies=[Depends(auth_dependency)]
)

tts_service = TTSService()


@router.post("/")
async def generate_tts(
    req: TTSRequest,
    request: Request,
    user: UserContext = Depends(auth_dependency)
):
    try:
        if not req.prompt.strip():
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")

        # ===== Очистка prompt =====
        try:
            safe_prompt = sanitize_user_prompt(req.prompt)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid prompt: {str(e)}")

        # ===== Вызов локального TTS API =====
        audio_stream = await tts_service.generate(
            prompt=safe_prompt,
            speaker=req.speaker or "Vivian",
            language=req.language or "Auto",
            instruct=req.instruct or "Say fast and shortly"
        )

        filename = f"{safe_prompt[:100].strip().replace(' ', '_')}.wav"  # имя файла
        return StreamingResponse(
            audio_stream,
            media_type="audio/wav",
            headers={"Content-Disposition": f"attachment; filename*=UTF-8''{filename}"}
        )

    except HTTPException:
        raise

    except Exception:
        print("=== TTS endpoint error ===")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")
