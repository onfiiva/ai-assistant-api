from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from app.infra.db.models.user_model import User
from app.core.security import hash_password, verify_password, create_access_token


async def authenticate_user(user_id: str, password: str, db: AsyncSession) -> str:
    """
    Checks login + password
    Returns JWT token
    Throws 401 HTTPException if incorrect
    """
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = create_access_token(subject=user.id, role=user.role)
    return token


async def register_user_service(
    user_id: str,
    password: str,
    role: str,
    db: AsyncSession
) -> str:
    """
    Registers new user
    Returns JWT token
    Throws HTTPError 400 if user exists
    """
    # Check if user exists
    result = await db.execute(select(User).where(User.id == user_id))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    new_user = User(
        id=user_id,
        hashed_password=hash_password(password),
        role=role
    )
    db.add(new_user)
    await db.commit()

    # Generate JWT
    token = create_access_token(subject=new_user.id, role=new_user.role)
    return token
