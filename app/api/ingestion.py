from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, Query
from app.dependencies.auth import auth_dependency
from app.dependencies.rate_limit import rate_limit_dependency
from app.services.ingestion import EmbeddingLimitExceeded, ingest_pdf

router = APIRouter(
    prefix="/ingestion",
    tags=["ingestion"],
    dependencies=[Depends(auth_dependency)]
)


@router.post("/ingest")
async def ingest(
    request: Request,
    file: UploadFile,
    source: str = Query(..., description="Источник документа"),
    _: None = Depends(rate_limit_dependency)
):
    if not hasattr(request.state, "timings"):
        request.state.timings = {}
    # file.file → transmit file-like obj
    try:
        result = await ingest_pdf(
            file.file,
            source,
            timings=request.state.timings,
            tokens=request.state.tokens,
        )
    except EmbeddingLimitExceeded as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ingestion failed: {str(e)}. Probably, PDF is to big for limits."
        )
    return {"status": "ok", **result}
