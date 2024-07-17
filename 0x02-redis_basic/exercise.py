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
from typing import Union


class Cache:
    """
    Class that write string to Redis.
    """
    def __init__(self):
        self._redis = redis.Redis()
        self.flushdb = redis.Redis().flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        rand_key = str(uuid.uuid4())
        self._redis.set(rand_key.encode('utf-8'), data)
        self.flushdb
        return rand_key
