import pytest

from pfmg.utils.test.data_for_test.ConcreteProduct import ConcreteProduct


@pytest.mark.parametrize("concrete_product", [
    [],
    set(),
    int(),
    complex(),
    frozenset(),
    bytearray()
])
def test_param_concrete_product_type(
        fx_partial_factory_method_missing_concrete_product,
        concrete_product
) -> None:
    with pytest.raises(
            AssertionError,
            match=r"'concrete_product' must be a string. A.*was given."
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
    with pytest.raises(AssertionError,
                       match=r"'concrete_product' can't be empty."):
        fx_partial_factory_method_missing_concrete_product(
            concrete_product=concrete_product
        )


@pytest.mark.parametrize("package", [
    [],
    set(),
    int(),
    complex(),
    frozenset(),
    bytearray()
])
def test_param_package_type(
        fx_partial_factory_method_missing_package,
        package
) -> None:
    with pytest.raises(
            AssertionError,
            match=r"'package' must be a string. A.*was given."
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
            match=r"'package' can't be empty."
    ):
        fx_partial_factory_method_missing_package(
            package=package
        )


@pytest.mark.parametrize("package", [
    ".path",
    "path."
])
def test_param_package_relative_path(
        fx_partial_factory_method_missing_package,
        package
) -> None:
    with pytest.raises(
            AssertionError,
            match=r"Relative path are not allowed."
    ):
        fx_partial_factory_method_missing_package(
            package=package
        )


@pytest.mark.parametrize("package", [
    "unknown_package",
    "package_unknown"
])
def test_param_package_module_not_found(
        fx_partial_factory_method_missing_package, package) -> None:
    with pytest.raises(NameError, match="The module.*was not found."):
        fx_partial_factory_method_missing_package(
            package=package
        )


@pytest.mark.parametrize("concrete_product, package", [
    ("unknown_concrete_product", "utils.test.data_for_test"),
    ("concrete_product_unknown", "utils.test.data_for_test")
])
def test_param_concrete_product_not_found_in_package(
        fx_partial_factory_method_missing_concrete_product_package,
        concrete_product, package) -> None:
    with pytest.raises(NameError, match=r".*is not a concrete product of.*"):
        fx_partial_factory_method_missing_concrete_product_package(
            concrete_product=concrete_product,
            package=package
        )


def test_factory_method_return_value(fx_factory_method) -> None:
    assert isinstance(fx_factory_method(), ConcreteProduct)
