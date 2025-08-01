from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import pprint
from app.core.llm import stream_chat
from app.services.query_handler import query_handler
from app.services.general_query_resolver import query_general_resolver
from app.services.prompt_builder import build_prompt
from fastapi.responses import RedirectResponse
from app.services.session_store import save_response
from fastapi.responses import HTMLResponse
from app.services.session_store import load_response

router = APIRouter()

SYSTEM_PROMPT = "You are a helpful assistant answering financial queries with the help of structured financial data."
class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = "default"  # Kept for interface, but not used internally

@router.post("/chat")
async def chat_endpoint(req: ChatRequest):
    is_general = await query_general_resolver(req.query)
    if is_general:
        print(f'yes general query: "{req.query}"')
        return StreamingResponse(
            stream_chat([{"role": "user", "content": req.query}]),
            media_type="text/markdown"
        )
    context_parts = await query_handler(req.query)

    # Handle suggestion case
    if (
        isinstance(context_parts, list)
        and len(context_parts) == 1
        and isinstance(context_parts[0], dict)
        and context_parts[0].get("agent") == "suggestion"
    ):
        suggestion = context_parts[0]
        content = (
            f"**Incomplete query detected.**\n\n"
            f"{suggestion['message']}\n\n"
            + "\n".join(f"- {q}" for q in suggestion["suggestions"])
        )
        return StreamingResponse(
            stream_chat([{"role": "user", "content": content}]),
            media_type="text/markdown"
        )

    # Extract structured financial facts
    flattened_rows = []
    for part in context_parts:
        content = part.get("content") if isinstance(part, dict) else None
        if isinstance(content, list):
            for item in content:
                if all(k in item for k in ("metric", "fiscal_year", "period", "value")):
                    flattened_rows.append(item)
    print("[DEBUG] Flattened rows:", flattened_rows)
    pprint.pformat(flattened_rows)
    # Build structured prompt with table
    prompt = build_prompt(req.query, flattened_rows)

    # Final prompt to LLM
    chat_payload = [{"role": "user", "content": prompt}]
    full_response = ""
    async for chunk in stream_chat(chat_payload):
        full_response += chunk
    # Save and redirect
    session_id = save_response(full_response)
    return RedirectResponse(url=f"/result?session_id={session_id}", status_code=302)

@router.get("/result")
def show_result(session_id: str):
    html = load_response(session_id)
    return HTMLResponse(content=html)