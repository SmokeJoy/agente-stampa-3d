"""Rate limiting decorator for API endpoints.

This module implements a sliding window rate limiting decorator that can be used
with FastAPI endpoints to enforce rate limits based on IP address or API key.
"""
import functools
import hashlib
import time
from typing import Any, Callable, Dict, Optional, Tuple, Union, cast

from fastapi import Depends, HTTPException, Request, status
from starlette.responses import Response

from services.redis.redis_client import RedisClient, default_redis_client


def rate_limit(
    limit: int = 100,
    window: int = 60,
    key_func: Optional[Callable[[Request], str]] = None,
    redis_client: RedisClient = default_redis_client,
) -> Callable:
    """Rate limit decorator for FastAPI endpoints.

    Implements a sliding window rate limit based on IP address or a custom key.
    
    Args:
        limit: Maximum number of requests allowed in the window
        window: Time window in seconds
        key_func: Function that takes a Request and returns a unique key for rate limiting
                 If not provided, uses the client's IP address
        redis_client: Redis client to use for rate limiting
                     
    Returns:
        Callable: Decorator function for FastAPI endpoints
    """

    def get_default_key(request: Request) -> str:
        """Get default rate limit key based on IP address.
        
        Args:
            request: FastAPI request object
            
        Returns:
            str: Rate limit key
        """
        # Get client IP, considering X-Forwarded-For header if behind proxy
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            # Take the first IP if multiple IPs are in the header
            client_ip = forwarded_for.split(",")[0].strip()
        else:
            client_ip = request.client.host if request.client else "unknown"

        # Get the API key from header, if present
        api_key = request.headers.get("X-API-Key", "")

        # Create a hash combining IP and optional API key
        key_parts = f"{client_ip}:{api_key}"
        key_hash = hashlib.md5(key_parts.encode()).hexdigest()
        
        return f"ratelimit:{key_hash}"

    def decorator(func: Callable) -> Callable:
        """Decorator function for FastAPI endpoints.
        
        Args:
            func: FastAPI endpoint function
            
        Returns:
            Callable: Wrapped function
        """
        @functools.wraps(func)
        async def wrapper(
            request: Request, 
            response: Response, 
            *args: Any, 
            **kwargs: Any
        ) -> Any:
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
            key_generator = key_func if key_func else get_default_key
            key = key_generator(request)
            
            # Increment counter and set expiry if needed
            current_count = redis_client.incr(key)
            
            # Only set expiry on first request (when counter is 1)
            if current_count == 1:
                redis_client.expire(key, window)
            
            # Add rate limit headers to response
            response.headers["X-RateLimit-Limit"] = str(limit)
            response.headers["X-RateLimit-Remaining"] = str(max(0, limit - current_count))
            response.headers["X-RateLimit-Reset"] = str(redis_client.ttl(key))
            
            # Check if rate limit is exceeded
            if current_count > limit:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Rate limit exceeded. Try again in {redis_client.ttl(key)} seconds.",
                )
            
            # Call the original function
            return await func(*args, **kwargs)
        
        return wrapper
    
    return decorator
