import httpx, asyncio
from app.core.config import settings

async def call_fmp(endpoint: str, **params):
    """
    Generic FMP GET helper.
    Usage:  await call_fmp("income-statement/AAPL", limit=1)
    """
    url = f"{str(settings.fmp_base_url).rstrip('/')}/{endpoint.lstrip('/')}"
    params["apikey"] = settings.fmp_api_key
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        return r.json()


# Convenience example
async def latest_income_statement(ticker: str):
    data = await call_fmp(f"income-statement/{ticker}", limit=1)
    return data[0] if data else None
