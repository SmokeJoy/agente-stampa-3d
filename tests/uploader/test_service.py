# flake8: noqa
"""Unit tests for uploader service."""
import io
import json
import uuid
from typing import Dict, List, Tuple
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import requests
from fastapi import HTTPException, UploadFile
from pytest_mock import MockerFixture

from config import upload_settings
from services.uploader.storage import InMemoryStorage, StorageBackend
from services.uploader.uploader_service import UploadResult, notify_webhook, upload_file


class MockResponse:
    """Mock per requests.Response."""
    def __init__(self, status_code: int = 200, json_data: Dict = None):
        self.status_code = status_code
        self.json_data = json_data or {}
        
    def json(self):
        return self.json_data


@pytest.fixture
def mock_file() -> UploadFile:
    """Create a mock file for testing."""
    content = b"mock file content"
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "test_file.stl"
    mock_file.content_type = "model/stl"
    
    async def mock_read():
        return content
    
    async def mock_seek(position):
        pass
    
    mock_file.read = AsyncMock(side_effect=mock_read)
    mock_file.seek = AsyncMock(side_effect=mock_seek)
    mock_file.size = len(content)
    
    return mock_file


@pytest.fixture
def storage() -> InMemoryStorage:
    """Create an in-memory storage instance for testing."""
    return InMemoryStorage(base_url="https://test-storage.example.com")


@pytest.mark.asyncio
async def test_upload_file_happy_path(mock_file: UploadFile, storage: InMemoryStorage):
    """Test successful file upload."""
    # Arrange
    file_id = str(uuid.uuid4())
    with patch('uuid.uuid4', return_value=uuid.UUID(file_id)):
        # Act
        result = await upload_file(mock_file, storage_backend=storage)
        
        # Assert
        assert result.file_id == file_id
        assert result.filename == mock_file.filename
        assert result.content_type == mock_file.content_type
        assert result.size == mock_file.size
        assert result.status == "stored"
        assert result.url == f"https://test-storage.example.com/{file_id}"
        
        # Verify storage was called correctly
        assert file_id in storage.storage
        assert storage.storage[file_id]["filename"] == mock_file.filename
        assert storage.storage[file_id]["content_type"] == mock_file.content_type


@pytest.mark.asyncio
async def test_upload_file_with_webhook(mock_file: UploadFile, storage: InMemoryStorage, mocker: MockerFixture):
    """Test file upload with webhook notification."""
    # Arrange
    webhook_url = "https://webhook.example.com/endpoint"
    mock_notify = mocker.patch(
        "services.uploader.uploader_service.notify_webhook", 
        return_value=True
    )
    
    # Act
    result = await upload_file(
        mock_file, 
        storage_backend=storage, 
        webhook_url=webhook_url
    )
    
    # Assert
    assert result.status == "stored"
    mock_notify.assert_called_once()
    call_args = mock_notify.call_args[0]
    assert call_args[0] == webhook_url
    assert isinstance(call_args[1], dict)
    assert call_args[1]["file_id"] == result.file_id


@pytest.mark.asyncio
async def test_upload_file_validation_failure(mock_file: UploadFile, storage: InMemoryStorage, mocker: MockerFixture):
    """Test upload with validation failure."""
    # Arrange
    mocker.patch(
        "services.uploader.uploader_service.validate_upload_file",
        return_value=(False, "Invalid file", None, None, None)
    )
    
    # Act & Assert
    with pytest.raises(HTTPException) as excinfo:
        await upload_file(mock_file, storage_backend=storage)
    
    assert excinfo.value.status_code == 422
    assert excinfo.value.detail == "Invalid file"


@pytest.mark.asyncio
async def test_upload_file_storage_error(mock_file: UploadFile, mocker: MockerFixture):
    """Test upload with storage error."""
    # Arrange
    mock_storage = MagicMock(spec=StorageBackend)
    mock_storage.save = AsyncMock(side_effect=Exception("Storage error"))
    
    # Act & Assert
    with pytest.raises(HTTPException) as excinfo:
        await upload_file(mock_file, storage_backend=mock_storage)
    
    assert excinfo.value.status_code == 500
    assert excinfo.value.detail == "Error storing file"


def test_notify_webhook_success(mocker: MockerFixture):
    """Test successful webhook notification."""
    # Arrange
    webhook_url = "https://webhook.example.com/endpoint"
    data = {"file_id": "test-id", "status": "stored"}
    
    # Creo il mock di requests.post prima di usarlo
    requests_post_mock = mocker.patch("requests.post")
    mock_response = MockResponse(status_code=200)
    requests_post_mock.return_value = mock_response
    
    # Act
    result = notify_webhook(webhook_url, data)
    
    # Assert
    assert result is True
    # Verifico che requests.post sia chiamato con i parametri corretti
    requests_post_mock.assert_called_once_with(
        webhook_url,
        json=data,
        timeout=5.0,
        headers={"Content-Type": "application/json"}
    )


def test_notify_webhook_failure(mocker: MockerFixture):
    """Test webhook notification failure."""
    # Arrange
    webhook_url = "https://webhook.example.com/endpoint"
    data = {"file_id": "test-id", "status": "stored"}
    
    # Mock per una risposta con codice 500
    mock_response = MockResponse(status_code=500)
    mocker.patch("requests.post", return_value=mock_response)
    
    # Act
    result = notify_webhook(webhook_url, data)
    
    # Assert
    assert result is False


def test_notify_webhook_exception(mocker: MockerFixture):
    """Test webhook notification with exception."""
    # Arrange
    webhook_url = "https://webhook.example.com/endpoint"
    data = {"file_id": "test-id", "status": "stored"}
    
    # Simulo un'eccezione durante la chiamata a requests.post
    mocker.patch("requests.post", side_effect=Exception("Connection error"))
    
    # Act
    result = notify_webhook(webhook_url, data)
    
    # Assert
    assert result is False 