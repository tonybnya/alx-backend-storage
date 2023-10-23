#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
Module tracks how many times a particular URL was accessed
"""
import redis
import requests
from functools import wraps
from typing import Callable

# Initialize the Redis connection
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
        count_key = f"count:{url}"
        result_key = f"result:{url}"

        # Increment the count
        r.incr(count_key)

        # Check if the result is in the cache
        result = r.get(result_key)

        if result:
            return result.decode("utf-8")

        # If not in cache, fetch the result
        result = method(url)

        # Store the count and result in Redis
        r.setex(result_key, CACHE_EXPIRATION_SECONDS, result)

        return result


CACHE_EXPIRATION_SECONDS = 10  # Constant for cache expiration


@count_calls
def get_page(url: str) -> str:
    """
    Get the HTML content from a URL
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.text
    except requests.RequestException as e:
        print(f"Failed to retrieve the page: {e}")
        return "Error: Unable to retrieve the page."


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk"
    page_content = get_page(url)
    if page_content:
        print(page_content)
