import pytest
from frozendict import frozendict

from lexique.realizer import realize_lexeme, realize_forme
from lexique.ruler import ruler_suffix, ruler_radical
from lexique.structures import Lexeme, Paradigm, Forme, Phonology


@pytest.mark.parametrize("lexeme, paradigm, expected", [
    (Lexeme(stem="banane", pos="N", sigma=frozendict(Genre="m"), traduction=None),
     Paradigm(gloses={"N": [frozendict(Genre="m", Nombre="sg"), frozendict(Genre="m", Nombre="pl"),
                            frozendict(Genre="f", Nombre="sg"), frozendict(Genre="f", Nombre="pl")]},
              blocks={"N": [[ruler_suffix(rule="X+s", sigma=frozendict(Nombre="pl"))]]}),
     [Forme(pos="N", morphemes=[ruler_radical(rule="", sigma=frozendict(Genre="m", Nombre="sg"), stems="banane")],
            sigma=frozendict(Genre="m", Nombre="sg"), traduction=None),
      Forme(pos="N", morphemes=[ruler_suffix(rule="X+s", sigma=frozendict(Nombre="pl"))],
            sigma=frozendict(Genre="m", Nombre="pl"), traduction=None)])
])
def test_realize_lexeme(lexeme, paradigm, expected) -> None:
    actual = realize_lexeme(lexeme, paradigm)
    for i_idx in range(len(actual)):
        assert actual[i_idx].pos == expected[i_idx].pos
        for j_idx in range(len(actual[i_idx].morphemes)):
            assert actual[i_idx].morphemes[j_idx].rule.string == expected[i_idx].morphemes[j_idx].rule.string
        assert actual[i_idx].sigma == expected[i_idx].sigma
        assert actual[i_idx].traduction == expected[i_idx].traduction


@pytest.mark.parametrize("forme, phonology, expected", [
    (Forme(pos="N", morphemes=[ruler_radical(rule="",
                                             sigma=frozendict(Genre="m",
                                                              Nombre="sg"),
                                             stems="banane")],
           sigma=frozendict(Genre="m", Nombre="sg"),
           traduction=None),
     Phonology(consonnes=frozenset("zrtpmkl"),
               voyelles=frozenset("aeiou"),
               mutations=frozendict(a="b"),
               derives=frozendict(a="b"),
               apophonies=frozendict(a="b")),
     "banane")
])
def test_realize_forme(forme, phonology, expected):
    actual = realize_forme(forme, phonology)
    assert actual == expected
