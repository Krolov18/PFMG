# Copyright (c) <year>, <copyright holder>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. 
import pytest
from frozendict import frozendict

from pfmg.lexique.stem_space.StemSpace import StemSpace
from pfmg.lexique.morpheme.Suffix import Suffix
from pfmg.lexique.phonology.Phonology import Phonology


@pytest.mark.parametrize("rule, expected_groups, sigma", [
    ("X+d", ("d",), frozendict(Genre="m")),
])
def test_suffix(rule, expected_groups, sigma) -> None:
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
    suffix = Suffix(
        rule=rule,
        sigma=sigma,
        phonology=phonology
    )

    # test d'identité
    assert suffix == suffix

    # test d'égalité
    other_suffix = Suffix(
        rule=rule,
        sigma=sigma,
        phonology=phonology
    )
    assert suffix == other_suffix

    # test avec le sigma qui diffère
    other_suffix = Suffix(
        rule=rule,
        sigma=frozendict(Genre="f"),
        phonology=phonology
    )
    assert suffix != other_suffix

    # test avec le rule qui diffère
    other_suffix = Suffix(
        rule="X+a",
        sigma=sigma,
        phonology=phonology
    )
    assert suffix != other_suffix

    # test avec rule et sigma qui diffèrent
    other_suffix = Suffix(
        rule="X+a", sigma=frozendict(Genre="f"),
        phonology=phonology
    )
    assert suffix != other_suffix


def test_suffix_type_error() -> None:
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
        Suffix(
            rule="",
            sigma=frozendict(),
            phonology=phonology
        )

    with pytest.raises(TypeError):
        Suffix(
            rule="hHPJLK",
            sigma=frozendict(),
            phonology=phonology
        )


def test_to_string() -> None:
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
    suffix = Suffix(
        rule="X+d",
        sigma=frozendict(Genre="m"),
        phonology=phonology
    )
    with pytest.raises(NotImplementedError):
        _ = suffix.to_string(None)
    assert suffix.to_string("toto") == "totod"
    assert suffix.to_string(StemSpace(("toto",))) == "totod"


def test_repr() -> None:
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
    suffix = Suffix(
        rule="X+d",
        sigma=frozendict(Genre="m"),
        phonology=phonology
    )
    assert repr(suffix) == "Suffix(rule=X+d, sigma=frozendict({'Genre': 'm'}))"
