from fastapi import APIRouter

router = APIRouter()


@router.get("/health", status_code=200)
async def health_check():
    """
    Check if the API is up and running.
    """
    return {"status": "ok", "message": "Pipeline API is running"}
