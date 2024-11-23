import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
import firebase_admin
from firebase_admin import credentials

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    FIREBASE_CREDENTIALS_PATH: str
    CHUNK_SIZE: int = 2000
    CHUNK_OVERLAP: int = 200
    TAVILY_API_KEY: str | None = None
    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_ENDPOINT: str | None = None
    LANGCHAIN_API_KEY: str | None = None
    LANGCHAIN_PROJECT: str | None = None
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow"  # 추가 필드 허용
    )

@lru_cache()
def get_settings():
    return Settings()

# Firebase 초기화
try:
    cred = credentials.Certificate(get_settings().FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)
except ValueError:
    # 이미 초기화된 경우 패스
    pass