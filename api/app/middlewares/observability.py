import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import logger


class ObservabilityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.timings = {}
        request.state.tokens = {}

        start = time.perf_counter()
        try:
            response = await call_next(request)
            return response
        finally:
            total_ms = (time.perf_counter() - start) * 1000

            logger.info(
                "request completed",
                extra={
                    "path": request.url.path,
                    "method": request.method,
                    "latency_ms": round(total_ms, 2),
                },
            )

            if request.state.timings:
                breakdown = ", ".join(
                    f"{k}={v}ms" for k, v in request.state.timings.items()
                )
                logger.info(f"request breakdown: {breakdown}")

            if request.state.tokens:
                tokens = ", ".join(
                    f"{k}={v}" for k, v in request.state.tokens.items()
                )
                logger.info(f"request tokens: {tokens}")
