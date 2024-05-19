# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import pytest
from frozendict import frozendict

from pfmg.lexique.stem_space.StemSpace import StemSpace
from pfmg.lexique.morpheme.Suffix import Suffix


@pytest.mark.parametrize("rule, expected_groups, sigma", [
    ("X+d", ("d",), frozendict(Genre="m")),
])
def test_suffix(fx_df_phonology, rule, expected_groups, sigma) -> None:
    suffix = Suffix(
        rule=rule,
        sigma=sigma,
        phonology=fx_df_phonology
    )

    # test d'identité
    assert suffix == suffix

    # test d'égalité
    other_suffix = Suffix(
        rule=rule,
        sigma=sigma,
        phonology=fx_df_phonology
    )
    assert suffix == other_suffix

    # test avec le sigma qui diffère
    other_suffix = Suffix(
        rule=rule,
        sigma=frozendict(Genre="f"),
        phonology=fx_df_phonology
    )
    assert suffix != other_suffix

    # test avec le rule qui diffère
    other_suffix = Suffix(
        rule="X+a",
        sigma=sigma,
        phonology=fx_df_phonology
    )
    assert suffix != other_suffix

    # test avec rule et sigma qui diffèrent
    other_suffix = Suffix(
        rule="X+a", sigma=frozendict(Genre="f"),
        phonology=fx_df_phonology
    )
    assert suffix != other_suffix


def test_suffix_type_error(fx_df_phonology) -> None:
    with pytest.raises(TypeError):
        Suffix(
            rule="",
            sigma=frozendict(),
            phonology=fx_df_phonology
        )

    with pytest.raises(TypeError):
        Suffix(
            rule="hHPJLK",
            sigma=frozendict(),
            phonology=fx_df_phonology
        )


def test_to_string(fx_df_phonology) -> None:
    suffix = Suffix(
        rule="X+d",
        sigma=frozendict(Genre="m"),
        phonology=fx_df_phonology
    )
    with pytest.raises(NotImplementedError):
        _ = suffix.to_string(None)
    assert suffix.to_string("toto") == "totod"
    assert suffix.to_string(StemSpace(("toto",))) == "totod"


def test_repr(fx_df_phonology) -> None:
    suffix = Suffix(
        rule="X+d",
        sigma=frozendict(Genre="m"),
        phonology=fx_df_phonology
    )
    assert repr(suffix) == "Suffix(rule=X+d, sigma=frozendict({'Genre': 'm'}))"


def test_to_decoupe(fx_df_phonology) -> None:
    suffix = Suffix(
        rule="X+i",
        sigma=frozendict(Genre="m"),
        phonology=fx_df_phonology
    )

    with pytest.raises(NotImplementedError):
        _ = suffix.to_decoupe(None)

    assert suffix.to_decoupe(StemSpace(("toto",))) == "toto-i"

    assert suffix.to_decoupe("toto") == "toto-i"
