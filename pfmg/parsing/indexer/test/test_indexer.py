# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import pytest

from pfmg.lexique.lexicon import Lexicon
from pfmg.parsing.indexer import new_indexer
from pfmg.utils.paths import get_project_path


@pytest.fixture()
def fx_lexicon():
    config_path = (
        get_project_path() / "pfmg" / "parsing" / "indexer" / "test" / "data"
    )
    return Lexicon.from_yaml(config_path)


@pytest.mark.parametrize("tokens, expected", [
    pytest.param(
        [],
        None,
        marks=pytest.mark.xfail(raises=AssertionError)),
    pytest.param(
        ["xcvkh:kv", "sdiojsd"],
        None,
        marks=pytest.mark.xfail(raises=AssertionError)),

    (["le", "bruit"],
     [["106", "108", "110"],
      ["124"]]),
])
def test_indexer(fx_lexicon, tokens, expected) -> None:
    indexer = new_indexer(id_indexer="Desamb", lexicon=fx_lexicon)
    actual = indexer(tokens)
    assert actual == expected
