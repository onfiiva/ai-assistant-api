import faiss
import numpy as np
from typing import List


class VectorStore:
    def __init__(self, dim: int):
        self.dim = dim
        self.index = None
        self.documents: List[str] = []

    def build(self, embeddings: List[List[float]], documents: List[str]):
        if not embeddings:
            raise ValueError("Embeddings list is empty")
        if len(embeddings) != len(documents):
            raise ValueError("Number of embeddings must match number of documents")

        # Преобразуем в numpy и проверим размерность
        vectors = np.array(embeddings, dtype=np.float32)
        if vectors.shape[1] != self.dim:
            raise ValueError(
                f"Embeddings dimension {vectors.shape[1]}"
                f"does not match index dimension {self.dim}"
            )

        # Нормализуем L2 (для cosine similarity)
        faiss.normalize_L2(vectors)

        # Создаём индекс FAISS
        self.index = faiss.IndexFlatIP(self.dim)
        self.index.add(vectors)

        # Сохраняем документы
        self.documents = documents.copy()

    def search(self, query_embedding: List[float], k: int):
        if self.index is None:
            raise ValueError("Vector index is empty. Call build() first.")

        query = np.array([query_embedding], dtype=np.float32)
        faiss.normalize_L2(query)

        scores, indices = self.index.search(query, k)

        results = []
        for pos, i in enumerate(indices[0]):
            if i < len(self.documents):
                results.append((self.documents[i], float(scores[0][pos])))
        return results
