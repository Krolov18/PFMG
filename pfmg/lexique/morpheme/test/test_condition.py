# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import pytest
from frozendict import frozendict

from pfmg.lexique.morpheme.Condition import Condition
from pfmg.lexique.phonology.Phonology import Phonology
from pfmg.lexique.stem_space.StemSpace import StemSpace


@pytest.mark.parametrize("rule, expected, sigma", [
    ("X2?X1:X1", ("X2", "X1", "X1"), frozendict(Genre="m")),
])
def test_condition(fx_df_phonology, rule, expected, sigma) -> None:
    condition = Condition(
        rule=rule,
        sigma=sigma,
        phonology=fx_df_phonology
    )

    assert condition.phonology is fx_df_phonology

    assert condition.rule.groups() == expected

    assert condition.sigma == sigma == condition.get_sigma()

    assert str(condition) == f"Condition({rule})"

    # test d'identité
    assert condition == condition

    # test d'égalité
    other_condition = Condition(
        rule=rule,
        sigma=sigma,
        phonology=fx_df_phonology
    )
    assert condition == other_condition

    # test avec le sigma qui diffère
    other_condition = Condition(
        rule=rule,
        sigma=frozendict(Genre="f"),
        phonology=fx_df_phonology
    )
    assert condition != other_condition

    # test avec le rule qui diffère
    other_condition = Condition(
        rule="X3?X2:X1",
        sigma=sigma,
        phonology=fx_df_phonology
    )
    assert condition != other_condition

    # test avec rule et sigma qui diffèrent
    other_condition = Condition(
        rule="X3?X2:X1",
        sigma=frozendict(),
        phonology=fx_df_phonology
    )
    assert condition != other_condition


@pytest.mark.parametrize("rule, sigma", [
    ("", frozendict(Genre="m")),
    ("hHPJLK", frozendict(Genre="m")),
    ("X2X1:X1", frozendict(Genre="m")),
    ("X2?X1X1", frozendict(Genre="m")),
    ("X2X1X1", frozendict(Genre="m")),
    ("X2?X1:XD", frozendict(Genre="m")),
    ("X2?X2:X1+s", frozendict(Genre="m")),  # TODO: C'est une règle qu'on voudrait licite
])
def test_suffix_error(fx_df_phonology, rule, sigma) -> None:
    with pytest.raises(TypeError):
        _ = Condition(
            rule=rule,
            sigma=sigma,
            phonology=fx_df_phonology
        )


def test_to_string_with_none(fx_df_phonology) -> None:
    condition = Condition(
        rule="X2?X1:X1",
        sigma=frozendict(Genre="m"),
        phonology=fx_df_phonology
    )

    with pytest.raises(NotImplementedError):
        _ = condition.to_string(None)

    assert condition.to_string(StemSpace(("toto",))) == "toto"
    assert condition.to_string(StemSpace(("toto", "tutu"))) == "toto"

    with pytest.raises(NotImplementedError):
        _ = condition.to_string("toto")


def test_to_decoupe(fx_df_phonology) -> None:
    condition = Condition(
        rule="X2?X2:X1",
        sigma=frozendict(Genre="m"),
        phonology=fx_df_phonology
    )

    with pytest.raises(NotImplementedError):
        _ = condition.to_decoupe(None)

    assert condition.to_decoupe(StemSpace(("toto",))) == "toto"
    assert condition.to_decoupe(StemSpace(("toto", "tutu"))) == "tutu"

    assert condition.to_decoupe("toto") == "toto"
