import pytest
from frozendict import frozendict

from pfmg.lexique.morpheme.Selection import Selection
from pfmg.lexique.phonology.Phonology import Phonology
from pfmg.lexique.stem_space.StemSpace import StemSpace


@pytest.mark.parametrize("rule, expected, sigma", [
    ("X1", ("1",), frozendict(Genre="m")),
])
def test_selection(rule, expected, sigma) -> None:
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
    selection = Selection(
        rule=rule,
        sigma=sigma,
        phonology=phonology
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
        phonology=phonology
    )
    assert selection == other_selection

    # test avec le sigma qui diffère
    other_selection = Selection(
        rule=rule,
        sigma=frozendict(Genre="f"),
        phonology=phonology
    )
    assert selection != other_selection

    # test avec le rule qui diffère
    other_selection = Selection(
        rule="X2",
        sigma=sigma,
        phonology=phonology
    )
    assert selection != other_selection

    # test avec rule et sigma qui diffèrent
    other_selection = Selection(
        rule="X2",
        sigma=frozendict(),
        phonology=phonology
    )
    assert selection != other_selection


def test_selection_type_error() -> None:
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
        Selection(
            rule="",
            sigma=frozendict(),
            phonology=phonology
        )

    with pytest.raises(TypeError):
        Selection(
            rule="hHPJLK",
            sigma=frozendict(),
            phonology=phonology
        )


def test_selection_to_string_not_implemented_error() -> None:
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
    with (pytest.raises(NotImplementedError)):
        Selection(
            rule="X1",
            sigma=frozendict(),
            phonology=phonology
        ).to_string("")
    with pytest.raises(NotImplementedError):
        Selection(
            rule="X1",
            sigma=frozendict(),
            phonology=phonology
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
def test_selection_to_string(rule, stem_space, expected) -> None:
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
    selection = Selection(
        rule=rule,
        sigma=frozendict(),
        phonology=phonology
    )

    assert selection.to_string(StemSpace(stem_space)) == expected


def test_selection_to_string_index_error() -> None:
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
    selection = Selection(
        rule="X2",
        sigma=frozendict(),
        phonology=phonology
    )

    with pytest.raises(IndexError):
        selection.to_string(StemSpace(()))

    with pytest.raises(IndexError):
        selection.to_string(StemSpace(("X1",)))


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

    sigma = frozendict()
    selection = Selection(
        rule="X2",
        sigma=sigma,
        phonology=phonology
    )
    assert selection.get_sigma() == sigma
    assert selection.get_sigma() is sigma

    sigma = frozendict(Genre="f")
    selection = Selection(
        rule="X2",
        sigma=sigma,
        phonology=phonology
    )
    assert selection.get_sigma() == sigma
    assert selection.get_sigma() is sigma


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

    rule = "X2"
    selection = Selection(
        rule=rule,
        sigma=frozendict(),
        phonology=phonology
    )
    assert selection.get_rule().string == rule

    rule = "X1"
    selection = Selection(
        rule=rule,
        sigma=frozendict(Genre="f"),
        phonology=phonology
    )
    assert selection.get_rule().string == rule
