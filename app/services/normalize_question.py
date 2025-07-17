import re
from typing import List, Dict
from app.core import db
from app.core.llm import stream_chat
# Top of file


async def normalize_question(raw_question: str) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "You are an assistant that rewrites user questions to fix grammar, spelling, and phrasing. "
                "Convert phrases like 'quarter 1st' to 'first quarter', fix misspellings like 'firs quart', "
                "and correct company names to proper case (e.g., 'apple' to 'Apple')."
            ),
        },
        {"role": "user", "content": raw_question},
    ]
    result = []
    async for token in stream_chat(messages):
        result.append(token)
    return "".join(result).strip()


def fallback_normalize_phrases(text: str) -> str:
    replacements = {
    r"\b(first|1st)\s+and\s+(second|2nd)\s+quarters?\b": "first 2 quarters",
    r"\b(first|1st)\s+and\s+(third|3rd)\s+quarters?\b": "first 3 quarters",
    r"\b(first|1st)\s+and\s+(fourth|4th)\s+quarters?\b": "first 4 quarters",
    r"\bquarter\s+1st\b": "first quarter",
    r"\bquarter\s+2nd\b": "second quarter",
    r"\bquarter\s+3rd\b": "third quarter",
    r"\bquarter\s+4th\b": "fourth quarter",
    r"\bfirs[t]?\s+quart(er)?\b": "first quarter",
    r"\bsecnd\s+quart\b": "second quarter",
}
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text, flags=re.I)
    return text