from .metrics import exact_match, cosine_similarity, embedding
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
            answer = await runner.run(question)  # <-- await
            latency = time.time() - start

            if not answer:
                answer = ""

            exact = exact_match(answer, expected)

            emb_pred = embedding(answer)
            emb_exp = embedding(expected)
            cosine = cosine_similarity(emb_pred, emb_exp)

            results.append({
                "question": question,
                "expected": expected,
                "answer": answer,
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
