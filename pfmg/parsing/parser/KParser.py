"""Two-phase parser: translate then validate (KParser loads from YAML and holds translator + validator)."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Literal, Self, overload

from pfmg.external.reader import ABCReader
from pfmg.parsing.backends import is_parse_tree
from pfmg.parsing.parsable.MixinParseParsable import MixinParseParsable
from pfmg.parsing.parser.Parser import Parser

if TYPE_CHECKING:
    from pfmg.parsing.grammar_bundle import GrammarBundle


def flatten_translation(value: str | tuple) -> Iterator[str]:
    """Yield the words of a ``translation`` feature, however deeply nested.

    A rule builds its ``translation`` by collecting the ones of its
    constituents, so a rule whose constituent is itself a nonterminal ends up
    with a tuple of tuples. Only the leaves are words.

    Args:
        value: A word, or a (possibly nested) tuple of translations.

    Yields:
        str: Each word, left to right.

    """
    if isinstance(value, str):
        yield value
    else:
        for item in value:
            yield from flatten_translation(item)


@dataclass
class KParser(ABCReader, MixinParseParsable):
    """Two-phase parser: parses once to translate, then again to validate the translation.

    Attributes:
        translator: Parser for the translation phase.
        validator: Parser for the validation phase.

    """

    translator: Parser
    validator: Parser

    @classmethod
    def from_bundle(cls, bundle: GrammarBundle) -> Self:
        """Build a KParser from a loaded :class:`GrammarBundle`.

        Args:
            bundle: Loaded lexicon and grammar pair.

        Returns:
            KParser: Instance with translator and validator parsers.

        """
        return cls(
            translator=Parser(
                lexique=bundle.lexicon,
                grammar=bundle.grammar.translator,
                how="translation",
            ),
            validator=Parser(
                lexique=bundle.lexicon,
                grammar=bundle.grammar.validator,
                how="validation",
            ),
        )

    @classmethod
    def from_yaml(cls, path: str | Path) -> Self:
        """Load lexicon and grammars from a directory containing MorphoSyntax.yaml and lexicon data.

        Args:
            path: Path to the directory (must contain MorphoSyntax.yaml and lexicon data).

        Returns:
            KParser: Instance with translator and validator parsers.

        """
        from pfmg.parsing.grammar_bundle import GrammarBundle

        return cls.from_bundle(GrammarBundle.from_directory(path))

    def to_file(
        self, path: str | Path, id_grammar: Literal["validator", "translator"]
    ) -> None:
        """Write the chosen grammar to a text file.

        Args:
            path: Output path for the file.
            id_grammar: Which grammar to export ("validator" or "translator").

        """
        getattr(self, id_grammar).to_file(path)

    @overload
    def parse(self, data: str, keep: Literal["first"]) -> str: ...

    @overload
    def parse(self, data: str | list[str], keep: Literal["all"]) -> list[str]: ...

    @overload
    def parse(self, data: list[str], keep: Literal["first", "all"]) -> list[str]: ...

    def parse(self, data, keep) -> str | list[str]:
        """Parse input: translate then validate; return first or all results.

        Args:
            data: String or list of strings to parse.
            keep: "first" for one result per input, "all" for all parses.

        Returns:
            str | list[str]: Parsed result(s) (string or list of strings).

        """
        translation: str | list[str]
        try:
            tree = self.translator.parse(data, keep)
            match tree:
                case _ if is_parse_tree(tree):
                    translation = " ".join(
                        flatten_translation(tree.label()["translation"])
                    )
                case Iterator() | list():
                    translation = [
                        " ".join(flatten_translation(x.label()["translation"]))
                        for x in tree
                    ]
                case _:
                    raise TypeError
        except Exception:  # noqa BLE001
            message = f"'{data}' n'est pas reconnu par le traducteur."
            raise ValueError(message) from None
        else:
            try:
                self.validator.parse(translation, keep)
            except Exception:  # noqa BLE001
                message = (
                    f"'{data}' a été correctement traduite mais le "
                    f"validateur l'a refusée. Revoyez le champ "
                    f"'translation'."
                )
                raise ValueError(message) from None
            else:
                return translation
