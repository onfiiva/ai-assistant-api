from app.embeddings.vector_store import VectorStore
from app.embeddings.service import EmbeddingService
from app.embeddings.factory import get_embedding_client
from app.core.config import settings

vector_store = VectorStore(dim=3072)

embedding_client = get_embedding_client(settings.EMBEDDING_PROVIDER)
embedding_service = EmbeddingService(
    client=embedding_client
)
