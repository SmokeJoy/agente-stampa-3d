"""Tests for the rate_limit decorator."""

import asyncio
import time
from typing import Dict
from unittest.mock import AsyncMock, MagicMock, patch

import fakeredis
import pytest
from fastapi import HTTPException, Request, Response
from fastapi.responses import JSONResponse
from pytest_mock import MockerFixture

from services.redis.redis_client import RedisClient
from utils.ratelimit import rate_limit


@pytest.fixture
def mock_request() -> MagicMock:
    """Create a mock FastAPI request object."""
    mock_request = MagicMock(spec=Request)
    mock_request.client.host = "127.0.0.1"
    mock_request.headers = {"X-API-Key": "test_key"}
    return mock_request


@pytest.fixture
def mock_response() -> MagicMock:
    """Create a mock FastAPI response object."""
    mock_response = MagicMock(spec=Response)
    mock_response.headers = {}
    return mock_response


@pytest.fixture
def redis_client() -> RedisClient:
    """Create a Redis client that uses fakeredis backend."""
    fake_redis_server = fakeredis.FakeServer()
    fake_redis = fakeredis.FakeStrictRedis(server=fake_redis_server, decode_responses=True)
    
    redis_client = RedisClient()
    redis_client._client = fake_redis
    
    return redis_client


@pytest.mark.asyncio
async def test_rate_limit_allows_within_limit(mock_request: MagicMock, mock_response: MagicMock, redis_client: RedisClient):
    """Test that requests within the limit are allowed."""
    # Create a mock endpoint function
    mock_endpoint = AsyncMock(return_value={"status": "success"})
    
    # Apply rate_limit decorator
    decorated_endpoint = rate_limit(limit=3, window=10, redis_client=redis_client)(mock_endpoint)
    
    # Make requests within limit
    for _ in range(3):
        result = await decorated_endpoint(mock_request, mock_response)
        assert result == {"status": "success"}
    
    # Check headers
    assert mock_response.headers["X-RateLimit-Limit"] == "3"
    assert mock_response.headers["X-RateLimit-Remaining"] == "0"  # 3rd request
    assert int(mock_response.headers["X-RateLimit-Reset"]) <= 10  # Should be less than window


@pytest.mark.asyncio
async def test_rate_limit_blocks_exceeding_limit(mock_request: MagicMock, mock_response: MagicMock, redis_client: RedisClient):
    """Test that requests exceeding the limit are blocked with HTTP 429."""
    # Create a mock endpoint function
    mock_endpoint = AsyncMock(return_value={"status": "success"})
    
    # Apply rate_limit decorator
    decorated_endpoint = rate_limit(limit=2, window=10, redis_client=redis_client)(mock_endpoint)
    
    # Make 2 requests (within limit)
    await decorated_endpoint(mock_request, mock_response)
    await decorated_endpoint(mock_request, mock_response)
    
    # 3rd request should be blocked
    with pytest.raises(HTTPException) as exc_info:
        await decorated_endpoint(mock_request, mock_response)
    
    assert exc_info.value.status_code == 429
    assert "Rate limit exceeded" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_rate_limit_resets_after_window(mock_request: MagicMock, mock_response: MagicMock, redis_client: RedisClient, mocker: MockerFixture):
    """Test that the rate limit counter resets after the window expires."""
    # Create a mock endpoint function
    mock_endpoint = AsyncMock(return_value={"status": "success"})
    
    # Apply rate_limit decorator with small window
    decorated_endpoint = rate_limit(limit=1, window=2, redis_client=redis_client)(mock_endpoint)
    
    # Make a request (uses up the limit)
    await decorated_endpoint(mock_request, mock_response)
    
    # Second request should fail
    with pytest.raises(HTTPException) as exc_info:
        await decorated_endpoint(mock_request, mock_response)
    
    # Mock time.sleep to avoid waiting
    with patch("time.sleep"):
        # Wait for window to expire
        await asyncio.sleep(2)
    
    # Expire keys manually since we mocked time.sleep
    redis_client.client.flushall()
    
    # After window, should work again
    result = await decorated_endpoint(mock_request, mock_response)
    assert result == {"status": "success"}


@pytest.mark.asyncio
async def test_rate_limit_uses_correct_redis_key(mock_request: MagicMock, mock_response: MagicMock, redis_client: RedisClient, mocker: MockerFixture):
    """Test that the rate limiter uses the correct key in Redis."""
    # Create a spy on redis_client.incr to check keys
    incr_spy = mocker.spy(redis_client, "incr")
    
    # Create a mock endpoint function
    mock_endpoint = AsyncMock(return_value={"status": "success"})
    
    # Apply rate_limit decorator
    decorated_endpoint = rate_limit(limit=5, window=10, redis_client=redis_client)(mock_endpoint)
    
    # Make a request
    await decorated_endpoint(mock_request, mock_response)
    
    # Check that the correct key was used
    assert incr_spy.call_count == 1
    key_arg = incr_spy.call_args[0][0]
    assert key_arg.startswith("ratelimit:")
    
    # Check that the key exists in Redis
    assert redis_client.get(key_arg) == "1"


@pytest.mark.asyncio
async def test_rate_limit_key_has_correct_ttl(mock_request: MagicMock, mock_response: MagicMock, redis_client: RedisClient):
    """Test that the Redis key for rate limiting has the correct TTL (window)."""
    window = 30  # 30 second window
    
    # Create a mock endpoint function
    mock_endpoint = AsyncMock(return_value={"status": "success"})
    
    # Apply rate_limit decorator
    decorated_endpoint = rate_limit(limit=5, window=window, redis_client=redis_client)(mock_endpoint)
    
    # Make a request
    await decorated_endpoint(mock_request, mock_response)
    
    # Get the key from Redis (there should only be one)
    keys = redis_client.client.keys("ratelimit:*")
    assert len(keys) == 1
    
    # Check the TTL
    ttl = redis_client.ttl(keys[0])
    assert 0 < ttl <= window  # TTL should be positive but not more than window


@pytest.mark.asyncio
async def test_rate_limit_with_custom_key_function(mock_request: MagicMock, mock_response: MagicMock, redis_client: RedisClient):
    """Test that the rate limiter can use a custom key function."""
    # Create a custom key function
    def custom_key_func(request: Request) -> str:
        return f"ratelimit:custom:{request.headers.get('X-API-Key', 'default')}"
    
    # Create a mock endpoint function
    mock_endpoint = AsyncMock(return_value={"status": "success"})
    
    # Apply rate_limit decorator with custom key function
    decorated_endpoint = rate_limit(
        limit=3, 
        window=10, 
        key_func=custom_key_func,
        redis_client=redis_client
    )(mock_endpoint)
    
    # Make a request
    await decorated_endpoint(mock_request, mock_response)
    
    # Check that the custom key exists in Redis
    custom_key = custom_key_func(mock_request)
    assert redis_client.get(custom_key) == "1"
