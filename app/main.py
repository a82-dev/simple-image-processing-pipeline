from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import router as api_router
from app.core.config import settings


def create_app() -> FastAPI:
    """
    Initialize Fastapi app.
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="Asynchronous Media Processing Pipeline",
        version="1.0.0",
    )

    # Set up CORS for the future if needed
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix="/api/v1")

    return app


app = create_app()
