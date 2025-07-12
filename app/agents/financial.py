# app/agents/financial.py
from typing import List, Dict, Literal
import asyncpg, httpx, datetime as dt

from app.core import db
from app.core.config import settings
from app.core.db import pool
from app.constants.metrics import STATEMENT_MAP
# from app.services.fmp_client import fetch_facts_fmp   # will build soon

Statement = Literal["IS", "BS", "CF"]


# ───────────────── public API used by the planner ──────────────────
async def run(
    ticker: str,
    statement: Statement,
    metrics: List[str] | None = None,
    fiscal_year: int | None = None,
    period: str = "FY",
    limit: int = 8,
) -> List[Dict]:
    if settings.data_source == "supabase":
        return await _fetch_from_supabase(
            ticker, statement, metrics, fiscal_year, period, limit
        )
    # elif settings.data_source == "fmp":
    #     return await fetch_facts_fmp(
    #         ticker, statement, metrics, fiscal_year, period, limit
    #     )
    else:
        raise RuntimeError(f"Unknown DATA_SOURCE {settings.data_source}")


# ───────────────── internal: Supabase SQL path ─────────────────────
async def _fetch_from_supabase(
    ticker: str,
    statement: Statement,
    metrics: List[str] | None,
    fiscal_year: int | None,
    period: str,
    limit: int,
) -> List[Dict]:
    metric_map = STATEMENT_MAP[statement]
    raw_metrics = (
        [metric_map[m] for m in metrics if m in metric_map]
        if metrics
        else list(metric_map.values())
    )

    sql = """
      SELECT metric, fiscal_year, fiscal_period, value
      FROM financial.financial_fact
      WHERE ticker = $1
        AND statement = $2
        AND metric = ANY($3::text[])
    """
    params: list = [ticker, statement, raw_metrics]

    if fiscal_year:
        sql += f" AND fiscal_year = ${len(params)+1}"
        params.append(fiscal_year)
    if period:
        sql += f" AND fiscal_period = ${len(params)+1}"
        params.append(period)

    sql += " ORDER BY fiscal_year DESC, fiscal_period DESC"

    async with db.pool.acquire() as conn:
        print("\n📊  SQL:", sql.replace("\n", " "))
        print("\n📊  PARAMS:", params)
        rows = await conn.fetch(sql, *params)
        print(f"📊  ROWS:{len(rows)}  sample→", rows[:2], "\n")

    reverse_map = {v: k for k, v in metric_map.items()}
    return [
        {
            "metric": reverse_map[r["metric"]],
            "fiscal_year": r["fiscal_year"],
            "period": r["fiscal_period"],
            "value": float(r["value"]) if r["value"] is not None else None,
        }
        for r in rows
    ]
