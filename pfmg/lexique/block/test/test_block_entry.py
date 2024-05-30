# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import pytest
import yaml
from frozendict import frozendict

from pfmg.lexique.block.Blocks import Blocks
from pfmg.lexique.block.BlockEntry import BlockEntry
from pfmg.lexique.block.Desinence import Desinence
from pfmg.lexique.sigma.Sigma import Sigma
from pfmg.lexique.morpheme.Circumfix import Circumfix
from pfmg.lexique.morpheme.Suffix import Suffix
from pfmg.conftest import fx_df_phonology


@pytest.mark.parametrize("blocks", [
    {"N": {"source": [{"genre=m": "X+s"}],
           "destination": [{"cas=erg": "a+X+s"}]}}
])
def test_blocks(fx_df_phonology, tmp_path, blocks):
    expected = (
        {"N": Blocks([[Suffix(rule="X+s", sigma=frozendict(genre="m"), phonology=fx_df_phonology)]])},
        {"N": Blocks([[Circumfix(rule="a+X+s", sigma=frozendict(cas="erg"), phonology=fx_df_phonology)]])},)

    with open(tmp_path / "Phonology.yaml", mode="w", encoding="utf8") as file_handler:
        yaml.safe_dump(fx_df_phonology.to_dict(), file_handler)

    with open(tmp_path / "Blocks.yaml", mode="w", encoding="utf8") as file_handler:
        yaml.safe_dump(blocks, file_handler)
    blocks = BlockEntry.from_yaml(tmp_path / "Blocks.yaml")
    assert blocks.source == expected[0]
    assert blocks.destination == expected[1]


@pytest.mark.parametrize("blocks, pos, sigma", [
    ({"N": {"source":      [{"genre=m": "X+s"}],
            "destination": [{"cas=erg": "a+X+s"}]}},
     "N",
     {"source":      frozendict(genre="m"),
      "destination": frozendict(cas="erg")}),
])
def test___call__(fx_df_phonology, tmp_path, blocks, pos, sigma):
    expected = Desinence(
        source=[Suffix(rule="X+s", sigma=frozendict(genre="m"), phonology=fx_df_phonology)],
        destination=[Circumfix(rule="a+X+s", sigma=frozendict(cas="erg"), phonology=fx_df_phonology)])

    with open(tmp_path / "Phonology.yaml", mode="w", encoding="utf8") as file_handler:
        yaml.safe_dump(fx_df_phonology.to_dict(), file_handler)

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
