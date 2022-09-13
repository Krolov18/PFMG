import re
from typing import Callable, Literal

import pytest
import yaml
from frozendict import frozendict  # type: ignore

from lexique import get_lexique_path
from lexique import etl
from lexique.realizer import realize
from lexique.ruler import ruler
from lexique.structures import Prefix, Suffix, Circumfix, Radical, Forme, Lexeme, Phonology


@pytest.fixture()
def fx_phonology() -> Phonology:
    with open("/home/korantin/Documents/Kalaba/lexique/data/kalaba/2/Phonology.yaml") as f:
        data = yaml.load(f, yaml.Loader)
        return Phonology(
            frozendict(data["apophonies"]),
            frozendict(data["derives"]),
            frozendict(data["mutations"]),
            frozenset(data["consonnes"]),
            frozenset(data["voyelles"]),
        )


@pytest.fixture(scope="module")
def fx_gloses2() -> tuple[dict[Literal["source", "destination"], frozendict],
                          dict[Literal["source", "destination"], frozendict]]:
    with open(f"{get_lexique_path()}/test/data_for_test/avec_traduction/Gloses.yaml", mode="r", encoding="utf8") as f:
        load = yaml.load(f, Loader=yaml.Loader)
        return etl.read_glose(glose=load)


@pytest.fixture(scope="module")
def fx_blocks2(fx_gloses2) -> dict[str, dict]:
    with open(f"{get_lexique_path()}/test/data_for_test/avec_traduction/Blocks.yaml") as f:
        return etl.read_blocks(data=yaml.load(f, Loader=yaml.Loader),
                               att_vals=fx_gloses2[1],
                               voyelles=frozenset())


@pytest.fixture()
def fx_paradigm2(fx_gloses2, fx_blocks2) -> dict[str, dict[frozendict, Callable[[Lexeme], Forme]]]:
    return etl.build_paradigm(glose=fx_gloses2[0],
                              blocks=fx_blocks2)


@pytest.mark.parametrize("term, accumulator, expected", [
    (Prefix(rule=re.compile(r"(\w+)\+X").fullmatch("e+X"), sigma=frozendict({"genre": "m"})),
     "qqch",
     "eqqch"),
    (Suffix(rule=re.compile(r"X\+(\w+)").fullmatch("X+e"), sigma=frozendict({"genre": "m"})),
     "qqch",
     "qqche"),
    (Circumfix(rule=re.compile(r"(\w+)\+X\+(\w+)").fullmatch("e+X+e"), sigma=frozendict({"genre": "m"})),
     "qqch",
     "eqqche"),
    # (Gabarit(rule=re.compile(r"(\w+)\+X\+(\w+)").fullmatch("e+X+e"), sigma=frozendict()), "", ""),
    (Radical(stem="banane", rule=None, sigma=frozendict()), "", "banane"),

    (Radical(stem=("banane",), rule=None, sigma=frozendict()), "", "banane"),

    (Radical(stem=("banane", "bananes"), rule=None, sigma=frozendict()), "", ("banane", "bananes")),

    (Forme(pos="N",
           morphemes=[
               Radical(stem=("qqch",), rule=None, sigma=frozendict()),
               Prefix(rule=re.compile(r"(\w+)\+X").fullmatch("i+X"), sigma=frozendict({"genre": "m"})),
               Prefix(rule=re.compile(r"(\w+)\+X").fullmatch("a+X"), sigma=frozendict({"genre": "m"})),
               Circumfix(rule=re.compile(r"(\w+)\+X\+(\w+)").fullmatch("e+X+e"), sigma=frozendict({"genre": "m"}))],
           sigma=frozendict(), traduction=None),
     None,
     "eaiqqche"),

    # (Lexeme(stem="banane", pos="N", sigma=frozendict(), traduction=None)),
    # (Lexeme(stem="banane", pos="N", sigma=frozendict(), traduction=Lexeme(stem=,pos=,sigma=,traduction=))),
    #
    # (Lexeme(stem=("banane",), pos="N", sigma=frozendict(), traduction=None)),
    # (Lexeme(stem=("banane",), pos="N", sigma=frozendict(), traduction=)),
    #
    # (Lexeme(stem=("banane", "bananes"), pos="N", sigma=frozendict(), traduction=None)),
    # (Lexeme(stem=("banane", "bananes"), pos="N", sigma=frozendict(), traduction=)),
])
def test_realize_(phonology, term, accumulator, expected) -> None:
    actual = realize(term=term, accumulator=accumulator, phonology=phonology)
    assert actual == expected


@pytest.mark.skipif(reason="le paradigme n'a pas de restriction, du coup la combinatoire est trop grande pour le test")
@pytest.mark.parametrize("term, expected", [
    (Lexeme(stem=("petit",), pos="ADJ", sigma=frozendict(),
            traduction=Lexeme(stem="petit", pos="ADJ", sigma=frozendict(), traduction=None)),
     ['petitiv', 'petitav', 'petitov', 'petitif', 'petitaf', 'petitof', 'petitid', 'petitad', 'petitod', 'petitik',
      'petitak', 'petitok', 'petitom', 'petitam', 'petitim', 'petitov', 'petitav', 'petitiv', 'petitot', 'petitat',
      'petitit', 'petitog', 'petitag', 'petitig']),

    (Lexeme(stem=("petit",), pos="ADJ", sigma=frozendict({"Genre": "A"}),
            traduction=Lexeme(stem="petit", pos="ADJ", sigma=frozendict(), traduction=None)),
     ['petitiv', 'petitav', 'petitov', 'petitom', 'petitam', 'petitim']),

    (Lexeme(stem=("épousailles",), pos="N", sigma=frozendict({"Genre": "B", "Nombre": "Pl"}),
            traduction=Lexeme(stem="petit", pos="ADJ", sigma=frozendict(), traduction=None)),
     ['reposowula', 'boposowula', 'koposowula', 'liposowula']),
])
def test_realize_lexeme(fx_paradigm2, phonology, term, expected) -> None:
    actual = realize(term=term, paradigm=fx_paradigm2)
    assert [realize(term=forme, phonology=phonology) for forme in actual] == expected


@pytest.mark.parametrize("forme", [
    Forme(pos='N',
          morphemes=[Radical(rule=None, sigma=frozendict(), stem=("padaN",)),
                     ruler(rule="1a4A2V3e", sigma=frozendict({'nombre': 'sg'}), voyelles=frozenset("aeiou"))],
          sigma=frozendict({'genre': 'm', 'nombre': 'sg', 'þgenre': 'þm', 'þnombre': 'þsg'}),
          traduction=Forme(pos='N',
                           morphemes=[Radical(rule=None, sigma=frozendict({'genre': 'f'}), stem=('plaine',))],
                           sigma=frozendict({'genre': 'm', 'nombre': 'sg', 'þgenre': 'þm', 'þnombre': 'þsg'}),
                           traduction=None))
])
def test_realize(forme, fx_phonology) -> None:
    assert realize(term=forme, phonology=fx_phonology) == "papudaNe"
    assert realize(term=forme.traduction, phonology=fx_phonology) == "plaine"
