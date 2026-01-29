from pydantic import BaseModel


class LoginRequest(BaseModel):
    user_id: str
    password: str


class RegisterRequest(BaseModel):
    user_id: str
    password: str
    role: str = "user"


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
