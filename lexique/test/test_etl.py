# pylint: disable=line-too-long,missing-module-docstring,missing-function-docstring
import re
from typing import List, Dict, Tuple

import pytest
import yaml
from frozendict import frozendict  # type: ignore

# from lexique import get_lexique_path
from lexique import get_lexique_path
from lexique.errors import Errors
from lexique.etl import (_read_blocks, read_glose, read_stems, read_phonology, read_traduction,
                         read_rules, read_blocks, TypeBlocks, split, build_paradigm)
from lexique.realizer import realize

from lexique.structures import Suffix, Lexeme, Phonology, MorphoSyntax


def test_read_glose_errors() -> None:
    with pytest.raises(ValueError):
        _ = read_glose({})


@pytest.mark.parametrize("glose, expected", [
    ({"source": {"N": {"genre": ["m", "f"]}},
      "destination": {"N": {"genre": ["m", "f"]}}},
     ({"source": {"N": [frozendict({"genre": "m"}), frozendict({"genre": "f"})]},
       "destination": {"N": [frozendict({"genre": "m"}), frozendict({"genre": "f"})]}},
      frozendict({"source": frozendict({"N": "pos", "m": "genre", "f": "genre"}),
                  "destination": frozendict({"N": "pos", "m": "genre", "f": "genre"})}))),

    ({"source": {"N": {"genre": ["m", "f"], "nombre": ["sg", "pl"]}},
      "destination": {"N": {"genre": ["m", "f"], "nombre": ["sg", "pl"]}}},
     ({"source": {"N": [{"genre": "m", "nombre": "sg"}, {"genre": "m", "nombre": "pl"},
                        {"genre": "f", "nombre": "sg"}, {"genre": "f", "nombre": "pl"}]},
       "destination": {"N": [{"genre": "m", "nombre": "sg"}, {"genre": "m", "nombre": "pl"},
                             {"genre": "f", "nombre": "sg"}, {"genre": "f", "nombre": "pl"}]}},
      {"source": frozendict({"N": "pos", "m": "genre", "f": "genre", "sg": "nombre", "pl": "nombre"}),
       "destination": frozendict({"N": "pos", "m": "genre", "f": "genre", "sg": "nombre", "pl": "nombre"})})),

    ({"source": {"V": [{"Mode": ["Inf"]}, {"Nombre": ["Sg", "Pl"]}]},
      "destination": {"V": [{"Mode": ["Inf"]}, {"Nombre": ["Sg", "Pl"]}]}},
     ({"source": {"V": [frozendict(Mode="Inf"), frozendict(Nombre="Sg"), frozendict(Nombre="Pl")]},
       "destination": {"V": [frozendict(Mode="Inf"), frozendict(Nombre="Sg"), frozendict(Nombre="Pl")]}},
      {"source": frozendict(Sg="Nombre", Pl="Nombre", Inf="Mode", V="pos"),
       "destination": frozendict(Sg="Nombre", Pl="Nombre", Inf="Mode", V="pos")}))
])
def test_read_glose(glose, expected) -> None:
    actual_gloses, actual_att_vals = read_glose(glose)
    assert actual_gloses == expected[0]
    assert actual_att_vals == expected[1]


@pytest.mark.parametrize("blocks, att_vals, expected", [
    ({}, frozendict(), {}),
])
def test_read_blocks_empty(blocks, att_vals, expected) -> None:
    with pytest.raises(ValueError):
        _ = _read_blocks(blocks, att_vals, frozenset("iueoa"))


@pytest.mark.parametrize("blocks, att_vals, expected", [
    ({"N": {"1": {"genre=m": "X+e"}}},
     frozendict({"N": "pos", "m": "genre"}),
     {"N": [[Suffix(rule=re.compile(r"X\+(\w+)").fullmatch("X+e"), sigma=frozendict({"genre": "m"}))]]}),
])
def test_read_blocks(blocks, att_vals, expected) -> None:
    actual = _read_blocks(blocks, att_vals, frozenset("iueoa"))
    actual_blocks = list(actual.values())[0]
    expected_blocks = list(expected.values())[0]

    for actual_block, expected_block in zip(actual_blocks, expected_blocks):
        for actual_morpheme, expected_morpheme in zip(actual_block, expected_block):
            assert actual_morpheme.sigma == expected_morpheme.sigma
            assert actual_morpheme.rule.groups() == expected_morpheme.rule.groups()


@pytest.fixture(params=[{"source": {"ADJ": {"genre": ["m", "f"], "nombre": ["sg", "pl"]}},
                         "destination": {"ADJ": {"genre": ["m", "f"], "nombre": ["sg", "pl"]}}}])
def fx_gloses(request) -> Tuple[Dict[str, List[frozendict]], frozendict]:
    return read_glose(request.param)


@pytest.fixture(params=[{"source": {"ADJ": {"1": {"genre=f": "X+f"}}},
                         "destination": {"ADJ": {"1": {"genre=f": "X+e"},
                                                 "2": {"nombre=pl": "X+s"}}}}])
def fx_blocks(request, fx_gloses) -> Dict[str, Dict[str, TypeBlocks]]:
    _, att_vals = fx_gloses
    return read_blocks(request.param, att_vals, frozenset("iueoa"))


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


@pytest.fixture()
def fx_stem_file() -> Dict:
    with open(f"{get_lexique_path()}/test/data_for_test/avec_traduction/Stems.yaml", mode="r", encoding="utf8") as f:
        return yaml.load(f, Loader=yaml.Loader)


@pytest.mark.parametrize("stem,att_vals,expected", [
    ("Katisha", frozendict(), (("Katisha",), frozendict())),
    ("katiSa,katiSas", frozendict(), (("katiSa", "katiSas"), frozendict())),
    ("Katisha-1", frozendict({"1": "CF"}), (("Katisha",), frozendict({"CF": "1"}))),
    ("Katisha-1.F", frozendict({"1": "CF", "F": "Genre"}),
     (("Katisha",), frozendict({"CF": "1", "Genre": "F"}))),
    ("Katisha,Katishas-1.F", frozendict({"1": "CF", "F": "Genre"}),
     (("Katisha", "Katishas"), frozendict({"CF": "1", "Genre": "F"}))),
])
def test_read_traduction(stem, att_vals, expected) -> None:
    actual = read_traduction(stem=stem, att_vals=att_vals)
    assert actual == expected


@pytest.mark.parametrize("data, att_vals, expected", [

    ({"N": {"A": {"kalaba1": "français1"}}},
     frozendict({"source": {"N": "pos", "A": "genre"}, "destination": {"N": "pos"}}),
     [Lexeme(stem=("kalaba1",), pos="N", sigma=frozendict({"genre": "A"}),
             traduction=Lexeme(stem=("français1",), pos="N", sigma=frozendict({}), traduction=None))]),

    ({"N": {"A": {"paF": "balai"}}}, frozendict({"source": {"N": "pos", "A": "genre"}, "destination": {}}),
     [Lexeme(stem=("paF",), pos="N", sigma=frozendict({"genre": "A"}),
             traduction=Lexeme(stem=("balai",), pos="N", sigma=frozendict({}), traduction=None))]),

    ({"N": {"A": {"padaN": "plaine-1.F"}}},
     frozendict({"source": {"N": "pos", "A": "genre"}, "destination": {"N": "pos", "1": "CF", "F": "genre"}}),
     [Lexeme(stem=("padaN",), pos="N", sigma=frozendict({"genre": "A"}),
             traduction=Lexeme(stem=("plaine",), pos="N", sigma=frozendict({"CF": "1", "genre": "F"}),
                               traduction=None))]),

    ({"N": {"A": {"padaN": "plaine-1"}}},
     frozendict({"source": {"N": "pos", "A": "genre"}, "destination": {"N": "pos", "1": "CF"}}),
     [Lexeme(stem=("padaN",), pos="N", sigma=frozendict({"genre": "A"}),
             traduction=Lexeme(stem=("plaine",), pos="N", sigma=frozendict({"CF": "1"}),
                               traduction=None))]),

    ({"N": {"A": {"padaN": "plaine,plaines"}}},
     frozendict({"source": {"N": "pos", "A": "genre"}, "destination": {"N": "pos", "1": "CF", "F": "genre"}}),
     [Lexeme(stem=("padaN",), pos="N", sigma=frozendict({"genre": "A"}),
             traduction=Lexeme(stem=("plaine", "plaines"), pos="N", sigma=frozendict({}),
                               traduction=None))]),

    ({"N": {"A": {"padaN": "plaine,plaines-1.F"}}},
     frozendict({"source": {"N": "pos", "A": "genre"}, "destination": {"N": "pos", "1": "CF", "F": "genre"}}),
     [Lexeme(stem=("padaN",), pos="N", sigma=frozendict({"genre": "A"}),
             traduction=Lexeme(stem=("plaine", "plaines"), pos="N", sigma=frozendict({"CF": "1", "genre": "F"}),
                               traduction=None))]),

])
def test_read_stems(data, att_vals, expected) -> None:
    actual = [*read_stems(data=data, att_vals=att_vals, accumulator="")]
    assert actual == expected


@pytest.mark.parametrize("data, att_vals, message", [
    ({}, frozendict({"source": {}, "destination": {}}), re.escape(Errors.E013)),

    ({"N": {}}, frozendict({"source": {}, "destination": {}}), re.escape(Errors.E013)),

    ({"N": {"A": {}}}, frozendict({"source": {}, "destination": {}}), re.escape(Errors.E013)),

    ({"N": {"A": {"B": {}}}}, frozendict({"source": {}, "destination": {}}), re.escape(Errors.E013)),

    ({"": {}}, frozendict({"source": {"N": "pos", "A": "genre"}, "destination": {}}), re.escape(Errors.E012)),

    ({"N": {"A": {"toto": ""}}}, frozendict({"source": {"N": "pos", "A": "genre"}, "destination": {}}),
     re.escape(Errors.E012)),

    ({"N": {"A": {"": "toto"}}}, frozendict({"source": {"N": "pos", "A": "genre"}, "destination": {}}),
     re.escape(Errors.E012)),

    ({"N": {"A": {"paF": "balai2.M"}}},
     frozendict({"source": {"N": "pos", "A": "genre"}, "destination": {"N": "pos", "M": "genre", "2": "CF"}}),
     re.escape(Errors.E014)),

])
def test_read_stems_errors(data, att_vals, message) -> None:
    with pytest.raises(ValueError, match=message):
        _ = [*read_stems(data=data, att_vals=att_vals)]


@pytest.mark.parametrize("data", [
    {},
    {"unknown_key": []},
])
def test_read_phonology_errors(data) -> None:
    with pytest.raises((AssertionError, KeyError)):  # type: ignore
        _ = read_phonology(data)


@pytest.mark.parametrize("data, expected", [
    ({"apophonies": frozendict(),
      "derives": frozendict(),
      "mutations": frozendict(),
      "consonnes": frozenset(),
      "voyelles": frozenset()},
     Phonology(**{"apophonies": frozendict(),
                  "derives": frozendict(),
                  "mutations": frozendict(),
                  "consonnes": frozenset(),
                  "voyelles": frozenset()})),
    ({"apophonies": frozendict(a="e"),
      "derives": frozendict(z="r"),
      "mutations": frozendict(t="p"),
      "consonnes": frozenset("drftg"),
      "voyelles": frozenset("aeiou")},
     Phonology(**{"apophonies": frozendict(a="e"),
                  "derives": frozendict(z="r"),
                  "mutations": frozendict(t="p"),
                  "consonnes": frozenset("drftg"),
                  "voyelles": frozenset("aeiou")})),
])
def test_read_phonology(data, expected) -> None:
    actual = read_phonology(data)
    assert actual == expected


@pytest.mark.parametrize("morphosyntax, expected", [
    (MorphoSyntax(contractions=frozendict(),
                  start="NP",
                  syntagmes={"NP": [["DET", "N"]]},
                  accords={"NP": [[{"sGenre": "*", "sNombre": "*", "dGenre": "*", "dNombre": "*", "dCas": "*"},
                                   {"sGenre": "*", "sNombre": "*", "dGenre": "*", "dNombre": "*", "dCas": "*"}]]},
                  percolations={"NP": [{"sGenre": "*", "sNombre": "*", "dGenre": "*", "dNombre": "*", "dCas": "*"}]},
                  traductions={"NP": [[1, 0]]}),
     (["% start NP",
       "NP[Source=[Genre=?sgenre,Nombre=?snombre,Traduction=(?n+?det)],Destination=[Genre=?dgenre,Nombre=?dnombre,Cas=?dcas]] ->"
       " DET[Source=[Genre=?sgenre,Nombre=?snombre,Traduction=?det],Destination=[Genre=?dgenre,Nombre=?dnombre,Cas=?dcas]]"
       " N[Source=[Genre=?sgenre,Nombre=?snombre,Traduction=?n],Destination=[Genre=?dgenre,Nombre=?dnombre,Cas=?dcas]]"],
      ["% start NP",
       "NP[Genre=?dgenre,Nombre=?dnombre,Cas=?dcas] ->"
       " N[Genre=?dgenre,Nombre=?dnombre,Cas=?dcas]"
       " DET[Genre=?dgenre,Nombre=?dnombre,Cas=?dcas]"])),

    (MorphoSyntax(contractions=frozendict(),
                  syntagmes={"NP": [["deux", "N"]]},
                  start="NP",
                  accords={"NP": [[{}, {"sGenre": "*", "sNombre": "*", "dGenre": "*", "dNombre": "Du", "dCas": "*"}]]},
                  percolations={"NP": [{"sGenre": "*", "sNombre": "*", "dGenre": "*", "dNombre": "Du", "dCas": "*"}]},
                  traductions={"NP": [[1]]}),
     (["% start NP",
       "NP[Source=[Genre=?sgenre,Nombre=?snombre,Traduction=(?n)],Destination=[Genre=?dgenre,Nombre=Du,Cas=?dcas]] ->"
       " 'deux'"
       " N[Source=[Genre=?sgenre,Nombre=?snombre,Traduction=?n],Destination=[Genre=?dgenre,Nombre=Du,Cas=?dcas]]"],
      ["% start NP",
       "NP[Genre=?dgenre,Nombre=Du,Cas=?dcas] -> N[Genre=?dgenre,Nombre=Du,Cas=?dcas]"])),

    (MorphoSyntax(contractions=frozendict(),
                  syntagmes={"NP": [["DET", "deux", "ADJ/?", "N"]]},
                  start="NP",
                  accords={"NP": [[{"sGenre": "*", "sNombre": "*", "dGenre": "*", "dNombre": "Du", "dCas": "*"},
                                   {},
                                   {"sGenre": "*", "sNombre": "*", "dGenre": "*", "dNombre": "Du"},
                                   {"sGenre": "*", "sNombre": "*", "dGenre": "*", "dNombre": "Du", "dCas": "*"}]]},
                  percolations={"NP": [{"sGenre": "*", "sNombre": "*", "dGenre": "*", "dNombre": "Du", "dCas": "*"}]},
                  traductions={"NP": [[0, 2, 3]]}),
     (["% start NP",
       "NP[Source=[Genre=?sgenre,Nombre=?snombre,Traduction=(?det+?n)],Destination=[Genre=?dgenre,Nombre=Du,Cas=?dcas]] -> DET[Source=[Genre=?sgenre,Nombre=?snombre,Traduction=?det],Destination=[Genre=?dgenre,Nombre=Du,Cas=?dcas]] 'deux' N[Source=[Genre=?sgenre,Nombre=?snombre,Traduction=?n],Destination=[Genre=?dgenre,Nombre=Du,Cas=?dcas]]",
       "NP[Source=[Genre=?sgenre,Nombre=?snombre,Traduction=(?det+?adj+?n)],Destination=[Genre=?dgenre,Nombre=Du,Cas=?dcas]] -> DET[Source=[Genre=?sgenre,Nombre=?snombre,Traduction=?det],Destination=[Genre=?dgenre,Nombre=Du,Cas=?dcas]] 'deux' ADJ[Source=[Genre=?sgenre,Nombre=?snombre,Traduction=?adj],Destination=[Genre=?dgenre,Nombre=Du]] N[Source=[Genre=?sgenre,Nombre=?snombre,Traduction=?n],Destination=[Genre=?dgenre,Nombre=Du,Cas=?dcas]]"
       ],
      ["% start NP",
       "NP[Genre=?dgenre,Nombre=Du,Cas=?dcas] -> DET[Genre=?dgenre,Nombre=Du,Cas=?dcas] N[Genre=?dgenre,Nombre=Du,Cas=?dcas]",
       "NP[Genre=?dgenre,Nombre=Du,Cas=?dcas] -> DET[Genre=?dgenre,Nombre=Du,Cas=?dcas] ADJ[Genre=?dgenre,Nombre=Du] N[Genre=?dgenre,Nombre=Du,Cas=?dcas]",
       ])),

    (MorphoSyntax(contractions=frozendict(),
                  syntagmes={"NP": [["DET", "N"],
                                    ["deux", "N"]]},
                  start="NP",
                  accords={
                      "NP": [[{"sGenre": "*", "sNombre": "*", "dGenre": "*", "dNombre": "*", "dCas": "*"},
                              {"sGenre": "*", "sNombre": "*", "dGenre": "*", "dNombre": "*", "dCas": "*"}],
                             [{},
                              {"sGenre": "*", "sNombre": "*", "dGenre": "*", "dNombre": "Du", "dCas": "*"}]]},
                  percolations={"NP": [{"sGenre": "*", "sNombre": "*", "dGenre": "*", "dNombre": "*", "dCas": "*"},
                                       {"sGenre": "*", "sNombre": "*", "dGenre": "*", "dNombre": "Du", "dCas": "*"}]},
                  traductions={"NP": [[0, 1],
                                      [1]]}),
     (["% start NP",
       "NP[Source=[Genre=?sgenre,Nombre=?snombre,Traduction=(?det+?n)],Destination=[Genre=?dgenre,Nombre=?dnombre,Cas=?dcas]] ->"
       " DET[Source=[Genre=?sgenre,Nombre=?snombre,Traduction=?det],Destination=[Genre=?dgenre,Nombre=?dnombre,Cas=?dcas]]"
       " N[Source=[Genre=?sgenre,Nombre=?snombre,Traduction=?n],Destination=[Genre=?dgenre,Nombre=?dnombre,Cas=?dcas]]",
       "NP[Source=[Genre=?sgenre,Nombre=?snombre,Traduction=(?n)],Destination=[Genre=?dgenre,Nombre=Du,Cas=?dcas]] ->"
       " 'deux'"
       " N[Source=[Genre=?sgenre,Nombre=?snombre,Traduction=?n],Destination=[Genre=?dgenre,Nombre=Du,Cas=?dcas]]"],
      ["% start NP",
       "NP[Genre=?dgenre,Nombre=?dnombre,Cas=?dcas] -> DET[Genre=?dgenre,Nombre=?dnombre,Cas=?dcas] N[Genre=?dgenre,Nombre=?dnombre,Cas=?dcas]",
       "NP[Genre=?dgenre,Nombre=Du,Cas=?dcas] -> N[Genre=?dgenre,Nombre=Du,Cas=?dcas]"]
      )),

    (MorphoSyntax(contractions=frozendict(),
                  syntagmes={"NP": [["DET", "N", "ADJ"]]},
                  start="NP",
                  accords={"NP": [[{"sGenre": "*", "sNombre": "*", "dGenre": "*", "dNombre": "*", "dCas": "*"},
                                   {"sGenre": "*", "sNombre": "*", "dGenre": "*", "dNombre": "*", "dCas": "*"},
                                   {"sGenre": "*", "sNombre": "*", "dGenre": "*", "dNombre": "*"}]]},
                  percolations={"NP": [{"sGenre": "*", "sNombre": "*", "dGenre": "*", "dNombre": "*", "dCas": "*"}]},
                  traductions={"NP": [[0, 2, 1]]}),
     (["% start NP",
       "NP[Source=[Genre=?sgenre,Nombre=?snombre,Traduction=(?det+?adj+?n)],Destination=[Genre=?dgenre,Nombre=?dnombre,Cas=?dcas]] ->"
       " DET[Source=[Genre=?sgenre,Nombre=?snombre,Traduction=?det],Destination=[Genre=?dgenre,Nombre=?dnombre,Cas=?dcas]]"
       " N[Source=[Genre=?sgenre,Nombre=?snombre,Traduction=?n],Destination=[Genre=?dgenre,Nombre=?dnombre,Cas=?dcas]]"
       " ADJ[Source=[Genre=?sgenre,Nombre=?snombre,Traduction=?adj],Destination=[Genre=?dgenre,Nombre=?dnombre]]",
       ],
      ["% start NP",
       "NP[Genre=?dgenre,Nombre=?dnombre,Cas=?dcas] -> DET[Genre=?dgenre,Nombre=?dnombre,Cas=?dcas] ADJ[Genre=?dgenre,Nombre=?dnombre] N[Genre=?dgenre,Nombre=?dnombre,Cas=?dcas]"]
      )),

    (MorphoSyntax(contractions=frozendict(),
                  syntagmes={"NP": [["DET", "ADJ", "N", "ADJ"]]},
                  start="NP",
                  accords={"NP": [[{"sGenre": "*", "sNombre": "*", "dGenre": "*", "dNombre": "*", "dCas": "*"},
                                   {"sGenre": "*", "sNombre": "*", "dGenre": "*", "dNombre": "*"},
                                   {"sGenre": "*", "sNombre": "*", "dGenre": "*", "dNombre": "*", "dCas": "*"},
                                   {"sGenre": "*", "sNombre": "*", "dGenre": "*", "dNombre": "*"}]]},
                  percolations={"NP": [{"sGenre": "*", "sNombre": "*", "dGenre": "*", "dNombre": "*", "dCas": "*"}]},
                  traductions={"NP": [[0, 1, 3, 2]]}),
     (["% start NP",
       "NP[Source=[Genre=?sgenre,Nombre=?snombre,Traduction=(?det+?adj+?adj1+?n)],Destination=[Genre=?dgenre,Nombre=?dnombre,Cas=?dcas]] ->"
       " DET[Source=[Genre=?sgenre,Nombre=?snombre,Traduction=?det],Destination=[Genre=?dgenre,Nombre=?dnombre,Cas=?dcas]]"
       " ADJ[Source=[Genre=?sgenre,Nombre=?snombre,Traduction=?adj],Destination=[Genre=?dgenre,Nombre=?dnombre]]"
       " N[Source=[Genre=?sgenre,Nombre=?snombre,Traduction=?n],Destination=[Genre=?dgenre,Nombre=?dnombre,Cas=?dcas]]"
       " ADJ[Source=[Genre=?sgenre,Nombre=?snombre,Traduction=?adj1],Destination=[Genre=?dgenre,Nombre=?dnombre]]",
       ],
      ["% start NP",
       "NP[Genre=?dgenre,Nombre=?dnombre,Cas=?dcas] ->"
       " DET[Genre=?dgenre,Nombre=?dnombre,Cas=?dcas]"
       " ADJ[Genre=?dgenre,Nombre=?dnombre]"
       " ADJ[Genre=?dgenre,Nombre=?dnombre]"
       " N[Genre=?dgenre,Nombre=?dnombre,Cas=?dcas]"]
      )),
])
def test_read_rules(morphosyntax, expected):
    assert read_rules(morphosyntax) == expected


@pytest.mark.parametrize("sequence, expected", [
    ("", []),
    ("l'avion", ["l'", "avion"]),
    ("le baron", ["le", "baron"]),
    ("le baron.", ["le", "baron", "."]),
    ("ce chasseur lançait l'infirmière", ["ce", "chasseur", "lançait", "l'", "infirmière"]),
])
def test_split(sequence, expected) -> None:
    actual = split(sequence)
    assert actual == expected


@pytest.mark.parametrize("gloses, blocks, cat, sigma, lexeme, expected", [
    ({"source": {"N": {"genre": ["m", "f"]}},
      "destination": {"N": {"genre": ["m", "f"]}}},
     {"source": {"N": None}, "destination": {"N": None}},
     "N",
     frozendict(),
     Lexeme(stem="mict", pos="N", sigma=frozendict(),
            traduction=Lexeme(stem="banane", pos="N", sigma=frozendict(),
                              traduction=None)), ["mict", "mict"]),

    ({"source": {"N": {"genre": ["m", "f"]}},
      "destination": {"N": {"genre": ["m", "f"]}}},
     {"source": {"N": {"1": {"genre=m": "X+e"}}},
      "destination": {"N": {"1": {"genre=m": "X+a"}}}},
     "N",
     frozendict(),
     Lexeme(stem="mict", pos="N", sigma=frozendict(),
            traduction=Lexeme(stem="banane", pos="N", sigma=frozendict(),
                              traduction=None)), ["micte", "mict"]),

])
def test_build_paradigm(fx_phonology, gloses, blocks, cat, sigma, lexeme, expected):
    gloses, att_vals = read_glose(gloses)
    _blocks = read_blocks(blocks, att_vals, frozenset("aeiou"))
    actual = build_paradigm(gloses, _blocks)

    assert [realize(term=lex, phonology=fx_phonology) for lex in realize(term=lexeme, paradigm=actual)] == expected
