import pytest

from pfmg.utils.test.data_for_test.ConcreteProduct import ConcreteProduct


parametrize = pytest.mark.parametrize("concrete_product", [
    [],
    set(),
    int(),
    complex(),
    frozenset(),
    bytearray()
])

@parametrize
def test_param_concrete_product_type(
        fx_partial_factory_method_missing_concrete_product,
        concrete_product
) -> None:
    with pytest.raises(
            AssertionError,
    ):
        fx_partial_factory_method_missing_concrete_product(
            concrete_product=concrete_product
        )


@pytest.mark.parametrize("concrete_product", [
    ""
])
def test_param_concrete_product_empty(
        fx_partial_factory_method_missing_concrete_product,
        concrete_product) -> None:
    with pytest.raises(
        AssertionError,
    ):
        fx_partial_factory_method_missing_concrete_product(
            concrete_product=concrete_product
        )


parametrize = pytest.mark.parametrize("package", [
    [],
    set(),
    int(),
    complex(),
    frozenset(),
    bytearray()
])

@parametrize
def test_param_package_type(
        fx_partial_factory_method_missing_package,
        package
) -> None:
    with pytest.raises(
            AssertionError,
    ):
        fx_partial_factory_method_missing_package(
            package=package
        )


@pytest.mark.parametrize("package", [
    ""
])
def test_param_package_empty(
        fx_partial_factory_method_missing_package,
        package
) -> None:
    with pytest.raises(
            AssertionError,
    ):
        fx_partial_factory_method_missing_package(
            package=package
        )


parametrize = pytest.mark.parametrize("package", [
    ".path",
    "path."
])

@parametrize
def test_param_package_relative_path(
        fx_partial_factory_method_missing_package,
        package
) -> None:
    with pytest.raises(
            AssertionError,
    ):
        fx_partial_factory_method_missing_package(
            package=package
        )


parametrize = pytest.mark.parametrize("package", [
    "unknown_package",
    "package_unknown"
])

@parametrize
def test_param_package_module_not_found(
        fx_partial_factory_method_missing_package, package) -> None:
    with pytest.raises(
        NameError,
    ):
        fx_partial_factory_method_missing_package(
            package=package
        )


parametrize = pytest.mark.parametrize("concrete_product, package", [
    ("unknown_concrete_product", "utils.test.data_for_test"),
    ("concrete_product_unknown", "utils.test.data_for_test")
])

@parametrize
def test_param_concrete_product_not_found_in_package(
        fx_partial_factory_method_missing_concrete_product_package,
        concrete_product, package) -> None:
    with pytest.raises(
        NameError,
    ):
        fx_partial_factory_method_missing_concrete_product_package(
            concrete_product=concrete_product,
            package=package
        )


def test_factory_method_return_value(fx_factory_method) -> None:
    assert isinstance(fx_factory_method(), ConcreteProduct)
