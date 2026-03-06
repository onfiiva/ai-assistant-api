from pydantic import BaseModel


class EvalRequest(BaseModel):
    prompt: str