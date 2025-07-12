# scripts/peek_fin_data.py
import asyncio, asyncpg, os
dsn = os.getenv("SUPABASE_DB_URL")
async def main():
    conn = await asyncpg.connect(dsn)
    rows = await conn.fetch("""
        SELECT statement, metric, fiscal_year, fiscal_period, value
        FROM financial.financial_fact
        WHERE ticker = 'AAPL'
        AND fiscal_year = 2023
        AND fiscal_period = 'FY'
    """)
    for r in rows:
        print(r)
    await conn.close()
asyncio.run(main())
