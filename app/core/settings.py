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

        # Snowflake settings
    snowflake_user: Optional[str] = None
    snowflake_password: Optional[str] = None
    snowflake_account: Optional[str] = None
    snowflake_role: Optional[str] = None
    snowflake_warehouse: Optional[str] = None
    snowflake_database: Optional[str] = None
    snowflake_schema: Optional[str] = None


    # pydantic-settings configuration: read .env and be case-insensitive
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

# global settings instance
settings = Settings()
