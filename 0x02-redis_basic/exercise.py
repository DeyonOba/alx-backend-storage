#!/usr/bin/env python3
"""
Module creates a `Cache` class. In the `__init__` method, store an instance
of the Redis client as a private variable named `_redis`
(using `redis.Redis()`) and flush the instance using flushdb.

Create a store method that takes a data agrument and returns a string.
The method should generate a random key (e.g. using `uuid`), store the
input data in Redis using the random key and return the key.
"""
import uuid
import redis
from typing import Union, Optional, Callable


class Cache:
    """
    Class that write string to Redis.
    """
    def __init__(self):
        self._redis = redis.Redis()
        self.flushdb = redis.Redis().flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        rand_key = str(uuid.uuid4())
        self._redis.set(rand_key, data)
        return rand_key

    def get(
        self, key: str, fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float, None]:
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        return self.get(key, fn=lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        return self.get(key, fn=int)
