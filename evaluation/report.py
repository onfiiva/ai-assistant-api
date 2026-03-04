import os
import json
import statistics
from datetime import datetime


REPORTS_DIR = os.path.join(os.path.dirname(__file__), "reports")


def summarize(results):
    return {
        "exact": statistics.mean([r["exact"] for r in results]),
        "cosine": statistics.mean([r["cosine"] for r in results]),
        "latency": statistics.mean([r["latency"] for r in results])
    }


def ensure_reports_dir():
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)


def save_report(results: dict) -> str:
    """
    Saves reports into evaluation/reports/
    Returns file path.
    """
    ensure_reports_dir()

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"report_{timestamp}.json"

    path = os.path.join(REPORTS_DIR, filename)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    return path
