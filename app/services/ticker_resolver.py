# app/services/ticker_resolver.py
"""
Resolve user-typed company text → stock ticker
using the refdata.companies table in Supabase/Postgres.
"""

from typing import List, Dict
import asyncpg
from app.core import db


async def suggest(term: str, limit: int = 8) -> List[Dict]:
    """
    Returns list[{ticker, company_name, score}] ordered best→worst.

    * symbol prefix match gets priority score 100
    * trigram similarity on company_name gets actual similarity*100
    """
    term = term.strip()
    if not term:
        return []

    sql = """
      WITH q AS ( SELECT $1::text AS term )
      SELECT
          c.symbol              AS ticker,
          c.company_name,
          CASE
            WHEN c.symbol ILIKE term || '%' THEN 100                
            ELSE (similarity(c.company_name, term) * 100)::int
          END                    AS score
      FROM refdata.companies c, q
      WHERE
            c.symbol ILIKE term || '%'                
         OR similarity(c.company_name, term) > 0.35   
      ORDER BY
          CASE WHEN c.symbol ILIKE term || '%' THEN 0 ELSE 1 END, 
          score DESC
      LIMIT $2;
    """

    async with db.pool.acquire() as conn:
        rows = await conn.fetch(sql, term, limit)

    return [dict(r) for r in rows]


async def resolve_one(term: str) -> str | None:
    """Return best ticker match or None."""
    rows = await suggest(term, limit=1)
    return rows[0]["ticker"] if rows else None
