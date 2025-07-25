from app.core.llm import stream_chat

async def call_llm_response(prompt: str) -> str:
    messages = [{"role": "user", "content": prompt}]
    response = ""
    async for chunk in stream_chat(messages):
        response += chunk
    return response.strip()
