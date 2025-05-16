"""Router for file upload endpoints."""

import os
from typing import Optional

from fastapi import (APIRouter, File, Form, HTTPException, Request, Response,
                     UploadFile, status)

from config import upload_settings
from services.uploader.uploader_service import upload_file
from utils.ratelimit import rate_limit

# Create router with prefix and tags
router = APIRouter(
    tags=["upload"],
)


@router.post(
    "/upload",
    summary="Upload a 3D model file",
    description=(
        "Upload an STL or OBJ file for 3D printing. "
        "Files are validated for type and size."
    ),
    response_description="File upload result with metadata and storage information",
    status_code=status.HTTP_201_CREATED,
)
@rate_limit(limit=10, window=60)  # 10 uploads per minute per IP/API key
async def upload_model(
    request: Request,
    response: Response,
    file: UploadFile = File(...),
    webhook_url: Optional[str] = Form(
        None, description="Optional webhook URL to notify when processing completes"
    ),
    max_size_bytes: Optional[int] = Form(
        None, description="Optional override for maximum upload size in bytes"
    ),
) -> dict:
    """Handle upload of 3D model files (STL, OBJ).

    Args:
        request: FastAPI request object
        response: FastAPI response object
        file: The uploaded file
        webhook_url: Optional webhook URL to notify on completion
        max_size_bytes: Optional override for maximum upload size in bytes

    Returns:
        dict: Upload result with file metadata

    Raises:
        HTTPException: If validation fails or rate limit is exceeded
    """
    # Check if we have a file
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    # Check if filename exists
    if not file.filename:
        raise HTTPException(status_code=400, detail="File has no name")

    # Use environment variable override if provided, otherwise use config or passed value
    effective_max_size = (
        int(os.environ.get("MAX_UPLOAD_SIZE_BYTES"))
        if "MAX_UPLOAD_SIZE_BYTES" in os.environ
        else (max_size_bytes or upload_settings.MAX_UPLOAD_SIZE_BYTES)
    )

    try:
        # Process the upload through the service
        result = await upload_file(  # noqa: E501
            file, webhook_url=webhook_url, max_size_bytes=effective_max_size
        )

        # Return the result with 201 Created status
        return result.model_dump()

    except HTTPException:
        # Re-raise any HTTPExceptions (from validation, rate limiting, etc)
        raise

    except Exception as e:
        # Log the error (in production this would use structured logging)
        print(f"Error during upload: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred during upload. Please try again later.",
        )
