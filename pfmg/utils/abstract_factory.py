"""Abstract factory implementation using import_module and getattr."""

from collections.abc import Callable
from importlib import import_module
from typing import TypeVar

AbstractClass = TypeVar("AbstractClass", type, Callable)
AbstractProduct = TypeVar("AbstractProduct")


def factory_function(
    concrete_product: str,
    package: str,
    **kwargs,
) -> AbstractProduct:
    """Call a concrete function or constructor from the given package.

    Args:
        concrete_product: Name of the concrete object (function or class).
        package: Package path (module location).
        **kwargs: Arguments to pass to the function/constructor.

    Returns:
        AbstractProduct: Instance or return value of the concrete product.

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
) -> AbstractProduct:
    """Build any concrete class from package; module path is package.concrete_product.

    Args:
        concrete_product: Name of the concrete class or function.
        package: Base package path.
        **kwargs: Arguments to pass to the constructor.

    Returns:
        AbstractProduct: Instance of the concrete product.

    """
    assert __validate_params(concrete_product, package)

    module_product = (package + "." if package else "") + concrete_product
    return factory_function(
        concrete_product=concrete_product,
        package=module_product,
        **kwargs,
    )


def __validate_params(concrete_product: str, package: str) -> bool:
    """Validate concrete_product and package (non-empty, no leading/trailing dots).

    Args:
        concrete_product: Name to validate.
        package: Package path to validate.

    Returns:
        bool: True if valid (assertions run for side effects).

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
) -> AbstractClass:
    """Look up and return a concrete class from a package without instantiating it."""
    return getattr(
        import_module(package),
        concrete_product,
    )


def factory_class(
    concrete_product: str,
    package: str,
) -> AbstractClass:
    """Look up and return a concrete class (module name must equal class name).

    Args:
        concrete_product: Name of the class (and module).
        package: Base package path.

    Returns:
        AbstractClass: The class object.

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
) -> AbstractProduct:
    """Return an instance of the concrete class (module name must equal class name).

    Args:
        concrete_product: Name of the class (and module).
        package: Base package path.
        **kwargs: Arguments to pass to the constructor.

    Returns:
        AbstractProduct: Instance of the concrete class.

    """
    return factory_class(
        concrete_product=concrete_product,
        package=package,
    )(
        **kwargs,
    )
