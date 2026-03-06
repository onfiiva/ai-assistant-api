from .metrics.answer_quality_metrics import exact_match, cosine_similarity, embedding
from .metrics.retrieval_metrics import precision_at_k, recall_at_k, reciprocal_rank
from .report import save_report, summarize
import time
import traceback


async def evaluate(runner, dataset):
    results = []
    total = len(dataset)

    for idx, item in enumerate(dataset, 1):
        question = item["question"]
        expected = item["expected"]

        print(f"[{idx}/{total}] Evaluating: {question[:60]}")

        try:
            start = time.time()
            answer, retrieved = await runner.run(question)
            latency = time.time() - start

            relevant = item.get("relevant_chunks", [])
            retrieved_chunks = []
            filtered_chunks = []

            # RAG runner returns dict
            if isinstance(result, dict):
                answer = result.get("text", "")
                retrieved_chunks = result.get("retrieved_chunks", [])
                filtered_chunks = result.get("filtered_chunks", [])

            else:
                answer = result or ""

            exact = exact_match(answer, expected)

            emb_pred = embedding(answer)
            emb_exp = embedding(expected)
            cosine = cosine_similarity(emb_pred, emb_exp)

            results.append({
                "question": question,
                "expected": expected,
                "answer": answer,

                "retrieved_chunks": [
                    c.get("text", "")[:200] for c in retrieved_chunks
                ],

                "filtered_chunks": [
                    c.get("text", "")[:200] for c in filtered_chunks
                ],

                "exact": exact,
                "cosine": round(float(cosine), 4),
                "latency": round(latency, 3),
                "error": None
            })

        except Exception as e:
            print("Error:", e)
            traceback.print_exc()

            results.append({
                "question": question,
                "expected": expected,
                "answer": None,

                "retrieved_chunks": [],
                "filtered_chunks": [],

                "exact": 0,
                "cosine": 0,
                "latency": None,
                "error": str(e)
            })

    summary = summarize(results)
    report_path = save_report({
        "summary": summary,
        "details": results
    })
    print(f"Report saved to: {report_path}")

    return results
