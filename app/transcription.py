import whisper
from pathlib import Path
from .config import settings

_model_cache: whisper.Whisper | None = None

def _get_model():
    global _model_cache
    if _model_cache is None:
        _model_cache = whisper.load_model(settings.whisper_model_size)
    return _model_cache

def transcribe(audio_path: Path) -> str:
    """Return plain‑text transcription of `audio_path`."""
    model = _get_model()
    result = model.transcribe(str(audio_path))
    return result["text"].strip()