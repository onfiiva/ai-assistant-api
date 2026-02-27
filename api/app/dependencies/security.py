import json
from datetime import datetime
from fastapi import Request, HTTPException, Depends

from app.core.config import settings
from app.models.user import UserContext
from app.dependencies.auth import auth_dependency


LOG_FILE = "/app/logs/security.log"


def log_instruction(data: dict):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def security_dependency(
    request: Request,
    user: UserContext = Depends(auth_dependency),
):
    body = request.state.body

    forbidden = settings.FORBIDDEN_COMMANDS

    if not body:
        return

    text = body.get("prompt", "") + " " + (body.get("instruction") or "")

    for cmd in forbidden:
        if cmd.lower() in text.lower():
            log_instruction({
                "timestamp": datetime.utcnow().isoformat(),
                "event": "forbidden_command",
                "command": cmd,
                "user_id": user.id,
                "role": user.role,
                "ip": request.client.host if request.client else None,
                "user_agent": request.headers.get("user-agent"),
            })

            raise HTTPException(
                status_code=403,
                detail="Forbidden command detected"
            )
