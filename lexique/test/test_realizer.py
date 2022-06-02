import re
from typing import Dict, List, Tuple, Callable

import pytest
import yaml
from frozendict import frozendict
from multimethod import DispatchError

from lexique import get_lexique_path
from lexique.etl import read_glose, TypeBlocks, build_paradigm, read_blocks
from lexique.realizer import realize
from lexique.ruler import ruler
from lexique.structures import Prefix, Suffix, Circumfix, Radical, Forme, Lexeme, Phonology


@pytest.fixture()
def fx_phonology() -> Phonology:
    with open("/home/korantin/PycharmProjects/Kalaba/lexique/data/kalaba/2/Phonology.yaml") as f:
        data = yaml.load(f, yaml.Loader)
        return Phonology(
            frozendict(data["apophonies"]),
            frozendict(data["derives"]),
            frozendict(data["mutations"]),
            frozenset(data["consonnes"]),
            frozenset(data["voyelles"]),
        )


@pytest.fixture(scope="module")
def fx_gloses2() -> Tuple[Dict[str, List[frozendict]], frozendict]:
    with open(f"{get_lexique_path()}/test/data_for_test/avec_traduction/Gloses.yaml", mode="r", encoding="utf8") as f:
        load = yaml.load(f, Loader=yaml.Loader)
        return read_glose(glose=load)


@pytest.fixture(scope="module")
def fx_blocks2(fx_gloses2) -> Dict[str, Dict[str, TypeBlocks]]:
    with open(f"{get_lexique_path()}/test/data_for_test/avec_traduction/Blocks.yaml") as f:
        return read_blocks(data=yaml.load(f, Loader=yaml.Loader), att_vals=fx_gloses2[1])


@pytest.fixture()
def fx_paradigm2(fx_gloses2, fx_blocks2) -> Dict[str, Dict[frozendict, Callable[[Lexeme], Forme]]]:
    return build_paradigm(fx_gloses2[0], fx_blocks2)


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
    (Radical(stem=("banane",), rule=None, sigma=frozendict()),
     "",
     ("banane",)),
    (Forme(pos="N",
           morphemes=[
               Radical(stem=("qqch",), rule=None, sigma=frozendict()),
               Prefix(rule=re.compile(r"(\w+)\+X").fullmatch("i+X"), sigma=frozendict({"genre": "m"})),
               Prefix(rule=re.compile(r"(\w+)\+X").fullmatch("a+X"), sigma=frozendict({"genre": "m"})),
               Circumfix(rule=re.compile(r"(\w+)\+X\+(\w+)").fullmatch("e+X+e"), sigma=frozendict({"genre": "m"}))],
           sigma=frozendict(), traduction=None),
     None,
     "eaiqqche"),
])
def test_realize_(phonology, term, accumulator, expected) -> None:
    try:
        actual = realize(term, accumulator, phonology)
    except DispatchError:
        try:
            actual = realize(term, accumulator)
        except DispatchError:
            try:
                actual = realize(term, phonology)
            except DispatchError:
                actual = realize(term)
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
    actual = realize(term, fx_paradigm2)
    assert [realize(forme, phonology) for forme in actual] == expected


@pytest.mark.parametrize("forme", [Forme(pos='N',
                                         morphemes=[Radical(rule=None,
                                                            sigma=frozendict(),
                                                            stem=("padaN",)),
                                                    ruler(id_ruler="gabarit",
                                                          rule="1a4A2V3e",
                                                          sigma=frozendict({'nombre': 'sg'}))],
                                         sigma=frozendict({'genre': 'm', 'nombre': 'sg',
                                                           'þgenre': 'þm', 'þnombre': 'þsg'}),
                                         traduction=Forme(pos='N',
                                                          morphemes=[Radical(rule=None,
                                                                             sigma=frozendict({'genre': 'f'}),
                                                                             stem=('plaine',))],
                                                          sigma=frozendict({'genre': 'm', 'nombre': 'sg',
                                                                            'þgenre': 'þm', 'þnombre': 'þsg'}),
                                                          traduction=None))])
def test_realize(forme, fx_phonology) -> None:
    assert realize(forme, fx_phonology) == "papudaNe"
    assert realize(forme.traduction, fx_phonology) == ("plaine",)
