from fastapi import UploadFile, HTTPException
from service.video_service import VideoService
from schema.video_upload_schema import VideoUploadResponse
from logger import setup_custom_logger

logger = setup_custom_logger(__name__)

class VideoUploadController:
    def __init__(self):
        self.video_service = VideoService()
    
    async def upload_video(self, interview_id: str, file: UploadFile) -> VideoUploadResponse:
       
        try:
            logger.info(f"Starting video upload for interview: {interview_id}")
            
            if not file.filename:
                raise HTTPException(status_code=400, detail="No file provided")
            
            file_content = await file.read()
            
            if not file_content:
                raise HTTPException(status_code=400, detail="Empty file provided")
            
            success, message, file_path = await self.video_service.save_video_file(
                interview_id, file_content,file.filename
            )
            
            if success:
                logger.info(f"Video upload completed successfully for interview: {interview_id}")
                return VideoUploadResponse(
                    success=True,
                    message=message,
                    file_path=file_path
                )
            else:
                logger.error(f"Video upload failed for interview: {interview_id} - {message}")
                raise HTTPException(status_code=500, detail=message)
                
        except HTTPException:
            raise
        except Exception as e:
            error_msg = f"Unexpected error during video upload: {str(e)}"
            logger.error(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)
