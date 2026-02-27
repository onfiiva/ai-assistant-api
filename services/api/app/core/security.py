from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.core.config import settings
from passlib.context import CryptContext

# BCrypt setting
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# ==== JWT ====
def create_access_token(
    subject: str,
    role: str,
) -> str:
    expire = datetime.utcnow() + timedelta(
        minutes=settings.JWT_EXPIRE_MINUTES
    )

    payload = {
        "sub": subject,
        "role": role,
        "exp": expire
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
    except JWTError:
        return {}


# ==== Passwords ====
def hash_password(password: str) -> str:
    """
    Creates password hash for DB
    """
    truncated = password[:72]
    return pwd_context.hash(truncated)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Checks login password
    """
    truncated = plain_password[:72]
    return pwd_context.verify(truncated, hashed_password)
