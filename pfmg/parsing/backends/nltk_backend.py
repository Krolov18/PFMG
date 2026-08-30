"""NLTK chart parser backend."""

from collections.abc import Iterator
from typing import Any

from pfmg.parsing.backends.parse_backend import ParseBackend

_REQUIRED_CORPORA = ("wordnet",)


def ensure_nltk_data() -> None:
    """Download required NLTK corpora if missing (e.g. wordnet for parsing)."""
    import nltk

    for resource in _REQUIRED_CORPORA:
        try:
            nltk.data.find(f"corpora/{resource}")
        except LookupError:
            nltk.download(resource, quiet=True)


class NltkParseBackend(ParseBackend):
    """Chart parser backed by NLTK ``FeatureEarleyChartParser``."""

    def create(self, grammar_string: str) -> Any:
        """Build a FeatureEarleyChartParser from a grammar string."""
        ensure_nltk_data()
        import nltk.grammar
        from nltk import FeatureEarleyChartParser

        grammar = nltk.grammar.FeatureGrammar.fromstring(grammar_string)
        return FeatureEarleyChartParser(grammar)

    def parse_one(self, handle: Any, tokens: list[str]) -> Any | None:
        """Return the first parse tree for *tokens*, or None."""
        return handle.parse_one(tokens)

    def parse_all(self, handle: Any, tokens: list[str]) -> Iterator[Any]:
        """Yield all parse trees for *tokens*."""
        return handle.parse_all(tokens)

    def parse_sents(
        self, handle: Any, token_lists: list[list[str]]
    ) -> Iterator[Iterator[Any]]:
        """Yield parse iterators for each token list in *token_lists*."""
        return handle.parse_sents(token_lists)

    def grammar_text(self, handle: Any) -> str:
        """Return the grammar string backing *handle*."""
        return str(handle.grammar())
