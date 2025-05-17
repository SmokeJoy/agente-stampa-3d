"""Main entry point for FastAPI application."""

import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import uploader_router

# API version and prefix constants
API_VERSION = "v1"
API_PREFIX = f"/api/{API_VERSION}"

# Create the FastAPI app with metadata
app = FastAPI(
    title="API Assistente Lavori 3D",
    description=(
        "API per l'assistente di stampa 3D con funzionalità di upload, "
        "ricerca e calendario"
    ),
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(uploader_router, prefix=API_PREFIX)


# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage startup and shutdown events."""
    # Startup logic
    print("Application startup...")
    from config.upload_settings import UPLOAD_ROOT

    if not os.path.exists(UPLOAD_ROOT):
        Path(UPLOAD_ROOT).mkdir(parents=True, exist_ok=True)
        print(f"Created upload directory: {UPLOAD_ROOT}")
    else:
        print(f"Upload directory already exists: {UPLOAD_ROOT}")

    yield

    # Shutdown logic
    print("Application shutdown...")
    # Qui eventuali operazioni di cleanup, es. chiusura connessioni Redis
    pass


# Aggiorna l'app con il lifespan manager
app.router.lifespan_context = lifespan


@app.get("/")
async def root():
    """Root endpoint that returns information about the API."""
    return {
        "app": "API Assistente Lavori 3D",
        "version": app.version,
        "endpoints": [
            {"path": "/", "methods": ["GET"], "summary": "Root endpoint with API info"},
            {
                "path": f"{API_PREFIX}/upload",
                "methods": ["POST"],
                "summary": "Upload 3D models",
            },
        ],
    }
