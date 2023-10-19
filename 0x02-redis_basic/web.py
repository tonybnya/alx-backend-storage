#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
Module tracks how many times a particular URL was accessed
"""
from functools import wraps
from typing import Callable
import redis
import requests

r = redis.Redis()


def count_calls(method: Callable) -> Callable:
    """
    Track how many times a particular URL was accessed
    and cache with expiration
    """
    @wraps(method)
    def wrapper(url):
        """
        Wrapper function to count and cache
        """
        r.incr(f"count:{url}")
        cached = r.get(f"cached:{url}")

        if cached:
            return cached.decode('utf-8')

        try:
            html = method(url)
            r.setex(f"cached:{url}", 10, html)
            return html
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL: {e}")
            return None

    return wrapper


@count_calls
def get_page(url: str) -> str:
    """
    Get the HTML content from a URL
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
