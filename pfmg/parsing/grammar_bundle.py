"""Load a grammar data directory into lexicon and grammars."""

from dataclasses import dataclass
from pathlib import Path
from typing import Self

from pfmg.lexique.lexicon import Lexicon
from pfmg.parsing.grammar import KGrammar


@dataclass
class GrammarBundle:
    """Typed view of a grammar YAML directory (lexicon + MorphoSyntax grammars).

    Attributes:
        path: Root directory containing the five YAML files.
        lexicon: Loaded lexicon (Paradigm + Stems).
        grammar: Translator and validator grammars from MorphoSyntax.yaml.

    """

    path: Path
    lexicon: Lexicon
    grammar: KGrammar

    @classmethod
    def from_directory(cls, path: str | Path) -> Self:
        """Load all grammar objects from a YAML directory.

        Args:
            path: Directory containing Gloses, Blocks, Stems, Phonology, and
                MorphoSyntax YAML files.

        Returns:
            GrammarBundle: Loaded lexicon and grammar pair.

        """
        path = Path(path)
        assert path.exists() and path.is_dir()

        return cls(
            path=path,
            lexicon=Lexicon.from_yaml(path),
            grammar=KGrammar.from_yaml(path / "MorphoSyntax.yaml"),
        )
