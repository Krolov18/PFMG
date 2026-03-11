"""Helper functions."""

import functools
from collections.abc import Callable


def static_vars(**kwargs):
    """Decorator that attaches static variables to a function (via attributes).

    Args:
        **kwargs: Attribute names and values to set on the wrapped function.

    Returns:
        Callable: A decorator that sets those attributes on the wrapped function.

    """

    def _(func: Callable):
        """Attach kwargs as attributes on func and return func.

        Args:
            func: Function to attach attributes to.

        Returns:
            Callable: The same function with attributes set.

        """
        for key, value in kwargs.items():
            setattr(func, key, value)
        return func

    return _


def compose(*functions: Callable) -> Callable:
    """Return a single callable that applies the given callables left to right.

    For example, the result of compose(f, g, h) applied to x yields f(g(h(x))).

    Args:
        *functions: Callables to compose (left to right).

    Returns:
        Callable: Single callable that applies the composition.

    """

    def __compose(f: Callable, g: Callable):
        """Return a callable that applies the first callable to the result of the second.

        Args:
            f: Outer callable.
            g: Inner callable.

        Returns:
            Callable: Composed callable f(g(*args)).

        """
        return lambda *args: f(g(*args))

    return functools.reduce(__compose, functions, lambda y: y)
