#!/usr/bin/env python3
"""
Writing strings to Redis
"""

from functools import wraps
from typing import Callable, Optional, Union
import redis
import uuid


def count_calls(method: Callable) -> Callable:
    """
    Incrementing values
    Implementing a counter for how many times
    methods of the Cache class are called
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Storing lists
    Storing the history of inputs and outputs
    for a particular function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function
        """
        input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)
        return output

    return wrapper


def replay(func: Callable):
    """ Replay function """
    r = redis.Redis()
    func_name = func.__qualname__
    number_calls = r.get(func_name)

    try:
        number_calls = number_calls.decode('utf-8')
    except Exception:
        number_calls = 0

    print(f'{func_name} was called {number_calls} times:')

    ins = r.lrange(func_name + ":inputs", 0, -1)
    outs = r.lrange(func_name + ":outputs", 0, -1)

    for cin, cout in zip(ins, outs):
        try:
            cin = cin.decode('utf-8')
        except Exception:
            cin = ""
        try:
            cout = cout.decode('utf-8')
        except Exception:
            cout = ""

        print(f'{func_name}(*{cin}) -> {cout}')


class Cache:
    """
    Definition of the class Cache
    """
    def __init__(self):
        """ Initialization """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        This method takes 'data' as argument and returns a string
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)

        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
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
