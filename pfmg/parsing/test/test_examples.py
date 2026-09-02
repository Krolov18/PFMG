"""End-to-end tests of the example grammars shipped in `examples/`."""

import pytest

from pfmg.parsing.parser import KParser
from pfmg.utils.paths import get_project_path


@pytest.fixture(scope="module")
def fx_kparser() -> KParser:
    """KParser built from the `examples/data` grammar."""
    return KParser.from_yaml(get_project_path() / "examples" / "data")


def test_parse_all(fx_kparser) -> None:
    """"des garçons" translates to the Kalaba noun phrases of the example."""
    actual = fx_kparser.parse(data="des garçons", keep="all")

    assert sorted(actual) == [
        "tulo ze",
        "tulo zi",
        "tulo zo",
        "tulol zej",
        "tulol zij",
        "tulol zoj",
    ]


def test_parse_first(fx_kparser) -> None:
    """keep="first" returns one of the translations, as a string."""
    actual = fx_kparser.parse(data="des garçons", keep="first")

    assert isinstance(actual, str)
    assert actual in fx_kparser.parse(data="des garçons", keep="all")


def test_parse_list(fx_kparser) -> None:
    """A list of sentences is parsed sentence by sentence."""
    actual = fx_kparser.parse(data=["des garçons", "le bruit"], keep="all")

    assert "tulol zoj" in actual
    assert "apsanv ros" in actual


def test_parse_unknown_word(fx_kparser) -> None:
    """A word outside the lexicon is reported as untranslatable."""
    with pytest.raises(ValueError, match="n'est pas reconnu par le traducteur"):
        fx_kparser.parse(data="des zzzz", keep="all")
