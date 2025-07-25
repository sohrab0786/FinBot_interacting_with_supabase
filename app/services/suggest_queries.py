import re
from typing import List
from difflib import get_close_matches
from app.constants.metrics import STATEMENT_MAP
from app.core.llm_tools import call_llm_response

# ---- You missed this: SAMPLE_QUERIES and ALL_METRICS were removed ----
SAMPLE_QUERIES = [
    "What was Apple's revenue in 2022?",
    "Show me the net income and gross profit for Microsoft for the last 3 years.",
    "Give me the ebit margin of Tesla for FY2021.",
    "What is Google's gross profit margin over the past 2 years?",
    "Show the quarterly revenue for Amazon in 2023.",
]

ALL_METRICS = {
    friendly.lower().replace("_", " "): (stmt, friendly)
    for stmt, mapping in STATEMENT_MAP.items()
    for friendly in mapping
}

def _find_possible_metrics(text: str) -> List[str]:
    norm = text.lower().replace("&", " and ").replace("/", "").replace("_", " ").replace("-", " ")
    words = re.findall(r"\b[a-zA-Z ]{3,}\b", norm)
    phrases = set()

    for key in ALL_METRICS:
        phrases.update(key.split())

    candidate_phrases = [' '.join(words[i:j]) for i in range(len(words)) for j in range(i+1, min(i+4, len(words)+1))]
    return [p for p in candidate_phrases if p not in ALL_METRICS]

# --- LLM prompt & helper ---
LLM_SUGGESTION_PROMPT = """
You are a helpful financial assistant.
A user asked: "{user_question}"

Using this context, generate 3 example questions a user might ask related to company financials.
Make sure the questions use valid financial metrics such as:
{valid_metrics}

Each question should include:
- A real company name (e.g. Apple, Tesla)
- A valid financial metric
- A timeframe (e.g. FY2023, past 3 years, etc.)
Respond with each question on a new line.
"""

async def generate_llm_suggestions(original_question: str, valid_metrics: List[str]) -> List[str]:
    prompt = LLM_SUGGESTION_PROMPT.format(
        user_question=original_question,
        valid_metrics=", ".join(valid_metrics)
    )
    response = await call_llm_response(prompt)
    suggestions = [line.strip("-• ").strip() for line in response.split("\n") if line.strip()]
    return suggestions[:3]

# --- Main function ---
async def suggest_queries(original_question: str) -> List[dict]:
    possible_metrics = _find_possible_metrics(original_question)
    suggestions = SAMPLE_QUERIES.copy()
    closest_matches = []

    for word in possible_metrics:
        matches = get_close_matches(word, ALL_METRICS.keys(), n=1, cutoff=0.75)
        if matches:
            stmt, metric_key = ALL_METRICS[matches[0]]
            sample = f"What is the {matches[0]} of Tesla for FY2023?"
            closest_matches.append(sample)

    if not closest_matches:
        all_metric_keys = list(ALL_METRICS.keys())
        closest_matches = await generate_llm_suggestions(original_question, all_metric_keys)

    suggestions = closest_matches + suggestions[:3]

    return [{
        "agent": "suggestion",
        "message": (
            "We couldn't recognize some of the financial metrics you mentioned.\n"
            "Here are some example queries you can try using supported metrics:"
        ),
        "suggestions": suggestions,
        "original_question": original_question
    }]
