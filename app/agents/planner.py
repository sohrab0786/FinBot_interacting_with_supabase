# app/agents/planner.py
"""
Planner Agent
─────────────
Turns a user question into a list of execution steps.
"""
from __future__ import annotations

import re
from typing import List, Dict

from app.constants.metrics import STATEMENT_MAP
from app.services.ticker_resolver import resolve_one

PLAN = List[Dict]

# Build lookup: raw_token → (statement, friendly_key)
ALL_METRICS: dict[str, tuple[str, str]] = {
    raw.lower(): (stmt, friendly)
    for stmt, mapping in STATEMENT_MAP.items()
    for friendly, raw in mapping.items()
}


# Common stop words to strip from the company phrase
_STOP_WORDS = {
    "what","give","show","find","please","me","for","the","a","an","of","and","in","on","to","is","was"
}


async def plan(question: str) -> PLAN:
    q_lc = question.lower()

    # 1) Price queries
    if "price" in q_lc:
        return [{"agent": "stock_price", "query": question}]

    # 2) Financial metrics
    tokens = _find_metric_tokens(q_lc)
    if tokens:
        # --- extract the phrase before the first metric token ---
        first = tokens[0]
        prefix_match = re.split(rf"\b{re.escape(first)}\b", question, flags=re.IGNORECASE)[0]
        # tokenize, remove stop words
        words = re.findall(r"\b\w+\b", prefix_match)
        company_phrase = " ".join(w for w in words if w.lower() not in _STOP_WORDS).strip()

        # resolve to ticker (fuzzy / DB / FMP)
        ticker = await resolve_one(company_phrase) if company_phrase else None
        # fallback to literal ticker in parentheses or ALL-CAPS
        if not ticker:
            ticker = _guess_ticker_fallback(question)

        plan_steps: PLAN = []
        for stmt in ("IS", "BS", "CF"):
            stmt_metrics = [
                friendly
                for tok in tokens
                if (s := ALL_METRICS[tok])[0] == stmt
                for friendly in [s[1]]
            ]
            if stmt_metrics:
                plan_steps.append({
                    "agent": "financial",
                    "ticker": ticker,
                    "statement": stmt,
                    "metrics": stmt_metrics,
                    "period": "FY" if "fy" in q_lc else None,
                })
        return plan_steps

    # 3) Fallback retrieval agent
    return [{"agent": "documents", "query": question}]


def _find_metric_tokens(text: str) -> list[str]:
    """
    Return every metric raw token present (spaces ignored, case-insensitive).
    """
    compact = text.replace(" ", "")
    return [tok for tok in ALL_METRICS if tok in compact]


def _guess_ticker_fallback(raw: str) -> str | None:
    """
    Last-chance extraction of a literal ticker:
      - (AAPL)
      - ANY ALL-CAPS WORD
    """
    m = re.search(r"\(([A-Z]{1,5})\)", raw)
    if m:
        return m.group(1)
    m = re.search(r"\b([A-Z]{2,5})\b", raw)
    return m.group(1) if m else None
