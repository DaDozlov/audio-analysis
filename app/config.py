from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

API_URL = "http://localhost:8000"


# config classes
class Settings(BaseSettings):

    # general
    app_name: str = "Audio‑Transcribe"

    # paths
    temp_dir: Path = BASE_DIR / "temp"
    data_dir: Path = BASE_DIR / "spaces"

    # whisper
    whisper_model_size: str = "small"

    # ollama
    ollama_model: str = "llama3.2:1b"
    ollama_base_url: str | None = None
    ollama_host: str | None = None

    # openai
    openai_api_key: str | None = None
    openai_model: str = "gpt-3.5-turbo"
    openai_temperature: float = 0.2
    openai_max_tokens: int = 1024

    # groq
    groq_api_key: str | None = None
    groq_model: str = "meta-llama/llama-4-scout-17b-16e-instruct"
    groq_temperature: float = 0.2
    groq_max_tokens: int = 1024

    groq_model: str = "meta-llama/llama-4-scout-17b-16e-instruct"

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"


settings = Settings()
