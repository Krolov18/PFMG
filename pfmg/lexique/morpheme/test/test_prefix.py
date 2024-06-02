# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import pytest
from frozendict import frozendict

from pfmg.lexique.morpheme.Prefix import Prefix
from pfmg.lexique.phonology.Phonology import Phonology
from pfmg.lexique.stem_space.StemSpace import StemSpace


@pytest.mark.parametrize(
    "rule, expected, sigma", [
        ("d+X", ("d",), frozendict(Genre="m")),
    ]
)
def test_prefix(fx_df_phonology, rule, expected, sigma) -> None:
    prefix = Prefix(
        rule=rule,
        sigma=sigma,
        phonology=fx_df_phonology
    )

    assert str(prefix) == f"Prefix({rule})"

    # test d'identité
    assert prefix == prefix

    # test d'égalité
    other_prefix = Prefix(
        rule=rule,
        sigma=sigma,
        phonology=fx_df_phonology
    )
    assert prefix == other_prefix

    # test avec le sigma qui diffère
    other_prefix = Prefix(
        rule=rule,
        sigma=frozendict(Genre="f"),
        phonology=fx_df_phonology
    )
    assert prefix != other_prefix

    # test avec le rule qui diffère
    other_prefix = Prefix(
        rule="a+X",
        sigma=sigma,
        phonology=fx_df_phonology
    )
    assert prefix != other_prefix

    # test avec rule et sigma qui diffèrent
    other_prefix = Prefix(
        rule="a+X",
        sigma=frozendict(Genre="f"),
        phonology=fx_df_phonology
    )
    assert prefix != other_prefix


def test_prefix_type_error(fx_df_phonology) -> None:
    with pytest.raises(TypeError):
        Prefix(
            rule="",
            sigma=frozendict(),
            phonology=fx_df_phonology
        )

    with pytest.raises(TypeError):
        Prefix(
            rule="hHPJLK",
            sigma=frozendict(),
            phonology=fx_df_phonology
        )


def test_get_sigma(fx_df_phonology) -> None:
    prefix = Prefix(
        rule="d+X",
        sigma=frozendict(Genre="m"),
        phonology=fx_df_phonology
    )
    assert prefix.get_sigma() == frozendict(Genre="m")


def test_get_rule(fx_df_phonology) -> None:
    prefix = Prefix(
        rule="d+X",
        sigma=frozendict(Genre="m"),
        phonology=fx_df_phonology
    )
    assert prefix.get_rule().string == "d+X"


def test_to_string(fx_df_phonology) -> None:
    prefix = Prefix(
        rule="d+X",
        sigma=frozendict(Genre="m"),
        phonology=fx_df_phonology
    )

    with pytest.raises(NotImplementedError):
        _ = prefix.to_string(None)

    assert prefix.to_string(StemSpace(("toto",))) == "dtoto"

    assert prefix.to_string("toto") == "dtoto"


def test_to_decoupe(fx_df_phonology) -> None:
    prefix = Prefix(
        rule="d+X",
        sigma=frozendict(Genre="m"),
        phonology=fx_df_phonology
    )

    with pytest.raises(NotImplementedError):
        _ = prefix.to_decoupe(None)

    assert prefix.to_decoupe(StemSpace(("toto",))) == "d-toto"

    assert prefix.to_decoupe("toto") == "d-toto"


def test_to_glose(fx_df_phonology) -> None:
    prefix = Prefix(
        rule="d+X",
        sigma=frozendict(Genre="m"),
        phonology=fx_df_phonology
    )

    with pytest.raises(NotImplementedError):
        _ = prefix.to_glose(None)

    assert prefix.to_glose(StemSpace(("toto",))) == "m-toto"

    assert prefix.to_glose("toto") == "m-toto"
