import json, httpx, asyncio
from typing import AsyncGenerator, List, Dict
from app.core.config import settings


async def stream_chat(
    messages: List[Dict[str, str]]
) -> AsyncGenerator[str, None]:
    """
    Yield tokens from Ollama (provider=http) or OpenAI cloud (provider=openai)
    """
    print("[DEBUG] LLM stream_chat called. Message preview:", messages[0]["content"][:300], "...\n---END PREVIEW---\n")
    if settings.llm_provider == "openai":
        async for tok in _stream_openai(messages):
            print("[DEBUG] LLM token:", repr(tok))
            yield tok
        print("[DEBUG] LLM stream ended (openai)")
    elif settings.llm_provider == "http":
        async for tok in _stream_http(messages):
            print("[DEBUG] LLM token:", repr(tok))
            yield tok
        print("[DEBUG] LLM stream ended (http)")
    else:
        raise RuntimeError(f"Unsupported LLM_PROVIDER={settings.llm_provider}")


# ───── provider=http → local Ollama / vLLM / LM Studio ─────────────
async def _stream_http(messages):
    url = f"{str(settings.openai_base_url).rstrip('/')}/chat/completions"
    headers = {"Content-Type": "application/json"}
    if settings.openai_api_key:
        headers["Authorization"] = f"Bearer {settings.openai_api_key}"  # not used by Ollama

    payload = {
        "model": settings.openai_model,
        "stream": True,
        "temperature": settings.llm_temperature,
        "max_tokens": settings.llm_max_tokens,
        "messages": messages,
    }

    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream("POST", url, headers=headers, json=payload) as resp:
            async for line in resp.aiter_lines():
                if not line.startswith("data:"):
                    continue
                chunk = line.removeprefix("data:").strip()
                if chunk == "[DONE]":
                    break
                token = json.loads(chunk)["choices"][0]["delta"].get("content")
                if token:
                    yield token


# ───── provider=openai → cloud (OpenAI, Groq, Together…) ───────────
async def _stream_openai(messages):
    import openai
    openai.api_key = settings.openai_api_key
    openai.base_url = str(settings.openai_base_url)

    response = await openai.chat.completions.create(  # type: ignore[attr-defined]
        model=settings.openai_model,
        stream=True,
        temperature=settings.llm_temperature,
        max_tokens=settings.llm_max_tokens,
        messages=messages,
    )
    async for chunk in response:
        delta = chunk.choices[0].delta
        if delta and delta.content:
            yield delta.content
