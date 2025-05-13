import whisper
from pathlib import Path
from .config import settings

_model_cache: dict[str, whisper.Whisper] = {}


def _get_model(size: str) -> whisper.Whisper:
    """Load and cache a Whisper model of the given size."""
    if size not in _model_cache:
        _model_cache[size] = whisper.load_model(size)
    return _model_cache[size]


def transcribe(audio_path: Path, model_size: str | None = None) -> str:
    """Return plain-text transcription of `audio_path`, using the specified or default model size."""
    size = model_size or settings.whisper_model_size
    model = _get_model(size)
    result = model.transcribe(str(audio_path))
    return result["text"].strip()
