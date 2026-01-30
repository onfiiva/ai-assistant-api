from fastapi import APIRouter, Depends, UploadFile, Query
from app.dependencies.auth import auth_dependency
from app.dependencies.rate_limit import rate_limit_dependency
from app.services.ingestion import ingest_pdf

router = APIRouter(
    prefix="/ingestion",
    tags=["ingestion"],
    dependencies=[Depends(auth_dependency)]
)


@router.post("/ingest")
async def ingest(
    file: UploadFile,
    source: str = Query(..., description="Источник документа"),
    _: None = Depends(rate_limit_dependency)
):
    result = await ingest_pdf(file.file, source)  # file.file → передаём file-like объект
    return {"status": "ok", **result}
