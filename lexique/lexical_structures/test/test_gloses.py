import pytest
import yaml
from frozendict import frozendict

from lexique.lexical_structures.Gloses import Gloses


@pytest.mark.parametrize("gloses, expected", [
    ({"N": {"Genre": ["m"]}},
     {"N": [frozendict(Genre="m", m="Genre")]}),

    ({"N": {"Genre": ["m", "f"]}},
     {"N": [frozendict(Genre="m", m="Genre"),
            frozendict(Genre="f", f="Genre")]}),

    ({"N": {"Genre": ["m", "f"],
            "Nombre": ["sg", "pl"]}},
     {"N": [frozendict(Genre="m", Nombre="sg", m="Genre", sg="Nombre"),
            frozendict(Genre="m", Nombre="pl", m="Genre", pl="Nombre"),
            frozendict(Genre="f", Nombre="sg", f="Genre", sg="Nombre"),
            frozendict(Genre="f", Nombre="pl", f="Genre", pl="Nombre")]}),

    ({"N": {"Genre": ["m", "f"],
            "Nombre": ["sg", "pl"]},
      "A": {"Cas": ["erg"]}},
     {"N": [frozendict(Genre="m", Nombre="sg", m="Genre", sg="Nombre"),
            frozendict(Genre="m", Nombre="pl", m="Genre", pl="Nombre"),
            frozendict(Genre="f", Nombre="sg", f="Genre", sg="Nombre"),
            frozendict(Genre="f", Nombre="pl", f="Genre", pl="Nombre")],
      "A": [frozendict(Cas="erg", erg="Cas")]}),

    ({"N": [{"Genre": "m"}]},
     {"N": [frozendict(Genre="m", m="Genre")]}),

    ({"N": []},
     {"N": [[]]}),

    ({"N": [{}]}, {"N": []})

])
def test_gloses_from_disk(tmp_path, gloses, expected) -> None:
    gloses_path = tmp_path / "Gloses.yaml"
    with open(gloses_path, mode="w", encoding="utf8") as file_handler:
        yaml.dump(gloses, file_handler)
    actual = Gloses.from_disk(gloses_path)

    assert actual == Gloses(data=expected)


def test_gloses_search(tmp_path) -> None:
    gloses_path = tmp_path / "Gloses.yaml"
    with open(gloses_path, mode="w", encoding="utf8") as file_handler:
        yaml.dump({"N": []}, file_handler)
    with pytest.raises(ValueError):
        _ = Gloses.from_disk(gloses_path).search("N", "Genre")

    gloses_path = tmp_path / "Gloses.yaml"
    with open(gloses_path, mode="w", encoding="utf8") as file_handler:
        yaml.dump({"N": [{"Genre": "m"}]}, file_handler)
    assert Gloses.from_disk(gloses_path).search("N", "Genre") == "m"

    gloses_path = tmp_path / "Gloses.yaml"
    with open(gloses_path, mode="w", encoding="utf8") as file_handler:
        yaml.dump({"N": [{"Genre": "f"}, {"Genre": "m"}]}, file_handler)
    assert Gloses.from_disk(gloses_path).search("N", "Genre") == "f"


def test_is_pos(tmp_path) -> None:
    gloses_path = tmp_path / "Gloses.yaml"
    with open(gloses_path, mode="w", encoding="utf8") as file_handler:
        yaml.dump({"N": [{"Genre": "f"}, {"Genre": "m"}]}, file_handler)
    assert Gloses.from_disk(gloses_path).is_pos("N")
    assert not Gloses.from_disk(gloses_path).is_pos("A")
