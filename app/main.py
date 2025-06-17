"""
Main FastAPI application for Climate Adaptation Simulation Backend.
Maintains exact compatibility with original main.py functionality.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd

try:
    from .config import settings
    from .api import api_router
    from .models import ErrorResponse
except ImportError:
    # For direct execution
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent))
    from app.config import settings
    from app.api import api_router
    from app.models import ErrorResponse

# Create FastAPI application
app = FastAPI(
    title="Climate Adaptation Simulation API",
    description="Backend API for climate change adaptation scenario simulation and analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware (maintaining original logic)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# For backward compatibility, also include routes at root level
app.include_router(api_router)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled errors.
    """
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            detail="Internal server error",
            error_code="INTERNAL_ERROR",
            timestamp=pd.Timestamp.utcnow().isoformat()
        ).model_dump()
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """
    HTTP exception handler for API errors.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            detail=exc.detail,
            error_code="HTTP_ERROR",
            timestamp=pd.Timestamp.utcnow().isoformat()
        ).model_dump()
    )


@app.on_event("startup")
async def startup_event():
    """
    Application startup event.
    """
    print("🚀 Climate Adaptation Simulation Backend starting up...")
    print(f"📊 Data directory: {settings.DATA_DIR}")
    print(f"🌐 CORS origins: {settings.CORS_ORIGINS}")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown event.
    """
    print("🛑 Climate Adaptation Simulation Backend shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
