# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Implémentation de l'abstract factory avec import_module et getattr."""

from collections.abc import Callable
from importlib import import_module
from typing import TypeVar

AbstractClass = TypeVar("AbstractClass", type, Callable)
AbstractProduct = TypeVar("AbstractProduct")


def factory_function(
    concrete_product: str,
    package: str,
    **kwargs,
) -> AbstractProduct:  # type: ignore reportInvalidTypeVarUse
    """Appelle n'importe quel fonction concrète.

    :param concrete_product: nom de l'objet concret
    :param package: string représentant la localisation du package
    :param kwargs: arguments de la classe/fonction
                   que l'on cherche à construire
    :return: instance de la classe ou de la fonction voulue
    """
    assert __validate_params(concrete_product, package)

    try:
        py_module = import_module(package)
    except ModuleNotFoundError as ex:
        message = f"The module '{package}' was not found."
        raise NameError(message) from ex

    if not hasattr(py_module, concrete_product):
        message = f"{concrete_product} is not a concrete product of {package}"
        raise NameError(message)

    return getattr(py_module, concrete_product)(**kwargs)


def factory_method(
    concrete_product: str,
    package: str,
    **kwargs,
) -> AbstractProduct:  # type: ignore reportInvalidTypeVarUse
    """Construit n'importe quelle classe concrète.

    :param concrete_product:
    :param package:
    :param kwargs:
    :return:
    """
    assert __validate_params(concrete_product, package)

    module_product = (package + "." if package else "") + concrete_product
    return factory_function(
        concrete_product=concrete_product,
        package=module_product,
        **kwargs,
    )


def __validate_params(concrete_product: str, package: str) -> bool:
    """Préconditions.

    :param concrete_product:
    :param package:
    :return:
    """
    assert isinstance(concrete_product, str)
    assert concrete_product
    assert isinstance(package, str)
    assert package
    assert not (package.startswith(".") or package.endswith("."))
    return True


def factory_type(
    concrete_product: str,
    package: str,
) -> AbstractClass:  # type: ignore reportInvalidTypeVarUse
    """Recherche et renvoie une classe concrète d'un package sans l'instantier.

    :param concrete_product:
    :param package:
    :param getattr_:
    :return:
    """
    return getattr(
        import_module(package),
        concrete_product,
    )


def factory_class(
    concrete_product: str,
    package: str,
) -> AbstractClass:  # type: ignore reportInvalidTypeVarUse
    """Recherche et renvoie une classe concrète d'un package sans l'instantier.

    Contrainte: nom du module == nom de la classe qu'il contient

    :param concrete_product:
    :param package:
    :return:
    """
    assert package
    assert concrete_product

    module_product = f"{package}.{concrete_product}"
    return factory_type(
        concrete_product=concrete_product,
        package=module_product,
    )


def factory_object(
    concrete_product: str,
    package: str,
    **kwargs,
) -> AbstractProduct:  # type: ignore reportInvalidTypeVarUse
    """Renvoie un object concret.

    Contrainte: nom du module == nom de la classe qu'il contient

    :param concrete_product:
    :param package:
    :param kwargs:
    :return:
    """
    return factory_class(
        concrete_product=concrete_product,
        package=package,
    )(
        **kwargs,
    )
