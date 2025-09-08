from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router.video_upload_router import interview_router
from config import Config
from logger import setup_custom_logger

logger = setup_custom_logger(__name__)


app = FastAPI(
    title="Interview Video Upload API",
    description="API for uploading interview video files",
    version="1.0.0"
)

app.include_router(interview_router)

# Startup event
@app.on_event("startup")
async def startup_event():
    Config.ensure_upload_directory()
    logger.info("Application started successfully")
    logger.info(f"Video upload base path: {Config.VIDEO_UPLOAD_BASE_PATH}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
