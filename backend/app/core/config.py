from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR=Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    """Application settings."""

    APP_NAME: str = "KnowledgeForge AI"
    APP_V1_PREFIX: str = "/api/v1"
    OPENAI_API_KEY: str = ""
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-large"
    OPENAI_CHAT_MODEL: str = "gpt-4.1-mini"
    CHROMA_PERSIST_DIRECTORY:Path = BACKEND_DIR / "data"/"chroma"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10 MB
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 150

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()