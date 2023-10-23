#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
Module tracks how many times a particular URL was accessed
"""
import redis
import requests
from functools import wraps
from typing import Callable

# Constants for cache expiration and initial count
CACHE_EXPIRATION_SECONDS = 10
INITIAL_COUNT = 0

# Initialize the Redis connection with error handling
try:
    r = redis.Redis()
except redis.ConnectionError as e:
    print(f"Failed to connect to Redis: {e}")
    exit(1)


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
        try:
            r.incr(f"count:{url}")
            result = r.get(f"result:{url}")

            if result:
                return result.decode("utf-8")

            result = method(url)
            r.setex(f"result:{url}", CACHE_EXPIRATION_SECONDS, result)
            return result
        except Exception as e:
            print(f"An error occurred: {e}")
            return "Error: Unable to retrieve the page."

    return wrapper


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


if __name__ == "__main":
    url = "http://slowwly.robertomurray.co.uk"
    page_content = get_page(url)
    if page_content:
        print(page_content)
