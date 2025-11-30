# app/core/config.py
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o"

    model_config = SettingsConfigDict(env_file=".env")

print(Settings())
settings = Settings()


