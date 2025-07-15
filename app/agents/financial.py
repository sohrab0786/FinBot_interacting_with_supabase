# app/agents/financial.py
from typing import List, Dict, Literal

from app.core import db
from app.core.config import settings
from app.constants.metrics import STATEMENT_MAP
# from app.services.fmp_client import fetch_facts_fmp   # to implement later

Statement = Literal["IS", "BS", "CF"]


async def run(
    ticker: str,
    statement: Statement,
    metrics: List[str] | None = None,
    fiscal_year: int | None = None,
    period: str | None = "FY",
    limit: int = 8,
) -> List[Dict]:
    """
    Public entrypoint for the Financial Agent.
    Routes to Supabase SQL or (future) FMP branch.
    """
    if settings.data_source == "supabase":
        return await _fetch_from_supabase(
            ticker, statement, metrics, fiscal_year, period, limit
        )
    # elif settings.data_source == "fmp":
    #     return await fetch_facts_fmp(…)
    else:
        raise RuntimeError(f"Unknown DATA_SOURCE {settings.data_source}")


async def _fetch_from_supabase(
    ticker: str,
    statement: Statement,
    metrics: List[str] | None,
    fiscal_year: int | None,
    period: str | None,
    limit: int,
) -> List[Dict]:
    """
    Fetch rows from financial.financial_fact, exactly matching:
    • ticker
    • statement
    • any of the requested metrics
    • (optional) fiscal_year
    • (optional) fiscal_period
    • LIMIT to the most recent `limit` rows
    """
    # 1) Map friendly → raw metric names
    metric_map = STATEMENT_MAP[statement]
    raw_metrics = (
        [metric_map[m] for m in metrics if m in metric_map]
        if metrics
        else list(metric_map.values())
    )

    # 2) Build base SQL & params
    sql = """
      SELECT metric, fiscal_year, fiscal_period, value
      FROM financial.financial_fact
      WHERE ticker = $1
        AND statement = $2
        AND metric = ANY($3::text[])
    """
    params: list = [ticker, statement, raw_metrics]

    # 3) Optional single-year filter (skip if using last-N-years)
    if fiscal_year is not None:
        sql += f" AND fiscal_year = ${len(params)+1}"
        params.append(fiscal_year)

    # 4) Exact period filter (e.g. 'FY' or 'Q1')
    if period:
        sql += f" AND fiscal_period = ${len(params)+1}"
        params.append(period)

    # 5) Order most recent first, then LIMIT
    sql += f" ORDER BY fiscal_year DESC, fiscal_period DESC LIMIT {limit}"

    # 6) Execute & debug-log
    async with db.pool.acquire() as conn:
        print("\n📊  SQL:", sql.replace("\n", " "))
        print("\n📊  PARAMS:", params)
        rows = await conn.fetch(sql, *params)
        print(f"📊  ROWS:{len(rows)}  sample→", rows[:4], "\n")

    # 7) Reverse-map raw → friendly and cast
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
