# pylint: disable=line-too-long,missing-module-docstring,missing-function-docstring
import re
from typing import List, Dict, Tuple

import pytest
import yaml
from frozendict import frozendict

# from lexique import get_lexique_path
from lexique import get_lexique_path
from lexique.etl import (_read_blocks,
                         read_glose,
                         read_stems,
                         read_phonology,
                         read_traduction,
                         read_rules,
                         read_blocks,
                         TypeBlocks,
                         _filter_grid, split)

from lexique.structures import Suffix, Lexeme, Phonology, MorphoSyntax


@pytest.mark.parametrize("grid,constraints,expected", [
    ([], {}, []),
    ([frozendict()], {}, [frozendict()]),  # peut-être, il faut exclure cette possibilité
    ([frozendict(Genre="f", þGenre="þf")], {"Genre"}, [frozendict(Genre="f", þGenre="þf")]),
    ([frozendict(Genre="f", þGenre="þm")], {"Genre"}, []),
    ([frozendict(Nombre="Sg", þNombre="þSg")], {"Nombre"}, [frozendict(Nombre="Sg", þNombre="þSg")]),
    ([frozendict(Nombre="Sg", þNombre="þPl")], {"Nombre": "Du>Pl"}, []),
    ([frozendict(Nombre="Du", þNombre="þPl")], {"Nombre": "Du>Pl"}, [frozendict(Nombre="Du", þNombre="þPl")]),
    ([frozendict(Nombre="Pl", þNombre="þPl")], {"Nombre": "Du>Pl"}, [frozendict(Nombre="Pl", þNombre="þPl")]),
])
def test_filter_grid(grid, constraints, expected) -> None:
    actual = _filter_grid(grid, constraints)
    assert actual == expected


def test_read_glose_errors() -> None:
    with pytest.raises(ValueError):
        _ = read_glose({})


@pytest.mark.parametrize("glose, expected", [
    ({"N": {"genre": ["m", "f"]}},
     ({"N": [frozendict({"genre": "m"}), frozendict({"genre": "f"})]},
      frozendict({"N": "pos", "m": "genre", "f": "genre"}))),

    ({"N": {"genre": ["m", "f"], "nombre": ["sg", "pl"]}},
     ({"N": [{"genre": "m", "nombre": "sg"}, {"genre": "m", "nombre": "pl"},
             {"genre": "f", "nombre": "sg"}, {"genre": "f", "nombre": "pl"}]},
      frozendict({"N": "pos", "m": "genre", "f": "genre", "sg": "nombre", "pl": "nombre"}))),

    ({"V": [{"Mode": ["Inf"]}, {"Nombre": ["Sg", "Pl"]}]},
     ({"V": [frozendict(Mode="Inf"), frozendict(Nombre="Sg"), frozendict(Nombre="Pl")]},
      frozendict(Sg="Nombre", Pl="Nombre", Inf="Mode", V="pos")))
])
def test_read_glose(glose, expected) -> None:
    actual = read_glose(glose)
    assert actual == expected


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


@pytest.fixture(params=[{"ADJ": {"genre": ["m", "f"], "nombre": ["sg", "pl"]}}])
def fx_gloses(request) -> Tuple[Dict[str, List[frozendict]], frozendict]:
    return read_glose(request.param)


@pytest.fixture(params=[{"kalaba": {"ADJ": {"1": {"genre=f": "X+e"}, "2": {"nombre=pl": "X+s"}}},
                         "translation": {"ADJ": {"1": {"genre=f": "X+f"}}}}])
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
    ("Katisha-1", frozendict({"þ1": "þCF"}), (("Katisha",), frozendict({"þCF": "þ1"}))),
    ("Katisha-1.F", frozendict({"þ1": "þCF", "þF": "þGenre"}),
     (("Katisha",), frozendict({"þCF": "þ1", "þGenre": "þF"}))),
    ("Katisha,Katishas-1.F", frozendict({"þ1": "þCF", "þF": "þGenre"}),
     (("Katisha", "Katishas"), frozendict({"þCF": "þ1", "þGenre": "þF"}))),
])
def test_read_traduction(stem, att_vals, expected) -> None:
    actual = read_traduction(stem=stem, att_vals=att_vals)
    assert actual == expected


@pytest.mark.parametrize("expected", [
    [Lexeme(stem=('katiSa',), pos='N', sigma=frozendict({'Genre': 'A'}),
            traduction=Lexeme(stem=('Katisha',), pos='N',
                              sigma=frozendict({'þCF': 'þ1', 'þGenre': 'þF'}), traduction=None)),
     Lexeme(stem=('padaN',), pos='N', sigma=frozendict({'Genre': 'A'}),
            traduction=Lexeme(stem=('viande',), pos='N',
                              sigma=frozendict({'þCF': 'þ2', 'þGenre': 'þF'}),
                              traduction=None)),
     Lexeme(stem=('toSik',), pos='N', sigma=frozendict({'Genre': 'A'}),
            traduction=Lexeme(stem=('fruit',), pos='N',
                              sigma=frozendict({'þCF': 'þ2', 'þGenre': 'þM'}),
                              traduction=None)),
     Lexeme(stem=('modak',), pos='N', sigma=frozendict({'Genre': 'A'}),
            traduction=Lexeme(stem=('infirmière',), pos='N',
                              sigma=frozendict({'þCF': 'þ2', 'þGenre': 'þF'}),
                              traduction=None)),
     Lexeme(stem=('gatok',), pos='N', sigma=frozendict({'Genre': 'A'}),
            traduction=Lexeme(stem=('balai',), pos='N',
                              sigma=frozendict({'þCF': 'þ2', 'þGenre': 'þM'}),
                              traduction=None)),
     Lexeme(stem=('pebiz',), pos='N', sigma=frozendict({'Genre': 'A'}),
            traduction=Lexeme(stem=('plaine',), pos='N',
                              sigma=frozendict({'þCF': 'þ2', 'þGenre': 'þF'}),
                              traduction=None)),
     Lexeme(stem=('nikol',), pos='N', sigma=frozendict({'Genre': 'B'}),
            traduction=Lexeme(stem=('Nicole',), pos='N',
                              sigma=frozendict({'þCF': 'þ1', 'þGenre': 'þF'}),
                              traduction=None)),
     Lexeme(stem=('minet',), pos='N', sigma=frozendict({'Genre': 'B'}),
            traduction=Lexeme(stem=('autruche',), pos='N',
                              sigma=frozendict({'þCF': 'þ2', 'þGenre': 'þF'}),
                              traduction=None)),
     Lexeme(stem=('SeNon',), pos='N', sigma=frozendict({'Genre': 'B'}),
            traduction=Lexeme(stem=('souris',), pos='N',
                              sigma=frozendict({'þCF': 'þ1', 'þGenre': 'þF'}),
                              traduction=None)),
     Lexeme(stem=('sapum',), pos='N', sigma=frozendict({'Genre': 'B'}),
            traduction=Lexeme(stem=('coussin',), pos='N',
                              sigma=frozendict({'þCF': 'þ2', 'þGenre': 'þM'}),
                              traduction=None)),
     Lexeme(stem=('gitun',), pos='N', sigma=frozendict({'Genre': 'B'}),
            traduction=Lexeme(stem=('chambre',), pos='N',
                              sigma=frozendict({'þCF': 'þ2', 'þGenre': 'þF'}),
                              traduction=None)),
     Lexeme(stem=('maren',), pos='N', sigma=frozendict({'Genre': 'B'}),
            traduction=Lexeme(stem=('thé',), pos='N',
                              sigma=frozendict({'þCF': 'þ2', 'þGenre': 'þM'}),
                              traduction=None)),
     Lexeme(stem=('diNol',), pos='N', sigma=frozendict({'Genre': 'C'}),
            traduction=Lexeme(stem=('chasseur',), pos='N',
                              sigma=frozendict({'þCF': 'þ2', 'þGenre': 'þM'}),
                              traduction=None)),
     Lexeme(stem=('minut',), pos='N', sigma=frozendict({'Genre': 'C'}),
            traduction=Lexeme(stem=('fille',), pos='N',
                              sigma=frozendict({'þCF': 'þ2', 'þGenre': 'þF'}),
                              traduction=None)),
     Lexeme(stem=('Zerom',), pos='N', sigma=frozendict({'Genre': 'C'}),
            traduction=Lexeme(stem=('oeuf',), pos='N',
                              sigma=frozendict({'þCF': 'þ2', 'þGenre': 'þM'}),
                              traduction=None)),
     Lexeme(stem=('felot',), pos='N', sigma=frozendict({'Genre': 'C'}),
            traduction=Lexeme(stem=('café',), pos='N',
                              sigma=frozendict({'þCF': 'þ2', 'þGenre': 'þM'}),
                              traduction=None)),
     Lexeme(stem=('potaS',), pos='N', sigma=frozendict({'Genre': 'C'}),
            traduction=Lexeme(stem=('coyote',), pos='N',
                              sigma=frozendict({'þCF': 'þ2', 'þGenre': 'þM'}),
                              traduction=None)),
     Lexeme(stem=('kasab',), pos='N', sigma=frozendict({'Genre': 'C'}),
            traduction=Lexeme(stem=('village',), pos='N',
                              sigma=frozendict({'þCF': 'þ2', 'þGenre': 'þM'}),
                              traduction=None)),
     Lexeme(stem=('nabil',), pos='N', sigma=frozendict({'Genre': 'D'}),
            traduction=Lexeme(stem=('Nabil',), pos='N',
                              sigma=frozendict({'þCF': 'þ1', 'þGenre': 'þM'}),
                              traduction=None)),
     Lexeme(stem=('mesaZ',), pos='N', sigma=frozendict({'Genre': 'D'}),
            traduction=Lexeme(stem=('garçon',), pos='N',
                              sigma=frozendict({'þCF': 'þ2', 'þGenre': 'þM'}),
                              traduction=None)),
     Lexeme(stem=('pulop',), pos='N', sigma=frozendict({'Genre': 'D'}),
            traduction=Lexeme(stem=('cuisine',), pos='N',
                              sigma=frozendict({'þCF': 'þ2', 'þGenre': 'þF'}),
                              traduction=None)),
     Lexeme(stem=('Nazon',), pos='N', sigma=frozendict({'Genre': 'D'}),
            traduction=Lexeme(stem=('table',), pos='N',
                              sigma=frozendict({'þCF': 'þ2', 'þGenre': 'þF'}),
                              traduction=None)),
     Lexeme(stem=('rumak',), pos='N', sigma=frozendict({'Genre': 'D'}),
            traduction=Lexeme(stem=('chat', 'chatte'), pos='N', sigma=frozendict({'þCF': 'þ2'}),
                              traduction=None)),
     Lexeme(stem=('gobid',), pos='N', sigma=frozendict({'Genre': 'D'}),
            traduction=Lexeme(stem=('lit',), pos='N',
                              sigma=frozendict({'þCF': 'þ2', 'þGenre': 'þM'}),
                              traduction=None)),
     Lexeme(stem=('kuroz',), pos='N', sigma=frozendict({'Genre': 'D'}),
            traduction=Lexeme(stem=('maison',), pos='N',
                              sigma=frozendict({'þCF': 'þ2', 'þGenre': 'þF'}),
                              traduction=None)),
     Lexeme(stem=('meN',), pos='ADJ', sigma=frozendict({'CF': '1'}),
            traduction=Lexeme(stem=('grand', 'grande'), pos='ADJ', sigma=frozendict({'þCF': 'þ1'}),
                              traduction=None)),
     Lexeme(stem=('rug',), pos='ADJ', sigma=frozendict({'CF': '1'}),
            traduction=Lexeme(stem=('petit', 'petite'), pos='ADJ', sigma=frozendict({'þCF': 'þ1'}),
                              traduction=None)),
     Lexeme(stem=('nor',), pos='ADJ', sigma=frozendict({'CF': '1'}),
            traduction=Lexeme(stem=('blanc', 'blanche'), pos='ADJ', sigma=frozendict({'þCF': 'þ1'}),
                              traduction=None)),
     Lexeme(stem=('dos',), pos='ADJ', sigma=frozendict({'CF': '1'}),
            traduction=Lexeme(stem=('noir', 'noire'), pos='ADJ', sigma=frozendict({'þCF': 'þ1'}),
                              traduction=None)),
     Lexeme(stem=('lik',), pos='ADJ', sigma=frozendict({'CF': '1'}),
            traduction=Lexeme(stem=('bas', 'basse'), pos='ADJ', sigma=frozendict({'þCF': 'þ4'}),
                              traduction=None)),
     Lexeme(stem=('lap',), pos='ADJ', sigma=frozendict({'CF': '2'}),
            traduction=Lexeme(stem=('gros', 'grosse'), pos='ADJ', sigma=frozendict({'þCF': 'þ4'}),
                              traduction=None)),
     Lexeme(stem=('Nul',), pos='ADJ', sigma=frozendict({'CF': '2'}),
            traduction=Lexeme(stem=('maigre',), pos='ADJ', sigma=frozendict({'þCF': 'þ2'}),
                              traduction=None)),
     Lexeme(stem=('kun',), pos='ADJ', sigma=frozendict({'CF': '2'}),
            traduction=Lexeme(stem=('jaune',), pos='ADJ', sigma=frozendict({'þCF': 'þ2'}),
                              traduction=None)),
     Lexeme(stem=('gil',), pos='ADJ', sigma=frozendict({'CF': '2'}),
            traduction=Lexeme(stem=('rouge',), pos='ADJ', sigma=frozendict({'þCF': 'þ2'}),
                              traduction=None)),
     Lexeme(stem=('bat',), pos='ADJ', sigma=frozendict({'CF': '2', 'Nombre': 'Pl'}),
            traduction=Lexeme(stem=('trois',), pos='ADJ',
                              sigma=frozendict({'þCF': 'þ3', 'þNombre': 'þPl'}),
                              traduction=None)),
     Lexeme(stem=('jig',), pos='ADJ', sigma=frozendict({'CF': '2', 'Nombre': 'Pl'}),
            traduction=Lexeme(stem=('quatre',), pos='ADJ',
                              sigma=frozendict({'þCF': 'þ3', 'þNombre': 'þPl'}),
                              traduction=None)),
     Lexeme(stem=('briN',), pos='V', sigma=frozendict({'Type': 'VI'}),
            traduction=Lexeme(stem=('dormir', 'dort', 'dorment', 'dormait', 'dormaient'), pos='V',
                              sigma=frozendict({'þType': 'þVI'}), traduction=None)),
     Lexeme(stem=('rnif',), pos='V', sigma=frozendict({'Type': 'VI'}),
            traduction=Lexeme(stem=('tomber', 'tombe', 'tombent', 'tombait', 'tombaient'), pos='V',
                              sigma=frozendict({'þType': 'þVI'}), traduction=None)),
     Lexeme(stem=('svit',), pos='V', sigma=frozendict({'Type': 'VI'}),
            traduction=Lexeme(stem=('arriver', 'arrive', 'arrivent', 'arrivait', 'arrivaient'), pos='V',
                              sigma=frozendict({'þType': 'þVI'}), traduction=None)),
     Lexeme(stem=('btir',), pos='V', sigma=frozendict({'Type': 'VI'}),
            traduction=Lexeme(stem=('entrer', 'entre', 'entrent', 'entrait', 'entraient'), pos='V',
                              sigma=frozendict({'þType': 'þVI'}), traduction=None)),
     Lexeme(stem=('pled',), pos='V', sigma=frozendict({'Type': 'VT'}),
            traduction=Lexeme(stem=('manger', 'mange', 'mangent', 'mangeait', 'mangeaient'), pos='V',
                              sigma=frozendict({'þType': 'þVT'}), traduction=None)),
     Lexeme(stem=('Srev',), pos='V', sigma=frozendict({'Type': 'VT'}),
            traduction=Lexeme(stem=('boire', 'boit', 'boivent', 'buvait', 'buvaient'), pos='V',
                              sigma=frozendict({'þType': 'þVT'}), traduction=None)),
     Lexeme(stem=('grej',), pos='V', sigma=frozendict({'Type': 'VT'}),
            traduction=Lexeme(stem=('acheter', 'achète', 'achètent', 'achetait', 'achetaient'), pos='V',
                              sigma=frozendict({'þType': 'þVT'}), traduction=None)),
     Lexeme(stem=('nkem',), pos='V', sigma=frozendict({'Type': 'VT'}),
            traduction=Lexeme(stem=('supporter', 'supporte', 'supportent', 'supportait', 'supportaient'), pos='V',
                              sigma=frozendict({'þType': 'þVT'}), traduction=None)),
     Lexeme(stem=('dNet',), pos='V', sigma=frozendict({'Type': 'VT'}),
            traduction=Lexeme(stem=('chasser', 'chasse', 'chassent', 'chassait', 'chassaient'), pos='V',
                              sigma=frozendict({'þType': 'þVT'}), traduction=None)),
     Lexeme(stem=('psag',), pos='V', sigma=frozendict({'Type': 'VD'}),
            traduction=Lexeme(stem=('donner', 'donne', 'donnent', 'donnait', 'donnaient'), pos='V',
                              sigma=frozendict({'þType': 'þVD'}), traduction=None)),
     Lexeme(stem=('rdan',), pos='V', sigma=frozendict({'Type': 'VD'}),
            traduction=Lexeme(stem=('offrir', 'offre', 'offrent', 'offrait', 'offraient'), pos='V',
                              sigma=frozendict({'þType': 'þVD'}), traduction=None)),
     Lexeme(stem=('pral',), pos='V', sigma=frozendict({'Type': 'VD'}),
            traduction=Lexeme(stem=('lancer', 'lance', 'lancent', 'lançait', 'lançaient'), pos='V',
                              sigma=frozendict({'þType': 'þVD'}), traduction=None)),
     Lexeme(stem=('pnab',), pos='V', sigma=frozendict({'Type': 'VD'}),
            traduction=Lexeme(stem=('montrer', 'montre', 'montrent', 'montrait', 'montraient'), pos='V',
                              sigma=frozendict({'þType': 'þVD'}), traduction=None)),
     Lexeme(stem=('b',), pos='DET', sigma=frozendict({}),
            traduction=Lexeme(stem=('le', 'la', 'les', 'le'), pos='DET', sigma=frozendict({'þDEF': 'þDEF'}),
                              traduction=None)),
     Lexeme(stem=('k',), pos='DET', sigma=frozendict({}),
            traduction=Lexeme(stem=('un', 'une', 'des'), pos='DET', sigma=frozendict({'þDEF': 'þINDEF'}),
                              traduction=None)),
     Lexeme(stem=('l',), pos='DET', sigma=frozendict({}),
            traduction=Lexeme(stem=('ce', 'cette', 'ces', 'cet'),
                              pos='DET', sigma=frozendict({'þDEF': 'þDEM'}), traduction=None)),
     Lexeme(stem=('kal',), pos='PREP', sigma=frozendict({}),
            traduction=Lexeme(stem=('dans',), pos='PREP', sigma=frozendict({}), traduction=None)),
     Lexeme(stem=('lab',), pos='PREP', sigma=frozendict({}),
            traduction=Lexeme(stem=('sur',), pos='PREP', sigma=frozendict({}), traduction=None)),
     Lexeme(stem=('bak',), pos='PREP', sigma=frozendict({}),
            traduction=Lexeme(stem=('avec',), pos='PREP', sigma=frozendict({}), traduction=None)),
     Lexeme(stem=('jan',), pos='PREP', sigma=frozendict({}),
            traduction=Lexeme(stem=('sous',), pos='PREP', sigma=frozendict({}), traduction=None)),
     Lexeme(stem=('dul',), pos='PREP', sigma=frozendict({}),
            traduction=Lexeme(stem=('devant',), pos='PREP', sigma=frozendict({}), traduction=None)),
     Lexeme(stem=('laN',), pos='PREP', sigma=frozendict({}),
            traduction=Lexeme(stem=('pour',), pos='PREP', sigma=frozendict({}), traduction=None)),
     Lexeme(stem=('sil',), pos='PREP', sigma=frozendict({}),
            traduction=Lexeme(stem=('de',), pos='PREP', sigma=frozendict({}), traduction=None))]
])
def test_read_stems_2(fx_stem_file, expected) -> None:
    actual = [*read_stems(data=fx_stem_file,
                          accumulator="",
                          att_vals=frozendict({"DET": "pos", "ADJ": "pos", "N": "pos", "V": "pos", "PREP": "pos",
                                               "A": "Genre", "B": "Genre", "C": "Genre", "D": "Genre",
                                               "þF": "þGenre", "þM": "þGenre",
                                               "1": "CF", "2": "CF",
                                               "þ1": "þCF", "þ2": "þCF", "þ3": "þCF", "þ4": "þCF",
                                               "3": "Personne",
                                               "DEF": "DEF", "INDEF": "DEF", "DEM": "DEF",
                                               "þDEF": "þDEF", "þINDEF": "þDEF", "þDEM": "þDEF",
                                               "Sg": "Nombre", "Du": "Nombre", "Pl": "Nombre",
                                               "þSg": "þNombre", "þPl": "þNombre",
                                               "Erg": "Cas", "Abs": "Cas", "Obl": "Cas", "Dat": "Cas",
                                               "VI": "Type", "VT": "Type", "VD": "Type",
                                               "þVI": "þType", "þVT": "þType", "þVD": "þType",
                                               "þCONS": "þLIAIS", "þVOC": "þLIAIS",
                                               "þGauche": "þCOTE", "þDroite": "þCOTE"}))]
    assert actual == expected


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
                  accords={"NP": [[{"Genre": "*", "Nombre": "*", "Cas": "*"},
                                   {"Genre": "*", "Nombre": "*", "Cas": "*"}]]},
                  percolations={"NP": [{"Genre": "*", "Nombre": "*", "Cas": "*"}]},
                  traductions={"NP": [[1, 0]]}),
     (["% start NP",
       "NP[Genre=?genre,Nombre=?nombre,Cas=?cas,Traduction=(?n+?det)] -> DET[Genre=?genre,Nombre=?nombre,Cas=?cas,Traduction=?det] N[Genre=?genre,Nombre=?nombre,Cas=?cas,Traduction=?n]"],
      ["% start NP",
       "NP[Genre=?genre,Nombre=?nombre,Cas=?cas] -> N[Genre=?genre,Nombre=?nombre,Cas=?cas] DET[Genre=?genre,Nombre=?nombre,Cas=?cas]"])),

    (MorphoSyntax(contractions=frozendict(),
                  syntagmes={"NP": [["deux", "N"]]},
                  start="NP",
                  accords={"NP": [[{}, {"Genre": "*", "Nombre": "Du", "Cas": "*"}]]},
                  percolations={"NP": [{"Genre": "*", "Nombre": "Du", "Cas": "*"}]},
                  traductions={"NP": [[1]]}),
     (["% start NP",
       "NP[Genre=?genre,Nombre=Du,Cas=?cas,Traduction=?n] -> 'deux' N[Genre=?genre,Nombre=Du,Cas=?cas,Traduction=?n]"],
      ["% start NP", "NP[Genre=?genre,Nombre=Du,Cas=?cas] -> N[Genre=?genre,Nombre=Du,Cas=?cas]"])),

    (MorphoSyntax(contractions=frozendict(),
                  syntagmes={"NP": [["DET", "deux", "ADJ/?", "N"]]},
                  start="NP",
                  accords={"NP": [[{"Genre": "*", "Nombre": "Du", "Cas": "*"}, {}, {"Genre": "*", "Nombre": "Du"},
                                   {"Genre": "*", "Nombre": "Du", "Cas": "*"}]]},
                  percolations={"NP": [{"Genre": "*", "Nombre": "Du", "Cas": "*"}]},
                  traductions={"NP": [[0, 2, 3]]}),
     (["% start NP",
       "NP[Genre=?genre,Nombre=Du,Cas=?cas,Traduction=(?det+?n)] -> DET[Genre=?genre,Nombre=Du,Cas=?cas,Traduction=?det] 'deux' N[Genre=?genre,Nombre=Du,Cas=?cas,Traduction=?n]",
       "NP[Genre=?genre,Nombre=Du,Cas=?cas,Traduction=(?det+?adj+?n)] -> DET[Genre=?genre,Nombre=Du,Cas=?cas,Traduction=?det] 'deux' ADJ[Genre=?genre,Nombre=Du,Traduction=?adj] N[Genre=?genre,Nombre=Du,Cas=?cas,Traduction=?n]"],
      ["% start NP",
       "NP[Genre=?genre,Nombre=Du,Cas=?cas] -> DET[Genre=?genre,Nombre=Du,Cas=?cas] N[Genre=?genre,Nombre=Du,Cas=?cas]",
       "NP[Genre=?genre,Nombre=Du,Cas=?cas] -> DET[Genre=?genre,Nombre=Du,Cas=?cas] ADJ[Genre=?genre,Nombre=Du] N[Genre=?genre,Nombre=Du,Cas=?cas]"])),

    (MorphoSyntax(contractions=frozendict(),
                  syntagmes={"NP": [["DET", "N"],
                                    ["deux", "N"]]},
                  start="NP",
                  accords={
                      "NP": [[{"Genre": "*", "Nombre": "*", "Cas": "*"}, {"Genre": "*", "Nombre": "*", "Cas": "*"}],
                             [{}, {"Genre": "*", "Nombre": "Du", "Cas": "*"}]]},
                  percolations={"NP": [{"Genre": "*", "Nombre": "*", "Cas": "*"},
                                       {"Genre": "*", "Nombre": "Du", "Cas": "*"}]},
                  traductions={"NP": [[0, 1],
                                      [1]]}),
     (["% start NP",
       "NP[Genre=?genre,Nombre=?nombre,Cas=?cas,Traduction=(?det+?n)] -> DET[Genre=?genre,Nombre=?nombre,Cas=?cas,Traduction=?det] N[Genre=?genre,Nombre=?nombre,Cas=?cas,Traduction=?n]",
       "NP[Genre=?genre,Nombre=Du,Cas=?cas,Traduction=?n] -> 'deux' N[Genre=?genre,Nombre=Du,Cas=?cas,Traduction=?n]"],
      ["% start NP",
       "NP[Genre=?genre,Nombre=?nombre,Cas=?cas] -> DET[Genre=?genre,Nombre=?nombre,Cas=?cas] N[Genre=?genre,Nombre=?nombre,Cas=?cas]",
       "NP[Genre=?genre,Nombre=Du,Cas=?cas] -> N[Genre=?genre,Nombre=Du,Cas=?cas]"]
      )),

    (MorphoSyntax(contractions=frozendict(),
                  syntagmes={"NP": [["DET", "N", "ADJ"]]},
                  start="NP",
                  accords={"NP": [[{"Genre": "*", "Nombre": "*", "Cas": "*"}, {"Genre": "*", "Nombre": "*", "Cas": "*"},
                                   {"Genre": "*", "Nombre": "*"}]]},
                  percolations={"NP": [{"Genre": "*", "Nombre": "*", "Cas": "*"}]},
                  traductions={"NP": [[0, 2, 1]]}),
     (["% start NP",
       "NP[Genre=?genre,Nombre=?nombre,Cas=?cas,Traduction=(?det+?adj+?n)] -> DET[Genre=?genre,Nombre=?nombre,Cas=?cas,Traduction=?det] N[Genre=?genre,Nombre=?nombre,Cas=?cas,Traduction=?n] ADJ[Genre=?genre,Nombre=?nombre,Traduction=?adj]"],
      ["% start NP",
       "NP[Genre=?genre,Nombre=?nombre,Cas=?cas] -> DET[Genre=?genre,Nombre=?nombre,Cas=?cas] ADJ[Genre=?genre,Nombre=?nombre] N[Genre=?genre,Nombre=?nombre,Cas=?cas]"]
      )),

    (MorphoSyntax(contractions=frozendict(),
                  syntagmes={"NP": [["DET", "ADJ", "N", "ADJ"]]},
                  start="NP",
                  accords={"NP": [[{"Genre": "*", "Nombre": "*", "Cas": "*"}, {"Genre": "*", "Nombre": "*"},
                                   {"Genre": "*", "Nombre": "*", "Cas": "*"}, {"Genre": "*", "Nombre": "*"}]]},
                  percolations={"NP": [{"Genre": "*", "Nombre": "*", "Cas": "*"}]},
                  traductions={"NP": [[0, 1, 3, 2]]}),
     (["% start NP",
       "NP[Genre=?genre,Nombre=?nombre,Cas=?cas,Traduction=(?det+?adj+?adj1+?n)] -> "
       "DET[Genre=?genre,Nombre=?nombre,Cas=?cas,Traduction=?det] ADJ[Genre=?genre,Nombre=?nombre,Traduction=?adj] "
       "N[Genre=?genre,Nombre=?nombre,Cas=?cas,Traduction=?n] ADJ[Genre=?genre,Nombre=?nombre,Traduction=?adj1]"],
      ["% start NP",
       "NP[Genre=?genre,Nombre=?nombre,Cas=?cas] -> DET[Genre=?genre,Nombre=?nombre,Cas=?cas] "
       "ADJ[Genre=?genre,Nombre=?nombre] ADJ[Genre=?genre,Nombre=?nombre] N[Genre=?genre,Nombre=?nombre,Cas=?cas]"]
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
