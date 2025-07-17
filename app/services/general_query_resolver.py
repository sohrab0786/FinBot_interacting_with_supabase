# app/services/query.py
from app.core.llm import stream_chat
import asyncio

async def query_general_resolver(query: str) -> bool:
    """
    Ask the LLM to classify if the query is general/basic and DOES NOT require DB or structured data.
    """
    system_msg = {
        "role": "system",
        "content": (
            "Classify the following query. "
            "If it can be answered without accessing any structured financial data or database, "
            "respond with only 'GENERAL'. Otherwise, respond with 'DATA_REQUIRED'."
        )
    }
    user_msg = {"role": "user", "content": query}
    response = ""

    async for tok in stream_chat([system_msg, user_msg]):
        response += tok

    response = response.strip().upper()
    return "GENERAL" in response
