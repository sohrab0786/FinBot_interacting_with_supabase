import re
from collections import defaultdict
from app.services.metric_registry import metric_registry
def camel_to_snake(name: str) -> str:
    s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
# Build STATEMENT_MAP
STATEMENT_MAP = defaultdict(dict)

for metric_key, meta in metric_registry.items():
    statement = meta["statement"]
    column = meta["column"]
    
    # Add camelCase and snake_case keys
    STATEMENT_MAP[statement][metric_key] = column  # camelCase from registry
    STATEMENT_MAP[statement][camel_to_snake(metric_key)] = column  # snake_case fallback
