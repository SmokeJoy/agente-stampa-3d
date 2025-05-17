"""TODO: Implement MIME type validation for uploader."""

import inspect
import re
from pathlib import Path
from typing import NamedTuple

from fastapi import HTTPException, UploadFile, status

from config import upload_settings

_INVALID_CHARS = re.compile(r"[^A-Za-z0-9_.\-]")


class ValidatedFile(NamedTuple):
    """Risultato della validazione di un file."""

    sanitized_filename: str
    size: int
    mime_type: str


def validate_mime(file_mime: str | None, allowed_mimes: list[str]) -> bool:
    """Validates the MIME type of the uploaded file."""
    if file_mime is None:
        return False
    return file_mime in allowed_mimes


def validate_size(file_size: int | None, max_size_bytes: int) -> bool:
    """Validates the size of the uploaded file."""
    if file_size is None:
        return False  # Should not happen if UploadFile is processed correctly
    return file_size <= max_size_bytes


def sanitize_filename(filename: str) -> str:
    path_name = Path(filename).name
    if path_name in ("", "."):
        path_name = "default_filename"

    stem, dot, ext = path_name.partition(".")
    if not stem:
        stem = "sanitized_file"
    if not dot:
        ext = "dat"

    safe_stem = _INVALID_CHARS.sub("_", stem)
    safe_name = f"{safe_stem}.{ext}"
    if len(safe_name) > 255:
        keep = 255 - len(ext) - 1
        safe_stem_trimmed = safe_stem[: max(0, keep)]
        safe_name = f"{safe_stem_trimmed}.{ext}"
    return safe_name


async def validate_upload_file(
    file: UploadFile,
    allowed_mimes: list[str] = upload_settings.ALLOWED_MIME_TYPES,
    max_size_bytes: int = upload_settings.MAX_UPLOAD_SIZE_BYTES,
) -> ValidatedFile:
    """
    Validates an UploadFile instance against MIME type and size.
    Raises HTTPException if the file is invalid.

    Args:
        file: The uploaded file
        allowed_mimes: List of allowed MIME types
        max_size_bytes: Maximum allowed file size in bytes

    Returns:
        ValidatedFile: Oggetto contenente i dati del file validato

    Raises:
        HTTPException: If file size exceeds the limit or MIME type is not allowed
    """
    file_size = getattr(file, "size", None)
    if file_size is None:
        # Try to get size by reading the file if 'size' attribute is not present
        # This is a fallback and might be slow for large files if not spooled to disk
        contents = await file.read()
        file_size = len(contents)
        if hasattr(file, "seek"):
            if inspect.iscoroutinefunction(file.seek):
                await file.seek(0)
            else:
                file.seek(0)  # Reset file pointer to the beginning

    if not validate_size(file_size, max_size_bytes):
        error_msg = (
            f"File size {file_size / (1024*1024):.2f} MB exceeds maximum of "
            f"{max_size_bytes / (1024*1024):.2f} MB."
        )
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=error_msg
        )

    if not validate_mime(file.content_type, allowed_mimes):
        allowed_types_str = ", ".join(allowed_mimes)
        error_msg = (
            f"File MIME type '{file.content_type}' is not allowed. "
            f"Allowed types: {allowed_types_str}."
        )
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail=error_msg
        )

    sanitized = sanitize_filename(file.filename or "default_upload")

    return ValidatedFile(sanitized, file_size, file.content_type)
