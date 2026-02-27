from app.llm.runner import run_llm_async


async def summarize_history(
    self,
    history_chunk: list[dict]
) -> str:
    history_text = "\n".join(
        f"Thought:{h.get('thought', '')}\n"
        f"Action:{h.get('action', '')}\n"
        f"Observation:{h.get('observation', '')}"
        for h in history_chunk
    )

    prompt = f"""
    Summarize the following agent steps briefly.
    Preserve important facts and results.
    Remove reasoning noise.

    {history_text}
    """.strip()

    response = await run_llm_async(
        prompt=prompt,
        gen_config=self.gen_config,
        client=self.llm_client
    )

    return response.result.text.strip()
