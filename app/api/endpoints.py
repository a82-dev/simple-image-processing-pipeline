import os
import shutil

from celery.result import AsyncResult
from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse

from app.core.config import settings
from app.worker.celery_app import celery_app
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


@router.get("/status/{task_id}")
async def get_task_status(task_id: str, request: Request):
    """
    Checks Redis for the current status of the task.
    """
    task_result = AsyncResult(task_id, app=celery_app)

    response = {
        "task_id": task_id,
        "status": task_result.status,
    }

    if task_result.status == "SUCCESS":
        filename = task_result.result["file"]

        base = str(request.base_url)

        response["download_url"] = f"{base}api/v1/download/{filename}"

    return response


@router.get("/download/{filename}")
async def download_result(filename: str):
    """
    download the processed image.
    """
    file_path = os.path.join(settings.PROCESSED_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found or expired.")

    return FileResponse(path=file_path, filename=filename, media_type="image/jpeg")
