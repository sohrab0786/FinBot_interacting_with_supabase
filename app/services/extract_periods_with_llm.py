from typing import Tuple, Optional
from app.core.llm import stream_chat
import json

async def extract_period_info_llm(question: str) -> Tuple[int, Optional[str]]:
    """
    Extract number of periods and period type ('Q', 'FY', 'Q1', etc.) from user query.
    """
    messages = [
    {
    "role": "system",
    "content": (
        "You are a financial query interpreter. Given a user query, extract:\n"
        "- limit: the number of fiscal periods (quarter or year).\n"
        "- period: the period type — either:\n"
        "    • 'Q' for quarterly,\n"
        "    • 'FY' for full-year,\n"
        "    • a single quarter like 'Q3',\n"
        "    • or a list of specific quarters like ['Q1', 'Q2'].\n\n"
        "When the query includes phrases like 'past 3 quarters of 2020', assume it means the most recent 3 quarters of that year (e.g., Q2–Q4).\n\n"
        "Examples:\n"
        "- 'last 4 quarters' → {\"limit\": 4, \"period\": \"Q\"}\n"
        "- 'last 2 years' → {\"limit\": 2, \"period\": \"FY\"}\n"
        "- 'Q3 2022' → {\"limit\": 1, \"period\": \"Q3\"}\n"
        "- '2020 revenue' → {\"limit\": 1, \"period\": \"FY\"}\n"
        "- 'first and second quarters of 2022' → {\"limit\": 2, \"period\": [\"Q1\", \"Q2\"]}\n"
        "- 'Q1 and Q2 of 2022' → {\"limit\": 2, \"period\": [\"Q1\", \"Q2\"]}\n"
        "- 'past 3 quarters of 2020' → {\"limit\": 3, \"period\": [\"Q2\", \"Q3\", \"Q4\"]}\n"
        "- '1st and 3rd quarter of 2020' → {\"limit\": 2, \"period\": [\"Q1\", \"Q3\"]}\n"
        "- Unknown → {\"limit\": 1, \"period\": null}\n\n"
        "Return only compact valid JSON like: {\"limit\": 2, \"period\": [\"Q1\", \"Q2\"]} — no extra text or explanation."
    )
},
    {"role": "user", "content": question}
]
    chunks = []
    async for token in stream_chat(messages):
        chunks.append(token)
    full = "".join(chunks).strip()

    try:
        parsed = json.loads(full)
        return parsed.get("limit", 1), parsed.get("period")
    except Exception as e:
        print("[ERROR] JSON parse failed:", e)
        return 1, None
