import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import logger

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.timings = {}

        start = time.perf_counter()
        try:
            response = await call_next(request)
            return response
        finally:
            total_ms = (time.perf_counter() - start) * 1000

            # общий тайминг
            logger.info(
                "request completed",
                extra={
                    "path": request.url.path,
                    "method": request.method,
                    "latency_ms": round(total_ms, 2),
                },
            )

            # breakdown всех шагов
            if hasattr(request.state, "timings") and request.state.timings:
                breakdown = ", ".join(f"{k}={v}ms" for k, v in request.state.timings.items())
                logger.info(f"request breakdown: {breakdown}")
