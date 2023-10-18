#!/usr/bin/env python3
"""
Writing strings to Redis
"""

from typing import Union
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
