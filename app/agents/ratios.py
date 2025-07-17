from typing import List, Dict, Literal
from app.core import db
from app.core.config import settings
from app.constants.metrics import STATEMENT_MAP
from typing import Union, List
Statement = Literal["RM", "KM"]

async def run(
    ticker: str,
    statement: Statement,
    metrics: List[str] | None = None,
    fiscal_year: int | None = None,
    period: str | None = None,
    limit: int = 8,
) -> List[Dict]:
    print(f"\n🚧 ratios.run: statement={statement}, metrics={metrics}, fiscal_year={fiscal_year}, period={period}, limit={limit}")
    if settings.data_source != "supabase":
        raise RuntimeError(f"Unknown DATA_SOURCE {settings.data_source}")

    return await _fetch_from_supabase(
        ticker, statement, metrics, fiscal_year, period, limit
    )

def is_quarterly_request(period: Union[str, List[str], None], limit: int) -> bool:
    if isinstance(period, list):
        return all(p in {"Q1", "Q2", "Q3", "Q4"} for p in period)

    if period in {"Q1", "Q2", "Q3", "Q4"}:
        return True

    if period is None and limit and limit <= 4:
        return True

    if period == "Q":  # e.g., normalized from extraction
        return True

    return False
async def _fetch_from_supabase(
    ticker: str,
    statement: Statement,
    metrics: List[str] | None,
    fiscal_year: int | None,
    period: str | None,
    limit: int,
) -> List[Dict]:
    table_name = "financial.ratios" if statement == "RM" else "financial.key_metrics"
    metric_map = STATEMENT_MAP[statement]
    raw_metrics = (
        [metric_map[m] for m in metrics if m in metric_map]
        if metrics
        else list(metric_map.values())
    )

    sql = f"""
      SELECT metric, fiscal_year, fiscal_period, value
      FROM {table_name}
      WHERE ticker = $1
        AND metric = ANY($2::text[])
    """
    params = [ticker, raw_metrics]
    reverse = False
    order_clause = ""

    is_quarterly = is_quarterly_request(period, limit)
    if isinstance(fiscal_year, list):
        sql += f" AND fiscal_year = ANY(${len(params)+1}::int[])"
        params.append(fiscal_year)
    elif fiscal_year is not None:
        sql += f" AND fiscal_year = ${len(params)+1}"
        params.append(fiscal_year)

        if isinstance(period, list):
            sql += f" AND fiscal_period = ANY(${len(params)+1}::text[])"
            params.append(period)
            order_clause = " ORDER BY fiscal_year DESC, fiscal_period DESC"
            reverse = False

        elif period in {"Q1", "Q2", "Q3", "Q4"}:
            sql += f" AND fiscal_period = ${len(params)+1}"
            params.append(period)
            order_clause = " ORDER BY fiscal_year DESC"

        else:
            sql += f" AND fiscal_period = ${len(params)+1}"
            params.append("FY")
            order_clause = " ORDER BY fiscal_year DESC"
    elif is_quarterly:
        sql += " AND fiscal_period IN ('Q1', 'Q2', 'Q3', 'Q4')"
        order_clause = " ORDER BY fiscal_year DESC, fiscal_period DESC"
        reverse = False

    else:
        sql += " AND fiscal_period = 'FY'"
        order_clause = " ORDER BY fiscal_year DESC"
        reverse = True
    if not order_clause:
        print("⚠️ No order clause detected — using fallback ordering")
        order_clause = " ORDER BY fiscal_year DESC"

    sql += order_clause

    # Apply LIMIT if not overridden by FY + known fiscal_year
    if limit:
       sql += f" LIMIT {limit}"

    async with db.pool.acquire() as conn:
        print("\n📊 SQL:", sql.replace("\n", " "))
        print("📊 PARAMS:", params)
        rows = await conn.fetch(sql, *params)
        if reverse:
            rows = list(reversed(rows))
        print(f"📊 ROWS: {len(rows)} →", rows[:4])

    reverse_map = {v: k for k, v in metric_map.items()}
    return [
        {
            "metric": reverse_map.get(r["metric"], r["metric"]),
            "fiscal_year": r["fiscal_year"],
            "period": r["fiscal_period"],
            "value": float(r["value"]) if r["value"] is not None else None,
        }
        for r in rows
    ]
