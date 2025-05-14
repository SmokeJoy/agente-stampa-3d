"""Storage abstraction for uploader service.

Provides a consistent interface for file storage operations.
The `StorageBackend` class defines the interface that all storage backends must implement.
This module also includes an in-memory implementation for testing.
"""

import abc
import uuid
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import UploadFile


class StorageBackend(abc.ABC):
    """Abstract base class for storage backends."""

    @abc.abstractmethod
    async def save(self, file: UploadFile, file_id: Optional[str] = None) -> str:
        """Save a file to the storage backend.

        Args:
            file: The file to save
            file_id: Optional file ID to use, otherwise generated

        Returns:
            str: The file ID used for the saved file
        """
        pass

    @abc.abstractmethod
    def get_url(self, file_id: str) -> str:
        """Get the URL for a stored file.

        Args:
            file_id: The ID of the stored file

        Returns:
            str: The URL to access the file
        """
        pass


class InMemoryStorage(StorageBackend):
    """In-memory storage backend for testing.

    Simulates an S3-like object storage without external dependencies.
    """

    def __init__(self, base_url: str = "https://storage.example.com"):
        """Initialize the in-memory storage.

        Args:
            base_url: The base URL to use for generated file URLs
        """
        self.base_url = base_url
        self.storage: Dict[str, Any] = {}

    async def save(self, file: UploadFile, file_id: Optional[str] = None) -> str:
        """Save a file to in-memory storage.

        Args:
            file: The file to save
            file_id: Optional file ID to use, otherwise generated

        Returns:
            str: The file ID used for the saved file
        """
        if file_id is None:
            file_id = str(uuid.uuid4())

        # Read the file content
        content = await file.read()

        # Store the file data in memory
        self.storage[file_id] = {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(content),
            "content": content,
        }

        # Reset file pointer for potential reuse
        if hasattr(file, "seek"):
            await file.seek(0)

        return file_id

    def get_url(self, file_id: str) -> str:
        """Get the URL for a stored file.

        Args:
            file_id: The ID of the stored file

        Returns:
            str: The URL to access the file

        Raises:
            KeyError: If the file ID doesn't exist
        """
        if file_id not in self.storage:
            raise KeyError(f"File not found: {file_id}")

        return f"{self.base_url}/{file_id}"


# For convenience, export a default instance for testing
default_storage = InMemoryStorage()
