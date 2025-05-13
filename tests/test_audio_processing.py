import pytest
from pydub import AudioSegment
from app.audio_processing import preprocess_audio


def test_preprocess_audio(tmp_settings, sine_wav_bytes, tmp_path):
    mp3_path = preprocess_audio(sine_wav_bytes, "wav")
    assert mp3_path.exists()

    audio = AudioSegment.from_mp3(mp3_path)
    assert audio.frame_rate == 16000
    assert audio.channels == 1
    assert audio.duration_seconds == pytest.approx(1, rel=0.2)
