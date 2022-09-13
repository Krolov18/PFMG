# pylint: disable=missing-module-docstring,line-too-long,missing-function-docstring
import pytest
from frozendict import frozendict

from lexique.syntax import develop, repeat, cleave
from lexique.etl import read_rules


@pytest.mark.parametrize("term", [
    "",
    "PP{",
    "PP}",
    "PP{}",  # Dans une regex classique, c'est valide, mais ne mène à rien. Permissif !
    "PP/{}",
    "PP/{,}",
    "PP/{2,}",  # Équivalent en regex : 2 ou plus. L'infini est permissif !
])
def test_syntax_assertions(term) -> None:
    with pytest.raises(AssertionError):
        _ = repeat(term)


@pytest.mark.parametrize("term", [
    "PP/*",  # Équivalent en regex 0 ou plus. L'infini est permissif.
    "PP/+",  # Équivalent en regex 1 ou plus. L'infini est permissif.
])
def test_syntax_raising(term) -> None:
    with pytest.raises(NotImplementedError):
        _ = repeat(term)


@pytest.mark.parametrize("term, expected", [
    ("VER", [["VER"]]),
    ("PP/?", [[""], ["PP"]]),
    ("PP/{,0}", [[""]]),
    ("PP/{,1}", [[""], ["PP"]]),
    ("PP/{,2}", [[""], ["PP"], ["PP", "PP"]]),
    ("PP/{0,2}", [[""], ["PP"], ["PP", "PP"]]),
    ("PP/{1,2}", [["PP"], ["PP", "PP"]]),
    ("PP/{2,2}", [["PP", "PP"]]),
    ("PP/{0, 2}", [[""], ["PP"], ["PP", "PP"]]),
    ("PP/{0 ,2}", [[""], ["PP"], ["PP", "PP"]]),
    ("PP/{0 , 2}", [[""], ["PP"], ["PP", "PP"]]),
    ("PP/{, 2}", [[""], ["PP"], ["PP", "PP"]]),
    ("PP/{0,1}", [[""], ["PP"]]),
    ("PP/{0 ,1}", [[""], ["PP"]]),
    ("PP/{0, 1}", [[""], ["PP"]]),
    ("PP/{0 , 1}", [[""], ["PP"]]),
    ("PP/{ 0,1 }", [[""], ["PP"]]),
])
def test_syntax(term, expected):
    actual = repeat(term)
    assert actual == expected


@pytest.mark.parametrize("term, expected", [
    (["PP/{,2}", "NP", "PP/{,2}", "VER"],
     [["", "NP", "", "VER"],  # 0 0
      ["", "NP", "PP", "VER"],  # 0 1
      ["", "NP", "PP", "PP", "VER"],  # 0 2
      ["PP", "NP", "", "VER"],  # 1 0
      ["PP", "NP", "PP", "VER"],  # 1 1
      ["PP", "NP", "PP", "PP", "VER"],  # 1 2
      ["PP", "PP", "NP", "", "VER"],  # 2 0
      ["PP", "PP", "NP", "PP", "VER"],  # 2 1
      ["PP", "PP", "NP", "PP", "PP", "VER"]]),  # 2 2

    ([["PP/{,2}", "NP", "PP/{,2}", "VER"]],
     [["", "NP", "", "VER"],
      ["", "NP", "PP", "VER"],
      ["", "NP", "PP", "PP", "VER"],
      ["PP", "NP", "", "VER"],
      ["PP", "NP", "PP", "VER"],
      ["PP", "NP", "PP", "PP", "VER"],
      ["PP", "PP", "NP", "", "VER"],
      ["PP", "PP", "NP", "PP", "VER"],
      ["PP", "PP", "NP", "PP", "PP", "VER"]]),
])
def test_develop(term, expected) -> None:
    actual = list(develop(term))
    assert actual == expected


# @pytest.mark.parametrize("word, morphosyntax, expected", [
#     ("Des",
#      MorphoSyntax(contractions=frozendict({"Des": ["de", "les"]}),
#                   start="", syntagmes=dict(), accords=dict(),
#                   percolations=dict(), traductions=dict()),
#      ["de", "les"]),
#     (["Des", "mots"],
#      MorphoSyntax(contractions=frozendict({"Des": ["de", "les"]}),
#                   start="", syntagmes=dict(), accords=dict(),
#                   percolations=dict(), traductions=dict()),
#      ["de", "les", "mots"]),
#     ([["Des", "mots"], ["Des", "mots"]],
#      MorphoSyntax(contractions=frozendict({"Des": ["de", "les"]}),
#                   start="", syntagmes=dict(), accords=dict(),
#                   percolations=dict(), traductions=dict()),
#      [["de", "les", "mots"], ["de", "les", "mots"]]),
# ])
# def test_cleave(word, morphosyntax, expected) -> None:
#     assert cleave(word, morphosyntax) == expected
