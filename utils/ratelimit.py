"""Rate limiting decorator for API endpoints.

This module implements a sliding window rate limiting decorator that can be used
with FastAPI endpoints to enforce rate limits based on IP address or API key.  # noqa: E501
"""

import functools
import hashlib
import time
from typing import Any, Callable, Optional

from fastapi import HTTPException, Request, status
from starlette.responses import Response

from services.redis.redis_client import RedisClient, default_redis_client

# Variabile di abilitazione per i test - se False, il rate limiter non blocca mai
# ma continua a impostare gli header
_RATE_LIMIT_ENABLED = True


def get_default_key(request: Request, key_prefix: str = "ratelimit") -> str:
    """Get default rate limit key based on IP address.

    Args:
        request: FastAPI request object
        key_prefix: Prefix for Redis keys to prevent collisions

    Returns:
        str: Rate limit key
    """
    # Get client IP, considering possible proxy headers
    client_ip = request.headers.get("X-Forwarded-For", "").split(",")[0].strip() or request.client.host

    # Create a unique key based on IP address
    key_hash = hashlib.md5(client_ip.encode()).hexdigest()
    return f"{key_prefix}:{key_hash}"


def create_key_func(key_prefix: str) -> Callable[[Request], str]:
    """Create a key function based on prefix.

    Args:
        key_prefix: Prefix for Redis keys to prevent collisions

    Returns:
        Callable: Key function that takes a request and returns a key
    """

    def key_func(request: Request) -> str:
        """Get rate limit key based on IP address and prefix.

        Args:
            request: FastAPI request object

        Returns:
            str: Rate limit key
        """
        return get_default_key(request, key_prefix)

    return key_func


def rate_limit(
    key_prefix: str = "ratelimit",
    max_calls: int = 100,
    window_seconds: int = 60,
    key_func: Optional[Callable[[Request], str]] = None,
    redis_client: RedisClient = default_redis_client,
) -> Callable:
    """Rate limit decorator for FastAPI endpoints.

    Args:
        key_prefix: Prefix for Redis keys to prevent collisions
        max_calls: Maximum number of calls allowed in the time window
        window_seconds: Time window in seconds
        key_func: Optional function to generate the rate limit key
        redis_client: Redis client to use for rate limiting

    Returns:
        Callable: Decorator function
    """

    def decorator(func: Callable) -> Callable:
        """Decorator function for rate limiting.

        Args:
            func: Function to decorate

        Returns:
            Callable: Wrapped function with rate limiting
        """

        @functools.wraps(func)
        async def wrapper(request: Request, response: Response, *args: Any, **kwargs: Any) -> Any:
            """Wrapper function that enforces rate limiting.

            Args:
                request: FastAPI request object
                response: FastAPI response object

            Returns:
                Any: Result of the wrapped function

            Raises:
                HTTPException: If rate limit is exceeded
            """
            # Get rate limit key
            if key_func:
                key_generator = key_func
            else:
                key_generator = create_key_func(key_prefix)

            key = key_generator(request)

            # If this is a custom key function, add window suffix if not present
            if not key.endswith(":window"):
                sorted_set_key = f"{key}:window"
            else:
                sorted_set_key = key

            try:
                # Current timestamp for sliding window
                try:
                    current_time = int(redis_client.client.time()[0])
                except Exception:
                    # Fallback to local time if Redis TIME command fails
                    current_time = int(time.time())

                # Remove expired entries from the sliding window
                redis_client.client.zremrangebyscore(sorted_set_key, 0, current_time - window_seconds)

                # Get current count before adding this request
                current_count = redis_client.client.zcard(sorted_set_key)

                # Check if rate limit is exceeded
                if _RATE_LIMIT_ENABLED and current_count >= max_calls:
                    # Set headers before raising exception
                    response.headers["X-RateLimit-Limit"] = str(max_calls)
                    response.headers["X-RateLimit-Remaining"] = "0"

                    # Determine the TTL for the rate limit window
                    if redis_client.client.exists(sorted_set_key):
                        ttl = redis_client.client.ttl(sorted_set_key)
                    else:
                        ttl = window_seconds

                    response.headers["X-RateLimit-Reset"] = str(ttl)

                    raise HTTPException(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail="rate limit exceeded",
                    )

                # Add current request to the sliding window
                member_id = f"{current_time}-{func.__name__}"
                member_value = f"{member_id}-{hash(str(args) + str(kwargs))}"  # noqa: E501
                redis_client.client.zadd(sorted_set_key, {member_value: current_time})

                # Set expiry on the sorted set
                redis_client.client.expire(sorted_set_key, window_seconds * 2)

                # Calculate the remaining requests (current_count was before adding the request)
                remaining = max(0, max_calls - (current_count + 1))

                # Add rate limit headers to response
                response.headers["X-RateLimit-Limit"] = str(max_calls)
                response.headers["X-RateLimit-Remaining"] = str(remaining)
                response.headers["X-RateLimit-Reset"] = str(redis_client.client.ttl(sorted_set_key))
            except Exception as e:
                # Log l'errore
                print(f"Rate limit error: {str(e)}. Proceeding without rate limiting.")
                # Imposta comunque gli header di default
                response.headers.update(
                    {
                        "X-RateLimit-Limit": str(max_calls),
                        "X-RateLimit-Remaining": str(max_calls - 1),
                        "X-RateLimit-Reset": str(window_seconds),
                    }
                )

            # Call the original function
            return await func(request, response, *args, **kwargs)

        return wrapper

    return decorator


# Funzioni di aiuto per i test
def disable_rate_limiting():
    """Disabilita il rate limiting globalmente (per i test)."""
    global _RATE_LIMIT_ENABLED
    _RATE_LIMIT_ENABLED = False


def enable_rate_limiting():
    """Abilita il rate limiting globalmente (per i test)."""
    global _RATE_LIMIT_ENABLED
    _RATE_LIMIT_ENABLED = True
