# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
from typing import Callable

import pytest

parametrize = pytest.mark.parametrize(
    "concrete_product", [
        [],
        set(),
        int(),
        complex(),
        frozenset(),
        bytearray()
    ]
)


@parametrize
def test_factory_function_concrete_product_type(
    fx_partial_factory_function_missing_concrete_product,
    concrete_product
) -> None:
    with pytest.raises(
        AssertionError,
    ):
        fx_partial_factory_function_missing_concrete_product(
            concrete_product=concrete_product
        )


@pytest.mark.parametrize(
    "concrete_product", [
        ""
    ]
)
def test_factory_function_concrete_product_empty(
    fx_partial_factory_function_missing_concrete_product,
    concrete_product
) -> None:
    with pytest.raises(
        AssertionError,
    ):
        fx_partial_factory_function_missing_concrete_product(
            concrete_product=concrete_product
        )


parametrize = pytest.mark.parametrize(
    "package", [
        [],
        set(),
        int(),
        complex(),
        frozenset(),
        bytearray()
    ]
)


@parametrize
def test_factory_function_package_type(
    fx_partial_factory_function_missing_package,
    package
) -> None:
    with pytest.raises(
        AssertionError,
    ):
        fx_partial_factory_function_missing_package(package=package)


@pytest.mark.parametrize(
    "package", [
        ""
    ]
)
def test_factory_function_package_empty(
    fx_partial_factory_function_missing_package,
    package
) -> None:
    with pytest.raises(
        AssertionError,
    ):
        fx_partial_factory_function_missing_package(
            package=package
        )


@pytest.mark.parametrize(
    "package", [
        ".path",
        "path."
    ]
)
def test_factory_function_package_relative_path(
    fx_partial_factory_function_missing_package,
    package
) -> None:
    with pytest.raises(
        AssertionError,
    ):
        fx_partial_factory_function_missing_package(
            package=package
        )


def test_factory_function(fx_factory_function):
    assert isinstance(fx_factory_function, Callable)
