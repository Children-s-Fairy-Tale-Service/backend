# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
import os
print("[DEBUG] OPENAI_API_KEY =", os.environ.get("OPENAI_API_KEY"))
class Settings(BaseSettings):
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o"

    model_config = SettingsConfigDict(env_file=".env")

print(Settings())
settings = Settings()


