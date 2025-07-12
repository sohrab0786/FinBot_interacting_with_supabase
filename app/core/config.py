from pydantic_settings import BaseSettings
from pydantic import Field, AnyHttpUrl


class Settings(BaseSettings):
    # ── data source choice ──────────────────────────────────────────
    data_source: str = Field("supabase", env="DATA_SOURCE")  # supabase | fmp

    # ── Supabase (SQL + Storage) ───────────────────────────────────
    supabase_url: AnyHttpUrl | None = Field(None, env="SUPABASE_URL")
    supabase_service_key: str | None = Field(None, env="SUPABASE_SERVICE_KEY")
    supabase_db_url: str | None = Field(None, env="SUPABASE_DB_URL")
    supabase_bucket: str | None = Field("chatbot-outputs", env="SUPABASE_BUCKET")

    # ── FMP REST API ───────────────────────────────────────────────
    fmp_api_key: str | None = Field(None, env="FMP_API_KEY")
    fmp_base_url: AnyHttpUrl = Field(
        "https://financialmodelingprep.com/api/v3", env="FMP_BASE_URL"
    )

    # ── LLM back-end selector ──────────────────────────────────────
    llm_provider: str = Field("http", env="LLM_PROVIDER")  # http | openai
    # OpenAI-spec options (used by BOTH cloud & local HTTP)
    openai_base_url: AnyHttpUrl = Field("http://localhost:11434/v1", env="OPENAI_BASE_URL")
    openai_model: str = Field("llama3:8b", env="OPENAI_MODEL")
    openai_api_key: str | None = Field(None, env="OPENAI_API_KEY")  # optional for Ollama

    llm_temperature: float = Field(0.7, env="LLM_TEMPERATURE")
    llm_max_tokens: int = Field(1024, env="LLM_MAX_TOKENS")

    # ── server defaults (uvicorn) ──────────────────────────────────
    host: str = Field("0.0.0.0", env="HOST")
    port: int = Field(8000, env="PORT")
    log_level: str = Field("info", env="LOG_LEVEL")

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
