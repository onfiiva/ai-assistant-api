from fastapi import APIRouter, UploadFile, Query
from app.services.ingestion import ingest_pdf

router = APIRouter()


@router.post("/ingest")
async def ingest(
    file: UploadFile,
    source: str = Query(..., description="Источник документа")
):
    result = await ingest_pdf(file.file, source)  # file.file → передаём file-like объект
    return {"status": "ok", **result}
