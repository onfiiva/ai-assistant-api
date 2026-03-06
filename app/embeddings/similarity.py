import math
from typing import List


# cos(theta) = (vec{a} * vec{b}) / (||vec{a}|| * ||vec{b}||)
def cosine_similarity(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))  # <-- (vec{a} * vec{b})
    norm_a = math.sqrt(sum(x * x for x in a))   # <-- ||vec{a}||
    norm_b = math.sqrt(sum(y * y for y in b))   # <-- ||vec{b}||
    return dot / (norm_a * norm_b)
