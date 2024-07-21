#!/usr/bin/env python3
"""
Module implements a `get_page` function
(prototype: def get_page(url: str) -> str:)
The core of the function is very simple. It uses the `requests`
module to obtain the HTML content of a particular URL and returns it.

Inside `get_page` track how many times a particular URL was accessed
in the key "count:{url}" and cache the result with an expiration time
of 10 seconds.
"""
import redis
import requests
from typing import Callable, Union
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator function that takes in a method and
    return the wrapper function.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Update number of time a URL has been accessed."""
        self._client.incr("count:{}".format(args[0]))
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """
    Cache the content of a URL and keep track of it.
    """

    def __init__(self) -> None:
        self._client: redis.Redis = redis.Redis()

    @count_calls
    def save(self, url: str) -> str:
        """Saves content from a URL link.

        Args:
            url (str): Link to be accessed and saved

        Returns:
            str: URL
        """
        content = self.get_content(url)

        if content:
            self._client.setex(url, 10, content)
        return url

    def get_content(self, url: str) -> Union[bytes, None]:
        """Gets the content of URL link.

        Args:
            url (str): Link to be accessed

        Returns:
            Union[bytes, None]: content of page or None
        """
        try:
            r = requests.get(url)

            if r.status_code != 200:
                return None
            return r.content
        except Exception as e:
            # print(e.__class__, e)
            return None


if __name__ == "__main__":
    cache = Cache()

    # url = "http://slowwly.robertomurray.co.uk"
    url = "https://stackoverflow.com/questions/\
        12802726/how-to-list-all-redis-databases"

    cache.save(url)
    result = cache._client.get(url)
    print(cache._client.get("count:{}".format(url)))
    print(result)
