# app/services/prompt.py
from typing import List, Dict

SYSTEM = (
    "You are a factual financial assistant. "
    "Use tables supplied in <CONTEXT> and cite metric names in bold. "
    "If data is missing, say you don’t have it."
)

def build_prompt(user_q: str, tables: List[Dict]) -> str:
    if tables:
        header = "metric | fiscal_year | period | value\n---|---|---|---\n"
        body = "\n".join(
            f"{r['metric']} | {r['fiscal_year']} | {r['period']} | {r['value']}"
            for r in tables
        )
        context = f"<CONTEXT>\n{header}{body}\n</CONTEXT>\n"
    else:
        context = ""

    return f"{SYSTEM}\n{context}\nUser question: {user_q}\nAssistant:"
