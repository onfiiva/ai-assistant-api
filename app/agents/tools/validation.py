from pydantic import BaseModel, Field, ValidationError


class VectorSearchArgs(BaseModel):
    query: str = Field(..., description="Request text for search")
    top_k: int = Field(
        5,
        description="Search results count (1-20)",
        ge=1,
        le=20
    )

class SummaryArgs(BaseModel):
    text: str

class ExternalAPIArgs(BaseModel):
    endpoint: str
    payload: str

def validate_args(schema: BaseModel, args: dict):
    try:
        return schema(**args)
    except ValidationError as e:
        raise ValueError(f"Invalid arguments: {e}")
