"""Parser combining a lexicon, grammar and tokenizer (NLTK FeatureEarleyChartParser)."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

from pfmg.parsing.backends import NltkParseBackend, ParseBackend
from pfmg.parsing.grammar import Grammar
from pfmg.parsing.lexical_grammar import LexicalGrammarExporter
from pfmg.parsing.lexicon_lookup import RealizedLexicon
from pfmg.parsing.parsable.MixinParseParsable import MixinParseParsable
from pfmg.parsing.tokenizer import ABCTokenizer, new_tokenizer

if TYPE_CHECKING:
    from nltk import Tree


@dataclass
class Parser(MixinParseParsable):
    """Parses input using a lexicon, a grammar and a tokenizer (NLTK-based).

    The generated grammar has surface forms as terminals, so a sentence is
    parsed once: a spelling shared by several paradigm cells yields several
    lexical productions and the chart parser explores them together.

    Attributes:
        lexique: Lexicon for lexical rules.
        grammar: Grammar for parsing.
        how: Mode name ("translation" or "validation") for lexicon export.
        backend: Parse backend; defaults to NLTK when None.
        tokenizer: Tokenizer; defaults to a space tokenizer when None.

    """

    lexique: RealizedLexicon
    grammar: Grammar
    how: str
    backend: ParseBackend | None = field(default=None, repr=False)
    tokenizer: ABCTokenizer | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        """Build NLTK FeatureGrammar and parser from grammar and lexicon."""
        backend = self.backend or NltkParseBackend()
        g = self.grammar.to_nltk()
        lexical = LexicalGrammarExporter().export_lexicon(self.lexique, self.how)
        grammar_string = "\n\n".join((g, lexical))

        self._backend = backend
        self.tokenizer = self.tokenizer or new_tokenizer(id_tokenizer="Space")
        self.parserj = backend.create(grammar_string)

    def to_file(self, path: str | Path) -> None:
        """Write the grammar content to a text file.

        Args:
            path: Output path for the grammar file.

        """
        path = Path(path)
        with open(path, mode="w") as fh:
            fh.write(self._backend.grammar_text(self.parserj))

    def _tokens_one(self, data: str) -> list[str]:
        """Tokenize a sentence, rejecting words the lexicon does not realize.

        Args:
            data: Input sentence.

        Returns:
            list[str]: The tokens, all of them known terminals.

        """
        assert self.tokenizer is not None
        tokens = self.tokenizer(data)
        assert tokens

        unknown = [x for x in tokens if not self.lexique.knows(x, self.how)]
        assert not unknown, f"Ces mots sont inconnus du lexique : {unknown}"
        return tokens

    def _parse_str_first(self, data: str) -> Tree:
        """Return the first parse tree for the given string.

        Args:
            data: Input sentence.

        Returns:
            Tree: First NLTK parse tree.

        """
        result = self._backend.parse_one(self.parserj, self._tokens_one(data))
        if result is None:
            message = f"Aucune analyse pour '{data}'."
            raise ValueError(message)
        return result

    def _parse_list_first(self, data: list[str]) -> list[Tree]:
        """Return the first parse tree for each sentence in data.

        Args:
            data: List of sentences.

        Returns:
            list[Tree]: First NLTK tree per sentence.

        """
        output: list[Tree] = []
        for d in data:
            result = self._backend.parse_one(self.parserj, self._tokens_one(d))
            if result is not None:
                output.append(result)
        return output

    def _parse_str_all(self, data: str) -> list[Tree]:
        """Return all parse trees for the given string.

        Args:
            data: Input sentence.

        Returns:
            list[Tree]: All NLTK parse trees for the sentence.

        """
        return list(self._backend.parse_all(self.parserj, self._tokens_one(data)))

    def _parse_list_all(self, data: list[str]) -> list[Tree]:
        """Return all parse trees for each sentence in data.

        Args:
            data: List of sentences.

        Returns:
            list[Tree]: All parse trees for all sentences (flattened).

        """
        output: list[Any] = []
        sentences = [self._tokens_one(d) for d in data]
        for parsing in self._backend.parse_sents(self.parserj, sentences):
            output.extend(parsing)
        return output
