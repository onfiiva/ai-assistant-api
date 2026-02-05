import asyncio
from app.inference.workers.async_inference_worker import AsyncInferenceWorker
from app.core.logging import logger

async def main():
    worker = AsyncInferenceWorker()
    await worker.run()

if __name__ == "__main__":
    logger.info("Starting AsyncInferenceWorker")
    asyncio.run(main())
