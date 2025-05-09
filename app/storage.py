from pathlib import Path
from datetime import datetime
from .config import settings

def save_output(content: str, user_filename: str, organisation_id: str) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = f"{timestamp}_{user_filename}.txt"
    dir_ = settings.data_dir / organisation_id / "data" / "public"
    dir_.mkdir(parents=True, exist_ok=True)
    out_path = dir_ / safe_name
    out_path.write_text(content, encoding="utf-8")
    return out_path