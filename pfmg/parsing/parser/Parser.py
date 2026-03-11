"""Parser combining a lexicon, grammar and tokenizer (NLTK FeatureEarleyChartParser)."""

from dataclasses import dataclass
from pathlib import Path

import nltk.grammar
from nltk import FeatureEarleyChartParser, Tree

from pfmg.lexique.lexicon import Lexicon
from pfmg.parsing.grammar import Grammar
from pfmg.parsing.parsable.MixinParseParsable import MixinParseParsable
from pfmg.parsing.tokenizer import ABCTokenizer, new_tokenizer


@dataclass
class Parser(MixinParseParsable):
    """Parses input using a lexicon, a grammar and a tokenizer (NLTK-based).

    Attributes:
        lexique: Lexicon for lexical rules.
        grammar: Grammar for parsing.
        how: Mode name ("translation" or "validation") for lexicon export.

    """

    lexique: Lexicon
    grammar: Grammar
    how: str

    def __post_init__(self) -> None:
        """Build NLTK FeatureGrammar and parser from grammar and lexicon."""
        g = self.grammar.to_nltk()
        grammar = nltk.grammar.FeatureGrammar.fromstring(
            "\n\n".join((g, getattr(self.lexique, f"to_{self.how}")()))
        )

        self.tokenizer: ABCTokenizer = new_tokenizer(id_tokenizer="Space")
        self.parserj = FeatureEarleyChartParser(grammar)

    def to_file(self, path: str | Path) -> None:
        """Write the grammar content to a text file.

        Args:
            path: Output path for the grammar file.

        """
        path = Path(path)
        with open(path, mode="w") as fh:
            fh.write(str(self.parserj.grammar()))

    def __tokenize(self, data: str | list[str]) -> list[str] | list[list[str]]:
        """Tokenize text (string or list of strings) using the configured tokenizer.

        Args:
            data: A single sentence or list of sentences.

        Returns:
            list[str] | list[list[str]]: Tokens for one sentence or list of token lists.

        """
        match data:
            case str():
                return self.tokenizer(data)
            case list():
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
            for x in self.__tokenize(data)
            if (result := self.parserj.parse_one(x)) is not None
        ]

    def _parse_str_all(self, data: str) -> list[Tree]:
        """Return all parse trees for the given string.

        Args:
            data: Input sentence.

        Returns:
            list[Tree]: All NLTK parse trees for the sentence.

        """
        return list(self.parserj.parse_all(self.__tokenize(data)))

    def _parse_list_all(self, data: list[str]) -> list[Tree]:
        """Return all parse trees for each sentence in data.

        Args:
            data: List of sentences.

        Returns:
            list[Tree]: All parse trees for all sentences (flattened).

        """
        output = []
        for parsing in self.parserj.parse_sents(self.__tokenize(data)):
            output.extend(parsing)
        return output
