"""Tests for factory_method (invalid params raise, valid returns ConcreteProduct)."""

import pytest

from pfmg.conftest import _assert_compare
from pfmg.utils.test.data_for_test.ConcreteProduct import ConcreteProduct


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
def test_factory_method_concrete_product_raises(
    fx_partial_factory_method_missing_concrete_product,
    params,
    expected,
) -> None:
    with pytest.raises(expected):
        fx_partial_factory_method_missing_concrete_product(**params)


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
def test_factory_method_package_raises(
    fx_partial_factory_method_missing_package,
    params,
    expected,
) -> None:
    with pytest.raises(expected):
        fx_partial_factory_method_missing_package(**params)


@pytest.mark.parametrize(
    "params, expected",
    [
        ({"package": "unknown_package"}, NameError),
        ({"package": "package_unknown"}, NameError),
    ],
)
def test_factory_method_package_module_not_found(
    fx_partial_factory_method_missing_package,
    params,
    expected,
) -> None:
    with pytest.raises(expected):
        fx_partial_factory_method_missing_package(**params)


@pytest.mark.parametrize(
    "params, expected",
    [
        (
            {"concrete_product": "unknown_concrete_product", "package": "pfmg.test.utils.data_for_test"},
            NameError,
        ),
        (
            {"concrete_product": "concrete_product_unknown", "package": "pfmg.test.utils.data_for_test"},
            NameError,
        ),
    ],
)
def test_factory_method_concrete_product_not_found_raises(
    fx_partial_factory_method_missing_concrete_product_package,
    params,
    expected,
) -> None:
    with pytest.raises(expected):
        fx_partial_factory_method_missing_concrete_product_package(**params)


@pytest.mark.parametrize(
    "params, expected",
    [
        ((), ConcreteProduct),
    ],
)
def test_factory_method_return_value(fx_factory_method, params, expected) -> None:
    result = fx_factory_method()
    _assert_compare(isinstance(result, expected), True)
