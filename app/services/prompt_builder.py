# app/services/prompt_builder.py

from typing import List, Dict
from app.services.prompt_utils import get_value_type

SYSTEM = (
    "You are a reliable and factual financial assistant. "
    "Always use the metric display names exactly as provided in the <CONTEXT> table. "
    "Use *all* rows from the <CONTEXT> table — each row represents a fiscal period — to answer the question. "
    "Format all dollar values with commas, a leading dollar sign, and round to the nearest whole number. "
    "Use shorthand suffixes for large numbers: thousands as K, millions as M, billions as B (with one decimal place if needed). "
    "Format percentage values appropriately using the % sign. "
    "Wrap metric names and their values in bold markdown (**like this**). "
    "If a value is missing or unavailable, clearly state that it is missing."
)


def build_prompt(user_q: str, tables: List[Dict]) -> str:
    context = ""
    if tables:
        header = "Metric | Fiscal Year | Period | Value\n" \
                 "---|---|---|---\n"
        rows = []

        for r in tables:
            display_name = r["metric"].replace("_", " ").title()
            fy = r["fiscal_year"]
            period = r["period"] or ""
            val = r["value"]
            metric_id = r["raw_metric"] if "raw_metric" in r else r["metric"]
            print(f"[DEBUG] Raw metric: {metric_id} → Value type: {get_value_type(metric_id)}")
            value_type = get_value_type(metric_id)

            if val is None:
                val_str = "N/A"
            else:
                if value_type == "percent":
                    percent = round(float(val) * 100, 1)
                    val_str = f"{percent}%"
                elif value_type == "plain":
                    val_str = f"{round(val, 2)}"  # e.g., 1.23
                else:  # dollar
                    val_str = f"${int(round(val)):,}"  # e.g., $1,234,567
            rows.append(f"{display_name} | {fy} | {period} | {val_str}")
        body = "\n".join(rows)
        context = f"<CONTEXT>\n{header}{body}\n</CONTEXT>\n"

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
