from fastapi import Header, HTTPException
from app.models.user import UserContext
from app.core.security import decode_access_token


async def get_current_user(authorization: str = Header(...)) -> UserContext:
    """
    Get user from JWT token w/o DB req
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")

    token = authorization.split(" ")[1]
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("sub")
    role = payload.get("role", "user")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    return UserContext(id=user_id, role=role)
