# app/services/prompt_builder.py
from typing import List, Dict
from collections import defaultdict
from app.services.prompt_utils import get_value_type

SYSTEM = (
    "You are a reliable and factual financial assistant. "
    "Always use the metric display names exactly as provided in the <CONTEXT> table. "
    "Use *all* rows from the <CONTEXT> table — each row represents a fiscal period. "
    "Format all dollar values with commas, a leading dollar sign, and round to the nearest whole number. "
    "Use shorthand suffixes for large numbers: thousands as K, millions as M, billions as B (with one decimal place if needed). "
    "Format percentage values appropriately using the % sign. "
    "Wrap metric names and their values in bold markdown (**like this**). "
    "If a value is missing or unavailable, clearly state that it is missing. "
    "When the data includes multiple fiscal years or multiple fiscal quarters, format the result as a markdown table. "
    "Use fiscal years as rows and fiscal periods (e.g. Q1, Q2, Q3, Q4) as columns. "
    "Otherwise, use bullet points or concise sentences for simple queries."
)
def build_prompt(user_q: str, tables: List[Dict]) -> str:
    if not tables:
        return f"{SYSTEM}\nUser question: {user_q}\nAssistant:"

    # Group values by metric → {metric: {period: value_str}}
    metric_groups = defaultdict(dict)
    all_periods = set()

    for r in tables:
        metric = r["metric"]
        fy = r["fiscal_year"]
        period = r["period"] or "FY"
        value = r["value"]
        raw_metric = r.get("raw_metric", metric)
        value_type = get_value_type(raw_metric)

        label = f"{period} {fy}" if period != "FY" else str(fy)
        all_periods.add(label)

        if value is None:
            val_str = "N/A"
        else:
            if value_type == "percent":
                val_str = f"{round(value * 100, 1)}%"
            elif value_type == "plain":
                val_str = f"{round(value, 2)}"
            else:  # dollar
                amount = float(value)
                if amount >= 1_000_000_000:
                    val_str = f"${round(amount / 1_000_000_000, 1)}B"
                elif amount >= 1_000_000:
                    val_str = f"${round(amount / 1_000_000, 1)}M"
                elif amount >= 1_000:
                    val_str = f"${round(amount / 1_000, 1)}K"
                else:
                    val_str = f"${int(round(amount)):,}"

        metric_groups[metric][label] = val_str

    # Sort periods chronologically
    def period_sort_key(label: str):
        parts = label.split()
        if len(parts) == 2:  # Q1 2023
            q, y = parts
            quarter_order = {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4}
            return (int(y), quarter_order.get(q, 5))
        return (int(label), 0)

    sorted_periods = sorted(all_periods, key=period_sort_key)

    # Build markdown table
    header = "Metric | " + " | ".join(sorted_periods)
    divider = "---|" + "|".join("---" for _ in sorted_periods)
    rows = []

    for metric, period_map in metric_groups.items():
        display_name = metric.replace("_", " ").title()
        row_values = [period_map.get(p, "N/A") for p in sorted_periods]
        rows.append(f"{display_name} | " + " | ".join(row_values))

    context = "<CONTEXT>\n" + header + "\n" + divider + "\n" + "\n".join(rows) + "\n</CONTEXT>\n"

    prompt = (
        f"{SYSTEM}\n"
        f"{context}"
        f"User question: {user_q}\n"
        f"Assistant:"
    )

    print("[DEBUG] Prompt length (chars):", len(prompt))
    print("[DEBUG] Prompt line count:", prompt.count('\n'))
    print("[DEBUG] Prompt preview:\n", prompt[:500], "...\n---END PREVIEW---\n")

    return prompt
