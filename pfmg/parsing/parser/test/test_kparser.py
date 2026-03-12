"""Tests for KParser (two-phase parser: translate then validate)."""

from pathlib import Path
from unittest.mock import MagicMock

import pytest
from nltk import Tree

from pfmg.parsing.parser.KParser import KParser
from pfmg.parsing.parser.Parser import Parser


def _tree_with_translation(translation: list[str]) -> Tree:
    """Build an NLTK Tree subclass whose label() returns a dict with 'translation' (KParser expects this)."""
    class TreeWithTranslation(Tree):
        def __init__(self, trans: list[str]) -> None:
            super().__init__("S", [])
            self._translation = trans

        def label(self) -> dict:
            return {"translation": self._translation}

    return TreeWithTranslation(translation)


@pytest.fixture
def kparser_mocked() -> KParser:
    """KParser with mock translator and validator (parse succeeds)."""
    translator = MagicMock(spec=Parser)
    translator.parse.return_value = _tree_with_translation(["hello", "world"])
    validator = MagicMock(spec=Parser)
    validator.parse.return_value = _tree_with_translation(["hello", "world"])
    return KParser(translator=translator, validator=validator)


@pytest.fixture
def kparser_translator_fails() -> KParser:
    """KParser whose translator.parse raises."""
    translator = MagicMock(spec=Parser)
    translator.parse.side_effect = RuntimeError("not recognized")
    validator = MagicMock(spec=Parser)
    return KParser(translator=translator, validator=validator)


@pytest.fixture
def kparser_validator_fails() -> KParser:
    """KParser whose validator.parse raises after translator succeeds."""
    translator = MagicMock(spec=Parser)
    translator.parse.return_value = _tree_with_translation(["ok"])
    validator = MagicMock(spec=Parser)
    validator.parse.side_effect = RuntimeError("invalid")
    return KParser(translator=translator, validator=validator)


@pytest.mark.parametrize(
    "params, expected",
    [
        ({"data": "x", "keep": "first"}, "hello world"),
        ({"data": "x", "keep": "all"}, "hello world"),
    ],
)
def test_kparser_parse_success_single_tree(kparser_mocked, params, expected) -> None:
    """When translator returns one Tree and validator succeeds, parse returns translation."""
    result = kparser_mocked.parse(data=params["data"], keep=params["keep"])
    assert result == expected


def test_kparser_parse_success_list_of_trees() -> None:
    """When translator returns list of Trees (keep='all'), parse returns list of strings."""
    translator = MagicMock(spec=Parser)
    translator.parse.return_value = [
        _tree_with_translation(["a", "b"]),
        _tree_with_translation(["c", "d"]),
    ]
    validator = MagicMock(spec=Parser)
    kparser = KParser(translator=translator, validator=validator)
    result = kparser.parse(data="x", keep="all")
    assert result == ["a b", "c d"]


@pytest.mark.parametrize(
    "params, expected",
    [
        ({"data": "bad", "keep": "first"}, ValueError),
        ({"data": "bad", "keep": "all"}, ValueError),
    ],
)
def test_kparser_parse_translator_raises(kparser_translator_fails, params, expected) -> None:
    """When translator fails, parse raises ValueError with message about traducteur."""
    with pytest.raises(expected) as exc_info:
        kparser_translator_fails.parse(data=params["data"], keep=params["keep"])
    assert "traducteur" in str(exc_info.value) or "n'est pas reconnu" in str(exc_info.value)


def test_kparser_parse_translator_returns_invalid_type() -> None:
    """When translator returns neither Tree nor list/Iterator, parse raises ValueError (via TypeError)."""
    translator = MagicMock(spec=Parser)
    translator.parse.return_value = "not a tree"  # invalid type
    validator = MagicMock(spec=Parser)
    kparser = KParser(translator=translator, validator=validator)
    with pytest.raises(ValueError) as exc_info:
        kparser.parse(data="x", keep="first")
    assert "traducteur" in str(exc_info.value) or "n'est pas reconnu" in str(exc_info.value)


@pytest.mark.parametrize(
    "params, expected",
    [
        ({"data": "x", "keep": "first"}, ValueError),
        ({"data": "x", "keep": "all"}, ValueError),
    ],
)
def test_kparser_parse_validator_raises(kparser_validator_fails, params, expected) -> None:
    """When validator fails after translation, parse raises ValueError about validateur."""
    with pytest.raises(expected) as exc_info:
        kparser_validator_fails.parse(data=params["data"], keep=params["keep"])
    assert "validateur" in str(exc_info.value) or "refusée" in str(exc_info.value)


@pytest.mark.parametrize(
    "params, expected",
    [
        ({"path": "out.txt", "id_grammar": "translator"}, None),
        ({"path": "out.txt", "id_grammar": "validator"}, None),
    ],
)
def test_kparser_to_file(kparser_mocked, tmp_path: Path, params, expected) -> None:
    """to_file delegates to the chosen grammar's to_file."""
    path = tmp_path / params["path"]
    kparser_mocked.to_file(path, id_grammar=params["id_grammar"])
    getattr(kparser_mocked, params["id_grammar"]).to_file.assert_called_once_with(path)
