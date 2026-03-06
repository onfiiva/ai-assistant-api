import json
import asyncio

from .runners.base_model_runner import BaseModelRunner
from .runners.finetuned_model_runner import FineTunedRunner
# from .runners.rag_runner import RAGRunner
from .evaluator import evaluate

DATASET_PATH = "evaluation/dataset.json"
BASE_URL = "http://localhost:8000"


async def main():
    # 1. Load dataset
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    # 2. Initialize runner
    print("Using BaseRunner")
    # runner = BaseModelRunner(BASE_URL)
    runner = FineTunedRunner(BASE_URL)
    # runner = RAGRunner(BASE_URL)

    # 3. Run evaluator
    await evaluate(runner, dataset)
    print("Evaluation finished")

if __name__ == "__main__":
    asyncio.run(main())
