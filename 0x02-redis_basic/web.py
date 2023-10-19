#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
Module tracks how many times a particular URL was accessed
"""
import redis
import requests
from typing import Callable
from functools import wraps


r = redis.Redis()


def count_calls(method: Callable) -> Callable:
    """
    Track how many times a particular URL was accessed
    """
    @wraps(method)
    def wrapper(url):
        """
        Wrapper function
        """
        r.incr(f"count:{url}")
        cached = r.get(f"cached:{url}")

        if cached:
            return cached.decode('utf-8')

        html = method(url)
        r.setex(f"cached:{url}", 10, html)
        return html

    return wrapper


@count_calls
def get_page(url: str) -> str:
    """
    Get the HTML content
    """
    return requests.get(url).text
