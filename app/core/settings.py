# app/core/settings.py
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # app
    app_name: str = "questbackend"
    host: str = "127.0.0.1"
    port: int = 8000
    reload: bool = True

    # generic DB/url (optional)
    database_url: Optional[str] = None

    # --- Snowflake config (declare env vars you will use) ---
    sf_user: Optional[str] = None
    sf_password: Optional[str] = None
    sf_account: Optional[str] = None
    sf_database: str = "SNOWFLAKE_LEARNING_DB"
    sf_schema: str = "PUBLIC"
    sf_warehouse: Optional[str] = None
    sf_role: Optional[str] = None

    # pydantic-settings configuration: read .env and be case-insensitive
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

# global settings instance
settings = Settings()
