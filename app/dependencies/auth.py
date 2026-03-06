from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_access_token
from app.models.user import UserContext

bearer_scheme = HTTPBearer(auto_error=False)  # if False, you can return 401 custom


def auth_dependency(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> UserContext:
    """
    JWT auth via Swagger UI
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = credentials.credentials
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return UserContext(
        id=payload.get("sub"),
        role=payload.get("role", "user")
    )


def require_admin(user: UserContext = Depends(auth_dependency)) -> UserContext:
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return user
