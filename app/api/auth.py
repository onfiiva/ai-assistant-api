from fastapi import APIRouter, Depends
from app.dependencies.auth import require_admin
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.infra.db.pg import get_session

from app.services.auth_service import authenticate_user, register_user_service

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_session)
):

    token = await authenticate_user(
        user_id=data.user_id,
        password=data.password,
        db=db
    )

    return TokenResponse(access_token=token)


@router.post("/register", response_model=TokenResponse)
async def register_user(
    data: RegisterRequest,
    db: AsyncSession = Depends(get_session),
    _: None = Depends(require_admin)
):
    token = await register_user_service(
        user_id=data.user_id,
        password=data.password,
        role=data.role,
        db=db
    )
    return TokenResponse(access_token=token)
