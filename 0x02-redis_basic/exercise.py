#!/usr/bin/env python3
"""
Module exercise
Contains class Cache
"""
import redis
import uuid
from typing import Union, Optional, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    implement a system to count how many times methods of
    the Cache class are called.
    takes a single method Callable argument and returns a Callable.
    As a key, use the qualified name of method using the
    __qualname__ dunder method.
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """
        Creates a return function that increments the count for that key
        every time the method is called and returns the value returned
        by the original method.

        the first argument of the wrapped function is self which is the
        instance itself, which lets you access the Redis instance.

        Protip: https://docs.python.org/3.7/library/functools.html
        #functools.wraps
        """
        self._redis.incr(key)
        return method(self, *args, **kwds)

    return wrapper


class Cache:
    def __init__(self) -> None:
        """Initialization"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        method generate a random key (e.g. using uuid),
        store the input data in Redis using the random key
        and return the key.
        """
        key: uuid.UUID = str(uuid.uuid1())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable]
            = None) -> Union[str, bytes, int, float]:
        """
        convert the data back to the desired format.
        """
        data = self._redis.get(key)
        if fn:
            data = fn(data)
        return data

    def get_str(self, data: bytes) -> str:
        """converts data to str"""
        return str(data, "utf-8")

    def get_int(self, data: bytes) -> int:
        """converts data to int"""
        return int(data, "base=0")
