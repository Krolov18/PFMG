import pytest
from frozendict import frozendict

from pfmg.lexique.morpheme.Prefix import Prefix
from pfmg.lexique.morpheme.Suffix import Suffix
from pfmg.lexique.morpheme import Circumfix
from pfmg.lexique.morpheme.Condition import Condition
from pfmg.lexique.morpheme.Selection import Selection
from pfmg.lexique.morpheme.Gabarit import Gabarit
from pfmg.lexique.morpheme.Factory import create_morpheme
from pfmg.lexique.phonology.Phonology import Phonology
from pfmg.lexique.stem_space.StemSpace import StemSpace


@pytest.mark.parametrize("rule, sigma, expected_type", [
    ("a+X", frozendict(), Prefix),
    ("X+a", frozendict(), Suffix),
    ("s+X+a", frozendict(), Circumfix),
    ("4U55e6V6", frozendict(), Gabarit),
    ("X1", frozendict(), Selection),
    ("X2?X2:X1", frozendict(), Condition),
])
def test_prefix(rule, sigma, expected_type) -> None:
    phonology = Phonology(
        apophonies=frozendict(Ø="i", i="a", a="u", u="u", e="o", o="o"),
        mutations=frozendict(p="p", t="p", k="t", b="p", d="b",
                             g="d", m="m", n="m", N="n", f="f",
                             s="f", S="s", v="f", z="v", Z="z",
                             r="w", l="r", j="w", w="w"),
        derives=frozendict(A="V", D="C"),
        consonnes=frozenset("ptkbdgmnNfsSvzZrljw"),
        voyelles=frozenset("iueoa"))
    actual = create_morpheme(
        rule=rule,
        sigma=sigma,
        phonology=phonology
    )
    assert isinstance(actual, expected_type)


@pytest.mark.parametrize("rule, sigma, expected_type", [
    ("", frozendict(), None),
    ("REGLE_INCOMPRISE", frozendict(), None),
])
def test_prefix_error(rule, sigma, expected_type) -> None:
    phonology = Phonology(
        apophonies=frozendict(Ø="i", i="a", a="u", u="u", e="o", o="o"),
        mutations=frozendict(p="p", t="p", k="t", b="p", d="b",
                             g="d", m="m", n="m", N="n", f="f",
                             s="f", S="s", v="f", z="v", Z="z",
                             r="w", l="r", j="w", w="w"),
        derives=frozendict(A="V", D="C"),
        consonnes=frozenset("ptkbdgmnNfsSvzZrljw"),
        voyelles=frozenset("iueoa"))
    with pytest.raises(TypeError):
        _ = create_morpheme(
            rule=rule,
            sigma=sigma,
            phonology=phonology
        )


@pytest.mark.parametrize("rule, sigma, stems, expected", [
    ("a+X", frozendict(), ("truc",), "atruc"),
    ("X+a", frozendict(), ("truc",), "truca"),
    ("s+X+a", frozendict(), ("truc",), "struca"),
    ("4U55e6V6", frozendict(), ("trup",), "puwwepup"),
    ("4U55Ae6V6", frozendict(), ("lvup",), "ruffuepup"),
    ("7U88e9V9", frozendict(), ("tvup",), "puffepup"),
    ("X1", frozendict(), ("truc",), "truc"),
    ("X2?X2:X1", frozendict(), ("truc",), "truc"),
    ("X2?X2:X1", frozendict(), ("truc", "machin"), "machin"),
])
def test_to_string_stemspace(rule, sigma, stems, expected) -> None:
    phonology = Phonology(
        apophonies=frozendict(Ø="i", i="a", a="u", u="u", e="o", o="o"),
        mutations=frozendict(p="p", t="p", k="t", b="p", d="b",
                             g="d", m="m", n="m", N="n", f="f",
                             s="f", S="s", v="f", z="v", Z="z",
                             r="w", l="r", j="w", w="w"),
        derives=frozendict(A="V", D="C"),
        consonnes=frozenset("ptkbdgmnNfsSvzZrljw"),
        voyelles=frozenset("iueoa"))
    actual = create_morpheme(
        rule=rule,
        sigma=sigma,
        phonology=phonology
    )
    assert actual.to_string(StemSpace(stems=stems)) == expected


@pytest.mark.parametrize("rule, sigma, stems, expected", [
    ("a+X", frozendict(), "truc", "atruc"),
    ("X+a", frozendict(), "truc", "truca"),
    ("s+X+a", frozendict(), "truc", "struca")
])
def test_to_string_str(rule, sigma, stems, expected) -> None:
    phonology = Phonology(
        apophonies=frozendict(Ø="i", i="a", a="u", u="u", e="o", o="o"),
        mutations=frozendict(p="p", t="p", k="t", b="p", d="b",
                             g="d", m="m", n="m", N="n", f="f",
                             s="f", S="s", v="f", z="v", Z="z",
                             r="w", l="r", j="w", w="w"),
        derives=frozendict(A="V", D="C"),
        consonnes=frozenset("ptkbdgmnNfsSvzZrljw"),
        voyelles=frozenset("iueoa"))
    actual = create_morpheme(
        rule=rule,
        sigma=sigma,
        phonology=phonology
    )
    assert actual.to_string(stems) == expected


@pytest.mark.parametrize("rule, sigma, stems, expected", [
    ("a+X", frozendict(), None, "atruc"),
    ("X+a", frozendict(), None, "truca"),
    ("s+X+a", frozendict(), None, "struca"),
    ("4U55e6V6", frozendict(), None, "puwwepup"),
    ("X1", frozendict(), None, "truc"),
    ("X2?X2:X1", frozendict(), None, "truc"),
])
def test_to_string_none_not_implemented_error(
        rule,
        sigma,
        stems,
        expected
) -> None:
    phonology = Phonology(
        apophonies=frozendict(Ø="i", i="a", a="u", u="u", e="o", o="o"),
        mutations=frozendict(p="p", t="p", k="t", b="p", d="b",
                             g="d", m="m", n="m", N="n", f="f",
                             s="f", S="s", v="f", z="v", Z="z",
                             r="w", l="r", j="w", w="w"),
        derives=frozendict(A="V", D="C"),
        consonnes=frozenset("ptkbdgmnNfsSvzZrljw"),
        voyelles=frozenset("iueoa"))
    actual = create_morpheme(
        rule=rule,
        sigma=sigma,
        phonology=phonology
    )
    with pytest.raises(NotImplementedError):
        _ = actual.to_string(stems)
