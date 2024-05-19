# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import pytest
from frozendict import frozendict

from pfmg.lexique.morpheme.Prefix import Prefix
from pfmg.lexique.morpheme.Suffix import Suffix
from pfmg.lexique.morpheme.Circumfix import Circumfix
from pfmg.lexique.morpheme.Condition import Condition
from pfmg.lexique.morpheme.Selection import Selection
from pfmg.lexique.morpheme.Gabarit import Gabarit
from pfmg.lexique.morpheme.Factory import create_morpheme
from pfmg.lexique.stem_space.StemSpace import StemSpace

parametrize = pytest.mark.parametrize(
    "rule, sigma, expected_type", [
        ("a+X", frozendict(
            {
                "Genre": "m"
            }
        ), Prefix),
        ("X+a", frozendict(), Suffix),
        ("s+X+a", frozendict(), Circumfix),
        ("4U55e6V6", frozendict(), Gabarit),
        ("X1", frozendict(), Selection),
        ("X2?X2:X1", frozendict(), Condition),
    ]
)


@parametrize
def test_prefix(fx_df_phonology, rule, sigma, expected_type) -> None:
    actual = create_morpheme(
        rule=rule,
        sigma=sigma,
        phonology=fx_df_phonology
    )
    assert isinstance(actual, expected_type)


parametrize = pytest.mark.parametrize(
    "rule, sigma, expected_type", [
        ("", frozendict(), None),
        ("REGLE_INCOMPRISE", frozendict(), None),
    ]
)


@parametrize
def test_prefix_error(fx_df_phonology, rule, sigma, expected_type) -> None:
    with pytest.raises(TypeError):
        _ = create_morpheme(
            rule=rule,
            sigma=sigma,
            phonology=fx_df_phonology
        )


parametrize = pytest.mark.parametrize(
    "rule, sigma, stems, expected", [
        ("a+X", frozendict(Genre="m"), ("truc",), "atruc"),
        ("X+a", frozendict(Genre="m"), ("truc",), "truca"),
        ("s+X+a", frozendict(Genre="m"), ("truc",), "struca"),
        ("4U55e6V6", frozendict(Genre="m"), ("trup",), "puwwepup"),
        ("4U55Ae6V6", frozendict(Genre="m"), ("lvup",), "ruffuepup"),
        ("7U88e9V9", frozendict(Genre="m"), ("tvup",), "puffepup"),
        ("X1", frozendict(Genre="m"), ("truc",), "truc"),
        ("X2?X2:X1", frozendict(Genre="m"), ("truc",), "truc"),
        ("X2?X2:X1", frozendict(Genre="m"), ("truc", "machin"), "machin"),
    ]
)


@parametrize
def test_to_string_stemspace(
    fx_df_phonology, rule, sigma, stems, expected
) -> None:
    actual = create_morpheme(
        rule=rule,
        sigma=sigma,
        phonology=fx_df_phonology
    )
    assert actual.to_string(StemSpace(stems=stems)) == expected


parametrize = pytest.mark.parametrize(
    "rule, sigma, stems, expected", [
        ("a+X", frozendict(Genre="m"), "truc", "atruc"),
        ("X+a", frozendict(Genre="m"), "truc", "truca"),
        ("s+X+a", frozendict(Genre="m"), "truc", "struca")
    ]
)


@parametrize
def test_to_string_str(fx_df_phonology, rule, sigma, stems, expected) -> None:
    actual = create_morpheme(
        rule=rule,
        sigma=sigma,
        phonology=fx_df_phonology
    )
    assert actual.to_string(stems) == expected


parametrize = pytest.mark.parametrize(
    "rule, sigma, stems", [
        ("a+X", frozendict(Genre="m"), None),
        ("X+a", frozendict(Genre="m"), None),
        ("s+X+a", frozendict(Genre="m"), None),
        ("4U55e6V6", frozendict(Genre="m"), None),
        ("X1", frozendict(Genre="m"), None),
        ("X2?X2:X1", frozendict(Genre="m"), None),
    ]
)


@parametrize
def test_to_string_none_not_implemented_error(
    fx_df_phonology,
    rule,
    sigma,
    stems
) -> None:
    actual = create_morpheme(
        rule=rule,
        sigma=sigma,
        phonology=fx_df_phonology
    )
    with pytest.raises(NotImplementedError):
        _ = actual.to_string(stems)
