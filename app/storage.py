from pathlib import Path
from datetime import datetime
from .config import settings

def save_transcription_file(
    content: str,
    organisation_id: str,
    file_name: str,
) -> Path:
    """Save the analysis as a distinct file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = f"transcription_{timestamp}_{file_name}.txt"

    out_dir = (
        settings.data_dir
        / organisation_id
        / "data"
        / "public"
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / safe_name
    out_path.write_text(content, encoding="utf-8")
    return out_path