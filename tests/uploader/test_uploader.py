# flake8: noqa
"""Tests for the uploader service and validator."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from config.upload_settings import ALLOWED_MIME_TYPES, MAX_UPLOAD_SIZE_BYTES
from services.uploader.uploader_service import UploadResult
from services.uploader.validator import (
    sanitize_filename,
    validate_mime,
    validate_size,
    validate_upload_file,
)

# Mock Redis client
mock_redis = MagicMock()
mock_redis.incr.return_value = 1
mock_redis.expire.return_value = True
mock_redis.ttl.return_value = 60

# Mock the RedisClient and rate_limit decorator
with (
    patch("services.redis.redis_client.default_redis_client", mock_redis),
    patch("utils.ratelimit.rate_limit", lambda *args, **kwargs: lambda f: f),
):
    # Import app after mocking Redis
    from main import app

    # Create test client
    client = TestClient(app)


# API Endpoint tests
def test_upload_endpoint_success():
    """Test successful upload to the API endpoint."""
    # Mock the upload_file function to avoid actual file processing
    with patch("routers.uploader.upload_file") as mock_upload:
        # Set up return value for the mock
        mock_result = UploadResult(
            file_id="test-uuid",
            filename="test_file.stl",
            content_type="model/stl",
            size=1024,
            status="stored",
            url="https://example.com/test-uuid",
        )
        mock_upload.return_value = mock_result

        # Create a test file
        test_file_content = b"test file content"

        # Make the request
        response = client.post(
            "/api/v1/upload",
            files={"file": ("test_file.stl", test_file_content, "model/stl")},
        )

        # Check response
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["file_id"] == "test-uuid"
        assert data["filename"] == "test_file.stl"
        assert data["content_type"] == "model/stl"
        assert data["size"] == 1024
        assert data["status"] == "stored"
        assert data["url"] == "https://example.com/test-uuid"

        # Verify the upload_file function was called with the correct arguments
        mock_upload.assert_called_once()


def test_upload_endpoint_with_webhook():
    """Test upload with webhook URL."""
    with patch("routers.uploader.upload_file") as mock_upload:
        mock_result = UploadResult(
            file_id="test-uuid-webhook",
            filename="test_file.stl",
            content_type="model/stl",
            size=1024,
            status="stored",
            url="https://example.com/test-uuid-webhook",
        )
        mock_upload.return_value = mock_result

        # Make the request with webhook URL
        response = client.post(
            "/api/v1/upload",
            files={"file": ("test_file.stl", b"test content", "model/stl")},
            data={"webhook_url": "https://example.com/webhook"},
        )

        # Check response
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["file_id"] == "test-uuid-webhook"

        # Verify webhook URL was passed
        mock_upload.assert_called_once()
        args, kwargs = mock_upload.call_args
        assert kwargs["webhook_url"] == "https://example.com/webhook"


def test_upload_endpoint_max_size_override():
    """Test upload with MAX_UPLOAD_SIZE_BYTES override."""
    with (
        patch("routers.uploader.upload_file") as mock_upload,
        patch.dict("os.environ", {"MAX_UPLOAD_SIZE_BYTES": "12345"}),
    ):

        mock_result = UploadResult(
            file_id="test-uuid-size",
            filename="test_file.stl",
            content_type="model/stl",
            size=1024,
            status="stored",
            url="https://example.com/test-uuid-size",
        )
        mock_upload.return_value = mock_result

        # Make the request
        response = client.post(
            "/api/v1/upload",
            files={"file": ("test_file.stl", b"test content", "model/stl")},
        )

        # Check response
        assert response.status_code == status.HTTP_201_CREATED

        # Verify max_size_bytes was passed correctly
        mock_upload.assert_called_once()
        args, kwargs = mock_upload.call_args
        assert kwargs["max_size_bytes"] == 12345


# TODO: Implement actual tests once service logic is in place.


@pytest.mark.skip(reason="TODO: Implement test_valid_stl_upload")
def test_valid_stl_upload():
    """Test uploading a valid STL file."""
    pass


@pytest.mark.skip(reason="TODO: Implement test_valid_obj_upload")
def test_valid_obj_upload():
    """Test uploading a valid OBJ file."""
    pass


@pytest.mark.skip(reason="TODO: Implement test_invalid_mime_type_upload")
def test_invalid_mime_type_upload():
    """Test uploading a file with an invalid MIME type."""
    pass


@pytest.mark.skip(reason="TODO: Implement test_upload_storage_called")
def test_upload_storage_called():
    """Test that the storage backend's save method is called."""
    pass


@pytest.mark.skip(reason="TODO: Implement test_file_id_returned_on_success")
def test_file_id_returned_on_success():
    """Test that a file_id and 'stored' status are returned on successful upload."""
    pass


# Tests for validator.py
@pytest.mark.skip(reason="TODO: Implement test_validator_valid_stl_mime")
def test_validator_valid_stl_mime():
    """Test validator with a valid STL MIME type."""
    pass


@pytest.mark.skip(reason="TODO: Implement test_validator_valid_obj_mime")
def test_validator_valid_obj_mime():
    """Test validator with a valid OBJ MIME type."""
    pass


@pytest.mark.skip(reason="TODO: Implement test_validator_invalid_mime")
def test_validator_invalid_mime():
    """Test validator with an invalid MIME type."""
    pass


# Unit tests for uploader validators
@pytest.mark.parametrize(
    "file_mime, allowed_mimes, expected",
    [
        ("model/stl", ["model/stl", "model/obj"], True),
        ("application/pdf", ["model/stl", "model/obj"], False),
        ("model/stl", [], False),
        (None, ["model/stl"], False),
        ("model/obj", ALLOWED_MIME_TYPES, True),
        ("application/sla", ALLOWED_MIME_TYPES, True),
        ("application/zip", ALLOWED_MIME_TYPES, False),
    ],
)
def test_validate_mime(file_mime, allowed_mimes, expected):
    assert validate_mime(file_mime, allowed_mimes) == expected


@pytest.mark.parametrize(
    "file_size, max_size_bytes, expected",
    [
        (100, 200, True),
        (200, 200, True),
        (201, 200, False),
        (0, 100, True),
        (None, 100, False),
        (1024 * 1024, MAX_UPLOAD_SIZE_BYTES, True),
        (MAX_UPLOAD_SIZE_BYTES + 1, MAX_UPLOAD_SIZE_BYTES, False),
    ],
)
def test_validate_size(file_size, max_size_bytes, expected):
    assert validate_size(file_size, max_size_bytes) == expected


@pytest.mark.parametrize(
    "filename, expected",
    [
        ("test_file.stl", "test_file.stl"),
        ("../secret/file.txt", "file.txt"),  # Path traversal is handled by Path().name
        ("file with spaces.obj", "file_with_spaces.obj"),
        ("file<>$&*.stl", "file_____.stl"),  # Characters <>$&* are replaced by _
        # Define long strings for clarity and to help flake8
        pytest.param(
            "very_long_filename_" + "a" * 300 + ".stl",
            ("very_long_filename_" + "a" * 300)[:251] + ".stl",
            id="long_filename_truncation",
        ),  # noqa: E501
        (".stl", "sanitized_file.stl"),  # Only extension
        ("", "default_filename.dat"),  # Empty filename, gets .dat
        ("no_extension", "no_extension.dat"),
        ("file.with.dots.stl", "file.with.dots.stl"),
        ("file.tar.gz", "file.tar.gz"),  # Multiple dots in stem are kept if valid
        ("image.JPEG", "image.JPEG"),
        (
            "config.json.backup",
            "config.json.backup",
        ),  # Multiple dots in extension part are partitioned
        # Unicode characters are replaced by underscores by the current regex
        # "你好世界" (4 chars) seems to become "_____" (5 underscores) in practice
        ("file_with_你好世界.stl", "file_with_____.stl"),
    ],
)
def test_sanitize_filename(filename, expected):
    # The conditional modification for unicode is no longer needed as it's in parametrize
    assert sanitize_filename(filename) == expected


@pytest.mark.asyncio
async def test_validate_upload_file_valid():
    mock_file = MagicMock()
    mock_file.filename = "test.stl"
    mock_file.content_type = "model/stl"
    mock_file.size = 1024 * 50  # 50KB

    is_valid, msg, sanitized_name, f_size, f_mime = await validate_upload_file(
        mock_file, ALLOWED_MIME_TYPES, MAX_UPLOAD_SIZE_BYTES
    )
    assert is_valid is True
    assert msg == "File is valid."
    assert sanitized_name == "test.stl"
    assert f_size == mock_file.size
    assert f_mime == mock_file.content_type


@pytest.mark.asyncio
async def test_validate_upload_file_invalid_mime():
    mock_file = MagicMock()
    mock_file.filename = "test.pdf"
    mock_file.content_type = "application/pdf"
    mock_file.size = 1024 * 50

    is_valid, msg, _, _, _ = await validate_upload_file(
        mock_file, ALLOWED_MIME_TYPES, MAX_UPLOAD_SIZE_BYTES
    )
    assert is_valid is False
    assert "MIME type 'application/pdf' is not allowed" in msg


@pytest.mark.asyncio
async def test_validate_upload_file_invalid_size():
    mock_file = MagicMock()
    mock_file.filename = "large_file.stl"
    mock_file.content_type = "model/stl"
    mock_file.size = MAX_UPLOAD_SIZE_BYTES + 100

    is_valid, msg, _, _, _ = await validate_upload_file(
        mock_file, ALLOWED_MIME_TYPES, MAX_UPLOAD_SIZE_BYTES
    )
    assert is_valid is False
    assert "exceeds maximum" in msg


@pytest.mark.asyncio
async def test_validate_upload_file_no_size_attr_valid():
    # Simulate a file object that doesn't have a .size attribute initially
    # but whose size can be determined by reading.
    file_content = b"a" * (1024 * 10)  # 10KB
    mock_file = MagicMock(spec=["filename", "content_type", "read", "seek"])
    mock_file.filename = "good_file.obj"
    mock_file.content_type = "model/obj"

    # Mock read() to return content and seek() to reset
    async def mock_read():
        return file_content

    mock_file.read = MagicMock(side_effect=mock_read)
    mock_file.seek = MagicMock()
    # Remove size attribute if it was auto-added by MagicMock
    if hasattr(mock_file, "size"):
        delattr(mock_file, "size")

    is_valid, msg, sanitized_name, f_size, f_mime = await validate_upload_file(
        mock_file, ALLOWED_MIME_TYPES, MAX_UPLOAD_SIZE_BYTES
    )
    assert is_valid is True
    assert msg == "File is valid."
    assert sanitized_name == "good_file.obj"
    assert f_size == len(file_content)
    assert f_mime == mock_file.content_type
    mock_file.read.assert_called_once()
    mock_file.seek.assert_called_once_with(0)


@pytest.mark.asyncio
async def test_validate_upload_file_no_size_attr_too_large():
    file_content = b"a" * (MAX_UPLOAD_SIZE_BYTES + 1)
    mock_file = MagicMock(spec=["filename", "content_type", "read", "seek"])
    mock_file.filename = "too_big.stl"
    mock_file.content_type = "model/stl"

    async def mock_read():
        return file_content

    mock_file.read = MagicMock(side_effect=mock_read)
    mock_file.seek = MagicMock()
    if hasattr(mock_file, "size"):
        delattr(mock_file, "size")

    is_valid, msg, _, _, _ = await validate_upload_file(
        mock_file, ALLOWED_MIME_TYPES, MAX_UPLOAD_SIZE_BYTES
    )
    assert is_valid is False
    assert "exceeds maximum" in msg
    mock_file.read.assert_called_once()
    mock_file.seek.assert_called_once_with(0)
