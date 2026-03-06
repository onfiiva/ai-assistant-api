import asyncio
import logging
from .normalizer import normalize_llm_response

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def run_llm_async(
    prompt: str,
    gen_config: dict,
    client,
    instruction: list[str] | None = None,
    max_retries: int = 3,
    backoff_factor: float = 60.0,
    timeout: float = 120.0
):
    """
    Fully async LLM runner with:
    - retry
    - exponential backoff
    - real cancellation
    - proper timeout
    """

    # TODO: default instruction conf needed
    instruction = instruction or ["You are a professional teacher. Explain simply."]

    logger.info(f"LLM async request started: prompt='{prompt[:50]}...'")

    for attempt in range(max_retries):
        try:
            # Timeout
            raw_response = await asyncio.wait_for(
                client.generate(
                    prompt=prompt,
                    gen_config=gen_config,
                    instruction=instruction,
                ),
                timeout=timeout,
            )

            logger.info("LLM response recieved")

            return normalize_llm_response(
                model=client.model_name,
                prompt=prompt,
                gen_config=gen_config,
                raw_response=raw_response,
            )

        except asyncio.TimeoutError:
            logger.warning(
                f"Attempt {attempt+1}/{max_retries} timed out after {timeout}s"
            )

        except Exception as e:
            logger.warning(
                f"Attempt {attempt+1}/{max_retries} failed: {e}"
            )

        if attempt < max_retries:
            sleep_time = backoff_factor ** attempt
            await asyncio.sleep(sleep_time)

    raise RuntimeError(
        f"LLM request failed after {max_retries} attempts"
    )
