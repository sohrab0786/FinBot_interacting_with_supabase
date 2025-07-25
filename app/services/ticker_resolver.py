# app/services/ticker_resolver.py
"""
Ticker resolver and suggester.
• resolve_one(question) → single best ticker (LLM-first, then DB fallback)
• suggest(term, limit)  → multiple ticker/company suggestions from DB
"""

import re
from typing import List, Dict
from app.core import db
from app.core.llm import stream_chat
from fastapi.concurrency import run_in_threadpool
# Top of file
from app.services.get_company_name_llm import extract_company_names_llm  # ← implement this if needed
from app.core.db import supabase
TICKER_REGEX = r"\b[A-Z]{1,5}\b"
# ─── LLM-based single-ticker extraction with DB validation ─────────────
async def _llm_ticker(question: str) -> str | None:
    messages = [
        {"role": "system", "content":
            "Return only the official stock ticker symbol in uppercase for a public U.S. company mentioned in the query. Respond with just the symbol (e.g., AAPL). Do not return anything else, not even punctuation."},
        {"role": "user", "content": question},
    ]
    buf = []
    async for tok in stream_chat(messages):
        buf.append(tok)
    cand = "".join(buf).strip().upper()
    # Basic format check
    if not re.fullmatch(r"[A-Z]{1,5}", cand):
        print(f"[WARN] LLM returned invalid ticker format: '{cand}'")
        return None

    # Validate against DB
    sql = "SELECT symbol FROM refdata.companies WHERE symbol = $1"
    try:
        conn = await db.get_conn()
        row = await conn.fetchrow(sql, cand)
    finally:
        await db.pool.release(conn)
    if row:
        return row["symbol"]

    print(f"[WARN] LLM returned unknown ticker: '{cand}'")
    return None


# ─── DB-based single-ticker fallback ────────────────────────────────────
async def _db_ticker(term: str) -> str | None:
    sql = """
      WITH q AS (SELECT $1::text AS term)
      SELECT c.symbol AS ticker
      FROM refdata.companies c, q
      WHERE c.symbol ILIKE q.term || '%'
         OR similarity(c.company_name, q.term) > 0.35
      ORDER BY
        CASE WHEN c.symbol ILIKE q.term || '%' THEN 0 ELSE 1 END,
        (similarity(c.company_name, q.term) * 100)::int DESC
      LIMIT 1;
    """
    try:
        conn = await db.get_conn()
        row = await conn.fetchrow(sql, term)
    finally:
        await db.pool.release(conn)
    if row:
        return row["ticker"]
    # ultimate fallback: best overall similarity
    fallback_sql = """
      WITH q AS (SELECT $1::text AS term)
      SELECT c.symbol AS ticker
      FROM refdata.companies c, q
      ORDER BY similarity(c.company_name, q.term) DESC
      LIMIT 1;
    """
    try:
        conn = await db.get_conn()
        row = await conn.fetchrow(sql, term)
    finally:
        await db.pool.release(conn)
    return row["ticker"] if row else None


# ─── Public single-ticker resolver ──────────────────────────────────────


async def get_ticker_for_company_name(name: str) -> str | None:
    if not supabase:
        return None

    def fetch():
        try:
            response = supabase.table("company").select("ticker").ilike("name", f"%{name}%").limit(1).execute()
            data = response.data if hasattr(response, "data") else response.get("data", [])
            if data and isinstance(data, list) and "ticker" in data[0]:
                return data[0]["ticker"]
        except Exception as e:
            print(f"[WARN] Failed to fetch ticker for {name}: {e}")
        return None

    return await run_in_threadpool(fetch)


async def resolve_one(question_or_name: str) -> str | None:
    ticker = await _llm_ticker(question_or_name)
    if ticker:
        return ticker

    # Try Supabase fallback
    fallback_ticker = await get_ticker_for_company_name(question_or_name)
    if fallback_ticker:
        return fallback_ticker

    # Try DB fuzzy fallback
    ticker = await _db_ticker(question_or_name)
    return ticker

async def resolve_many(query: str) -> list[str]:
    company_names = await extract_company_names_llm(query)
    if not company_names:
        return []
    
    tickers = []
    for name in company_names:
        # Normalize name for better resolution
        name = name.strip().title()  # 'apple' → 'Apple'
        ticker = await resolve_one(name)
        if ticker:
            tickers.append(ticker)
    return tickers

# ─── Public multi-suggest for autocomplete ───────────────────────────────
async def suggest(term: str, limit: int = 8) -> List[Dict]:
    """
    Return up to `limit` tickers + company_names + score,
    using prefix match first, then fuzzy similarity.
    """
    term = term.strip()
    if not term:
        return []

    sql = """
      WITH q AS (SELECT $1::text AS term)
      SELECT
        c.symbol   AS ticker,
        c.company_name,
        CASE
          WHEN c.symbol ILIKE q.term || '%' THEN 100
          ELSE (similarity(c.company_name, q.term) * 100)::int
        END AS score
      FROM refdata.companies c, q
      WHERE
        c.symbol ILIKE q.term || '%'
        OR similarity(c.company_name, q.term) > 0.2
      ORDER BY
        CASE WHEN c.symbol ILIKE q.term || '%' THEN 0 ELSE 1 END,
        score DESC
      LIMIT $2;
    """
    try:
        conn = await db.get_conn()
        rows = await conn.fetchrow(sql, term, limit)
    finally:
        await db.pool.release(conn)
    return [dict(r) for r in rows]
