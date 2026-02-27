from pydantic import BaseModel
from typing import List


class EmbedRequest(BaseModel):
    texts: List[str]    # List of texts which we want to turn into embeddings


class EmbedResponse(BaseModel):
    embeddings: List[List[float]]   # List of embedded vectors


class SimilarityResult(BaseModel):
    document: str   # document text
    score: float    # cosine similarity
