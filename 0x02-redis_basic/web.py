#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
Module tracks how many times a particular URL was accessed
"""
import redis
import requests
from functools import wraps
from typing import Callable

r = redis.Redis()


def count_calls(method: Callable) -> Callable:
    """
    Track how many times a particular URL was accessed
    and cache with expiration
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        """
        Wrapper function to count and cache
        """
        r.incr(f"count:{url}")
        result = r.get(f"result:{url}")

        if result:
            return result.decode('utf-8')

        result = method(url)
        r.set(f'count:{url}', 0)
        r.setex(f'result:{url}', 10, result)
        return result

    return wrapper


@count_calls
def get_page(url: str) -> str:
    """
    Get the HTML content from a URL
    """
    return requests.get(url).text


if __name__ == '__main__':
    url = "http://slowwly.robertomurray.co.uk"
    page_content = get_page(url)
    if page_content:
        print(page_content)
