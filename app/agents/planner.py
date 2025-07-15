# app/agents/planner.py
from __future__ import annotations
import re
from typing import List, Dict

from app.constants.metrics import STATEMENT_MAP
from app.services.ticker_resolver import resolve_one

PLAN = List[Dict]

# raw_token → (statement, friendly_key)
ALL_METRICS = {
    raw.lower(): (stmt, friendly)
    for stmt, mapping in STATEMENT_MAP.items()
    for friendly, raw in mapping.items()
}


async def plan(question: str) -> PLAN:
    q_lc = question.lower()

    # 1) price rule
    if "price" in q_lc:
        return [{"agent": "stock_price", "query": question}]

    # 2) capture explicit year or "last N years"
    year_match = re.search(r"\b(20\d{2})\b", question)
    fiscal_year = int(year_match.group(1)) if year_match else None

    last_n_match = re.search(r"last\s+(\d+)\s+years", q_lc)
    last_n = int(last_n_match.group(1)) if last_n_match else None

    # 3) find all metric tokens
    tokens = _find_metric_tokens(q_lc)
    if tokens:
        # resolve ticker from entire question
        ticker = await resolve_one(question) or _fallback_ticker(question)

        # 4) determine period
        q_match = re.search(r"\b(Q[1-4])\b", question, re.IGNORECASE)
        period = q_match.group(1).upper() if q_match else ("FY" if (fiscal_year or last_n) else None)

        # 5) assemble plan steps
        steps: PLAN = []
        for stmt in ("IS", "BS", "CF"):
            ms = [ALL_METRICS[t][1] for t in tokens if ALL_METRICS[t][0] == stmt]
            if ms:
                steps.append({
                    "agent": "financial",
                    "ticker": ticker,
                    "statement": stmt,
                    "metrics": ms,
                    # if last_n is set, don't filter by year; use limit
                    **({} if last_n else {"fiscal_year": fiscal_year}),
                    "period": period,
                    # always include limit: last_n or 1 if single-year
                    "limit": last_n or (1 if fiscal_year else 4),
                })
        return steps

    # 6) fallback
    return [{"agent": "documents", "query": question}]


def _find_metric_tokens(text: str) -> list[str]:
    compact = text.replace(" ", "")
    return [tok for tok in ALL_METRICS if tok in compact]


def _fallback_ticker(raw: str) -> str | None:
    m = re.search(r"\(([A-Z]{1,5})\)", raw)
    if m:
        return m.group(1)
    m = re.search(r"\b([A-Z]{2,5})\b", raw)
    return m.group(1) if m else None
