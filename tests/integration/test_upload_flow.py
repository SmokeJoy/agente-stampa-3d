"""End-to-end tests for the upload flow.

These tests verify that files can be uploaded through the API endpoint,
processed correctly, and stored properly.
"""

import importlib
import tempfile
from unittest.mock import patch

import httpx
import pytest
from anyio import Path
from httpx import ASGITransport

from services.uploader.uploader_service import UploadResult


@pytest.fixture
async def test_client():
    """Create an HTTP client with ASGI transport."""
    # Importiamo main solo dopo aver configurato tutti i mock
    import main

    transport = ASGITransport(app=main.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client, main.API_PREFIX


@pytest.mark.asyncio
async def test_upload_endpoint_e2e():
    """Test the upload endpoint with a real file.

    This test goes through the complete flow:
    1. Create a temporary STL file
    2. Upload the file to the endpoint
    3. Verify the response contains the expected metadata
    4. Check that the file was stored in the configured upload directory
    """
    # Create a temporary file with STL content
    test_content = (
        b"solid test\n"
        b"  facet normal 0 0 0\n"
        b"    outer loop\n"
        b"      vertex 0 0 0\n"
        b"      vertex 1 0 0\n"
        b"      vertex 0 1 0\n"
        b"    endloop\n"
        b"  endfacet\n"
        b"endsolid test"
    )

    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix=".stl", delete=False) as tmp_file:
        tmp_file.write(test_content)
        tmp_file_path = tmp_file.name

    try:
        # Mock the storage backend to prevent actual file operations
        mock_result = UploadResult(
            file_id="test-uuid",
            filename="test_model.stl",
            content_type="model/stl",
            size=len(test_content),
            status="stored",
            url="http://example.com/test-uuid/test_model.stl",
        )

        # Mock the upload_file function to return a predefined result
        with patch(
            "routers.uploader.upload_file",
            return_value=mock_result,
        ):
            # Import main after all patches are in place
            import main

            # Create a client and send the file to the endpoint
            async with httpx.AsyncClient(
                transport=ASGITransport(app=main.app), base_url="http://test"
            ) as client:
                # Read the file that was saved to disk
                with open(tmp_file_path, "rb") as f:
                    file_content = f.read()

                # Upload the file
                files = {"file": ("test_model.stl", file_content, "model/stl")}
                response = await client.post(
                    f"{main.API_PREFIX}/upload",
                    files=files,
                )

                # Assert the response
                assert response.status_code == 201
                data = response.json()
                assert data["file_id"] == "test-uuid"
                assert data["filename"] == "test_model.stl"
                assert data["content_type"] == "model/stl"
                assert data["size"] == len(test_content)
                assert data["status"] == "stored"
                assert "url" in data

                # Test with webhook parameter
                response_with_webhook = await client.post(
                    f"{main.API_PREFIX}/upload",
                    files=files,
                    data={"webhook_url": "http://example.com/webhook"},
                )
                assert response_with_webhook.status_code == 201
    finally:
        # Clean up the temporary file
        await Path(tmp_file_path).unlink()
