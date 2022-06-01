# pylint: disable=line-too-long,missing-function-docstring,missing-module-docstring

from typing import Callable

import pytest


@pytest.mark.parametrize("concrete_product", [[], set(), int(), complex(), frozenset(), bytearray()])
def test_factory_function_concrete_product_type(fx_partial_factory_function_missing_concrete_product,
                                                concrete_product) -> None:
    with pytest.raises(AssertionError, match=r"'concrete_product' must be a string. A.*was given."):
        fx_partial_factory_function_missing_concrete_product(concrete_product=concrete_product)


@pytest.mark.parametrize("concrete_product", [""])
def test_factory_function_concrete_product_empty(fx_partial_factory_function_missing_concrete_product,
                                                 concrete_product) -> None:
    with pytest.raises(AssertionError, match=r"'concrete_product' can't be empty."):
        fx_partial_factory_function_missing_concrete_product(concrete_product=concrete_product)


@pytest.mark.parametrize("package", [[], set(), int(), complex(), frozenset(), bytearray()])
def test_factory_function_package_type(fx_partial_factory_function_missing_package, package) -> None:
    with pytest.raises(AssertionError, match=r"'package' must be a string. A.*was given."):
        fx_partial_factory_function_missing_package(package=package)


@pytest.mark.parametrize("package", [""])
def test_factory_function_package_empty(fx_partial_factory_function_missing_package, package) -> None:
    with pytest.raises(AssertionError, match=r"'package' can't be empty."):
        fx_partial_factory_function_missing_package(package=package)


@pytest.mark.parametrize("package", [".path", "path."])
def test_factory_function_package_relative_path(fx_partial_factory_function_missing_package, package) -> None:
    with pytest.raises(AssertionError, match=r"Relative path are not allowed."):
        fx_partial_factory_function_missing_package(package=package)


def test_factory_function(fx_factory_function):
    assert isinstance(fx_factory_function, Callable)
