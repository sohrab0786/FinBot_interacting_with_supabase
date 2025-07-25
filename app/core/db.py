import asyncpg
import sys
from supabase import create_client, Client
from .config import settings  # loads .env via Pydantic already
import logging

pool: asyncpg.Pool | None = None
supabase: Client | None = None

# Use the value directly from settings, not os.getenv
SUPABASE_DB_URL = settings.supabase_db_url

async def init_pool():
    global pool

    if settings.data_source != "supabase":
        return

    if not SUPABASE_DB_URL:
        sys.exit("❌ SUPABASE_DB_URL not set in environment or config")

    if pool is None or pool._closed:
        try:
            pool = await asyncpg.create_pool(
                dsn=SUPABASE_DB_URL,
                min_size=1,
                max_size=10,
                max_inactive_connection_lifetime=300,
                command_timeout=60
            )
            print("✅ Database connection pool initialized.")
        except Exception as e:
            print(f"❌ Failed to initialize DB pool: {e}")
            raise

async def get_conn():
    global pool
    if pool is None or pool._closed:
        await init_pool()
    return await pool.acquire()

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
