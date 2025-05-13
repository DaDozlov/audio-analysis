def test_save_transcription_endpoint(client):
    resp = client.post(
        "/save_transcription",
        data={
            "content": "unit‑test save",
            "user_id": "u1",
            "organisation_id": "org1",
            "file_name": "spec_format",
        },
    )
    assert resp.status_code == 200
    path = resp.json()["file_path"]
    assert "transcription_" in path and path.endswith("_spec_format.txt")
