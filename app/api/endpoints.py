import os
import shutil

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core.config import settings
from app.worker.tasks import filter_image_task

router = APIRouter()


@router.get("/health", status_code=200)
async def health_check():
    """
    Check if the API is up and running.
    """
    return {"status": "ok", "message": "Pipeline API is running"}


@router.post("/process", status_code=202)
async def process_image(file: UploadFile = File(...)):
    """
    Accepts an image, saves it, and create a Celery task.
    """

    # File extentions validation
    allowed_extensions = {".jpg", ".jpeg", ".png"}
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only JPG and PNG are allowed."
        )

    file_path = os.path.join(settings.UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    task = filter_image_task.delay(file.filename)

    return {
        "message": "Image uploaded successfully. Processing in background.",
        "task_id": task.id,
    }
