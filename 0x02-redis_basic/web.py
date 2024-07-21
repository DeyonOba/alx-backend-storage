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


client = redis.Redis()


def get_content(method: Callable) -> Callable:
    """Gets or Saves the content of the URL link.
    Args:
        method (Callable): Callable method

    Returns:
        Callable: content.
    """
    @wraps(method)
    def wrapper(*args):
        """Function wrapper
        """
        # check if content is cached
        cached = client.get(args[0])

        if cached:
            return cached.decode("utf-8")

        content = method(*args)
        client.setex(url, 10, content)
        return content
    return wrapper


def count_url_calls(method: Callable) -> Callable:
    """Counts the number of time a URL link has been accessed.

    Args:
        method (Callable): Callable method

    Returns:
        Callable: wrapper function
    """
    @wraps(method)
    def wrapper(*args):
        """Function wrapper.
        """
        print(args)
        client.incr("count:" + args[0])
        return method(*args)
    return wrapper


@get_content
@count_url_calls
def get_page(url: str) -> str:
    """Gets page content and updates
    the database with URL content and function url call count.

    Args:
        url (str): web link.

    Returns:
        str: page text content.
    """
    r = requests.get(url)
    return r.text


if __name__ == "__main__":

    # url = "http://slowwly.robertomurray.co.uk"
    url = "https://www.google.com/"
    print(client.get("count:"+url))
    print(get_page(url))
    print(client.get("count:"+url))
