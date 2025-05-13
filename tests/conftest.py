import io
import wave
import numpy as np
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import config as cfg


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture(scope="session")
def sine_wav_bytes():
    """Return 1‑second 440 Hz mono WAV (16‑kHz, 16‑bit)."""
    sr = 16000
    t = np.linspace(0, 1, sr, endpoint=False)
    samples = (0.3 * np.sin(2 * np.pi * 440 * t) * 32767).astype(np.int16)

    buf = io.BytesIO()
    with wave.open(buf, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sr)
        wav.writeframes(samples.tobytes())
    buf.seek(0)
    return buf.read()


@pytest.fixture
def tmp_settings(tmp_path, monkeypatch):
    """Point BASE_DIR, temp_dir, data_dir to tmp_path for isolated tests."""
    monkeypatch.setattr(cfg.settings, "temp_dir", tmp_path / "temp")
    monkeypatch.setattr(cfg.settings, "data_dir", tmp_path / "spaces")
    cfg.settings.temp_dir.mkdir(parents=True, exist_ok=True)
    cfg.settings.data_dir.mkdir(parents=True, exist_ok=True)
    yield
