"""
Health check API routes.
"""
from fastapi import APIRouter
import pandas as pd

from ...models import HealthResponse

router = APIRouter()


@router.get("/ping")
async def ping():
    """
    Simple ping endpoint.
    EXACT COPY of original main.py /ping endpoint.
    """
    return {"message": "pong"}


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Comprehensive health check endpoint.
    """
    return HealthResponse(
        status="healthy",
        timestamp=pd.Timestamp.utcnow().isoformat(),
        version="1.0.0"
    )
