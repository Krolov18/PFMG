# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import pytest
from frozendict import frozendict

from pfmg.lexique.morpheme.Selection import Selection
from pfmg.lexique.stem_space.StemSpace import StemSpace


@pytest.mark.parametrize("rule, expected, sigma", [
    ("X1", ("1",), frozendict(Genre="m")),
])
def test_selection(fx_df_phonology, rule, expected, sigma) -> None:
    selection = Selection(
        rule=rule,
        sigma=sigma,
        phonology=fx_df_phonology
    )

    assert selection.get_rule().groups() == expected

    assert selection.get_sigma() == sigma

    assert str(selection) == f"Selection({rule})"

    # test d'identité
    assert selection == selection

    # test d'égalité
    other_selection = Selection(
        rule=rule,
        sigma=sigma,
        phonology=fx_df_phonology
    )
    assert selection == other_selection

    # test avec le sigma qui diffère
    other_selection = Selection(
        rule=rule,
        sigma=frozendict(Genre="f"),
        phonology=fx_df_phonology
    )
    assert selection != other_selection

    # test avec le rule qui diffère
    other_selection = Selection(
        rule="X2",
        sigma=sigma,
        phonology=fx_df_phonology
    )
    assert selection != other_selection

    # test avec rule et sigma qui diffèrent
    other_selection = Selection(
        rule="X2",
        sigma=frozendict(),
        phonology=fx_df_phonology
    )
    assert selection != other_selection


def test_selection_type_error(fx_df_phonology) -> None:
    with pytest.raises(TypeError):
        Selection(
            rule="",
            sigma=frozendict(),
            phonology=fx_df_phonology
        )

    with pytest.raises(TypeError):
        Selection(
            rule="hHPJLK",
            sigma=frozendict(),
            phonology=fx_df_phonology
        )


def test_selection_to_string_not_implemented_error(fx_df_phonology) -> None:
    with pytest.raises(NotImplementedError):
        Selection(
            rule="X1",
            sigma=frozendict(),
            phonology=fx_df_phonology
        ).to_string(
            None
        )


@pytest.mark.parametrize("rule, stem_space, expected", [
    ("X1", ("X1", "X2"), "X1"),
    ("X2", ("X1", "X2"), "X2"),
    ("X2", ("X1", "X2", "X3"), "X2"),
    ("X15", ("X1", "X2", "X3", "X4",
             "X5", "X6", "X7", "X8",
             "X9", "X10", "X11", "X12",
             "X13", "X14", "X15"), "X15"),
])
def test_selection_to_string(fx_df_phonology, rule, stem_space, expected) -> None:
    selection = Selection(
        rule=rule,
        sigma=frozendict(),
        phonology=fx_df_phonology
    )

    assert selection.to_string(StemSpace(stem_space)) == expected


def test_selection_to_string_index_error(fx_df_phonology) -> None:
    selection = Selection(
        rule="X2",
        sigma=frozendict(),
        phonology=fx_df_phonology
    )

    with pytest.raises(AssertionError):
        selection.to_string(StemSpace(()))

    with pytest.raises(IndexError):
        selection.to_string(StemSpace(("X1",)))


def test_get_sigma(fx_df_phonology) -> None:
    sigma = frozendict()
    selection = Selection(
        rule="X2",
        sigma=sigma,
        phonology=fx_df_phonology
    )
    assert selection.get_sigma() == sigma
    assert selection.get_sigma() is sigma

    sigma = frozendict(Genre="f")
    selection = Selection(
        rule="X2",
        sigma=sigma,
        phonology=fx_df_phonology
    )
    assert selection.get_sigma() == sigma
    assert selection.get_sigma() is sigma


def test_get_rule(fx_df_phonology) -> None:
    rule = "X2"
    selection = Selection(
        rule=rule,
        sigma=frozendict(),
        phonology=fx_df_phonology
    )
    assert selection.get_rule().string == rule

    rule = "X1"
    selection = Selection(
        rule=rule,
        sigma=frozendict(Genre="f"),
        phonology=fx_df_phonology
    )
    assert selection.get_rule().string == rule


@pytest.mark.parametrize("rule, sigma, stems, expected", [
    ("X1", {"Genre": "m"}, ("toto",), "toto"),
    ("X1", {"Genre": "m"}, ("toto", "tutu"), "toto"),
    ("X2", {"Genre": "m"}, ("toto", "tutu"), "tutu"),
])
def test_to_decoupe(fx_df_phonology, rule, sigma, stems, expected) -> None:
    selection = Selection(
        rule=rule,
        sigma=frozendict(sigma),
        phonology=fx_df_phonology
    )

    with pytest.raises(NotImplementedError):
        _ = selection.to_decoupe(None)

    assert selection.to_decoupe(StemSpace(stems)) == expected


# TODO : peut-être qu'il faudrait raise un NotImplementedError pour ce cas
@pytest.mark.parametrize("rule, sigma, stems, expected", [
    ("X1", {"Genre": "m"}, "toto", "toto"),
    ("X1", {"Genre": "m"}, "toto", "toto"),
    ("X2", {"Genre": "m"}, "toto", "toto"),
])
def test_to_decoupe_str(fx_df_phonology, rule, sigma, stems, expected):
    selection = Selection(
        rule=rule,
        sigma=frozendict(sigma),
        phonology=fx_df_phonology
    )

    with pytest.raises(NotImplementedError):
        _ = selection.to_decoupe(None)

    assert selection.to_decoupe(stems) == expected
