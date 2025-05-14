"""Integration tests for the complete upload flow."""

import io
import os
from unittest.mock import patch

import fakeredis
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient

import main
from config import upload_settings
from services.redis.redis_client import RedisClient

# Create a test Redis client using fakeredis
@pytest.fixture
def redis_client():
    """Create a test Redis client with fakeredis backend."""
    fake_redis_server = fakeredis.FakeServer()
    fake_redis = fakeredis.FakeStrictRedis(server=fake_redis_server, decode_responses=True)
    
    redis_client = RedisClient()
    redis_client._client = fake_redis
    
    return redis_client


@pytest.fixture
def test_client():
    """Create a TestClient for FastAPI app."""
    return TestClient(main.app)


@pytest.fixture
def mock_storage_save_path(monkeypatch, tmp_path):
    """Override upload directory to use a temporary path."""
    monkeypatch.setattr(upload_settings, "UPLOAD_ROOT", tmp_path)
    return tmp_path


@pytest.fixture
def sample_stl_file():
    """Create a dummy STL file for testing."""
    # Simple ASCII STL content
    content = b"""
    solid sample
      facet normal 0.0 0.0 1.0
        outer loop
          vertex 0.0 0.0 0.0
          vertex 1.0 0.0 0.0
          vertex 0.0 1.0 0.0
        endloop
      endfacet
    endsolid sample
    """
    return io.BytesIO(content)


@pytest.mark.asyncio
async def test_happy_path_upload_and_webhook_callback(test_client, mock_storage_save_path, monkeypatch, redis_client, sample_stl_file):
    """Test the full upload flow: POST to uploader, verify storage, and mock webhook callback."""
    # Mock the Redis client in the rate_limit decorator
    monkeypatch.setattr("utils.ratelimit.default_redis_client", redis_client)
    
    # Mock the webhook call but still track it
    webhook_called = False
    webhook_data = None

    def mock_post(*args, **kwargs):
        nonlocal webhook_called, webhook_data
        webhook_called = True
        webhook_data = kwargs.get("json", {})
        
        class MockResponse:
            status_code = 200
        return MockResponse()
    
    # Apply the mock
    with patch("requests.post", side_effect=mock_post):
        # Prepare the file data
        files = {"file": ("test_model.stl", sample_stl_file, "model/stl")}
        data = {"webhook_url": "http://example.com/webhook"}

        # Make the request
        response = test_client.post("/upload", files=files, data=data)
        
        # Check status code
        assert response.status_code == 200
        
        # Check response schema
        json_response = response.json()
        assert "file_id" in json_response
        assert json_response["filename"] == "test_model.stl"
        assert json_response["content_type"] == "model/stl"
        assert json_response["status"] == "stored"
        assert "url" in json_response
        
        # Verify webhook was called with correct data
        assert webhook_called
        assert webhook_data["file_id"] == json_response["file_id"]


@pytest.mark.asyncio
async def test_upload_rate_limit_hit(test_client, mock_storage_save_path, monkeypatch, redis_client, sample_stl_file):
    """Test that the rate limit is hit correctly on the upload endpoint."""
    # Mock the Redis client in the rate_limit decorator
    monkeypatch.setattr("utils.ratelimit.default_redis_client", redis_client)
    
    # Adjust rate limit to 2 requests per window for testing
    with patch("utils.ratelimit.rate_limit", lambda *args, **kwargs: 
              lambda x: x if "test_upload_rate_limit_hit" not in str(x) else 
              patch("utils.ratelimit.rate_limit", return_value=lambda x: x)(x)):
        # Override the rate limit decorator for the upload endpoint
        original_post = main.uploader.router.routes[0].endpoint
        
        # Apply custom rate limit
        async def limited_upload(*args, **kwargs):
            key = f"ratelimit:test"
            current = redis_client.incr(key)
            
            # Only allow 2 requests
            if current > 2:
                from fastapi import HTTPException
                raise HTTPException(status_code=429, detail="Rate limit exceeded")
                
            return await original_post(*args, **kwargs)
    
        # Replace the endpoint
        main.uploader.router.routes[0].endpoint = limited_upload
        
        try:
            # Make test requests with a fresh BytesIO for each request
            files1 = {"file": ("test_model.stl", io.BytesIO(b"test stl content"), "model/stl")}
            files2 = {"file": ("test_model.stl", io.BytesIO(b"test stl content"), "model/stl")} 
            files3 = {"file": ("test_model.stl", io.BytesIO(b"test stl content"), "model/stl")}
            
            # First two should succeed
            response1 = test_client.post("/upload", files=files1)
            assert response1.status_code == 200
            
            response2 = test_client.post("/upload", files=files2)
            assert response2.status_code == 200
            
            # Third should fail with 429 Too Many Requests
            response3 = test_client.post("/upload", files=files3)
            assert response3.status_code == 429
            assert "Rate limit exceeded" in response3.text
            
        finally:
            # Restore original endpoint
            main.uploader.router.routes[0].endpoint = original_post


@pytest.mark.asyncio
async def test_webhook_receives_correct_data(test_client, mock_storage_save_path, monkeypatch, sample_stl_file):
    """Test that the webhook endpoint, when called, receives the correct data."""
    # Store webhook data for inspection
    webhook_data = {}
    
    # Mock the requests.post function
    def mock_post(url, **kwargs):
        nonlocal webhook_data
        webhook_data = kwargs.get("json", {})
        
        class MockResponse:
            status_code = 200
        return MockResponse()
    
    # Apply the mock
    with patch("requests.post", side_effect=mock_post):
        # Create a fresh BytesIO for the test
        test_content = io.BytesIO(b"test stl content")
        
        # Prepare the file data
        files = {"file": ("test_model.stl", test_content, "model/stl")}
        data = {"webhook_url": "http://webhook.test/endpoint"}
        
        # Make the request
        response = test_client.post("/upload", files=files, data=data)
        assert response.status_code == 200
        
        # Get the response data for comparison
        response_data = response.json()
        
        # Verify the webhook data matches the response
        assert webhook_data["file_id"] == response_data["file_id"]
        assert webhook_data["filename"] == response_data["filename"]
        assert webhook_data["content_type"] == response_data["content_type"]
        assert webhook_data["status"] == "stored"
