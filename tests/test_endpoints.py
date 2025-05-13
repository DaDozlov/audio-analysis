import io
from fastapi import status


def test_transcribe_endpoint(client, monkeypatch, sine_wav_bytes):
    class DummyModel:
        def transcribe(self, _):
            return {"text": "Hello test"}

    monkeypatch.setattr("app.transcription.whisper.load_model", lambda *_: DummyModel())

    async def fake_analysis(text, industry):
        return "## Aufgaben\n- Task 1"

    monkeypatch.setattr("app.main.analyse_transcript", fake_analysis)

    resp = client.post(
        "/transcribe",
        files={"file": ("sine.mp3", sine_wav_bytes, "audio/mp3")},
        data={"user_id": "u1", "organisation_id": "org1"},
    )
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    assert data["transcription"] == "Hello test"
    assert "Task 1" in data["analysis"]
