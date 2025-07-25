from app.core.llm import stream_chat
import json
from typing import List
from app.services.metric_registry import metric_registry
async def extract_metrics_llm(user_query: str) -> list[str]:
    """
    Given a user question, extract a list of normalized metric keys.
    Output should be a JSON array of camelCase metric names (e.g., "ebitMargin", "netIncome").
    """
    supported_metrics = sorted(list(metric_registry.keys()))
    messages = [
        {
    "role": "system",
    "content": (
        "You are a financial metric extractor.\n"
        "Given a user query, return a JSON array of metric identifiers exactly as defined in the financial database.\n"
        "These identifiers are camelCase strings like 'ebitMargin', 'freeCashFlow', 'totalAssets', etc.\n"
        "Only return metrics that are available in the financial database.\n"
        "Respond ONLY with the array — no extra text or explanation.\n\n"
        "Avoid splitting compound terms like 'costAndExpenses', 'sellingGeneralAndAdministrativeExpenses', etc. "
        "into smaller components — always prefer the closest exact match from the supported list.\n\n"
        "IMPORTANT: If a user asks for a metric over time (e.g., 'over last 4 years', 'trend over 5 quarters'), "
        "assume they want to see historical values of the base metric, not a derived or percentage-based growth metric.\n"
        "For example:\n"
        "- 'revenue growth over 4 years' → [\"revenue\"]\n"
        "- 'trend of net income for past 5 years' → [\"netIncome\"]\n"
        "- 'earnings trend since 2019' → [\"netIncome\"]\n\n"
        f"Supported metrics:\n{json.dumps(supported_metrics)}\n\n"
        "Examples:\n"
        "'Show me EBIT margin and cash flow for Meta' → [\"ebitMargin\", \"freeCashFlow\"]\n"
        "'Quarterly total assets and liabilities' → [\"totalAssets\", \"totalLiabilities\"]\n"
        "'What is the net income of Apple in 2022' → [\"netIncome\"]\n"
        "'Give me cost and expenses of Meta for Q1 2023' → [\"costAndExpenses\"]"
    )
    },
        {"role": "user", "content": user_query}
    ]
    chunks = []
    async for token in stream_chat(messages):
        chunks.append(token)

    full = "".join(chunks).strip()
    try:
        print(f'full {full}')
        parsed = json.loads(full)
        return parsed if isinstance(parsed, list) else []
    except Exception as e:
        print("[ERROR] Metric JSON parsing failed:", e)
        return []

def normalize_metrics_llm_output(llm_metrics: List[str]) -> List[str]:
    from app.services.metric_registry import metric_registry
    registry_keys = set(metric_registry.keys())
    normalized = []
    for m in llm_metrics:
        if m in registry_keys:
            normalized.append(m)
        else:
            print(f"⚠️ Metric not found in registry: {m}")
    return normalized
