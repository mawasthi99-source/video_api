from fastapi import APIRouter, UploadFile, File, Path, Depends
from controller.video_upload_controller import VideoUploadController
from schema.video_upload_schema import VideoUploadResponse
from logger import setup_custom_logger

logger = setup_custom_logger(__name__)

interview_router = APIRouter(prefix="/interview", tags=["interviews"])

def get_interview_controller() -> VideoUploadController:
    return VideoUploadController()

@interview_router.post(
    "/interviews/{interview_id}/video/upload",
    response_model=VideoUploadResponse,
    summary="Upload video file for interview",
    description="Upload video file (blob) for a specific interview. Files are stored with sequential naming."
)
async def upload_video(
    interview_id: str = Path(..., description="The interview identifier"),
    file: UploadFile = File(..., description="Video file to upload"),
    controller: VideoUploadController = Depends(get_interview_controller)
) -> VideoUploadResponse:

    logger.info(f"Received video upload request for interview: {interview_id}")

    try:
        result= await controller.upload_video(interview_id, file)
        return result
    except Exception as e:
        return False

