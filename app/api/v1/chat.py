# app/api/v1/chat.py
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.agents.planner import plan
from importlib import import_module
from app.services.prompt_builder import build_prompt
from app.core.llm import stream_chat
from app.services.general_query_resolver import query_general_resolver
router = APIRouter()


class ChatRequest(BaseModel):
    query: str
@router.post("/chat")
async def chat_endpoint(req: ChatRequest):
    is_general = await query_general_resolver(req.query)

    if is_general:
        return StreamingResponse(stream_chat(
            [{"role": "user", "content": req.query}]),
            media_type="text/markdown"
        )
    # 1️⃣ plan
    plan_steps = await plan(req.query)
    
    # 2️⃣ handle suggestion/fallback (incomplete query)
    if len(plan_steps) == 1 and plan_steps[0].get("agent") == "suggestion":
        suggestion = plan_steps[0]
        content = (
            f"**Incomplete query detected.**\n\n"
            f"{suggestion['message']}\n\n"
            + "\n".join(f"- {q}" for q in suggestion["suggestions"])
        )
        return StreamingResponse(stream_chat(
            [{"role": "user", "content": content}]),
            media_type="text/markdown"
        )
    # 3️⃣ execute
    context_parts = []
    for step in plan_steps:
        agent_name = step.pop("agent")
        module = import_module(f"app.agents.{agent_name}")
        rows = await module.run(**step)
        context_parts.extend(rows)

    # 3️⃣ compose prompt & stream LLM
    prompt = build_prompt(req.query, context_parts)
    return StreamingResponse(stream_chat(
        [{"role": "user", "content": prompt}]),
        media_type="text/markdown")
