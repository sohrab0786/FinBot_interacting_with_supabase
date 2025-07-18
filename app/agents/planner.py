from __future__ import annotations
import re
from typing import List, Dict

from app.constants.metrics import STATEMENT_MAP
from app.services.ticker_resolver import resolve_one
from app.services.normalize_question import normalize_question, fallback_normalize_phrases
from app.services.extract_periods_with_llm import extract_period_info_llm
from app.services.suggest_queries import suggest_queries

PLAN = List[Dict]

# raw_token → (statement, friendly_key)
ALL_METRICS = {
    friendly.lower().replace("_", " "): (stmt, friendly)
    for stmt, mapping in STATEMENT_MAP.items()
    for friendly in mapping
}

# statement → agent
STATEMENT_TO_AGENT = {
    "IS": "financial",
    "BS": "financial",
    "CF": "financial",
    "RM": "ratios",
    "KM": "ratios",
}
async def plan(question: str) -> PLAN:
    question = await normalize_question(question)
    question = fallback_normalize_phrases(question)
    if not question:
        return suggest_queries(question)

    q_lc = question.lower()

    # Extract all years mentioned in the query (supports comparison queries)
    year_matches = re.findall(r"\b(20\d{2})\b", question)
    years = list(map(int, year_matches)) if year_matches else []

    # Extract period info using LLM
    limit, period = await extract_period_info_llm(question)
    print(f"Extracted from extract_period_info_llm: limit={limit}, period={period} for question: {question}")

    # Default fallback if fiscal year present but period missing
    if years and not period:
        period = "FY"
        limit = limit or 1
    elif period == "FY":
        limit = limit or 1

    # Detect metric tokens
    tokens = _find_metric_tokens(q_lc)
    print(f"Detected tokens: {tokens} for question: {question}")
    if tokens:
        ticker = await resolve_one(question) or _fallback_ticker(question)
        steps: PLAN = []

        for stmt in STATEMENT_TO_AGENT:
            ms = [ALL_METRICS[t][1] for t in tokens if ALL_METRICS[t][0] == stmt]
            if ms:
                if years:
                    for y in years:
                        step = {
                            "agent": STATEMENT_TO_AGENT[stmt],
                            "ticker": ticker,
                            "statement": stmt,
                            "metrics": ms,
                            "limit": limit,
                            "fiscal_year": y,
                        }
                        if period:
                            step["period"] = period
                        steps.append(step)
                else:
                    step = {
                        "agent": STATEMENT_TO_AGENT[stmt],
                        "ticker": ticker,
                        "statement": stmt,
                        "metrics": ms,
                        "limit": limit,
                    }
                    if period:
                        step["period"] = period
                    steps.append(step)

        return steps

    return suggest_queries(question)


def _find_metric_tokens(text: str) -> list[str]:
    norm = text.lower().replace("/", "").replace("_", " ")  # also normalize user input
    tokens = []
    for tok in sorted(ALL_METRICS.keys(), key=lambda x: -len(x)):  # longest match first
        if re.search(rf"\b{re.escape(tok)}\b", norm):
            tokens.append(tok)
            norm = norm.replace(tok, "")  # remove matched to avoid overlap
    return tokens

def _fallback_ticker(raw: str) -> str | None:
    m = re.search(r"\(([A-Z]{1,5})\)", raw)
    if m:
        return m.group(1)
    m = re.search(r"\b([A-Z]{2,5})\b", raw)
    return m.group(1) if m else None


# Optional: Detect comparison-type phrasing (not used but useful)
def _is_comparison_query(q: str) -> bool:
    return any(k in q.lower() for k in ["compare", "vs", "versus", "difference between"])
