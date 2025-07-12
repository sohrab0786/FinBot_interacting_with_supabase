# scripts/check_setup.py
import asyncio, os, textwrap, httpx, json

from app.core.config import settings
from app.core import db, llm
from app.services.fmp_client import call_fmp


async def main() -> None:
    print("\n— SETTINGS —")
    print(json.dumps(settings.model_dump(mode="json", exclude={"supabase_service_key"}), indent=2))

    # ---------- SUPABASE ------------------------------------------------
    if settings.data_source == "supabase":
        print("\n— SUPABASE POOL —")
        await db.init_pool()
        async with db.pool.acquire() as conn:
            ver = await conn.fetchval("select version()")
        print("postgres:", ver.split()[0])
        db.init_supabase()
        print("supabase client OK")

    else:
        print("\nSupabase skipped (DATA_SOURCE != supabase)")

    # ---------- FMP -----------------------------------------------------
    if settings.data_source == "fmp":
        print("\n— FMP —")
        js = await call_fmp("available-industries")
        print("FMP Industries:", js[0]["industry"])
    else:
        print("\nFMP skipped (DATA_SOURCE != fmp)")

    # ---------- LLM -----------------------------------------------------
    print("\n— LLM STREAM —")
    messages = [{"role": "user", "content": "say hello in two words"}]
    async for tok in llm.stream_chat(messages):
        print(tok, end="", flush=True)
        break  # just first token
    print("\nLLM path OK")

    # ---------- done ----------------------------------------------------
    if db.pool:
        await db.close_pool()


if __name__ == "__main__":
    asyncio.run(main())
