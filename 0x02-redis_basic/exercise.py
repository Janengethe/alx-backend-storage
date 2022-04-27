#!/usr/bin/env python3
"""
Module exercise
Contains class Cache
"""
import redis
import uuid
from typing import Union


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
