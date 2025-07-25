from typing import List, Dict, Literal, Union
from app.core import db
from app.core.config import settings
from app.services import metric_registry, dispatcher
Statement = Literal["IS", "BS", "CF", "RM", "KM"]
async def run(
    ticker: str,
    statement: Statement,
    metrics: List[str] | None = None,
    fiscal_year: int | None = None,
    period: str | None = None,
    limit: int = 8,
) -> List[Dict]:
    print(f"\n🚧 planner.run: statement={statement}, metrics={metrics}, fiscal_year={fiscal_year}, period={period}, limit={limit}")
    if settings.data_source != "supabase":
        raise RuntimeError(f"Unknown DATA_SOURCE {settings.data_source}")
    return await dispatcher.run_dispatch(
        ticker=ticker,
        metrics=metrics,
        fiscal_year=fiscal_year,
        period=period,
        limit=limit
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

