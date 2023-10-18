#!/usr/bin/env python3
"""
Writing strings to Redis
"""

from typing import Callable, Optional, Union
import redis
import uuid


class Cache:
    """
    Definition of the class Cache
    """
    def __init__(self):
        """ Initialization """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        This method takes 'data' as argument and returns a string
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)

        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        Reading from Redis and recovering original type
        """
        data = self._redis.get(key)

        if fn:
            data = fn(data)

        return data

    def get_str(self, key: str) -> str:
        """
        Parametrize Cache.get with string conversion
        """
        data = self._redis.get(key)

        return data.decode('utf-8')

    def get_int(self, key: str) -> int:
        """
        Parametrize Cache.get with integer conversion
        """
        data = self._redis.get(key)

        return int(data.decode('utf-8'))


cache = Cache()

TEST_CASES = {
    b"foo": None,
    123: int,
    "bar": lambda d: d.decode("utf-8")
}

for value, fn in TEST_CASES.items():
    key = cache.store(value)
    assert cache.get(key, fn=fn) == value
