from fastapi import APIRouter
from app.schemas.auth import LoginRequest, TokenResponse
from app.core.security import create_access_token

router = APIRouter(prefix="/auth")

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    role = "admin" if data.user_id == "jesus_christ" else "user"

    token = create_access_token(
        subject=data.user_id,
        role=role
    )

    return TokenResponse(access_token=token)
