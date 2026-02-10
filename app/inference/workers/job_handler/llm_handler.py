import asyncio
import json
from uuid import UUID
from app.inference.workers.job_handler.base import JobHandler
from app.llm.filter import refusal_response, validate_llm_output
from app.llm.sanitizer import sanitize_user_prompt


class LLMHandler(JobHandler):
    def __init__(self, llm_factory):
        self.llm_factory = llm_factory

    async def can_handle(self, job: dict) -> bool:
        payload = json.loads(job["prompt"])
        return "agent_type" not in payload

    async def handle(self, job: dict, repo):
        job_id = UUID(job["job_id"])
        await repo.update_status(job_id, "running")
        # payload = json.loads(job["prompt"])
        provider = job.get("model")
        llm_client = self.llm_factory.get(provider)

        gen_config = {
            "temperature": job.get("temperature", 0.7),
            "top_p": job.get("top_p", 1.0),
            "max_tokens": job.get("max_tokens", 512),
            "instruction": job.get("instruction"),
        }

        # sanitize
        try:
            safe_prompt = sanitize_user_prompt(job.get("prompt"))
            safe_instruction = sanitize_user_prompt(job.get("instruction"))
        except ValueError as e:
            await repo.update_status(job_id, "refused", result=refusal_response(str(e)))
            return {"status": "refused", "error": str(e)}

        try:
            llm_output = await asyncio.to_thread(
                llm_client.generate,
                prompt=safe_prompt,
                gen_config=gen_config,
                instruction=safe_instruction
            )

            status = "finished" if validate_llm_output(llm_output) else "fallback"
            result = llm_output if status == "finished" else """
                                                I might be mistaken. Please rephrase.
                                                """
            await repo.update_status(job_id, status, result=result)
            return {"status": status, "result": result}
        except asyncio.TimeoutError:
            await repo.update_status(job_id, "failed", error="timeout")
            return {"status": "failed", "error": "timeout"}
