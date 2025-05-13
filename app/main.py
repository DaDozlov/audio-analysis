from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import os
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .audio_processing import preprocess_audio
from .transcription import transcribe
from .analysis import analyse_transcript
from .storage import save_transcription_file
from fastapi.staticfiles import StaticFiles

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(settings.temp_dir, exist_ok=True)
os.makedirs(settings.data_dir, exist_ok=True)

app.mount(
    "/transcripts",
    StaticFiles(directory=settings.data_dir, html=False),
    name="transcripts",
)


@app.post("/transcribe")
async def transcribe_endpoint(
    file: UploadFile = File(...),
    industry: str | None = Form(None),
    user_id: str = Form(...),
    organisation_id: str = Form(...),
    file_name: str = Form(...),
):
    try:
        file_bytes = await file.read()
        audio_path = preprocess_audio(
            file_bytes, filename_ext=file.filename.split(".")[-1]
        )
        transcript_text = transcribe(audio_path)
        analysis_text = await analyse_transcript(transcript_text, industry)

        return {"transcription": transcript_text, "analysis": analysis_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        try:
            os.remove(audio_path)
        except Exception:
            pass


@app.post("/save_transcription")
async def save_transcription(
    content: str = Form(...),
    user_id: str = Form(...),
    organisation_id: str = Form(...),
    file_name: str = Form(...),
):
    try:
        path = save_transcription_file(
            content=content,
            organisation_id=organisation_id,
            user_id=user_id,
            file_name=file_name,
        )
        return {"success": True, "file_path": str(path)}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save transcription: {e}",
        )
