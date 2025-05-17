"""Router for file upload endpoints."""

import os
from typing import Optional

from fastapi import (APIRouter, File, Form, HTTPException, Request, Response,
                     UploadFile, status)

from config import upload_settings
from services.uploader.uploader_service import upload_file
from utils.ratelimit import rate_limit

# Prefissi per i codici HTTP e messaggi di errore di validazione
# Status code policy:
# - 400 Bad Request: errori di validazione nel router (file mancante, filename vuoto)
# - 413 Request Entity Too Large: file troppo grande
# - 415 Unsupported Media Type: tipo file non supportato
# - 422 Unprocessable Entity: validazione automatica FastAPI dei parametri
# - 429 Too Many Requests: rate limiting
# - 500 Internal Server Error: errori interni  # noqa: E501

# Create router with prefix and tags
router = APIRouter(
    tags=["upload"],
)

# Parameter descriptions for Form
WEBHOOK_DESC = "Optional webhook URL to notify when processing completes"
SIZE_DESC = "Optional override for maximum upload size in bytes"


@router.post(
    "/upload",
    summary="Upload a 3D model file",
    description=(
        "Upload an STL or OBJ file for 3D printing. "
        "Files are validated for type and size."
    ),
    response_description="File upload result with metadata and storage information",  # noqa: E501
    status_code=status.HTTP_201_CREATED,
)
@rate_limit(
    key_prefix="upload", max_calls=10, window_seconds=60
)  # 10 uploads per minute per IP/API key
async def upload_model(
    request: Request,
    response: Response,
    file: UploadFile = File(...),
    webhook_url: Optional[str] = Form(default=None, description=WEBHOOK_DESC),
    max_size_bytes: Optional[int] = Form(default=None, description=SIZE_DESC),
) -> dict:
    """Handle upload of 3D model files (STL, OBJ).

    Args:
        request: FastAPI request object
        response: FastAPI response object
        file: The uploaded file
        webhook_url: Optional webhook URL to notify on completion
        max_size_bytes: Optional override for maximum upload size in bytes  # noqa: E501

    Returns:
        dict: Upload result with file metadata

    Raises:
        HTTPException:
            - 400: Se il file non ha un nome
            - 413: Se il file supera la dimensione massima
            - 415: Se il tipo MIME non è supportato  # noqa: E501
            - 422: Se il parametro è invalido (gestito automaticamente da FastAPI)  # noqa: E501
            - 429: Se il rate limit è superato
            - 500: Per errori interni
    """
    # Check if filename exists - questa validazione deve avvenire PRIMA delle validazioni
    # automatiche di FastAPI, altrimenti sarà FastAPI a gestire questo caso con 422  # noqa: E501
    if not file or not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="File has no name"
        )

    # Use environment variable override if provided, otherwise use config or passed value
    effective_max_size = (
        int(os.environ.get("MAX_UPLOAD_SIZE_BYTES"))
        if "MAX_UPLOAD_SIZE_BYTES" in os.environ
        else (max_size_bytes or upload_settings.MAX_UPLOAD_SIZE_BYTES)
    )

    try:
        # Process the upload through the service
        result = await upload_file(
            file,
            webhook_url=webhook_url,
            max_size_bytes=effective_max_size,
        )

        # Return the result with 201 Created status
        return result.model_dump()

    except HTTPException:
        # Re-raise any HTTPExceptions (413, 415, 500)
        raise

    except Exception as e:
        # Log the error (in production this would use structured logging)
        print(f"Error during upload: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during upload. Please try again later.",
        )
