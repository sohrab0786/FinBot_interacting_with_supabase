# app/api/v1/chat.py
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.agents.planner import plan
from importlib import import_module
from app.services.prompt import build_prompt
from app.core.llm import stream_chat

router = APIRouter()


class ChatRequest(BaseModel):
    query: str


@router.post("/chat")
async def chat_endpoint(req: ChatRequest):
    # 1️⃣ plan
    plan_steps = await plan(req.query)

    # 2️⃣ execute
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
