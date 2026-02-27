from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams
from typing import List
from app.core.config import settings

client = QdrantClient(url=settings.QDRANT_URL, prefer_grpc=False)


def create_collection(name: str = "documents", vector_size: int = 3072):
    """Создаём коллекцию только если её нет"""
    try:
        client.get_collection(name=name)
        print(f"Collection '{name}' already exists")
    except Exception:  # коллекции нет → создаём
        try:
            client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(size=vector_size, distance="Cosine")
            )
            print(f"Collection '{name}' created")
        except Exception as e:
            # если вдруг кто-то параллельно создал коллекцию
            if "already exists" in str(e):
                print(f"Collection '{name}' already exists (race condition)")
            else:
                raise


def upsert_embedding(id: str, vector: List[float], content: str):
    client.upsert(
        collection_name="documents",
        points=[{"id": id, "vector": vector, "payload": {"content": content}}]
    )


def search(query_vector: List[float], limit: int = 5):
    # Используем query_points вместо client.search
    client.get_collection("documents")
    response = client.query_points(
        collection_name="documents",
        query=query_vector,
        limit=limit,
        with_payload=True  # чтобы достать текст chunk'а
    )
    # response.points — список найденных точек
    return [
        {
            "id": p.id,
            "vector": p.vector,
            "content": p.payload["content"],
            "score": getattr(p, "score", 0.0)
        }
        for p in response.points
    ]
