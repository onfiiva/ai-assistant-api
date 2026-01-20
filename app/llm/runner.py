import time
import logging
from .normalizer import normalize_llm_response

logger = logging.getLogger(__name__)

def run_llm(
    prompt: str,
    gen_config: dict,
    client,
    instruction: list[str] = None,
    max_retries: int = 3,
    backoff_factor: float = 2.0
):
    """
    Runner для LLM: добавлен retry + backoff.
    Возвращает нормализованный JSON через normalize_llm_response.
    """
    attempt = 0
    instruction = instruction or ["You are a professional teacher. Explain simply."]

    while attempt <= max_retries:
        try:
            # вызываем чистый адаптер
            raw = client.generate(
                prompt=prompt,
                gen_config=gen_config,
                instruction=instruction
            )
            # если успешно — возвращаем нормализованный ответ
            return normalize_llm_response(
                model=client.model_name,
                prompt=prompt,
                gen_config=gen_config,
                raw_response=raw
            )
        except Exception as e:
            attempt += 1
            wait = backoff_factor ** attempt
            logger.warning(f"Attempt {attempt}/{max_retries} failed: {e}. Retrying in {wait}s...")
            time.sleep(wait)

    # если все попытки упали — пробрасываем ошибку
    raise RuntimeError(f"LLM request failed after {max_retries} retries for prompt: {prompt}")