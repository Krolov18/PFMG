# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import pytest
from frozendict import frozendict

from pfmg.lexique.morpheme.Circumfix import Circumfix
from pfmg.lexique.stem_space.StemSpace import StemSpace


@pytest.mark.parametrize("rule, sigma", [
    # test avec un rule vide
    ("", frozendict(Genre="m")),
    # test avec un rule qui ne contient pas de +X+
    ("hHPJLK", frozendict(Genre="m")),
])
def test_circumfix_error(fx_df_phonology, rule, sigma) -> None:
    with pytest.raises(TypeError):
        _ = Circumfix(
            rule=rule,
            sigma=sigma,
            phonology=fx_df_phonology
        )


def test_get_rule(fx_df_phonology) -> None:
    circumfix = Circumfix(
        rule="a+X+d",
        sigma=frozendict(Genre="m"),
        phonology=fx_df_phonology
    )

    assert circumfix.get_rule().string == "a+X+d"
    assert circumfix.get_rule().groups() == ("a", "d")
    assert circumfix.get_rule().group(1) == "a"
    assert circumfix.get_rule().group(2) == "d"


def test_get_sigma(fx_df_phonology) -> None:
    circumfix = Circumfix(
        rule="a+X+d",
        sigma=frozendict(Genre="m"),
        phonology=fx_df_phonology
    )

    assert circumfix.get_sigma() == frozendict(Genre="m")


def test_repr(fx_df_phonology) -> None:
    circumfix = Circumfix(
        rule="a+X+d",
        sigma=frozendict(Genre="m"),
        phonology=fx_df_phonology
    )

    actual = str(circumfix)
    expected = "Circumfix(rule=a+X+d, sigma=frozendict({'Genre': 'm'}))"
    assert actual == expected


def test_to_string(fx_df_phonology) -> None:
    circumfix = Circumfix(
        rule="a+X+d",
        sigma=frozendict(Genre="m"),
        phonology=fx_df_phonology
    )

    assert circumfix.to_string("toto") == "atotod"

    with pytest.raises(NotImplementedError):
        _ = circumfix.to_string(None)

    actual = circumfix.to_string(StemSpace(("toto", "tata")))
    assert actual == "atotod"


def test_equal(fx_df_phonology) -> None:
    circumfix = Circumfix(
        rule="a+X+d",
        sigma=frozendict(Genre="m"),
        phonology=fx_df_phonology
    )
    other_circumfix = Circumfix(
        rule="a+X+d",
        sigma=frozendict(Genre="m"),
        phonology=fx_df_phonology
    )
    assert circumfix == other_circumfix

    other_circumfix = Circumfix(
        rule="a+X+d",
        sigma=frozendict(Genre="f"),
        phonology=fx_df_phonology
    )
    assert circumfix != other_circumfix

    other_circumfix = Circumfix(
        rule="a+X+t",
        sigma=frozendict(Genre="m"),
        phonology=fx_df_phonology
    )
    assert circumfix != other_circumfix


def test_to_decoupe(fx_df_phonology) -> None:
    prefix = Circumfix(
        rule="a+X+i",
        sigma=frozendict(Genre="m"),
        phonology=fx_df_phonology
    )

    with pytest.raises(NotImplementedError):
        _ = prefix.to_decoupe(None)

    assert prefix.to_decoupe(StemSpace(("toto",))) == "a+toto+i"

    assert prefix.to_decoupe("toto") == "a+toto+i"
