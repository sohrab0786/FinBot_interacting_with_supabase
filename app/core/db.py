import asyncpg, sys
from supabase import create_client, Client
from .config import settings

pool: asyncpg.Pool | None = None
supabase: Client | None = None


async def init_pool() -> None:
    """Create asyncpg pool if Supabase is selected."""
    global pool
    if settings.data_source != "supabase":
        return
    if not settings.supabase_db_url:
        sys.exit("❌ SUPABASE_DB_URL not set")
    pool = await asyncpg.create_pool(dsn=settings.supabase_db_url, max_size=10)


def init_supabase() -> None:
    global supabase
    if settings.data_source != "supabase":
        return
    if not (settings.supabase_url and settings.supabase_service_key):
        sys.exit("❌ SUPABASE_URL / SUPABASE_SERVICE_KEY not set")
    supabase = create_client(str(settings.supabase_url), settings.supabase_service_key)


async def close_pool() -> None:
    if pool:
        await pool.close()
