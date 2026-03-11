"""Context-free grammar with a start symbol and a list of productions."""

from dataclasses import dataclass

from pfmg.lexique.stem_space.StemSpace import StemSpace
from pfmg.parsing.production import Production


@dataclass
class Grammar:
    """A grammar: start symbol and list of Production rules.

    Attributes:
        start: Start symbol of the grammar.
        productions: List of Production rules.

    """

    start: str
    productions: list[Production]

    def to_nltk(self, term: StemSpace | str | None = None) -> str:
        """Return this grammar as a string parseable by NLTK FeatureGrammar.fromstring.

        Args:
            term: Unused in this implementation.

        Returns:
            str: Grammar string for NLTK.

        """
        return "\n\n".join(
            (
                f"% start {self.start}",
                "\n".join(x.to_nltk() for x in self.productions),
            )
        )
