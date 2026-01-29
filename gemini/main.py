from copy import deepcopy
import os
from app.llm.adapters.geminiAdapter import GeminiClient
from app.llm.config import DEFAULT_GEN_CONFIG as gen_config
from app.llm.config import CUSTOM_GEN_CONFIG
from app.llm.runner import run_llm
from dotenv import load_dotenv

load_dotenv()

# wanna save responses to json files
OUTPUT_DIR = "json_requests"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_response_json(response, filename: str):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(response.model_dump_json(indent=2))
    print(f"Saved: {path}")


gemini = GeminiClient(
    api_key=os.getenv("GEMINI_API_KEY"),
    model="gemini-3-flash-preview"
)

response = run_llm(
    prompt="What is an LLM?",
    gen_config=gen_config,
    client=gemini,
    instruction="You are a professional teacher. Explain simply.",
)

save_response_json(response, "llm_intro.json")
# print(response.model_dump_json(indent=2))

# ===============================================
custom_gen_config = deepcopy(CUSTOM_GEN_CONFIG)

# =======let's play with temperature=============

custom_gen_config["temperature"] = 0.0
custom_gen_config["top_p"] = 0.9
custom_gen_config["max_tokens"] = 512

# almost determinism
responseTemp00 = run_llm(
    prompt="What is an LLM?",
    gen_config=custom_gen_config,
    client=gemini,
    instruction="You are a professional teacher. Explain simply.",
)

save_response_json(responseTemp00, "responseTemp00.json")
# print(f"temp 0.0:\n{responseTemp00.model_dump_json(indent=2)}")

custom_gen_config["temperature"] = 0.2
custom_gen_config["top_p"] = 0.9
custom_gen_config["max_tokens"] = 512

# code, instructions
responseTemp02 = run_llm(
    prompt="What is an LLM?",
    gen_config=custom_gen_config,
    client=gemini,
    instruction="You are a professional teacher. Explain simply.",
)

save_response_json(responseTemp02, "responseTemp02.json")
# print(f"temp 0.2:\n{responseTemp02.model_dump_json(indent=2)}")

custom_gen_config["temperature"] = 0.7
custom_gen_config["top_p"] = 0.9
custom_gen_config["max_tokens"] = 512

# ideas
responseTemp07 = run_llm(
    prompt="What is an LLM?",
    gen_config=custom_gen_config,
    client=gemini,
    instruction="You are a professional teacher. Explain simply.",
)

save_response_json(responseTemp07, "responseTemp07.json")
# print(f"temp 0.7:\n{responseTemp07.model_dump_json(indent=2)}")

custom_gen_config["temperature"] = 1.5
custom_gen_config["top_p"] = 0.9
custom_gen_config["max_tokens"] = 512

# chaos
responseTemp15 = run_llm(
    prompt="What is an LLM?",
    gen_config=custom_gen_config,
    client=gemini,
    instruction="You are a professional teacher. Explain simply.",
)

save_response_json(responseTemp15, "responseTemp15.json")
# print(f"temp 1.5:\n{responseTemp15.model_dump_json(indent=2)}")

# =============================================================

# ===============let's play with top_p=========================

custom_gen_config["temperature"] = 0.2
custom_gen_config["top_p"] = 0.9
custom_gen_config["max_tokens"] = 512

# 90%
responseTop_p09 = run_llm(
    prompt="What is an LLM?",
    gen_config=custom_gen_config,
    client=gemini,
    instruction="You are a professional teacher. Explain simply.",
)

save_response_json(responseTop_p09, "responseTop_p09.json")
# print(f"top_p 0.9:\n{responseTop_p09.model_dump_json(indent=2)}")

custom_gen_config["temperature"] = 0.2
custom_gen_config["top_p"] = 0.5
custom_gen_config["max_tokens"] = 512

# 50%
responseTop_p05 = run_llm(
    prompt="What is an LLM?",
    gen_config=custom_gen_config,
    client=gemini,
    instruction="You are a professional teacher. Explain simply.",
)

save_response_json(responseTop_p05, "responseTop_p05.json")
# print(f"top_p 0.5:\n{responseTop_p05.model_dump_json(indent=2)}")

custom_gen_config["temperature"] = 0.2
custom_gen_config["top_p"] = 0.1
custom_gen_config["max_tokens"] = 512

# 10%
responseTop_p01 = run_llm(
    prompt="What is an LLM?",
    gen_config=custom_gen_config,
    client=gemini,
    instruction="You are a professional teacher. Explain simply.",
)

save_response_json(responseTop_p01, "responseTop_p01.json")
# print(f"top_p 0.1:\n{responseTop_p01.model_dump_json(indent=2)}")

# =============================================================

# ===============let's play with prompts=======================

# ======Summarize========
responseArticle = run_llm(
    prompt="""Write long article about AI.
            Answer format is JSON {"summary": "", "key_points": []}.
            Less than 50 words, only facts.""",
    gen_config=gen_config,
    client=gemini,
    instruction="You are a professional teacher.",
)

save_response_json(responseArticle, "responseArticle.json")
# print(f"long article short in JSON:\n{responseArticle.model_dump_json(indent=2)}")

responseNews = run_llm(
    prompt="""
    Write latest IT news via bullet points list in 5 points
    """,
    gen_config=gen_config,
    client=gemini,
    instruction="You are a journalist.",
)

save_response_json(responseNews, "responseNews.json")
# print(f"news in bullet points list:\n{responseNews.model_dump_json(indent=2)}")

# =======Code========
responseSorting = run_llm(
    prompt="""
    Write the numbers list sorting function
    Answer format is JSON {"code": "", "explanation": ""}
    Python 3.10+, 15 lines max
    """,
    gen_config=gen_config,
    client=gemini,
    instruction="You are a Python developer.",
)

save_response_json(responseSorting, "responseSorting.json")
# print(f"sort function:\n{responseSorting.model_dump_json(indent=2)}")

# =======Analysis========
responseSells = run_llm(
    prompt="""
    Write sells report for a month
    in JSON {"trends": [], "anomalies": []}
    sign only valuable changes (>10%)
    """,
    gen_config=gen_config,
    client=gemini,
    instruction="You are an Analyst.",
)

save_response_json(responseSells, "responseSells.json")
# print(f"sells:\n{responseSells.model_dump_json(indent=2)}")

responseSocial = run_llm(
    prompt="""
    Write app's users reviews
    in JSON {"positive": [], "negative": [], "suggestions": []}
    3 points max each category
    """,
    gen_config=gen_config,
    client=gemini,
    instruction="You are a Social Researcher.",
)

save_response_json(responseSocial, "responseSocial.json")
# print(f"social:\n{responseSocial.model_dump_json(indent=2)}")

# ======Reasoning======
responseLogical = run_llm(
    prompt="""
    If A->B and B->C what we can tell about A and C?
    in JSON {"step_by_step": "", "conclusion": ""}
    Step by step thinking
    """,
    gen_config=gen_config,
    client=gemini,
    instruction="You are a Logic Scientist.",
)

save_response_json(responseLogical, "responseLogical.json")
# print(f"social:\n{responseLogical.model_dump_json(indent=2)}")

responseFinance = run_llm(
    prompt="""
    Why X company's actions ruined after report?
    in JSON {"reasoning_steps": [], "summary": ""}
    only facts
    """,
    gen_config=gen_config,
    client=gemini,
    instruction="You are a Financial Analyst.",
)

save_response_json(responseFinance, "responseFinance.json")
# print(f"social:\n{responseSocial.model_dump_json(indent=2)}")

responseMath = run_llm(
    prompt="""
    If 3x+2=11 what's x?
    in JSON {"steps": [], "answer": ""}
    step by step in detail
    """,
    gen_config=gen_config,
    client=gemini,
    instruction="You are a Math Teacher.",
)

save_response_json(responseMath, "responseMath.json")
# print(f"social:\n{responseMath.model_dump_json(indent=2)}")

responseSystem = run_llm(
    prompt="""
    Help solve the problem: the server is not responding
    in JSON {"possible_causes": [], "recommended_actions": []}
    only real technical causes 5 points max
    """,
    gen_config=gen_config,
    client=gemini,
    instruction="You are a System Analyst.",
)

save_response_json(responseSystem, "responseSystem.json")
# print(f"social:\n{responseSystem.model_dump_json(indent=2)}")
