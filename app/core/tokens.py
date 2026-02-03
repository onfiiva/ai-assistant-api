import contextlib

from fastapi import Request

@contextlib.contextmanager
def track_tokens(obj, name: str, text: str):
    """
    Universal token counter
    
    obj: req or res
    name: req or res name, key "{name}_tokens"
    text: text to count tokens for
    """
    tokens = count_tokens(text)

    try:
        yield
    finally:
        # if obj - Request
        if isinstance(obj, Request):
            if not hasattr(obj.state, "tokens"):
                obj.state.tokens = {}
            obj.state.tokens[f"{name}_tokens"] = tokens

        # if obj - dict
        elif isinstance(obj, dict):
            obj[f"{name}_tokens"] = tokens

        else:
            raise TypeError("track_tokens expects Request or dict")

def count_tokens(text: str) -> int:
    """
    Approximate token counter.
    1 token ~= 3–4 characters (latin) or ~1–2 words.
    """
    if not text:
        return 0

    # очень грубая, но стабильная эвристика
    return max(1, len(text) // 4)