#!/usr/bin/env python3
"""
Module exercise
Contains class Cache
"""
import redis
import uuid
from typing import Union, Optional, Callable


class Cache:
    def __init__(self) -> None:
        """Initialization"""
        self._redis = redis.Redis()
        self._redis.flushdb()

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
