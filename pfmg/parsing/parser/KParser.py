"""Two-phase parser: translate then validate (KParser loads from YAML and holds translator + validator)."""

from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Self, overload

from nltk import Tree

from pfmg.external.reader import ABCReader
from pfmg.parsing.parsable.MixinParseParsable import MixinParseParsable
from pfmg.parsing.parser import Parser


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
    def from_yaml(cls, path: str | Path) -> Self:
        """Load lexicon and grammars from a directory containing MorphoSyntax.yaml and lexicon data.

        Args:
            path: Path to the directory (must contain MorphoSyntax.yaml and lexicon data).

        Returns:
            KParser: Instance with translator and validator parsers.

        """
        path = Path(path)
        from pfmg.lexique.lexicon import Lexicon
        from pfmg.parsing.grammar import KGrammar

        assert path.exists() and path.is_dir()

        lexicon = Lexicon.from_yaml(path)
        grammar = KGrammar.from_yaml(path / "MorphoSyntax.yaml")
        return cls(
            translator=Parser(
                lexique=lexicon, grammar=grammar.translator, how="translation"
            ),
            validator=Parser(
                lexique=lexicon, grammar=grammar.validator, how="validation"
            ),
        )

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
                case Tree():
                    translation = " ".join(tree.label()["translation"])
                case Iterator() | list():
                    translation = [" ".join(x.label()["translation"]) for x in tree]
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
