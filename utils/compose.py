# pylint: disable=line-too-long,missing-module-docstring,missing-function-docstring,invalid-name

import functools

from typing import Callable


def compose(*functions: Callable) -> Callable:
    def __compose(f: Callable, g: Callable):
        return lambda *args: f(g(*args))
    return functools.reduce(__compose, functions, lambda y: y)
