from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    LLM_PROVIDER: str = "groq"
    GROQ_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    MAX_EXECUTION_TIME_SECONDS: int = 10
    MAX_MEMORY_MB: int = 256
    MAX_CODE_SIZE_BYTES: int = 65536
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173"]

    class Config:
        env_file = ".env"

settings = Settings()
