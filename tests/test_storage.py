from app.storage import save_output

def test_save_output(tmp_settings, tmp_path):
    content = "hello world"
    p = save_output(content, user_filename="demo", organisation_id="org1")
    assert p.exists()
    assert p.read_text() == content
    assert "org1" in p.parts