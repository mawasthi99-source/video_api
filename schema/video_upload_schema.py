from pydantic import BaseModel
from typing import Optional

class VideoUploadResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    file_path: Optional[str] = None

