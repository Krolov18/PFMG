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
def test_condition(rule, expected, sigma) -> None:
    phonology = Phonology(
        apophonies=frozendict(Ø="i", i="a", a="u", u="u", e="o", o="o"),
        mutations=frozendict(p="p", t="p", k="t", b="p", d="b",
                             g="d", m="m", n="m", N="n", f="f",
                             s="f", S="s", v="f", z="v", Z="z",
                             r="w", l="r", j="w", w="w"),
        derives=frozendict(A="V", D="C"),
        consonnes=frozenset("ptkbdgmnNfsSvzZrljw"),
        voyelles=frozenset("iueoa")
    )
    condition = Condition(
        rule=rule,
        sigma=sigma,
        phonology=phonology
    )

    assert condition.phonology is phonology

    assert condition.rule.groups() == expected

    assert condition.sigma == sigma == condition.get_sigma()

    assert str(condition) == f"Condition({rule})"

    # test d'identité
    assert condition == condition

    # test d'égalité
    other_condition = Condition(
        rule=rule,
        sigma=sigma,
        phonology=phonology
    )
    assert condition == other_condition

    # test avec le sigma qui diffère
    other_condition = Condition(
        rule=rule,
        sigma=frozendict(Genre="f"),
        phonology=phonology
    )
    assert condition != other_condition

    # test avec le rule qui diffère
    other_condition = Condition(
        rule="X3?X2:X1",
        sigma=sigma,
        phonology=phonology
    )
    assert condition != other_condition

    # test avec rule et sigma qui diffèrent
    other_condition = Condition(
        rule="X3?X2:X1",
        sigma=frozendict(),
        phonology=phonology
    )
    assert condition != other_condition


@pytest.mark.parametrize("rule, expected, sigma", [
    ("", frozendict(Genre="m"), None),
    ("hHPJLK", frozendict(Genre="m"), None),
    ("X2X1:X1", frozendict(Genre="m"), None),
    ("X2?X1X1", frozendict(Genre="m"), None),
    ("X2X1X1", frozendict(Genre="m"), None),
    ("X2?X1:XD", frozendict(Genre="m"), None),
    ("X2?X2:X1+s", frozendict(Genre="m"), None),  # TODO: C'est une règle qu'on voudrait licite
])
def test_suffix_error(rule, expected, sigma) -> None:
    phonology = Phonology(
        apophonies=frozendict(Ø="i", i="a", a="u", u="u", e="o", o="o"),
        mutations=frozendict(p="p", t="p", k="t", b="p", d="b",
                             g="d", m="m", n="m", N="n", f="f",
                             s="f", S="s", v="f", z="v", Z="z",
                             r="w", l="r", j="w", w="w"),
        derives=frozendict(A="V", D="C"),
        consonnes=frozenset("ptkbdgmnNfsSvzZrljw"),
        voyelles=frozenset("iueoa")
    )

    with pytest.raises(TypeError):
        _ = Condition(
            rule=rule,
            sigma=sigma,
            phonology=phonology
        )


def test_to_string_with_none() -> None:
    phonology = Phonology(
        apophonies=frozendict(Ø="i", i="a", a="u", u="u", e="o", o="o"),
        mutations=frozendict(p="p", t="p", k="t", b="p", d="b",
                             g="d", m="m", n="m", N="n", f="f",
                             s="f", S="s", v="f", z="v", Z="z",
                             r="w", l="r", j="w", w="w"),
        derives=frozendict(A="V", D="C"),
        consonnes=frozenset("ptkbdgmnNfsSvzZrljw"),
        voyelles=frozenset("iueoa")
    )
    condition = Condition(
        rule="X2?X1:X1",
        sigma=frozendict(Genre="m"),
        phonology=phonology
    )

    with pytest.raises(NotImplementedError):
        _ = condition.to_string(None)

    assert condition.to_string(StemSpace(("toto",))) == "toto"
    assert condition.to_string(StemSpace(("toto", "tutu"))) == "toto"

    with pytest.raises(NotImplementedError):
        _ = condition.to_string("toto")
