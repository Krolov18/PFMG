# pylint: disable=line-too-long,missing-function-docstring,missing-module-docstring

import functools
import itertools
from typing import Dict, List

import pytest

from utils.abstract_factory import factory_method, factory_function

params_factory_method_concrete_product: List[str] = ["ConcreteProduct"]
params_factory_method_package: List[str] = ["utils.test.data_for_test"]
params_factory_method_kwargs: List[Dict] = [{}]
params_factory_method_concrete_product_package = list(itertools.product(params_factory_method_concrete_product,
                                                                        params_factory_method_package))
params_factory_method_concrete_product_kwargs = list(itertools.product(params_factory_method_concrete_product,
                                                                       params_factory_method_kwargs))
params_factory_method_package_kwargs = list(itertools.product(params_factory_method_package,
                                                              params_factory_method_kwargs))
params_factory_method_concrete_product_package_kwargs = list(itertools.product(params_factory_method_concrete_product,
                                                                               params_factory_method_package,
                                                                               params_factory_method_kwargs))


@pytest.fixture(scope="function", params=params_factory_method_package_kwargs)
def fx_partial_factory_method_missing_concrete_product(request) -> functools.partial:
    (package, kwargs) = request.param
    return functools.partial(factory_method, package=package, **kwargs)


@pytest.fixture(scope="function", params=params_factory_method_concrete_product_kwargs)
def fx_partial_factory_method_missing_package(request) -> functools.partial:
    (concrete_product, kwargs) = request.param
    return functools.partial(factory_method, concrete_product=concrete_product, **kwargs)


@pytest.fixture(scope="function", params=params_factory_method_kwargs)
def fx_partial_factory_method_missing_concrete_product_package(request) -> functools.partial:
    kwargs = request.param
    return functools.partial(factory_method, **kwargs)


@pytest.fixture(scope="function", params=params_factory_method_concrete_product_package_kwargs)
def fx_factory_method(request) -> functools.partial:
    (concrete_product, package, kwargs) = request.param
    return functools.partial(factory_method, concrete_product=concrete_product, package=package, **kwargs)


@pytest.fixture(scope="function", params=params_factory_method_package_kwargs)
def fx_partial_factory_function_missing_concrete_product(request) -> functools.partial:
    (package, kwargs) = request.param
    return functools.partial(factory_function, package=package, **kwargs)


@pytest.fixture(scope="function", params=params_factory_method_concrete_product_kwargs)
def fx_partial_factory_function_missing_package(request) -> functools.partial:
    (concrete_product, kwargs) = request.param
    return functools.partial(factory_function, concrete_product=concrete_product, **kwargs)


@pytest.fixture(scope="function", params=params_factory_method_concrete_product_package_kwargs)
def fx_factory_function(request) -> functools.partial:
    (concrete_product, package, kwargs) = request.param
    return functools.partial(factory_function, concrete_product=concrete_product, package=package, **kwargs)
