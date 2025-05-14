"""Redis client wrapper for the application.

This module provides a simple Redis client wrapper with connection management
and common Redis operations used across the application.
"""
import os
from typing import Any, Optional, Union

import redis
from redis import Redis


class RedisClient:
    """Redis client wrapper with connection management and common operations."""

    def __init__(
        self,
        host: str = os.environ.get("REDIS_HOST", "localhost"),
        port: int = int(os.environ.get("REDIS_PORT", 6379)),
        db: int = int(os.environ.get("REDIS_DB", 0)),
        password: Optional[str] = os.environ.get("REDIS_PASSWORD"),
        ssl: bool = os.environ.get("REDIS_SSL", "false").lower() == "true",
    ):
        """Initialize Redis client with connection parameters.

        Args:
            host: Redis server hostname
            port: Redis server port
            db: Redis database number
            password: Optional Redis password
            ssl: Whether to use SSL for connection
        """
        self.connection_params = {
            "host": host,
            "port": port,
            "db": db,
            "decode_responses": True,  # Always decode to str
        }
        
        if password:
            self.connection_params["password"] = password
        
        if ssl:
            self.connection_params["ssl"] = True
            self.connection_params["ssl_cert_reqs"] = None
        
        self._client: Optional[Redis] = None

    @property
    def client(self) -> Redis:
        """Get Redis client instance, creating it if needed.
        
        Returns:
            Redis: Configured Redis client
        """
        if self._client is None:
            self._client = redis.Redis(**self.connection_params)
        return self._client

    def incr(self, key: str, amount: int = 1) -> int:
        """Increment a key by the given amount.
        
        Args:
            key: The key to increment
            amount: The amount to increment by
            
        Returns:
            int: The new value
        """
        return self.client.incr(key, amount)

    def expire(self, key: str, seconds: int) -> bool:
        """Set an expiration time on a key.
        
        Args:
            key: The key to expire
            seconds: The expiration time in seconds
            
        Returns:
            bool: True if successful, False otherwise
        """
        return bool(self.client.expire(key, seconds))

    def ttl(self, key: str) -> int:
        """Get the TTL of a key.
        
        Args:
            key: The key to check
            
        Returns:
            int: TTL in seconds, -1 if no expiry, -2 if key doesn't exist
        """
        return self.client.ttl(key)

    def get(self, key: str) -> Optional[str]:
        """Get a string value from Redis.
        
        Args:
            key: The key to get
            
        Returns:
            str: The value or None if not found
        """
        return self.client.get(key)

    def set(
        self, 
        key: str, 
        value: Union[str, bytes, int, float], 
        ex: Optional[int] = None
    ) -> bool:
        """Set a string value in Redis with optional expiration.
        
        Args:
            key: The key to set
            value: The value to set
            ex: Optional expiration time in seconds
            
        Returns:
            bool: True if successful, False otherwise
        """
        return bool(self.client.set(key, value, ex=ex))

    def delete(self, key: str) -> bool:
        """Delete a key from Redis.
        
        Args:
            key: The key to delete
            
        Returns:
            bool: True if key was deleted, False otherwise
        """
        return bool(self.client.delete(key))


# Default client instance
default_redis_client = RedisClient()
