# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Configuration des fixtures."""

import functools
import itertools

import pytest
from frozendict import frozendict

from pfmg.lexique.phonology.Phonology import Phonology
from pfmg.utils.abstract_factory import factory_function, factory_method

params_factory_method_concrete_product: list[str] = ["ConcreteProduct"]
params_factory_method_package: list[str] = ["pfmg.utils.test.data_for_test"]
params_factory_method_kwargs: list[dict] = [{}]
params_factory_method_concrete_product_package = list(
    itertools.product(
        params_factory_method_concrete_product, params_factory_method_package
    )
)
params_factory_method_concrete_product_kwargs = list(
    itertools.product(
        params_factory_method_concrete_product, params_factory_method_kwargs
    )
)
params_factory_method_package_kwargs = list(
    itertools.product(
        params_factory_method_package, params_factory_method_kwargs
    )
)
params_factory_method_concrete_product_package_kwargs = list(
    itertools.product(
        params_factory_method_concrete_product,
        params_factory_method_package,
        params_factory_method_kwargs,
    )
)


@pytest.fixture(scope="function", params=params_factory_method_package_kwargs)
def fx_partial_factory_method_missing_concrete_product(
    request,  # noqa
) -> functools.partial:
    """Fixture à documenter."""
    (package, kwargs) = request.param
    return functools.partial(factory_method, package=package, **kwargs)


@pytest.fixture(
    scope="function", params=params_factory_method_concrete_product_kwargs
)
def fx_partial_factory_method_missing_package(request) -> functools.partial:  # noqa
    """Fixture à documenter."""
    (concrete_product, kwargs) = request.param
    return functools.partial(
        factory_method, concrete_product=concrete_product, **kwargs
    )


@pytest.fixture(scope="function", params=params_factory_method_kwargs)
def fx_partial_factory_method_missing_concrete_product_package(
    request,  # noqa
) -> functools.partial:
    """Fixture à documenter."""
    kwargs = request.param
    return functools.partial(factory_method, **kwargs)


@pytest.fixture(
    scope="function",
    params=params_factory_method_concrete_product_package_kwargs,
)
def fx_factory_method(request) -> functools.partial:  # noqa
    """Fixture à documenter."""
    (concrete_product, package, kwargs) = request.param
    return functools.partial(
        factory_method,
        concrete_product=concrete_product,
        package=package,
        **kwargs,
    )


@pytest.fixture(scope="function", params=params_factory_method_package_kwargs)
def fx_partial_factory_function_missing_concrete_product(
    request,  # noqa
) -> functools.partial:
    """Fixture à documenter."""
    (package, kwargs) = request.param
    return functools.partial(factory_function, package=package, **kwargs)


@pytest.fixture(
    scope="function", params=params_factory_method_concrete_product_kwargs
)
def fx_partial_factory_function_missing_package(request) -> functools.partial:  # noqa
    """Fixture à documenter."""
    (concrete_product, kwargs) = request.param
    return functools.partial(
        factory_function, concrete_product=concrete_product, **kwargs
    )


@pytest.fixture(
    scope="function",
    params=params_factory_method_concrete_product_package_kwargs,
)
def fx_factory_function(request) -> functools.partial:  # noqa
    """Fixture à documenter."""
    (concrete_product, package, kwargs) = request.param
    return functools.partial(
        factory_function,
        concrete_product=concrete_product,
        package=package,
        **kwargs,
    )


@pytest.fixture
def fx_df_phonology():
    """Fixture qui construit un Phonology avec des données "standards"."""
    return Phonology(
        apophonies=frozendict(Ø="i", i="a", a="u", u="u", e="o", o="o"),
        mutations=frozendict(
            p="p",
            t="p",
            k="t",
            b="p",
            d="b",
            g="d",
            m="m",
            n="m",
            N="n",
            f="f",
            s="f",
            S="s",
            v="f",
            z="v",
            Z="z",
            r="w",
            l="r",
            j="w",
            w="w",
        ),
        derives=frozendict(A="V", D="C"),
        consonnes=frozenset("ptkbdgmnNfsSvzZrljw"),
        voyelles=frozenset("iueoa"),
    )
