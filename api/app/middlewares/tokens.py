from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class TokensMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.tokens = {}
        response = await call_next(request)
        return response
