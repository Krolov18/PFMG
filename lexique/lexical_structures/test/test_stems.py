import pytest
import yaml
from frozendict import frozendict

from lexique.lexical_structures.Gloses import Gloses
from lexique.lexical_structures.Lexeme import Lexeme
from lexique.lexical_structures.StemSpace import StemSpace
from lexique.lexical_structures.Stems import Stems


def fx_gloses() -> Gloses:
    return Gloses(data={"N": [frozendict(Genre="m", Nombre="sg", m="Genre", sg="Nombre"),
                              frozendict(Genre="m", Nombre="pl", m="Genre", pl="Nombre"),
                              frozendict(Genre="f", Nombre="sg", f="Genre", sg="Nombre"),
                              frozendict(Genre="f", Nombre="pl", f="Genre", pl="Nombre")],
                        "A": [frozendict(Cas="erg", erg="Cas")]})


@pytest.mark.parametrize("data, searcher", [
    ([Lexeme(stem=StemSpace(stems=("chien", "chienne")),
             pos="N",
             sigma=frozendict())],
     fx_gloses())
])
def test_stems(data, searcher) -> None:
    actual = Stems(data=iter(data), searcher=searcher)
    assert list(actual) == list(data)
    assert list(actual) == []


@pytest.mark.parametrize("stems, gloses, expected", [
    ({"N": {"pSit": "toto,tutu"},
      "A": {"erg": {"ksit": "kiki,koko"}}
      },
     {"N": {"Genre": ["m", "f"],
            "Nombre": ["sg", "pl"]},
      "A": {"Cas": ["erg"]}},
     [Lexeme(stem=StemSpace(stems=("ksit",)),
             pos="A", sigma=frozendict(Cas="erg")),
      Lexeme(stem=StemSpace(stems=("pSit",)),
             pos="N", sigma=frozendict())]),

])
def test_from_disk(tmp_path, stems, gloses, expected):
    gloses_path = tmp_path / "Gloses.yaml"
    with open(gloses_path, mode="w", encoding="utf8") as file_handler:
        yaml.dump(gloses, file_handler)

    stems_path = tmp_path / "Stems.yaml"
    with open(stems_path, mode="w", encoding="utf8") as file_handler:
        yaml.dump(stems, file_handler)

    actual = Stems.from_disk(stems_path)
    assert list(actual.data) == expected


@pytest.mark.parametrize("stems, gloses, expected", [
    ({"N": {"A": {"padaN": "viande-2.F"}}},
     {"N": {"Genre": ["K", "B", "C", "D"],
            "Nombre": ["sg", "pl"]}},
     [Lexeme(stem=StemSpace(stems=("padaN",)),
             pos="N", sigma=frozendict({"Genre": "A"}))]),

])
def test_from_disk_error(tmp_path, stems, gloses, expected):
    gloses_path = tmp_path / "Gloses.yaml"
    with open(gloses_path, mode="w", encoding="utf8") as file_handler:
        yaml.dump(gloses, file_handler)

    stems_path = tmp_path / "Stems.yaml"
    with open(stems_path, mode="w", encoding="utf8") as file_handler:
        yaml.dump(stems, file_handler)

    with pytest.raises(ValueError):
        _ = list(Stems.from_disk(stems_path))
