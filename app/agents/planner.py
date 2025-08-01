from __future__ import annotations
import re
from typing import List, Dict, Optional, Tuple, Union
from app.services.metric_registry import get_metric, metric_registry
from app.services.normalize_question import normalize_question, fallback_normalize_phrases
from app.services.extract_periods_with_llm import extract_period_info_llm
from app.services.suggest_queries import suggest_queries
from app.services.ticker_resolver import resolve_many, resolve_one
from collections import defaultdict
#PLAN = List[Dict]

def camel_to_snake(name: str) -> str:
    s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def build_statement_map():
    statement_map = {}
    for key, meta in metric_registry.items():
        stmt = meta["statement"]
        if stmt not in statement_map:
            statement_map[stmt] = {}
        statement_map[stmt][camel_to_snake(meta["column"])] = meta["column"]
    return statement_map

STATEMENT_MAP = build_statement_map()

def get_statement_for_metric_set(metrics: List[str]) -> str:
    statements = {
        stmt
        for m in metrics
        for stmt, mapping in STATEMENT_MAP.items()
        if m in mapping.values()
    }
    if not statements:
        return "IS"
    if len(statements) == 1:
        return statements.pop()
    # Prefer RM or KM if present
    if "RM" in statements:
        return "RM"
    if "KM" in statements:
        return "KM"

    # Fallback for mixed statements: default to IS
    print(f"⚠️ Mixed statements in metrics: {statements}, falling back to IS")
    return "IS"

async def plan(user_query: str, metrics:List[str]) -> List[Dict]:
    print("✅ normalized metrics:", metrics)
    limit, period, fiscal_years = await extract_period_info_llm(user_query)
    #fiscal_years = extract_years(user_query)
    tickers = await resolve_many(user_query)
    if not tickers:
        return [{
            "agent": "suggestion",
            "message": "No companies found in your query.",
            "suggestions": [
                "Try including ticker symbols like AAPL or MSFT.",
                "Or write the full company names (e.g., Apple, Microsoft)."
            ]
        }]

    #statement = get_statement_for_metric_set(metrics)
    if not metrics or not tickers:
        suggestions = await suggest_queries(user_query)
        return [{
            "agent": "suggestion",
            "message": "Sorry, I couldn't determine which company or metric you're referring to.",
            "suggestions": suggestions
        }]

    stmt_to_metrics = defaultdict(list)
    for m in metrics:
        stmt = metric_registry[m]["statement"]
        stmt_to_metrics[stmt].append(m)

    plans = []

    for ticker in tickers:
        for stmt, mlist in stmt_to_metrics.items():
            agent = "financial" if stmt not in {"RM", "KM"} else "ratios"
            plans.append({
                "agent": agent,
                "ticker": ticker,
                "statement": stmt,
                "metrics": mlist,
                "fiscal_year": fiscal_years,
                "period": period,
                "limit": limit,
            })
    return plans

async def detect_ticker_and_statement(q: str) -> Tuple[str, str]:
    # Try to resolve company name → ticker
    ticker = await resolve_one(q)
    if not ticker:
        fallback = _fallback_ticker(q)
        if fallback:
            ticker = fallback
        else:
            raise ValueError("Unable to resolve ticker.")
    # Choose statement type based on metric hints
    metric_tokens = _find_metric_tokens(q)
    if any(m in metric_registry and metric_registry[m]["statement"] == "IS" for m in metric_tokens):
        return ticker, "IS"
    if any(m in metric_registry and metric_registry[m]["statement"] == "BS" for m in metric_tokens):
        return ticker, "BS"
    if any(m in metric_registry and metric_registry[m]["statement"] == "CF" for m in metric_tokens):
        return ticker, "CF"
    if any(m in metric_registry and metric_registry[m]["statement"] == "RM" for m in metric_tokens):
        return ticker, "RM"
    if any(m in metric_registry and metric_registry[m]["statement"] == "KM" for m in metric_tokens):
        return ticker, "KM"
    return ticker, "IS"  # fallback

def _find_metric_tokens(text: str) -> list[str]:
    norm = text.lower().replace("&", " and ").replace("/", "").replace("_", " ").replace("-", " ")
    tokens = []
    for tok in sorted(metric_registry.keys(), key=lambda x: -len(x)):
        if re.search(rf"\b{re.escape(tok)}\b", norm):
            tokens.append(tok)
            norm = norm.replace(tok, "")
    return tokens

def _fallback_ticker(raw: str) -> Optional[str]:
    m = re.search(r"\(([A-Z]{1,5})\)", raw)
    if m:
        return m.group(1)
    m = re.search(r"\b([A-Z]{2,5})\b", raw)
    return m.group(1) if m else None

def _is_comparison_query(q: str) -> bool:
    return any(k in q.lower() for k in ["compare", "vs", "versus", "difference between"])
