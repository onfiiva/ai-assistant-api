from app.llm.runner import run_llm_async


class SummaryTool:

    async def run(self, text: str, gen_config: dict, client) -> str:
        prompt = f"""
        Summarize the following text clearly and concisely:

        {text}
        """
        return await run_llm_async(
            prompt=prompt,
            gen_config=gen_config,
            client=client
        )
