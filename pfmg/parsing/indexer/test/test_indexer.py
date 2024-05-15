import pytest

from pfmg.lexique.lexicon import Lexicon
from pfmg.parsing.indexer import new_indexer
from pfmg.utils.paths import get_project_path


@pytest.fixture()
def fx_lexicon():
    config_path = get_project_path() / "examples" / "data"
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
     [['6376', '6378', '6380'],
      ['6598', '6600', '6602', '6604', '6606', '6608']]),
])
def test_indexer(fx_lexicon, tokens, expected) -> None:
    indexer = new_indexer(id_indexer="Desamb", lexicon=fx_lexicon)
    actual = indexer(tokens)
    assert actual == expected
