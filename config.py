import os
from pathlib import Path

class Config:
    # Base path configuration - following software practices
    BASE_PATH = os.getenv("BASE_PATH", str(Path.cwd()))
    VIDEO_UPLOAD_BASE_PATH = os.path.join(BASE_PATH, "uploads", "videos", "internal")
    
    # Ensure the upload directory exists
    @classmethod
    def ensure_upload_directory(cls):
        Path(cls.VIDEO_UPLOAD_BASE_PATH).mkdir(parents=True, exist_ok=True)
