import requests
import numpy as np


def exact_match(a: str, b: str) -> int:
    return int(a.strip().lower() == b.strip().lower())


def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def embedding(text: str):
    try:
        response = requests.post(
            "http://localhost:8000/embeddings",
            json={"input": text}
        )
        data = response.json()
        # проверяем, есть ли ключ 'embedding', если нет — возвращаем нулевой вектор
        if "embedding" in data:
            return data["embedding"]
        elif "data" in data and isinstance(data["data"], list) and len(data["data"]) > 0:
            # иногда API возвращает {"data": [{"embedding": [...]}, ...]}
            return data["data"][0].get("embedding", [])
        else:
            print("Warning: no embedding returned, using zero vector")
            return [0.0] * 768  # безопасный дефолт размерности 768
    except Exception as e:
        print("Embedding error:", e)
        return [0.0] * 768
