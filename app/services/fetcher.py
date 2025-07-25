from typing import List, Dict, Union, Optional
import re
from app.core import db
from app.services.metric_registry import metric_registry
def camel_to_snake(name: str) -> str:
    s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
def build_statement_map():
    statement_map = {}
    for key, meta in metric_registry.items():
        stmt = meta["statement"]
        if stmt not in statement_map:
            statement_map[stmt] = {}
        # snake_case → camelCase
        statement_map[stmt][camel_to_snake(meta["column"])] = meta["column"]
    return statement_map

STATEMENT_MAP = build_statement_map()

def is_quarterly_request(period: Union[str, List[str], None], limit: int) -> bool:
    if period == "FY":
        return False  # ✅ Prevent fallback to quarters when FY is explicitly requested
    if isinstance(period, list):
        return all(p in {"Q1", "Q2", "Q3", "Q4"} for p in period)
    if period in {"Q1", "Q2", "Q3", "Q4"}:
        return True
    if period is None and limit and limit <= 4:
        return True
    if period == "Q":
        return True
    return False
