from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# config classes
class Settings(BaseSettings):
    
    # general
    app_name: str = "Audio‑Transcribe"

    # paths
    temp_dir: Path = BASE_DIR / ".." / ".." / "temp"
    data_dir: Path = BASE_DIR / ".." / ".." / "spaces"

    # whisper
    whisper_model_size: str = "medium"

    # ollama
    ollama_model: str = "llama3.2"
    ollama_base_url: str | None = None
    ollama_host: str | None = None

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"

settings = Settings()