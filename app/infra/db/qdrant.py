from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams
from app.core.config import settings

client = QdrantClient(url=settings.QDRANT_URL)

def create_collection(name: str = "documents", vector_size: int = 1536):
    try:
        # check if collection exists
        client.get_collection(name=name)
        print(f"Collection '{name}' already exists")
    except Exception:
        # if not - create
        client.recreate_collection(
            collection_name=name,
            vectors_config=VectorParams(size=vector_size, distance="Cosine")
        )
        print(f"Collection '{name}' created")

def upsert_embedding(id: str, vector: list[float], content: str):
    client.upsert(
        collection_name="documents",
        points=[{"id": id, "vector": vector, "payload": {"content": content}}]
    )

def search(query_vector: list[float], limit: int = 5):
    return client.search(
        collection_name="documents",
        query_vector=query_vector,
        limit=limit
    )