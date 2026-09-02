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

    # each Lexicon numbers its own forms, starting at 0
    (["le", "bruit"],
     [["18", "20", "22"],
      ["36"]]),
])
def test_indexer(fx_lexicon, tokens, expected) -> None:
    indexer = new_indexer(id_indexer="Desamb", lexicon=fx_lexicon)
    actual = indexer(tokens)
    assert actual == expected


def test_indexer_is_deterministic(fx_lexicon) -> None:
    """Two Lexicon loaded from the same directory hand out the same indexes."""
    other = Lexicon.from_yaml(
        get_project_path() / "pfmg" / "parsing" / "indexer" / "test" / "data"
    )

    assert new_indexer(id_indexer="Desamb", lexicon=fx_lexicon)(["le"]) == new_indexer(
        id_indexer="Desamb", lexicon=other
    )(["le"])


def test_indexer_validation_side(fx_lexicon) -> None:
    """how="validation" looks tokens up among the destination forms."""
    indexer = new_indexer(id_indexer="Desamb", lexicon=fx_lexicon, how="validation")
    destination = next(iter(fx_lexicon)).destination

    assert str(destination.index) in indexer([destination.to_string()])[0]


def test_identity_indexer() -> None:
    """The identity indexer keeps tokens as they are."""
    assert new_indexer(id_indexer="Identity")(["le", "bruit"]) == [["le"], ["bruit"]]
