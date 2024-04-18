# Copyright (c) <year>, <copyright holder>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. 
import pytest
from frozendict import frozendict

from pfmg.lexique.morpheme.Prefix import Prefix
from pfmg.lexique.phonology.Phonology import Phonology
from pfmg.lexique.stem_space.StemSpace import StemSpace


@pytest.mark.parametrize("rule, expected, sigma", [
    ("d+X", ("d",), frozendict(Genre="m")),
])
def test_prefix(rule, expected, sigma) -> None:
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
    prefix = Prefix(
        rule=rule,
        sigma=sigma,
        phonology=phonology
    )

    assert str(prefix) == f"Prefix({rule})"

    # test d'identité
    assert prefix == prefix

    # test d'égalité
    other_prefix = Prefix(
        rule=rule,
        sigma=sigma,
        phonology=phonology
    )
    assert prefix == other_prefix

    # test avec le sigma qui diffère
    other_prefix = Prefix(
        rule=rule,
        sigma=frozendict(Genre="f"),
        phonology=phonology
    )
    assert prefix != other_prefix

    # test avec le rule qui diffère
    other_prefix = Prefix(
        rule="a+X",
        sigma=sigma,
        phonology=phonology
    )
    assert prefix != other_prefix

    # test avec rule et sigma qui diffèrent
    other_prefix = Prefix(
        rule="a+X",
        sigma=frozendict(),
        phonology=phonology
    )
    assert prefix != other_prefix


def test_prefix_type_error() -> None:
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
        Prefix(
            rule="",
            sigma=frozendict(),
            phonology=phonology
        )

    with pytest.raises(TypeError):
        Prefix(
            rule="hHPJLK",
            sigma=frozendict(),
            phonology=phonology
        )


def test_get_sigma() -> None:
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
    prefix = Prefix(
        rule="d+X",
        sigma=frozendict(Genre="m"),
        phonology=phonology
    )
    assert prefix.get_sigma() == frozendict(Genre="m")


def test_get_rule() -> None:
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
    prefix = Prefix(
        rule="d+X",
        sigma=frozendict(Genre="m"),
        phonology=phonology
    )
    assert prefix.get_rule().string == "d+X"


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
    prefix = Prefix(
        rule="d+X",
        sigma=frozendict(Genre="m"),
        phonology=phonology
    )

    with pytest.raises(NotImplementedError):
        _ = prefix.to_string(None) == "d+X"

    assert prefix.to_string(StemSpace(("toto",))) == "dtoto"

    assert prefix.to_string("toto") == "dtoto"
