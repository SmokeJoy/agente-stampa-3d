# flake8: noqa
"""Tests for the uploader service and validator."""

import sys
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException, status
from fastapi.testclient import TestClient

from config.upload_settings import ALLOWED_MIME_TYPES, MAX_UPLOAD_SIZE_BYTES
# from main import API_PREFIX # Rimosso
from services.uploader.uploader_service import UploadResult, upload_file
from services.uploader.validator import (ValidatedFile, sanitize_filename,
                                         validate_mime, validate_size,
                                         validate_upload_file)
from tests.conftest import redis_patch

# # Mock Redis client # Rimosso
# mock_redis = MagicMock() # Rimosso
# mock_redis.incr.return_value = 1 # Rimosso
# mock_redis.expire.return_value = True # Rimosso
# mock_redis.ttl.return_value = 60 # Rimosso

# # Mock the RedisClient and rate_limit decorator # Rimosso blocco intero
# with patch("utils.ratelimit.rate_limit", lambda *args, **kwargs: lambda f: f):
#     # Import app after mocking Redis
#     from main import app
#
#     # Create test client
#     client = TestClient(app)


@pytest.fixture(scope="function")
def test_app_client():
    """Fixture to create a TestClient instance with mocks for each test function."""
    # Import app DOPO che la fixture redis_patch è già stata attivata (grazie a autouse=True)
    from main import API_PREFIX, app

    # Crea il client di test
    client = TestClient(app)
    # Ritorna sia il client che l'API_PREFIX
    yield client, API_PREFIX


# API Endpoint tests
def test_upload_endpoint_success(test_app_client):
    """Test successful upload to the API endpoint."""
    # Estrai client e API_PREFIX dalla fixture
    client, api_prefix = test_app_client

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
            f"{api_prefix}/upload",
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


def test_upload_endpoint_with_webhook(test_app_client):
    """Test upload with webhook URL."""
    # Estrai client e API_PREFIX dalla fixture
    client, api_prefix = test_app_client

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
            f"{api_prefix}/upload",
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


def test_upload_endpoint_max_size_override(test_app_client):
    """Test upload with MAX_UPLOAD_SIZE_BYTES override."""
    # Estrai client e API_PREFIX dalla fixture
    client, api_prefix = test_app_client

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
            f"{api_prefix}/upload",
            files={"file": ("test_file.stl", b"test content", "model/stl")},
        )

        # Check response
        assert response.status_code == status.HTTP_201_CREATED

        # Verify max_size_bytes was passed correctly
        mock_upload.assert_called_once()
        args, kwargs = mock_upload.call_args
        assert kwargs["max_size_bytes"] == 12345


def test_upload_endpoint_max_size_custom_parameter_override(test_app_client):
    """Test upload with explicit max_size_bytes parameter."""
    # Estrai client e API_PREFIX dalla fixture
    client, api_prefix = test_app_client

    with patch("routers.uploader.upload_file") as mock_upload:
        mock_result = UploadResult(
            file_id="test-uuid-custom-size",
            filename="test_file.stl",
            content_type="model/stl",
            size=1024,
            status="stored",
            url="https://example.com/test-uuid-custom-size",
        )
        mock_upload.return_value = mock_result

        # Make the request with custom max_size_bytes parameter
        response = client.post(
            f"{api_prefix}/upload",
            files={"file": ("test_file.stl", b"test content", "model/stl")},
            data={"max_size_bytes": "54321"},
        )

        # Check response
        assert response.status_code == status.HTTP_201_CREATED

        # Verify max_size_bytes was passed correctly
        mock_upload.assert_called_once()
        args, kwargs = mock_upload.call_args
        # It should be an int, not a string
        assert kwargs["max_size_bytes"] == 54321


def test_upload_no_file(test_app_client):
    """Test uploading without a file."""
    # Estrai client e API_PREFIX dalla fixture
    client, api_prefix = test_app_client

    response = client.post(f"{api_prefix}/upload")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_upload_empty_filename(test_app_client):
    """Test uploading a file with an empty filename."""
    # Estrai client e API_PREFIX dalla fixture
    client, api_prefix = test_app_client

    with patch("routers.uploader.upload_file") as mock_upload:
        # Make the request with a file that has no name
        response = client.post(
            f"{api_prefix}/upload",
            files={"file": ("", b"test content", "model/stl")},
        )

        # Check response
        # FastAPI valida automaticamente i parametri prima che il nostro endpoint venga chiamato,
        # generando 422 Unprocessable Entity quando un parametro obbligatorio è invalido o mancante.
        # Nel caso di un file con nome vuoto, FastAPI lo considera un parametro invalido.
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        # Verify upload_file was not called since validation failed
        mock_upload.assert_not_called()


def test_upload_error_handling(test_app_client):
    """Test error handling during upload."""
    # Estrai client e API_PREFIX dalla fixture
    client, api_prefix = test_app_client

    with patch("routers.uploader.upload_file") as mock_upload:
        # Set the mock to raise an exception
        mock_upload.side_effect = Exception("Test error")

        # Make the request
        response = client.post(
            f"{api_prefix}/upload",
            files={"file": ("test_file.stl", b"test content", "model/stl")},
        )

        # Check response - deve essere 500 per errori interni generici
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "An error occurred during upload" in response.json()["detail"]


def test_upload_endpoint_oversize_file(monkeypatch, test_app_client):
    """Test uploading a file that exceeds the size limit (custom env var)."""
    # Estrai client e API_PREFIX dalla fixture
    client, api_prefix = test_app_client

    # Set a very small MAX_UPLOAD_SIZE_BYTES in the environment
    monkeypatch.setenv("MAX_UPLOAD_SIZE_BYTES", "10")

    with patch("routers.uploader.upload_file") as mock_upload:
        # Set the mock to raise an HTTPException (come farebbe il validator per file troppo grande)
        mock_upload.side_effect = HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File exceeds the maximum allowed size",
        )

        # Make the request with a file larger than the limit
        test_content = b"This content is more than 10 bytes long"
        response = client.post(
            f"{api_prefix}/upload",
            files={"file": ("test_file.stl", test_content, "model/stl")},
        )

        # Check response - deve propagare 413 dal validator
        assert response.status_code == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
        assert "exceeds the maximum allowed size" in response.json()["detail"]


@pytest.mark.asyncio
async def test_valid_stl_upload():
    """Test uploading a valid STL file."""
    # Create a mock file with STL MIME type
    mock_file = MagicMock()
    mock_file.content_type = "model/stl"
    mock_file.size = 1024
    mock_file.filename = "valid_model.stl"

    # Set up mocks for the required components
    storage_mock = MagicMock()
    storage_mock.save = AsyncMock(return_value="test-file-id")
    storage_mock.get_url = MagicMock(
        return_value="https://storage.example.com/test-file-id"
    )

    # Mock validate_upload_file to return a ValidatedFile
    validated_file = ValidatedFile(
        sanitized_filename="valid_model.stl", size=1024, mime_type="model/stl"
    )

    # Test that upload_file returns a valid UploadResult
    with patch(
        "services.uploader.validator.validate_upload_file", return_value=validated_file
    ):
        with patch("uuid.uuid4", return_value="test-uuid"):
            result = await upload_file(mock_file, storage_backend=storage_mock)

            # Verify the result
            assert isinstance(result, UploadResult)
            assert (
                result.file_id == "test-file-id"
            )  # Should use the value returned by storage.save
            assert result.filename == "valid_model.stl"
            assert result.content_type == "model/stl"
            assert result.size == 1024
            assert result.status == "stored"
            assert result.url == "https://storage.example.com/test-file-id"


@pytest.mark.asyncio
async def test_valid_obj_upload():
    """Test uploading a valid OBJ file."""
    # Create a mock file with OBJ MIME type
    mock_file = MagicMock()
    mock_file.content_type = "model/obj"
    mock_file.size = 2048
    mock_file.filename = "valid_model.obj"

    # Set up mocks for the required components
    storage_mock = MagicMock()
    storage_mock.save = AsyncMock(return_value="test-file-id-obj")
    storage_mock.get_url = MagicMock(
        return_value="https://storage.example.com/test-file-id-obj"
    )

    # Mock validate_upload_file to return a ValidatedFile
    validated_file = ValidatedFile(
        sanitized_filename="valid_model.obj", size=2048, mime_type="model/obj"
    )

    # Test that upload_file returns a valid UploadResult
    with patch(
        "services.uploader.validator.validate_upload_file", return_value=validated_file
    ):
        with patch("uuid.uuid4", return_value="test-uuid-obj"):
            result = await upload_file(mock_file, storage_backend=storage_mock)

            # Verify the result
            assert isinstance(result, UploadResult)
            assert result.file_id == "test-file-id-obj"
            assert result.filename == "valid_model.obj"
            assert result.content_type == "model/obj"
            assert result.size == 2048
            assert result.status == "stored"
            assert result.url == "https://storage.example.com/test-file-id-obj"


@pytest.mark.asyncio
async def test_invalid_mime_type_upload():
    """Test uploading a file with an invalid MIME type."""
    # Create a mock file with an invalid MIME type
    mock_file = MagicMock()
    mock_file.content_type = "application/pdf"
    mock_file.size = 1024
    mock_file.filename = "invalid.pdf"

    # Test that the exception from validate_upload_file is propagated
    with pytest.raises(HTTPException) as exc_info:
        await upload_file(mock_file)

    # Verify the exception details
    assert exc_info.value.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    assert "MIME type" in exc_info.value.detail
    assert "application/pdf" in exc_info.value.detail
    assert "is not allowed" in exc_info.value.detail


@pytest.mark.asyncio
async def test_upload_storage_called():
    """Test that the storage backend's save method is called."""
    # Create a mock file
    mock_file = MagicMock()
    mock_file.content_type = "model/stl"
    mock_file.size = 1024
    mock_file.filename = "test.stl"

    # Create a mock storage backend
    storage_mock = MagicMock()
    storage_mock.save = AsyncMock(return_value="saved-file-id")
    storage_mock.get_url = MagicMock(
        return_value="https://storage.example.com/saved-file-id"
    )

    # Mock validate_upload_file to return a ValidatedFile
    validated_file = ValidatedFile(
        sanitized_filename="test.stl", size=1024, mime_type="model/stl"
    )

    # Test that storage.save is called with the correct parameters
    with patch(
        "services.uploader.validator.validate_upload_file", return_value=validated_file
    ):
        with patch("uuid.uuid4", return_value="test-uuid"):
            await upload_file(mock_file, storage_backend=storage_mock)

            # Verify that storage.save was called with the correct parameters
            storage_mock.save.assert_called_once_with(mock_file, "test-uuid")
            storage_mock.get_url.assert_called_once_with("saved-file-id")


@pytest.mark.asyncio
async def test_file_id_returned_on_success():
    """Test that a file_id and 'stored' status are returned on successful upload."""
    # Create a mock file
    mock_file = MagicMock()
    mock_file.content_type = "model/stl"
    mock_file.size = 1024
    mock_file.filename = "test.stl"

    # Set up mocks for the required components
    storage_mock = MagicMock()
    storage_mock.save = AsyncMock(return_value="custom-file-id")
    storage_mock.get_url = MagicMock(
        return_value="https://storage.example.com/custom-file-id"
    )

    # Mock validate_upload_file to return a ValidatedFile
    validated_file = ValidatedFile(
        sanitized_filename="test.stl", size=1024, mime_type="model/stl"
    )

    # Test that upload_file returns a valid UploadResult with the correct file_id and status
    with patch(
        "services.uploader.validator.validate_upload_file", return_value=validated_file
    ):
        with patch("uuid.uuid4", return_value="test-uuid"):
            result = await upload_file(mock_file, storage_backend=storage_mock)

            # Verify the result
            assert result.file_id == "custom-file-id"
            assert result.status == "stored"
            assert result.url == "https://storage.example.com/custom-file-id"


# Tests for validator.py
def test_validator_valid_stl_mime():
    """Test validator with a valid STL MIME type."""
    # Test that validate_mime returns True for a valid STL MIME type
    assert validate_mime("model/stl", ALLOWED_MIME_TYPES) is True


def test_validator_valid_obj_mime():
    """Test validator with a valid OBJ MIME type."""
    # Test that validate_mime returns True for a valid OBJ MIME type
    assert validate_mime("model/obj", ALLOWED_MIME_TYPES) is True


def test_validator_invalid_mime():
    """Test validator with an invalid MIME type."""
    # Test that validate_mime returns False for an invalid MIME type
    assert validate_mime("application/pdf", ALLOWED_MIME_TYPES) is False


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
    """Test validate_upload_file with a valid file."""
    mock_file = MagicMock()
    mock_file.content_type = "model/stl"
    mock_file.size = 1024  # smaller than default MAX_UPLOAD_SIZE_BYTES
    mock_file.filename = "test.stl"

    # Call the function - ora restituisce un oggetto ValidatedFile
    result = await validate_upload_file(mock_file)

    # Check the result
    assert isinstance(result, ValidatedFile)
    assert result.sanitized_filename == "test.stl"
    assert result.size == 1024
    assert result.mime_type == "model/stl"


@pytest.mark.asyncio
async def test_validate_upload_file_invalid_mime():
    """Test validate_upload_file with an invalid MIME type."""
    mock_file = MagicMock()
    mock_file.content_type = "application/pdf"  # Not in ALLOWED_MIME_TYPES
    mock_file.size = 1024
    mock_file.filename = "test.pdf"

    # Check that it raises HTTPException
    with pytest.raises(HTTPException) as exc_info:
        await validate_upload_file(mock_file)

    # Check the exception
    assert exc_info.value.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE


@pytest.mark.asyncio
async def test_validate_upload_file_invalid_size():
    """Test validate_upload_file with a file that's too large."""
    mock_file = MagicMock()
    mock_file.content_type = "model/stl"
    mock_file.size = MAX_UPLOAD_SIZE_BYTES + 1  # Exceeds the limit
    mock_file.filename = "test.stl"

    # Check that it raises HTTPException
    with pytest.raises(HTTPException) as exc_info:
        await validate_upload_file(mock_file)

    # Check the exception
    assert exc_info.value.status_code == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE


@pytest.mark.asyncio
async def test_validate_upload_file_no_size_attr_valid():
    """Test validate_upload_file with a file object that doesn't have .size."""
    # Simulate a file object that doesn't have a .size attribute initially
    # but whose size can be determined by reading.
    mock_file = MagicMock()
    mock_file.content_type = "model/stl"
    # Remove size attribute
    del mock_file.size
    mock_file.filename = "test.stl"

    # Create a small file content
    file_content = b"small file content"

    # Mock the read method
    async def mock_read():
        return file_content

    mock_file.read = mock_read

    # Call the function
    result = await validate_upload_file(mock_file)

    # Check the result
    assert isinstance(result, ValidatedFile)
    # Check that .size was set
    assert result.size == len(file_content)


@pytest.mark.asyncio
async def test_validate_upload_file_no_size_attr_too_large():
    """Test validate_upload_file with a file that's too large and has no .size."""
    mock_file = MagicMock()
    mock_file.content_type = "model/stl"
    del mock_file.size  # Remove size attribute
    mock_file.filename = "test.stl"

    # Create a file content that's larger than the limit
    async def mock_read():
        return b"a" * (MAX_UPLOAD_SIZE_BYTES + 1)

    mock_file.read = mock_read

    # Check that it raises HTTPException
    with pytest.raises(HTTPException) as exc_info:
        await validate_upload_file(mock_file)

    # Check the exception
    assert exc_info.value.status_code == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
