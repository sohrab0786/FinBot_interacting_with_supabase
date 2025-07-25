# app/services/get_company_name_llm.py
import json
from app.core.llm import stream_chat

async def extract_company_names_llm(query: str) -> list[str]:
    prompt = (
        "Extract all company names mentioned in the query as a JSON array of strings. "
        "Respond only with the array. No explanation.\n\n"
        f'Query: "{query}"'
    )
    text = ""
    async for chunk in stream_chat([{"role": "user", "content": prompt}]):
        text += chunk
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        return []

