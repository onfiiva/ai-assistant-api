import time
import logging
from .normalizer import normalize_llm_response
import threading

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def run_llm(
    prompt: str,
    gen_config: dict,
    client,
    instruction: list[str] = None,
    max_retries: int = 3,
    backoff_factor: float = 2.0,
    timeout: float = 30.0
):
    """
    Runner for LLM: added retry + backoff.
    Returns normalized JSON via normalize_llm_response.
    """
    attempt = 0
    instruction = instruction or ["You are a professional teacher. Explain simply."]

    logger.info(f"LLM request started: prompt='{prompt[:50]}...', config={gen_config}")

    while attempt <= max_retries:
        result_container = {}
        exception_container = {}

        def target():
            try:
                # checking if instruction is present in the client
                if hasattr(client.generate, "__annotations__") \
                        and "instruction" in client.generate.__annotations__:
                    raw = client.generate(
                        prompt=prompt,
                        gen_config=gen_config,
                        instruction=instruction
                    )
                else:
                    raw = client.generate(
                        prompt=prompt,
                        gen_config=gen_config
                    )
                result_container["raw"] = raw
            except Exception as e:
                exception_container["error"] = e

        thread = threading.Thread(target=target)
        thread.start()
        thread.join(timeout=timeout)

        if thread.is_alive():
            logger.warning(
                f"Attempt {attempt+1}/{max_retries} "
                f"timed out after {timeout}s. Retrying..."
            )
            thread.join(0)  # завершить поток
            attempt += 1
            continue

        if "error" in exception_container:
            logger.warning(
                f"Attempt {attempt+1}/{max_retries} failed: "
                f"{exception_container['error']}"
            )
            attempt += 1
            time.sleep(backoff_factor ** attempt)
            continue

        # если успешно — возвращаем нормализованный ответ
        logger.info(f"LLM response received: prompt='{prompt[:50]}...'")
        return normalize_llm_response(
            model=client.model_name,
            prompt=prompt,
            gen_config=gen_config,
            raw_response=result_container["raw"]
        )

    raise RuntimeError(
        f"LLM request failed after "
        f"{max_retries} attempts for prompt: {prompt:20}, len of prompt: {len(prompt)}"
    )
