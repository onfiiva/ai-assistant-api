import uuid
from typing import List
from app.infra.pdf_loader import load_pdf
from app.infra.chunker import chunk_text
from app.embeddings.factory import get_embedding_client
from app.infra.db.pg import get_session
from app.infra.db.qdrant import upsert_embedding, create_collection
from app.infra.db.models import Document, Embedding
from app.core.config import settings

CHUNK_SIZE = 500  # Example
CHUNK_OVERLAP = 50


async def ingest_pdf(file_path: str, source: str):
    create_collection()
    # PDF → text
    text = load_pdf(file_path)

    # text → chunks
    chunks: List[str] = chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP)

    # chunks → embeddings
    embedding_client = get_embedding_client(provider=settings.EMBEDDING_PROVIDER)
    vectors = await embedding_client.embed(chunks)

    # save to PG & Qdrant
    async with get_session() as session:
        doc_id = str(uuid.uuid4())
        session.add(Document(id=doc_id, source=source))

        for idx, (chunk, vector) in enumerate(zip(chunks, vectors)):
            emb_id = str(uuid.uuid4())
            session.add(
                Embedding(
                    id=emb_id,
                    document_id=doc_id,
                    chunk_index=idx,
                    content=chunk,
                    embedding=vector
                )
            )
            upsert_embedding(id=f"{doc_id}_{idx}", vector=vector, content=chunk)

        await session.commit()

    return {"document_id": doc_id, "num_chunks": len(chunks)}
