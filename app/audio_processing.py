from pydub import AudioSegment, effects
from uuid import uuid4
from pathlib import Path
from .config import settings


def preprocess_audio(file_bytes: bytes, filename_ext: str = "wav") -> Path:
    """Return a path to a normalised mono 16 kHz MP3 in TEMP_DIR."""
    tmp_raw = settings.temp_dir / f"raw_{uuid4().hex}.{filename_ext}"
    tmp_raw.parent.mkdir(parents=True, exist_ok=True)
    tmp_raw.write_bytes(file_bytes)

    audio = AudioSegment.from_file(tmp_raw)
    audio = audio.set_channels(1)
    audio = audio.set_frame_rate(16000)
    audio = effects.normalize(audio)

    mp3_path = settings.temp_dir / f"audio_{uuid4().hex}.mp3"
    audio.export(mp3_path, format="mp3", bitrate="64k")

    tmp_raw.unlink(missing_ok=True)
    return mp3_path