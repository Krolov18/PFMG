"""Tests that NLTK is not loaded at package import time."""

import subprocess
import sys
from unittest.mock import MagicMock, patch

from pfmg.parsing.backends.nltk_backend import ensure_nltk_data
from pfmg.parsing.features.Features import Features
from pfmg.parsing.features.Percolation import Percolation
from pfmg.parsing.grammar.Grammar import Grammar
from pfmg.parsing.parser.Parser import Parser
from pfmg.parsing.production.Production import Production


def test_import_pfmg_does_not_touch_nltk() -> None:
    """Import pfmg must not import or download NLTK data."""
    script = (
        "import sys\n"
        "import pfmg\n"
        "assert 'nltk' not in sys.modules\n"
    )
    result = subprocess.run(  # noqa: S603
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr or result.stdout


def test_parser_creation_triggers_nltk_data_check() -> None:
    """Building a Parser should ensure NLTK corpora are available."""
    prod = Production(
        lhs="S",
        phrases=['"a"'],
        agreements=Features(data=[{}]),
        percolation=Percolation(data={}),
    )
    grammar = Grammar(start="S", productions=[prod])
    lexicon = MagicMock()
    lexicon.to_translation.return_value = ""
    lexicon.to_validation.return_value = ""

    with patch("pfmg.parsing.backends.nltk_backend.ensure_nltk_data") as mock_ensure:
        Parser(lexique=lexicon, grammar=grammar, how="translation")
        mock_ensure.assert_called_once()


def test_ensure_nltk_data_is_idempotent() -> None:
    """ensure_nltk_data can be called without error when corpora exist."""
    ensure_nltk_data()
