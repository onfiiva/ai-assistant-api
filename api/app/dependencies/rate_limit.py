from fastapi import Depends, HTTPException
from app.core.redis import redis_client
from app.core.config import settings
from app.dependencies.user import get_current_user
from app.models.user import UserContext


def rate_limit_dependency(user: UserContext = Depends(get_current_user)):
    key = f"rate_limit:{user.role}:{user.id}"

    try:
        current = redis_client.incr(key)
        if current == 1:
            redis_client.expire(key, settings.RATE_LIMIT_WINDOW)
    except Exception:
        if user.role == "admin":
            return
        raise HTTPException(status_code=503, detail="Rate limit service unavailable")

    limits = {
        "admin": settings.RATE_LIMIT_ADMIN_REQUESTS,
        "user": settings.RATE_LIMIT_USER_REQUESTS
    }
    limit = limits.get(user.role, settings.RATE_LIMIT_USER_REQUESTS)

    if current > limit:
        ttl = redis_client.ttl(key)
        raise HTTPException(
            status_code=429,
            detail="Too Many Requests",
            headers={"Retry-After": str(ttl)}
        )
