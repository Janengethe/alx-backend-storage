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


def call_history(method: Callable) -> Callable:
    """
    store the history of inputs and outputs
    for a particular function
    """
    key = method.__qualname__
    input_key = key + ":inputs"
    output_key = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """use rpush to append the input arguments"""
        self._redis.rpush(input_key, str(args))
        data = method(self, *args, **kwds)
        self._redis.rpush(output_key, str(data))
        return data
    return wrapper


class Cache:
    def __init__(self) -> None:
        """Initialization"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
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


def replay(method: Callable) -> Callable:
    """ display the history of calls for a function """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"
    redis = method.__self__._redis
    count = redis.get(key).decode("utf-8")
    print("{} was called {} times:".format(key, count))
    inputList = redis.lrange(inputs, 0, -1)
    outputList = redis.lrange(outputs, 0, -1)
    redis_all = list(zip(inputList, outputList))
    for a, b in redis_all:
        attr, data = a.decode("utf-8"), b.decode("utf-8")
        print("{}(*{}) -> {}".format(key, attr, data))
