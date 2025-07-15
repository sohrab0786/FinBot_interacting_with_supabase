# app/services/prompt.py
from typing import List, Dict

SYSTEM = (
    "You are a reliable and factual financial assistant. "
    "When quoting metrics, use the display names exactly as provided in the table, "
    "and Use *all* the rows in the <CONTEXT> table—each row is one fiscal period—to answer."
    "format all numbers with commas and a leading dollar sign, "
    "and round to the nearest whole dollar. "
    "and format all numbers using shorthand suffixes: "
    "- thousands as K, millions as M, billions as B (with one decimal place when needed)."
    "Format the metrics and its values in the bold text."
    "If a value is missing, say so clearly."
)

def build_prompt(user_q: str, tables: List[Dict]) -> str:
    """
    Constructs a prompt that injects a markdown table of facts,
    with user-friendly metric names and formatted values.
    """
    context = ""
    if tables:
        # Build the markdown table header
        header = "Metric | Fiscal Year | Period | Value\n" \
                 "---|---|---|---\n"
        rows = []
        for r in tables:
            # Turn "net_income" → "Net Income"
            display_name = r["metric"].replace("_", " ").title()
            fy = r["fiscal_year"]
            period = r["period"] or ""
            val = r["value"]
            if val is None:
                val_str = "N/A"
            else:
                # Round to whole dollars and format with commas
                val_int = int(round(val))
                val_str = f"${val_int:,}"
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
