import uuid
from typing import List
from app.core.timing import track_timing
from app.core.tokens import count_tokens
from app.core.logging import logger
from app.infra.pdf_loader import load_pdf
from app.infra.chunker import chunk_text
from app.embeddings.factory import get_embedding_client
from app.infra.db.pg import session_context
from app.infra.db.qdrant import upsert_embedding
from app.infra.db.models.models import Document, Embedding
from app.core.config import settings

CHUNK_SIZE = 500  # Example
CHUNK_OVERLAP = 50
MAX_EMBED_CHUNKS = settings.MAX_EMBED_CHUNKS
MAX_EMBED_TOKENS = settings.MAX_EMBED_TOKENS


class EmbeddingLimitExceeded(Exception):
    """Raised when ingestion exceeds MAX_EMBED_CHUNKS or MAX_EMBED_TOKENS"""
    pass


async def ingest_pdf(
    file_path: str,
    source: str,
    timings: dict,
    tokens: dict,
):
    # PDF → text
    if timings is not None:
        with track_timing(timings, "load_pdf"):
            text = load_pdf(file_path)
    else:
        text = load_pdf(file_path)

    # count pdf tokens
    if tokens is not None:
        tokens["raw_text_tokens"] = count_tokens(text)

    # text → chunks
    if timings is not None:
        with track_timing(timings, "chunk_text"):
            chunks: List[str] = chunk_text(
                text, chunk_size=CHUNK_SIZE,
                overlap=CHUNK_OVERLAP
            )
    else:
        chunks: List[str] = chunk_text(
            text, chunk_size=CHUNK_SIZE,
            overlap=CHUNK_OVERLAP
        )

    # count chunk tokens
    num_chunks = len(chunks)
    total_tokens = sum(count_tokens(c) for c in chunks)

    if num_chunks > MAX_EMBED_CHUNKS:
        logger.warning(
            "Ingestion truncated: too many chunks",
            extra={
                "original_chunks": num_chunks,
                "used_chunks": MAX_EMBED_CHUNKS,
            }
        )
        chunks = chunks[:MAX_EMBED_CHUNKS]
        if tokens is not None:
            tokens["truncated_chunks"] = True
        num_chunks = len(chunks)

    if total_tokens > MAX_EMBED_TOKENS:
        raise EmbeddingLimitExceeded(
            f"Ingestion aborted: total tokens {total_tokens} "
            f"exceed MAX_EMBED_TOKENS={MAX_EMBED_TOKENS}"
        )

    if tokens is not None:
        tokens["chunk_tokens"] = sum(count_tokens(c) for c in chunks)
        tokens["num_chunks"] = num_chunks

    # chunks → embeddings
    embedding_client = get_embedding_client(provider=settings.EMBEDDING_PROVIDER)
    if timings is not None:
        with track_timing(timings, "embedding_generation"):
            vectors = await embedding_client.embed(chunks)
    else:
        vectors = await embedding_client.embed(chunks)

    if tokens is not None:
        tokens["embedding_input_tokens"] = tokens["chunk_tokens"]

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

    if tokens is not None:
        logger.info(
            f"PDF ingested: document_id={doc_id}, "
            f"num_chunks={tokens.get('num_chunks', len(chunks))}, "
            f"tokens={tokens}, timings={timings}"
        )

    return {"document_id": doc_id, "num_chunks": len(chunks)}
