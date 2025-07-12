# app/agents/planner.py
"""
Planner Agent
─────────────
Turns a user question into execution steps.
"""
from __future__ import annotations

import re
from typing import List, Dict

from app.constants.metrics import STATEMENT_MAP
from app.services.ticker_resolver import resolve_one

PLAN = List[Dict]

ALL_METRICS: dict[str, tuple[str, str]] = {
    raw.lower(): (stmt, friendly)
    for stmt, mapping in STATEMENT_MAP.items()
    for friendly, raw in mapping.items()
}


async def plan(question: str) -> PLAN:
    q_lc = question.lower()

    # 1) price rule
    if "price" in q_lc:
        return [{"agent": "stock_price", "query": question}]

    # 2) metric tokens
    tokens = _find_metric_tokens(q_lc)
    if tokens:
        # 2a) try resolving a standalone company name
        name = _extract_company_name(question)
        ticker = await resolve_one(name) if name else None

        # 2b) fallback to regex-based ticker (e.g. "(AAPL)")
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

    # 3) fallback
    return [{"agent": "documents", "query": question}]


def _find_metric_tokens(text: str) -> list[str]:
    compact = text.replace(" ", "")
    return [tok for tok in ALL_METRICS if tok in compact]


def _extract_company_name(text: str) -> str | None:
    """
    Find the first capitalized word (not at sentence start)
    that is not a generic stop word.
    """
    stop = {"What", "Give", "Show", "For", "And", "The", "Find"}
    words = re.findall(r"\b([A-Z][a-z]+)\b", text)
    for w in words:
        if w not in stop:
            return w
    return None


def _guess_ticker_fallback(raw: str) -> str | None:
    # (AAPL)
    m = re.search(r"\(([A-Z]{1,5})\)", raw)
    if m:
        return m.group(1)
    # lone ALL-CAPS
    m = re.search(r"\b([A-Z]{2,5})\b", raw)
    return m.group(1) if m else None
