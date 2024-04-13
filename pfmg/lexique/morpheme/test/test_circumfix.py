import pytest
from frozendict import frozendict

from pfmg.lexique.morpheme.Circumfix import Circumfix
from pfmg.lexique.phonology.Phonology import Phonology
from pfmg.lexique.stem_space.StemSpace import StemSpace


@pytest.mark.parametrize("rule, expected, sigma", [
    # test avec un rule vide
    ("", frozendict(Genre="m"), None),
    # test avec un rule qui ne contient pas de +X+
    ("hHPJLK", frozendict(Genre="m"), None),
])
def test_circumfix_error(rule, expected, sigma) -> None:
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
        _ = Circumfix(
            rule=rule,
            sigma=sigma,
            phonology=phonology
        )


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
    circumfix = Circumfix(
        rule="a+X+d",
        sigma=frozendict(Genre="m"),
        phonology=phonology
    )

    assert circumfix.get_rule().string == "a+X+d"
    assert circumfix.get_rule().groups() == ("a", "d")
    assert circumfix.get_rule().group(1) == "a"
    assert circumfix.get_rule().group(2) == "d"


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
    circumfix = Circumfix(
        rule="a+X+d",
        sigma=frozendict(Genre="m"),
        phonology=phonology
    )

    assert circumfix.get_sigma() == frozendict(Genre="m")


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
    circumfix = Circumfix(
        rule="a+X+d",
        sigma=frozendict(Genre="m"),
        phonology=phonology
    )

    assert str(circumfix) == "Circumfix(rule=a+X+d, sigma=frozendict({'Genre': 'm'}))"


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
    circumfix = Circumfix(
        rule="a+X+d",
        sigma=frozendict(Genre="m"),
        phonology=phonology
    )

    assert circumfix.to_string("toto") == "atotod"

    with pytest.raises(NotImplementedError):
        _ = circumfix.to_string(None)

    actual = circumfix.to_string(StemSpace(("toto", "tata")))
    assert actual == "atotod"


def test_equal() -> None:
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

    circumfix = Circumfix(
        rule="a+X+d",
        sigma=frozendict(Genre="m"),
        phonology=phonology
    )
    other_circumfix = Circumfix(
        rule="a+X+d",
        sigma=frozendict(Genre="m"),
        phonology=phonology
    )
    assert circumfix == other_circumfix

    other_circumfix = Circumfix(
        rule="a+X+d",
        sigma=frozendict(Genre="f"),
        phonology=phonology
    )
    assert circumfix != other_circumfix

    other_circumfix = Circumfix(
        rule="a+X+t",
        sigma=frozendict(Genre="m"),
        phonology=phonology
    )
    assert circumfix != other_circumfix
