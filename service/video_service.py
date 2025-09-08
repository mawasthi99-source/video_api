
import aiofiles
from pathlib import Path
from typing import Tuple
from config import Config
from logger import setup_custom_logger

logger = setup_custom_logger(__name__)

class VideoService:
    def __init__(self):
        self.base_path = Config.VIDEO_UPLOAD_BASE_PATH
        Config.ensure_upload_directory()
    
    def _get_interview_directory(self, interview_id: str) -> Path:
        return Path(self.base_path) / interview_id
    
    def _get_next_file_number(self, interview_dir: Path) -> int:
        if not interview_dir.exists():
            return 1
        
        existing_files = list(interview_dir.glob("*"))
        if not existing_files:
            return 1
        
        file_numbers = []
        for file_path in existing_files:
            try:
                file_number = int(file_path.stem)
                file_numbers.append(file_number)
            except ValueError:
                continue
        
        return max(file_numbers, default=0) + 1
    
    def _extract_file_extension(self, filename: str) -> str:
        if not filename:
            return '.mp4'
        
        extension = Path(filename).suffix.lower()
        
        supported_extensions = {'.mp4', '.webm', '.avi', '.mov', '.mkv', '.flv', '.wmv'}
        
        if extension in supported_extensions:
            return extension
        else:
            logger.warning(f"Unsupported or missing file extension '{extension}' for file '{filename}'. Defaulting to .mp4")
            return '.mp4'
    
    async def save_video_file(self, interview_id: str, file_content: bytes,filename: str) -> Tuple[bool, str, str]:

        try:
            interview_dir = self._get_interview_directory(interview_id)
            interview_dir.mkdir(parents=True, exist_ok=True)
            
            file_number = self._get_next_file_number(interview_dir)
            file_extension = self._extract_file_extension(filename)

            filename = f"{file_number}{file_extension}"
            file_path = interview_dir / filename
            
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(file_content)
            
            relative_path = f"/uploads/videos/internal/{interview_id}/{filename}"
            
            logger.info(f"Successfully saved video file: {relative_path}")
            return True, "File uploaded successfully", relative_path
            
        except Exception as e:
            error_msg = f"Failed to save video file for interview {interview_id}: {str(e)}"
            logger.error(error_msg)
            return False, error_msg, ""
