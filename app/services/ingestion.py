import uuid
from typing import List
from app.core.timing import track_timing
from app.infra.pdf_loader import load_pdf
from app.infra.chunker import chunk_text
from app.embeddings.factory import get_embedding_client
from app.infra.db.pg import session_context
from app.infra.db.qdrant import upsert_embedding, create_collection
from app.infra.db.models.models import Document, Embedding
from app.core.config import settings

CHUNK_SIZE = 500  # Example
CHUNK_OVERLAP = 50


async def ingest_pdf(file_path: str, source: str, timings: dict):
    create_collection()
    # PDF → text
    if timings is not None:
        with track_timing(timings, "load_pdf"):
            text = load_pdf(file_path)
    else:
        text = load_pdf(file_path)

    # text → chunks
    if timings is not None:
        with track_timing(timings, "chunk_text"):
            chunks: List[str] = chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP)
    else:
        chunks: List[str] = chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP)

    # chunks → embeddings
    embedding_client = get_embedding_client(provider=settings.EMBEDDING_PROVIDER)
    if timings is not None:
        with track_timing(timings, "embedding_generation"):
            vectors = await embedding_client.embed(chunks)
    else:
        vectors = await embedding_client.embed(chunks)

    # save to PG & Qdrant
    if timings is not None:
        with track_timing(timings, "db_qdrant_upsert"):
            async with session_context() as session:
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

                    emb_id = str(uuid.uuid5(uuid.UUID(doc_id), str(idx)))
                    upsert_embedding(id=emb_id, vector=vector, content=chunk)

                await session.commit()
    else:
        async with session_context() as session:
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

                emb_id = str(uuid.uuid5(uuid.UUID(doc_id), str(idx)))
                upsert_embedding(id=emb_id, vector=vector, content=chunk)

            await session.commit()

    return {"document_id": doc_id, "num_chunks": len(chunks)}
