from typing import Tuple, Optional, List
from app.core.llm import stream_chat
import json

async def extract_period_info_llm(question: str) -> Tuple[int, Optional[str], Optional[List[int]]]:
    """
    Extract number of periods, period type ('Q', 'FY', etc.), and referenced years from a user query.
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
                "    • or a list of specific quarters like ['Q1', 'Q2'].\n"
                "- years: a list of all relevant years mentioned or implied (e.g. 2022, 2023).\n\n"
                "Examples:\n"
                "- 'last 4 quarters' → {\"limit\": 4, \"period\": \"Q\", \"years\": []}\n"
                "- 'last 2 years' → {\"limit\": 2, \"period\": \"FY\", \"years\": []}\n"
                "- 'Q3 2022' → {\"limit\": 1, \"period\": \"Q3\", \"years\": [2022]}\n"
                "- '2020 revenue' → {\"limit\": 1, \"period\": \"FY\", \"years\": [2020]}\n"
                "- 'F22 and F24 reports' → {\"limit\": 2, \"period\": \"FY\", \"years\": [2022, 2024]}\n"
                "- '2022 to 2025' → {\"limit\": 4, \"period\": \"FY\", \"years\": [2022, 2023, 2024, 2025]}\n"
                "- 'past 3 quarters of 2020' → {\"limit\": 3, \"period\": [\"Q2\", \"Q3\", \"Q4\"], \"years\": [2020]}\n"
                "- Unknown → {\"limit\": 1, \"period\": null, \"years\": []}\n\n"
                "Return only compact valid JSON like: {\"limit\": 2, \"period\": [\"Q1\", \"Q2\"], \"years\": [2022]} — no extra text or explanation."
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
        years = parsed.get("years")
        return parsed.get("limit", 1), parsed.get("period"), years if years else None
    except Exception as e:
        print("[ERROR] JSON parse failed:", e)
        return 1, None, []
