"""Parser combining a lexicon, grammar and tokenizer (NLTK FeatureEarleyChartParser)."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

from pfmg.lexique.lexicon import Lexicon
from pfmg.parsing.backends import NltkParseBackend, ParseBackend
from pfmg.parsing.grammar import Grammar
from pfmg.parsing.parsable.MixinParseParsable import MixinParseParsable
from pfmg.parsing.tokenizer import ABCTokenizer, new_tokenizer

if TYPE_CHECKING:
    from nltk import Tree


@dataclass
class Parser(MixinParseParsable):
    """Parses input using a lexicon, a grammar and a tokenizer (NLTK-based).

    Attributes:
        lexique: Lexicon for lexical rules.
        grammar: Grammar for parsing.
        how: Mode name ("translation" or "validation") for lexicon export.
        backend: Parse backend; defaults to NLTK when None.

    """

    lexique: Lexicon
    grammar: Grammar
    how: str
    backend: ParseBackend | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        """Build NLTK FeatureGrammar and parser from grammar and lexicon."""
        backend = self.backend or NltkParseBackend()
        g = self.grammar.to_nltk()
        grammar_string = "\n\n".join((g, getattr(self.lexique, f"to_{self.how}")()))

        self._backend = backend
        self.tokenizer: ABCTokenizer = new_tokenizer(id_tokenizer="Space")
        self.parserj = backend.create(grammar_string)

    def to_file(self, path: str | Path) -> None:
        """Write the grammar content to a text file.

        Args:
            path: Output path for the grammar file.

        """
        path = Path(path)
        with open(path, mode="w") as fh:
            fh.write(self._backend.grammar_text(self.parserj))

    def _tokenize_one(self, data: str) -> list[str]:
        """Tokenize a single sentence."""
        return self.tokenizer(data)

    def _tokenize_many(self, data: list[str]) -> list[list[str]]:
        """Tokenize each sentence in *data*."""
        return [self.tokenizer(d) for d in data]

    def _parse_str_first(self, data: str) -> Tree:
        """Return the first parse tree for the given string.

        Args:
            data: Input sentence.

        Returns:
            Tree: First NLTK parse tree.

        """
        return self._parse_str_all(data)[0]

    def _parse_list_first(self, data: list[str]) -> list[Tree]:
        """Return the first parse tree for each sentence in data.

        Args:
            data: List of sentences.

        Returns:
            list[Tree]: First NLTK tree per sentence.

        """
        return [
            result
            for x in self._tokenize_many(data)
            if (result := self._backend.parse_one(self.parserj, x)) is not None
        ]

    def _parse_str_all(self, data: str) -> list[Tree]:
        """Return all parse trees for the given string.

        Args:
            data: Input sentence.

        Returns:
            list[Tree]: All NLTK parse trees for the sentence.

        """
        return list(self._backend.parse_all(self.parserj, self._tokenize_one(data)))

    def _parse_list_all(self, data: list[str]) -> list[Tree]:
        """Return all parse trees for each sentence in data.

        Args:
            data: List of sentences.

        Returns:
            list[Tree]: All parse trees for all sentences (flattened).

        """
        output: list[Any] = []
        for parsing in self._backend.parse_sents(
            self.parserj, self._tokenize_many(data)
        ):
            output.extend(parsing)
        return output
