# File: app/agents/ratios.py

from typing import List, Dict, Literal, Union
from app.core import db
from app.core.config import settings
from app.services.metric_registry import get_metric
from app.services.fetcher import is_quarterly_request
Statement = Literal["RM", "KM"]  # Support both ratios and key metrics

async def run(
    ticker: str,
    statement: Statement,
    metrics: List[str] | None = None,
    fiscal_year: int | List[int] | None = None,
    period: str | List[str] | None = None,
    limit: int = 8,
) -> List[Dict]:
    print(f"\n🚧 ratios.run: statement={statement}, metrics={metrics}, fiscal_year={fiscal_year}, period={period}, limit={limit}")
    if settings.data_source != "supabase":
        raise RuntimeError(f"Unknown DATA_SOURCE {settings.data_source}")

    table_name = "financial.ratios" if statement == "RM" else "financial.key_metrics"

    return await _fetch_from_supabase(
        table_name=table_name,
        statement=statement,
        ticker=ticker,
        metrics=metrics,
        fiscal_year=fiscal_year,
        period=period,
        limit=limit
    )

async def _fetch_from_supabase(
    table_name: str,
    statement: Statement,
    ticker: str,
    metrics: List[str] | None,
    fiscal_year: Union[int, List[int], None],
    period: Union[str, List[str], None],
    limit: int,
) -> List[Dict]:
    raw_metrics = []
    for m in metrics or []:
        meta = get_metric(statement, m)
        if meta is None:
            print(f"[ERROR] Metric '{m}' not found in registry for statement '{statement}'")
            continue
        raw_metrics.append(meta["column"])

    sql = f"""
      SELECT  ticker, metric, fiscal_year, fiscal_period, value
      FROM {table_name}
      WHERE ticker = $1
    """
    params: list = [ticker]
    param_idx = 2

    if raw_metrics:
        sql += f" AND metric = ANY(${param_idx}::text[])"
        params.append(raw_metrics)
        param_idx += 1

    if isinstance(fiscal_year, list):
        sql += f" AND fiscal_year = ANY(${param_idx}::int[])"
        params.append(fiscal_year)
        param_idx += 1
    elif fiscal_year is not None:
        sql += f" AND fiscal_year = ${param_idx}"
        params.append(fiscal_year)
        param_idx += 1

    if period == "Q":
        sql += " AND fiscal_period IN ('Q1', 'Q2', 'Q3', 'Q4')"
    elif isinstance(period, list):
        sql += f" AND fiscal_period = ANY(${param_idx}::text[])"
        params.append(period)
        param_idx += 1
    elif period in {"Q1", "Q2", "Q3", "Q4"}:
        sql += f" AND fiscal_period = ${param_idx}"
        params.append(period)
        param_idx += 1
    elif is_quarterly_request(period, limit):
        sql += " AND fiscal_period IN ('Q1', 'Q2', 'Q3', 'Q4')"
    else:
        sql += " AND fiscal_period = 'FY'"
    sql += " ORDER BY fiscal_year DESC, fiscal_period DESC"

    if (not fiscal_year or not period) and limit:
        sql += f" LIMIT {limit}"
    rows = []  # Always initialize rows
    try:
        print("\n📊 SQL:", sql.replace("\n", " "))
        print("📊 PARAMS:", params)
        conn = await db.get_conn()
        rows = await conn.fetch(sql, *params)
        print(f"📊 ROWS: {len(rows)} →", rows[:])
        for row in rows:
            print(dict(row))
    finally:
        await db.pool.release(conn)
    results = []
    for r in rows:
        # Reverse match: find the original token from metrics that matches this DB column
        for token in metrics or []:
            meta = get_metric(statement, token)
            if meta is None:
                continue
            column = meta["column"]
            if r["metric"] == column:
                results.append({
                    "ticker": r.get("ticker", ticker),  # fallback to known ticker
                    "metric": column,
                    "raw_metric": token,
                    "fiscal_year": r["fiscal_year"],
                    "period": r["fiscal_period"],
                    "value": float(r["value"]) if r["value"] is not None else None,
                })

    return results
