# app/services/prompt_utils.py

from app.services.metric_registry import metric_registry
from app.services.metric_classification import classified_metrics  # ← You import the dictionary here

# Normalize to lowercase no-underscore for comparison
def normalize_metric_id(name: str) -> str:
    return name.strip().lower().replace("_", "")

# Build fast lookup sets from classified_metrics
VALUATION_PERCENT_NORM = {
    normalize_metric_id(k)
    for k, v in classified_metrics.items()
    if v["value_type"] == "percent"
}

PLAIN_RATIO_METRICS = {
    normalize_metric_id(k)
    for k, v in classified_metrics.items()
    if v["value_type"] == "ratio"
}

def get_value_type(metric_id: str) -> str:
    normalized_id = normalize_metric_id(metric_id)

    if normalized_id in VALUATION_PERCENT_NORM:
        return "percent"
    elif normalized_id in PLAIN_RATIO_METRICS:
        return "plain"
    else:
        print(f"[DEBUG] Unknown metric type for '{metric_id}' → normalized: '{normalized_id}' (defaulting to 'dollar')")
        return "dollar"
