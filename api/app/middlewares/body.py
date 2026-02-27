from fastapi import Request


async def body_middleware(request: Request, call_next):
    if request.method in ("POST", "PUT", "PATCH"):
        try:
            request.state.body = await request.json()
        except Exception:
            request.state.body = None

    response = await call_next(request)
    return response
