# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
from functools import cache
from collections.abc import Generator

import pytest
import yaml
from frozendict import frozendict

from pfmg.lexique.block.Blocks import Blocks
from pfmg.lexique.block.BlockEntry import BlockEntry
from pfmg.lexique.block.Desinence import Desinence
from pfmg.lexique.glose.Sigma import Sigma
from pfmg.lexique.morpheme.Circumfix import Circumfix
from pfmg.lexique.phonology.Phonology import Phonology
from pfmg.lexique.morpheme.Suffix import Suffix


@pytest.fixture(scope="module")
def fx_phonology() -> Generator[Phonology, None, None]:
    yield phonology()


@cache
def phonology() -> Phonology:
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
    ({"N": {"source": [{"genre=m": "X+s"}], "destination": [{"cas=erg": "a+X+s"}]}},
     ({"N": Blocks([[Suffix(rule="X+s", sigma=frozendict(genre="m"), phonology=phonology())]])},
      {"N": Blocks([[Circumfix(rule="a+X+s", sigma=frozendict(cas="erg"), phonology=phonology())]])})),])
def test_blocks(fx_phonology, tmp_path, blocks, expected):
    with open(tmp_path / "Phonology.yaml", mode="w", encoding="utf8") as file_handler:
        yaml.safe_dump(fx_phonology.to_dict(), file_handler)

    with open(tmp_path / "Blocks.yaml", mode="w", encoding="utf8") as file_handler:
        yaml.safe_dump(blocks, file_handler)
    blocks = BlockEntry.from_yaml(tmp_path / "Blocks.yaml")
    assert blocks.source == expected[0]
    assert blocks.destination == expected[1]


@pytest.mark.parametrize("blocks, pos, sigma, expected", [
    ({"N": {"source":      [{"genre=m": "X+s"}],
            "destination": [{"cas=erg": "a+X+s"}]}},
     "N",
     {"source":      frozendict(genre="m"),
      "destination": frozendict(cas="erg")},
     Desinence(
         source=[Suffix(rule="X+s", sigma=frozendict(genre="m"),
                        phonology=phonology())],
         destination=[Circumfix(rule="a+X+s", sigma=frozendict(cas="erg"),
                                phonology=phonology())])),
])
def test___call__(fx_phonology, tmp_path, blocks, pos, sigma, expected):
    with open(tmp_path / "Phonology.yaml", mode="w", encoding="utf8") as file_handler:
        yaml.safe_dump(fx_phonology.to_dict(), file_handler)

    with open(tmp_path / "Blocks.yaml", mode="w", encoding="utf8") as file_handler:
        yaml.safe_dump(blocks, file_handler)
    blocks = BlockEntry.from_yaml(tmp_path / "Blocks.yaml")
    assert blocks(pos, Sigma(**sigma)) == expected


def test_errors():
    with pytest.raises(AssertionError):
        BlockEntry(source={},
                   destination={"N": Blocks([])})

    with pytest.raises(AssertionError):
        BlockEntry(source={"N": Blocks([])},
                   destination={})