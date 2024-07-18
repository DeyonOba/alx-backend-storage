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
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator counts the number of time a method is called.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper count the number of time a method is called
        """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """
    Class that write string to Redis.
    """
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self.flushdb = redis.Redis().flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores data in Redis db.

        Args:
            data (Union[str, bytes, int, float]): Accepted data.

        Returns:
            str: The key value of the data in a uuid4 format.
        """
        rand_key = str(uuid.uuid4())
        self._redis.set(rand_key, data)
        return rand_key

    def get(
        self, key: str, fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float, None]:
        """
        Gets the value of data stored using the key and
        converts it to the proper type.

        Args:
            key (str): _description_
            fn (Optional[Callable], optional: Takes a callable function
        Returns:
            Union[str, bytes, int, float, None]: Accepted return types
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Assigns the proper function for retrieving a string.

        Args:
            key (str): Key value

        Returns:
            Optional[str]: String value
        """
        return self.get(key, fn=lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Assigns the proper function for retrieving an integer.

        Args:
            key (str): Key value

        Returns:
            Optional[int]: Integer value
        """
        return self.get(key, fn=int)
