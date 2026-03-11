"""Helper functions."""

import functools
from collections.abc import Callable


def static_vars(**kwargs):
    """Stocke des variables statiques.

    Façon détournée pour stocker des variables statiques
    dans une fonction.

    :param kwargs:
    :return:
    """

    def _(func: Callable):
        """Inner function stockant les variables.

        :param func:
        :return:
        """
        for key, value in kwargs.items():
            setattr(func, key, value)
        return func

    return _


def compose(*functions: Callable) -> Callable:
    """Implémente la fonction de composition de fonction.

    À l'image des angage fonctionnels :
    compose(f, g, h) équivaut à dans certains langage (f . g . h).

    :param functions: Callable chaînables
    :return:
    """

    def __compose(f: Callable, g: Callable):
        """Construit une lambda effectuant l'opération de base de la composition.

        :param f: fonction quelconque
        :param g: fonction quelconque
        :return: le résultat de f appliqué au résultat de g appliqué aux args
        """
        return lambda *args: f(g(*args))

    return functools.reduce(__compose, functions, lambda y: y)
