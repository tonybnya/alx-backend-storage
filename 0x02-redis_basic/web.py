#!/usr/bin/env python3
"""A module with tools for request caching and tracking.
"""
import redis
import requests
from functools import wraps
from typing import Callable

r = redis.Redis()


def count_calls(method: Callable) -> Callable:
    """Decorator to know the number of calls"""

    @wraps(method)
    def wrapper(url):
        """Wrapper decorator"""
        r.incr(f"count:{url}")
        cached_html = r.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode("utf-8")

        html = method(url)
        r.setex(f"cached:{url}", 10, html)
        return html

    return wrapper


@count_calls
def get_page(url: str) -> str:
    """Get page"""
    req = requests.get(url)
    return req.text
