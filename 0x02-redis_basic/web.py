#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
Module tracks how many times a particular URL was accessed
"""
import redis
import requests
from typing import Callable
from functools import wraps
import logging

logger = logging.getLogger(__name__)


class Cache:
    """
    Definition of the class Cache
    """
    def __init__(self):
        """
        Initialization
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def count_calls(method: Callable) -> Callable:
        """
        Track how many times a particular URL was accessed
        """
        @wraps(method)
        def wrapper(self, url):
            """
            Wrapper function
            """
            try:
                self._redis.incr(f"count:{url}")
                cached = self._redis.get(f"cached:{url}")

                if cached:
                    return cached.decode('utf-8')

                html = method(self, url)
                self._redis.setex(f"cached:{url}", 10, html)
                return html
            except Exception as e:
                logger.error(
                    f"Error in counting calls for URL: {url}, Error: {str(e)}"
                )

        return wrapper

    @count_calls
    def get_page(self, url: str) -> str:
        try:
            return requests.get(url).text
        except requests.RequestException as e:
            logger.error(
                f"Error in getting content for URL: {url}, Error: {str(e)}"
            )


if __name__ == '__main__':
    cache = Cache()
    url = "http://slowwly.robertomurray.co.uk"
    page_content = cache.get_page(url)
    print(page_content)
