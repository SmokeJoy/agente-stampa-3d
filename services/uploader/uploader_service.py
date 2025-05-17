"""Uploader service logic.

This module implements the core business logic for the uploader service,
orchestrating the validation, storage, and webhook notification steps.
"""

# TODO: [G8] Implementare la logica di retry per le notifiche webhook
# - Aggiungere un sistema di coda per i webhook falliti
# - Implementare un backoff esponenziale per i retry
# - Gestire stati persistenti dei tentativi di notifica
# - Aggiungere un endpoint di callback per verificare lo stato

import uuid
from typing import Dict, Optional

import requests  # Uso requests invece di httpx per la compatibilità
from fastapi import HTTPException, UploadFile, status
from pydantic.main import BaseModel

from config import upload_settings
from services.uploader.storage import StorageBackend, default_storage
from services.uploader.validator import validate_upload_file


class UploadResult(BaseModel):
    """Result of an upload operation."""

    file_id: str
    filename: str
    content_type: str
    size: int
    status: str = "stored"
    url: str


async def upload_file(
    file: UploadFile,
    storage_backend: StorageBackend = default_storage,
    webhook_url: Optional[str] = None,
    allowed_mimes: list[str] = upload_settings.ALLOWED_MIME_TYPES,
    max_size_bytes: int = upload_settings.MAX_UPLOAD_SIZE_BYTES,
) -> UploadResult:
    """Handle the complete upload process.

    Args:
        file: The file to upload
        storage_backend: Storage backend to use
        webhook_url: Optional URL to send webhook notification to
        allowed_mimes: List of allowed MIME types
        max_size_bytes: Maximum allowed file size in bytes

    Returns:
        UploadResult: Object containing file metadata and status

    Raises:
        HTTPException: If validation fails or storage errors occur
    """
    # Validate the file - lancia HTTPException se il file non è valido
    validated_file = await validate_upload_file(
        file,
        allowed_mimes,
        max_size_bytes,
    )

    # Generate a unique file ID
    file_id = str(uuid.uuid4())

    try:
        # Store the file (may override file_id if the storage has its own ID generation)
        saved_file_id = await storage_backend.save(file, file_id)

        # Get the URL for the stored file
        file_url = storage_backend.get_url(saved_file_id)

        # Create the result
        result = UploadResult(
            file_id=saved_file_id,
            filename=validated_file.sanitized_filename,
            content_type=validated_file.mime_type,
            size=validated_file.size,
            status="stored",
            url=file_url,
        )

        # If a webhook URL was provided, notify it
        if webhook_url:
            notify_webhook(webhook_url, result.model_dump())

        return result

    except Exception as e:
        # Log the error (this would use a proper logger in production)
        print(f"Error storing file: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error storing file",
        ) from e


def notify_webhook(webhook_url: str, data: Dict) -> bool:
    """Send a notification to a webhook URL.

    Args:
        webhook_url: The URL to send the notification to
        data: The data to send

    Returns:
        bool: True if notification was successful, False otherwise
    """
    try:
        # Utilizzo requests che è già disponibile nel container
        response = requests.post(
            webhook_url,
            json=data,
            timeout=5.0,  # 5 second timeout for webhook calls
            headers={"Content-Type": "application/json"},
        )
        return 200 <= response.status_code < 300  # 2xx status codes
    except Exception:
        # Log the error but don't fail the upload
        # In production, this should use proper structured logging
        print(f"Failed to notify webhook at {webhook_url}")
        return False
