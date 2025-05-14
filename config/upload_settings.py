"""Configuration settings for the uploader service."""

from pathlib import Path

# Root directory for uploads
UPLOAD_ROOT: Path = Path("/workspace/uploads")

# Maximum upload size in Megabytes
MAX_UPLOAD_SIZE_MB: int = 100

# Allowed MIME types for upload
ALLOWED_MIME_TYPES: list[str] = [
    "application/sla",  # .stl (ASCII)
    "model/stl",  # .stl (binary, common)
    "application/vnd.ms-pki.stl",  # .stl (another common one)
    "model/obj",  # .obj
    "text/plain",  # .obj (often as text/plain with .obj extension)
]

# Derived settings
MAX_UPLOAD_SIZE_BYTES: int = MAX_UPLOAD_SIZE_MB * 1024 * 1024

# Ensure the UPLOAD_ROOT directory exists (optional)
# UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)
