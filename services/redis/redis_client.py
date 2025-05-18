"""Redis client wrapper for the application.

This module provides a simple Redis client wrapper with connection management
and common Redis operations used across the application.
"""

from typing import Optional, Union

import redis


class RedisClient:
    """Redis client wrapper."""

    def __init__(self, host="localhost", port=6379, db=0, decode_responses=True):
        """Initialize the Redis client.

        Args:
            host: Redis host
            port: Redis port
            db: Redis database
            decode_responses: Whether to decode responses
        """
        self._client = None
        self._host = host
        self._port = port
        self._db = db
        self._decode_responses = decode_responses

    @property
    def client(self) -> redis.Redis:
        """Get the Redis client, initializing it if necessary.

        Returns:
            redis.Redis: Redis client
        """
        if self._client is None:
            self._client = redis.Redis(
                host=self._host,
                port=self._port,
                db=self._db,
                decode_responses=self._decode_responses,
            )
        return self._client

    def incr(self, key: str, amount: int = 1) -> int:
        """Increment a key's value.

        Args:
            key: Key to increment
            amount: Amount to increment by

        Returns:
            int: New value
        """
        return self.client.incr(key, amount)

    def expire(self, key: str, seconds: int) -> bool:
        """Set key expiration.

        Args:
            key: Key to set expiration for
            seconds: Expiration time in seconds

        Returns:
            bool: Whether expiration was set
        """
        return self.client.expire(key, seconds)

    def ttl(self, key: str) -> int:
        """Get key time-to-live.

        Args:
            key: Key to get TTL for

        Returns:
            int: TTL in seconds
        """
        return self.client.ttl(key)

    def exists(self, key: str) -> bool:
        """Check if key exists.

        Args:
            key: Key to check

        Returns:
            bool: Whether key exists
        """
        return bool(self.client.exists(key))

    def get(self, key: str) -> Optional[str]:
        """Get a string value from Redis.

        Args:
            key: The key to get

        Returns:
            str: The value or None if not found
        """
        return self.client.get(key)

    def set(self, key: str, value: Union[str, bytes, int, float], ex: Optional[int] = None) -> bool:
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


# Default Redis client instance
default_redis_client = RedisClient()
