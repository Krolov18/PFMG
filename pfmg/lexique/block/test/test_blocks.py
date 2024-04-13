from functools import cache

import pytest
import yaml
from frozendict import frozendict

from lexique.lexical_structures.Blocks import Blocks
from pfmg.lexique.morpheme import Circumfix
from lexique.lexical_structures.Phonology import Phonology
from lexique.lexical_structures.Suffix import Suffix


@pytest.fixture(scope="module")
def fx_phonology() -> Phonology:
    yield phonology()


@cache
def phonology():
    return Phonology(
        apophonies=frozendict(
            Ø="i", i="a", a="u",
            u="u", e="o", o="o"
        ),
        mutations=frozendict(
            p="p", t="p", k="t", b="p", d="b",
            g="d", m="m", n="m", N="n", f="f",
            s="f", S="s", v="f", z="v", Z="z",
            r="w", l="r", j="w", w="w"
        ),
        derives=frozendict(A="V", D="C"),
        consonnes=frozenset("ptkbdgmnNfsSvzZrljw"),
        voyelles=frozenset("iueoa")
    )


@pytest.mark.parametrize("blocks, expected", [
    ({"source": {"N": [{"genre=m": "X+s"}]},
      "destination": {"N": [{"cas=erg": "a+X+s"}]}},
     ({"N": [[Suffix(rule="X+s", sigma=frozendict(genre="m"), phonology=phonology())]]},
      {"N": [[Circumfix(rule="a+X+s", sigma=frozendict(cas="erg"), phonology=phonology())]]})),])
def test_blocks(fx_phonology, tmp_path, blocks, expected):
    with open(tmp_path / "Phonology.yaml", mode="w", encoding="utf8") as file_handler:
        yaml.dump(vars(fx_phonology), file_handler)

    with open(tmp_path / "Blocks.yaml", mode="w", encoding="utf8") as file_handler:
        yaml.dump(blocks, file_handler)
    blocks = Blocks.from_disk(tmp_path / "Blocks.yaml")
    assert blocks.source.data == expected[0]
    assert blocks.destination.data == expected[1]


@pytest.mark.parametrize("blocks, pos, sigma, expected", [
    ({"source": {"N": [{"genre=m": "X+s"}]},
      "destination": {"N": [{"cas=erg": "a+X+s"}]}},
     "N",
     {"source": frozendict(genre="m"),
      "destination": frozendict(cas="erg")},
     {"source": [Suffix(rule="X+s", sigma=frozendict(genre="m"), phonology=phonology())],
      "destination": [Circumfix(rule="a+X+s", sigma=frozendict(cas="erg"), phonology=phonology())]}),
])
def test___call__(fx_phonology, tmp_path, blocks, pos, sigma, expected):
    with open(tmp_path / "Phonology.yaml", mode="w", encoding="utf8") as file_handler:
        yaml.dump(vars(fx_phonology), file_handler)

    with open(tmp_path / "Blocks.yaml", mode="w", encoding="utf8") as file_handler:
        yaml.dump(blocks, file_handler)
    blocks = Blocks.from_disk(tmp_path / "Blocks.yaml")
    assert blocks(pos, sigma) == expected


def test_errors():
    with pytest.raises(AssertionError):
        Blocks(source={},
               destination={"N": {}})

    with pytest.raises(AssertionError):
        Blocks(source={"N": {}},
               destination={})