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
# Top of file



# ─── LLM-based single-ticker extraction ─────────────────────────────────
async def _llm_ticker(question: str) -> str | None:
    messages = [
        {"role": "system", "content":
            "Extract and return *only* the stock ticker symbol in uppercase "
            "from the user’s query, without any extra text."},
        {"role": "user", "content": question},
    ]
    buf = []
    async for tok in stream_chat(messages):
        buf.append(tok)
    cand = "".join(buf).strip().upper()
    return cand if re.fullmatch(r"[A-Z]{1,5}", cand) else None


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
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(sql, term)
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
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(fallback_sql, term)
    return row["ticker"] if row else None


# ─── Public single-ticker resolver ──────────────────────────────────────
async def resolve_one(question: str) -> str | None:
    # Try LLM extraction
    ticker = await _llm_ticker(question)
    if ticker:
        return ticker
    # Use normalized question for DB fallback too
    term = question.split("for", 1)[0]
    words = re.findall(r"[A-Za-z]+", term)
    stop = {"what","give","show","me","and","the","of","in"}
    term = " ".join(w for w in words if w.lower() not in stop)
    return await _db_ticker(term)

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
    async with db.pool.acquire() as conn:
        rows = await conn.fetch(sql, term, limit)
    return [dict(r) for r in rows]
