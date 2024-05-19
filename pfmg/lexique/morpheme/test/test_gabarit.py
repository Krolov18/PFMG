# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import pytest
from frozendict import frozendict

from pfmg.lexique.morpheme.Gabarit import Gabarit
from pfmg.lexique.stem_space.StemSpace import StemSpace

parametrize = pytest.mark.parametrize(
    "rule, expected, sigma", [
        ("1111", ("1111",), frozendict(Genre="m")),
        ("2222", ("2222",), frozendict(Genre="m")),
        ("VVVV", ("VVVV",), frozendict(Genre="m")),
        ("2V49", ("2V49",), frozendict(Genre="m")),
        ("4U55e6V6", ("4U55e6V6",), frozendict(Genre="m")),
    ]
)


@parametrize
def test_equal(fx_df_phonology, rule, expected, sigma) -> None:
    gabarit = Gabarit(
        rule=rule,
        sigma=sigma,
        phonology=fx_df_phonology
    )

    # test d'identité
    assert gabarit == gabarit

    # test d'égalité
    other_gabarit = Gabarit(
        rule=rule,
        sigma=sigma,
        phonology=fx_df_phonology
    )
    assert gabarit == other_gabarit

    # test avec le sigma qui diffère
    other_gabarit = Gabarit(
        rule=rule,
        sigma=frozendict(Genre="f"),
        phonology=fx_df_phonology
    )
    assert gabarit != other_gabarit

    # test avec le rule qui diffère
    other_gabarit = Gabarit(
        rule="5V44aV66",
        sigma=sigma,
        phonology=fx_df_phonology
    )
    assert gabarit != other_gabarit

    # test avec rule et sigma qui diffèrent
    other_gabarit = Gabarit(
        rule="5V44aV66",
        sigma=frozendict(),
        phonology=fx_df_phonology
    )
    assert gabarit != other_gabarit


def test_suffix_typeerror(fx_df_phonology) -> None:
    with pytest.raises(TypeError):
        _ = Gabarit(
            rule=1,  # type: ignore reportArgumentType
            sigma=frozendict(),
            phonology=fx_df_phonology
        )

    with pytest.raises(TypeError):
        _ = Gabarit(
            rule="1",
            sigma=1,  # type: ignore reportArgumentType
            phonology=fx_df_phonology
        )

    with pytest.raises(TypeError):
        _ = Gabarit(
            rule="1",
            sigma=frozendict(),
            phonology=1  # type: ignore reportArgumentType
        )

    with pytest.raises(TypeError):
        _ = Gabarit(
            rule="",
            sigma=frozendict(Genre="m"),
            phonology=fx_df_phonology
        )

    with pytest.raises(TypeError):
        _ = Gabarit(
            rule="hHPJLK",
            sigma=frozendict(Genre="m"),
            phonology=fx_df_phonology
        )


def test_to_string(fx_df_phonology) -> None:
    # rule avec 'V'
    gabarit = Gabarit(
        rule="5V44aV66",
        sigma=frozendict(Genre="m"),
        phonology=fx_df_phonology
    )

    with pytest.raises(NotImplementedError):
        assert gabarit.to_string(None)

    with pytest.raises(NotImplementedError):
        assert gabarit.to_string("truc")

    actual = gabarit.to_string(StemSpace(stems=("truk",)))
    expected = "wuppautt"
    assert actual == expected

    # rule avec 'U'
    gabarit = Gabarit(
        rule="5U44aV66",
        sigma=frozendict(Genre="m"),
        phonology=fx_df_phonology
    )

    with pytest.raises(NotImplementedError):
        assert gabarit.to_string(None)

    with pytest.raises(NotImplementedError):
        assert gabarit.to_string("truc")

    actual = gabarit.to_string(StemSpace(stems=("truk",)))
    expected = "wuppautt"
    assert actual == expected

    # rule avec 'A'
    gabarit = Gabarit(
        rule="5A44aV66",
        sigma=frozendict(Genre="m"),
        phonology=fx_df_phonology
    )

    with pytest.raises(NotImplementedError):
        assert gabarit.to_string(None)

    with pytest.raises(NotImplementedError):
        assert gabarit.to_string("truc")

    actual = gabarit.to_string(StemSpace(stems=("truk",)))
    expected = "wuppautt"
    assert actual == expected

    # rule avec 789
    gabarit = Gabarit(
        rule="5A44aV68",
        sigma=frozendict(Genre="m"),
        phonology=fx_df_phonology
    )

    with pytest.raises(NotImplementedError):
        assert gabarit.to_string(None)

    with pytest.raises(NotImplementedError):
        assert gabarit.to_string("truc")

    actual = gabarit.to_string(StemSpace(stems=("truk",)))
    expected = "wuppautw"
    assert actual == expected


def test_repr(fx_df_phonology) -> None:
    gabarit = Gabarit(
        rule="5A44aV66",
        sigma=frozendict(Genre="m"),
        phonology=fx_df_phonology
    )
    actual = repr(gabarit)
    assert actual == "Gabarit(5A44aV66)"
