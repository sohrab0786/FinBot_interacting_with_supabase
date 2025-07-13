# app/agents/planner.py
from __future__ import annotations
import re
from typing import List, Dict

from app.constants.metrics import STATEMENT_MAP
from app.services.ticker_resolver import resolve_one  # LLM+DB resolver

PLAN = List[Dict]

# raw_token → (statement, friendly_key)
ALL_METRICS: dict[str, tuple[str, str]] = {
    raw.lower(): (stmt, friendly)
    for stmt, mapping in STATEMENT_MAP.items()
    for friendly, raw in mapping.items()
}


async def plan(question: str) -> PLAN:
    """
    1) If 'price' in question → stock_price
    2) Extract fiscal_year and period
    3) Find all metric tokens
    4) Resolve ticker via LLM-first resolve_one(question)
    5) Fallback to regex (_fallback_ticker) if needed
    6) Emit one financial step per statement
    """
    q_lc = question.lower()

    # 1) price rule
    if "price" in q_lc:
        return [{"agent": "stock_price", "query": question}]

    # 2) capture year (e.g. 2023)
    ym = re.search(r"\b(20\d{2})\b", question)
    fiscal_year = int(ym.group(1)) if ym else None

    # 3) metric tokens
    tokens = _find_metric_tokens(q_lc)
    if tokens:
        # 4) LLM‐based ticker resolution
        ticker = await resolve_one(question)
        # 5) fallback if LLM failed
        if not ticker:
            ticker = _fallback_ticker(question)

        # 6) detect quarter vs FY
        m = re.search(r"\b(Q[1-4])\b", question, re.IGNORECASE)
        period = m.group(1).upper() if m else ("FY" if fiscal_year else None)

        steps: PLAN = []
        for stmt in ("IS", "BS", "CF"):
            ms = [ALL_METRICS[t][1] for t in tokens if ALL_METRICS[t][0] == stmt]
            if ms:
                steps.append({
                    "agent": "financial",
                    "ticker": ticker,
                    "statement": stmt,
                    "metrics": ms,
                    "fiscal_year": fiscal_year,
                    "period": period,
                })
        return steps

    # 7) fallback to retrieval agent
    return [{"agent": "documents", "query": question}]


def _find_metric_tokens(text: str) -> list[str]:
    """Return every metric raw token present (spaces removed, case-insensitive)."""
    compact = text.replace(" ", "")
    return [tok for tok in ALL_METRICS if tok in compact]


def _fallback_ticker(raw: str) -> str | None:
    """Last-ditch: literal (AAPL) or any ALL-CAPS word."""
    m = re.search(r"\(([A-Z]{1,5})\)", raw)
    if m:
        return m.group(1)
    m = re.search(r"\b([A-Z]{2,5})\b", raw)
    return m.group(1) if m else None
