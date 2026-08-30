"""Abstract parse backend (NLTK or test doubles)."""

from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import Any


def is_parse_tree(obj: object) -> bool:
    """Return True if *obj* looks like an NLTK parse tree."""
    label = getattr(obj, "label", None)
    return callable(label)


class ParseBackend(ABC):
    """Builds a chart parser from a grammar string and runs parse operations."""

    @abstractmethod
    def create(self, grammar_string: str) -> Any:
        """Create a parser handle from a FeatureGrammar string."""

    @abstractmethod
    def parse_one(self, handle: Any, tokens: list[str]) -> Any | None:
        """Return the first parse tree for *tokens*, or None."""

    @abstractmethod
    def parse_all(self, handle: Any, tokens: list[str]) -> Iterator[Any]:
        """Yield all parse trees for *tokens*."""

    @abstractmethod
    def parse_sents(
        self, handle: Any, token_lists: list[list[str]]
    ) -> Iterator[Iterator[Any]]:
        """Yield parse iterators for each token list in *token_lists*."""

    @abstractmethod
    def grammar_text(self, handle: Any) -> str:
        """Return the grammar string backing *handle*."""
