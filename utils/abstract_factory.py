# pylint: disable=line-too-long,missing-module-docstring,missing-function-docstring

import typing
from importlib import import_module

AbstractClass = typing.TypeVar("AbstractClass", type, typing.Callable)
AbstractProduct = typing.TypeVar("AbstractProduct")


def factory_function(
        concrete_product: str,
        package: str,
        getattr_=getattr,
        **kwargs
) -> AbstractProduct:
    """
    abstract factory générique qui pourra
    construire n'importe quel objet concret.

    :param concrete_product: nom de l'objet concret
    :param package: string représentant la localisation du package
    :param kwargs: arguments de la classe/fonction
                   que l'on cherche à construire
    :param getattr_: optimisation d'appel à getattr
    :return: instance de la classe ou de la fonction voulue
    """
    assert __validate_params(concrete_product, package)

    try:
        py_module = import_module(package)
    except ModuleNotFoundError as ex:
        raise NameError(f"The module '{package}' was not found.") from ex

    if not hasattr(py_module, concrete_product):
        raise NameError(
            f"{concrete_product} is not a concrete product of {package}"
        )

    return getattr_(py_module, concrete_product)(**kwargs)


def factory_method(
        concrete_product: str,
        package: str,
        **kwargs
) -> AbstractProduct:
    assert __validate_params(concrete_product, package)

    module_product = (package + "." if package else "") + concrete_product
    return factory_function(
        concrete_product=concrete_product,
        package=module_product,
        **kwargs
    )


def __validate_params(concrete_product, package):
    assert isinstance(concrete_product, str), f"'concrete_product' must be a string. A {type(package)} was given."
    assert concrete_product, "'concrete_product' can't be empty."
    assert isinstance(package, str), f"'package' must be a string. A {type(package)} was given."
    assert package, "'package' can't be empty."
    assert not (package.startswith(".") or package.endswith(".")), "Relative path are not allowed."

    return True


def factory_type(concrete_product: str, package: str, getattr_=getattr) -> AbstractClass:
    return getattr_(
        import_module(package),
        concrete_product
    )


def factory_class(concrete_product: str, package: str) -> AbstractClass:
    assert package
    assert concrete_product

    module_product = f"{package}.{concrete_product}"
    return factory_type(
        concrete_product=concrete_product,
        package=module_product
    )


def factory_object(
        concrete_product: str,
        package: str,
        **kwargs
) -> AbstractProduct:
    return factory_class(
        concrete_product=concrete_product,
        package=package
    )(**kwargs)
