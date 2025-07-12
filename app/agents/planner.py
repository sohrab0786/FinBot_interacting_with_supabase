# app/agents/planner.py
"""
Planner Agent
─────────────
Turns a user’s question into a list of agent-execution steps.

Plan schema (each step):
    {
        "agent": "financial" | "stock_price" | "documents",
        "ticker": "AAPL",
        "statement": "IS" | "BS" | "CF",
        "metrics": ["revenue", "net_income"],
        "period": "FY" | "Q1" | None,
    }
"""

from __future__ import annotations

import re
from typing import List, Dict
from app.constants.metrics import STATEMENT_MAP

PLAN = List[Dict]

# Build reverse lookup  raw_token → (statement, friendly_key)
ALL_METRICS: dict[str, tuple[str, str]] = {
    raw.lower(): (stmt, friendly)
    for stmt, mapping in STATEMENT_MAP.items()
    for friendly, raw in mapping.items()
}


# ────────────────────────────────────────────────────────────────────
def plan(question: str) -> PLAN:
    q_lc = question.lower()

    # 1) crude price rule
    if "price" in q_lc:
        return [{"agent": "stock_price", "query": question}]

    # 2) collect ALL metric tokens in the text
    tokens = _find_metric_tokens(q_lc)
    if tokens:
        ticker = _guess_ticker(question)
        # Split tokens by statement so we can call financial once per statement
        plan_steps: PLAN = []
        for stmt in ("IS", "BS", "CF"):
            stmt_metrics = [
                friendly
                for tok in tokens
                if (s := ALL_METRICS[tok])[0] == stmt
                for friendly in [s[1]]
            ]
            if stmt_metrics:
                plan_steps.append(
                    {
                        "agent": "financial",
                        "ticker": ticker,
                        "statement": stmt,
                        "metrics": stmt_metrics,
                        "period": "FY" if "fy" in q_lc else None,
                    }
                )
        return plan_steps

    # 3) fallback: documents / RAG
    return [{"agent": "documents", "query": question}]


# ───────── helpers ────────────────────────────────────────────────
def _find_metric_tokens(text: str) -> list[str]:
    """
    Return every metric raw token present in `text`.
    • spaces removed so "net income" matches "netincome"
    • case-insensitive
    """
    compact = text.replace(" ", "")
    return [tok for tok in ALL_METRICS if tok in compact]


def _guess_ticker(raw: str) -> str | None:
    """
    • (AAPL)  -> AAPL
    • lone ALL-CAPS word  -> that word
    """
    m = re.search(r"\(([A-Z]{1,5})\)", raw)
    if m:
        return m.group(1)
    m = re.search(r"\b([A-Z]{2,5})\b", raw)
    return m.group(1) if m else None
