#!/usr/bin/python3
from typing import Any, Callable

from functools import lru_cache

class StringFunctor:
    def __init__(self, value: str):
        self.value = value
    # memoize results    
    @lru_cache
    def map(self, func: Callable[[Any], str]) -> "StringFunctor":
        # Recursively apply func() to a text input.
        return StringFunctor(func(self.value))