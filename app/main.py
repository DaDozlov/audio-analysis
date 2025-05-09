from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import shutil
import os
from .config import settings
from .audio_processing import preprocess_audio
from .transcription import transcribe
from .analysis import analyse_transcript
from .storage import save_output

app = FastAPI(title=settings.app_name)

@app.post("/transcribe")
async def transcribe_endpoint(
    file: UploadFile = File(...),
    industry: str | None = Form(None),
    user_id: str = Form(...),
    organisation_id: str = Form(...),
):
    try:
        file_bytes = await file.read()
        audio_path = preprocess_audio(file_bytes, filename_ext=file.filename.split(".")[-1])
        transcript_text = transcribe(audio_path)
        analysis_text = analyse_transcript(transcript_text, industry)
        return {"transcription": transcript_text, "analysis": analysis_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        try:
            os.remove(audio_path)
        except Exception:
            pass

@app.post("/save")
async def save_endpoint(
    content: str = Form(...),
    user_filename: str = Form(...),
    organisation_id: str = Form(...),
):
    path = save_output(content, user_filename, organisation_id)
    return {"success": True, "file_path": str(path)}