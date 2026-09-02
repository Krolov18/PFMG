"""Parser combining a lexicon, grammar and tokenizer (NLTK FeatureEarleyChartParser)."""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

from pfmg.parsing.backends import NltkParseBackend, ParseBackend
from pfmg.parsing.grammar import Grammar
from pfmg.parsing.indexer import ABCindexer, new_indexer
from pfmg.parsing.lexical_grammar import LexicalGrammarExporter
from pfmg.parsing.lexicon_index import RealizedLexicon
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
        indexer: Maps each token to its candidate terminals; defaults to a
            Desamb indexer over `lexique`, which is what the generated
            grammars expect since their terminals are Forme indexes.

    """

    lexique: RealizedLexicon
    grammar: Grammar
    how: str
    backend: ParseBackend | None = field(default=None, repr=False)
    tokenizer: ABCTokenizer | None = field(default=None, repr=False)
    indexer: ABCindexer | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        """Build NLTK FeatureGrammar and parser from grammar and lexicon."""
        backend = self.backend or NltkParseBackend()
        g = self.grammar.to_nltk()
        lexical = LexicalGrammarExporter().export_lexicon(self.lexique, self.how)
        grammar_string = "\n\n".join((g, lexical))

        self._backend = backend
        self.tokenizer = self.tokenizer or new_tokenizer(id_tokenizer="Space")
        self._indexer: ABCindexer = self.indexer or new_indexer(
            id_indexer="Desamb", lexicon=self.lexique, how=self.how
        )
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
        assert self.tokenizer is not None
        return self.tokenizer(data)

    def _index_one(self, data: str) -> list[list[str]]:
        """Return every terminal sequence a sentence can stand for.

        A token is morphologically ambiguous: the indexer maps it to all the
        Forme indexes sharing that spelling. The grammar only accepts a flat
        token list, so each combination is parsed separately.

        Args:
            data: Input sentence.

        Returns:
            list[list[str]]: Candidate terminal sequences.

        """
        candidates = self._indexer(self._tokenize_one(data))
        return [list(sequence) for sequence in itertools.product(*candidates)]

    def _index_many(self, data: list[str]) -> list[list[str]]:
        """Return the candidate terminal sequences of every sentence in *data*."""
        return [sequence for d in data for sequence in self._index_one(d)]

    def _parse_str_first(self, data: str) -> Tree:
        """Return the first parse tree for the given string.

        Args:
            data: Input sentence.

        Returns:
            Tree: First NLTK parse tree.

        """
        for sequence in self._index_one(data):
            result = self._backend.parse_one(self.parserj, sequence)
            if result is not None:
                return result
        message = f"Aucune analyse pour '{data}'."
        raise ValueError(message)

    def _parse_list_first(self, data: list[str]) -> list[Tree]:
        """Return the first parse tree for each sentence in data.

        Args:
            data: List of sentences.

        Returns:
            list[Tree]: First NLTK tree per sentence.

        """
        output: list[Tree] = []
        for d in data:
            for sequence in self._index_one(d):
                result = self._backend.parse_one(self.parserj, sequence)
                if result is not None:
                    output.append(result)
                    break
        return output

    def _parse_str_all(self, data: str) -> list[Tree]:
        """Return all parse trees for the given string.

        Args:
            data: Input sentence.

        Returns:
            list[Tree]: All NLTK parse trees for the sentence.

        """
        return self._parse_sequences(self._index_one(data))

    def _parse_list_all(self, data: list[str]) -> list[Tree]:
        """Return all parse trees for each sentence in data.

        Args:
            data: List of sentences.

        Returns:
            list[Tree]: All parse trees for all sentences (flattened).

        """
        return self._parse_sequences(self._index_many(data))

    def _parse_sequences(self, sequences: list[list[str]]) -> list[Tree]:
        """Return every parse tree of every terminal sequence, flattened."""
        output: list[Any] = []
        for parsing in self._backend.parse_sents(self.parserj, sequences):
            output.extend(parsing)
        return output
