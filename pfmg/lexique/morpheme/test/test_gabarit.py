# Copyright (c) <year>, <copyright holder>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. 
import pytest
from frozendict import frozendict

from pfmg.lexique.morpheme.Gabarit import Gabarit
from pfmg.lexique.phonology.Phonology import Phonology
from pfmg.lexique.stem_space.StemSpace import StemSpace


@pytest.mark.parametrize("rule, expected, sigma", [
    ("1111", ("1111",), frozendict(Genre="m")),
    ("2222", ("2222",), frozendict(Genre="m")),
    ("VVVV", ("VVVV",), frozendict(Genre="m")),
    ("2V49", ("2V49",), frozendict(Genre="m")),
    ("4U55e6V6", ("4U55e6V6",), frozendict(Genre="m")),
])
def test_equal(rule, expected, sigma) -> None:
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
    gabarit = Gabarit(
        rule=rule,
        sigma=sigma,
        phonology=phonology
    )

    # test d'identité
    assert gabarit == gabarit

    # test d'égalité
    other_gabarit = Gabarit(
        rule=rule,
        sigma=sigma,
        phonology=phonology
    )
    assert gabarit == other_gabarit

    # test avec le sigma qui diffère
    other_gabarit = Gabarit(
        rule=rule,
        sigma=frozendict(Genre="f"),
        phonology=phonology
    )
    assert gabarit != other_gabarit

    # test avec le rule qui diffère
    other_gabarit = Gabarit(
        rule="5V44aV66",
        sigma=sigma,
        phonology=phonology
    )
    assert gabarit != other_gabarit

    # test avec rule et sigma qui diffèrent
    other_gabarit = Gabarit(
        rule="5V44aV66",
        sigma=frozendict(),
        phonology=phonology
    )
    assert gabarit != other_gabarit


def test_suffix_typeerror() -> None:
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
        _ = Gabarit( 
            rule=1,  # type: ignore reportArgumentType
            sigma=frozendict(),
            phonology=phonology 
        )

    with pytest.raises(TypeError):
        _ = Gabarit(
            rule="1",
            sigma=1,  # type: ignore reportArgumentType
            phonology=phonology
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
            phonology=phonology
        )

    with pytest.raises(TypeError):
        _ = Gabarit(
            rule="hHPJLK",
            sigma=frozendict(Genre="m"),
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

    # rule avec 'V'
    gabarit = Gabarit(
        rule="5V44aV66",
        sigma=frozendict(Genre="m"),
        phonology=phonology
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
        phonology=phonology
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
        phonology=phonology
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
        phonology=phonology
    )

    with pytest.raises(NotImplementedError):
        assert gabarit.to_string(None)

    with pytest.raises(NotImplementedError):
        assert gabarit.to_string("truc")

    actual = gabarit.to_string(StemSpace(stems=("truk",)))
    expected = "wuppautw"
    assert actual == expected


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

    gabarit = Gabarit(
        rule="5A44aV66",
        sigma=frozendict(Genre="m"),
        phonology=phonology
    )
    actual = repr(gabarit)
    assert actual == "Gabarit(5A44aV66)"
