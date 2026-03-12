"""Tests for factory_function (invalid params raise, valid returns callable)."""

from collections.abc import Callable

import pytest

from pfmg.conftest import _assert_compare


@pytest.mark.parametrize(
    "params, expected",
    [
        ({"concrete_product": []}, AssertionError),
        ({"concrete_product": set()}, AssertionError),
        ({"concrete_product": int()}, AssertionError),
        ({"concrete_product": complex()}, AssertionError),
        ({"concrete_product": frozenset()}, AssertionError),
        ({"concrete_product": bytearray()}, AssertionError),
        ({"concrete_product": ""}, AssertionError),
    ],
)
def test_factory_function_concrete_product_raises(
    fx_partial_factory_function_missing_concrete_product,
    params,
    expected,
) -> None:
    with pytest.raises(expected):
        fx_partial_factory_function_missing_concrete_product(**params)


@pytest.mark.parametrize(
    "params, expected",
    [
        ({"package": []}, AssertionError),
        ({"package": set()}, AssertionError),
        ({"package": int()}, AssertionError),
        ({"package": complex()}, AssertionError),
        ({"package": frozenset()}, AssertionError),
        ({"package": bytearray()}, AssertionError),
        ({"package": ""}, AssertionError),
        ({"package": ".path"}, AssertionError),
        ({"package": "path."}, AssertionError),
    ],
)
def test_factory_function_package_raises(
    fx_partial_factory_function_missing_package,
    params,
    expected,
) -> None:
    with pytest.raises(expected):
        fx_partial_factory_function_missing_package(**params)


@pytest.mark.parametrize(
    "params, expected",
    [
        ({}, Callable),
    ],
)
def test_factory_function(fx_factory_function, params, expected) -> None:
    result = fx_factory_function
    _assert_compare(isinstance(result, expected), True)
