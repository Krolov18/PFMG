"""Production rule for context-free grammar with features and percolation."""

from dataclasses import dataclass
from typing import Literal

from pfmg.parsing.features.Features import Features
from pfmg.parsing.features.Percolation import Percolation


@dataclass
class Production:
    """A single production rule (LHS -> RHS) with feature agreements and percolation.

    Attributes:
        lhs: Left-hand side nonterminal symbol.
        phrases: Right-hand side phrase list (terminals and nonterminals).
        agreements: Feature agreements per RHS phrase.
        percolation: Unified feature dict for the production.

    """

    lhs: str
    phrases: list[str]
    agreements: Features
    percolation: Percolation

    def __post_init__(self) -> None:
        """Validate field types after dataclass initialization."""
        assert isinstance(self.lhs, str)
        assert isinstance(self.phrases, list)
        assert all(isinstance(x, str) for x in self.phrases)
        assert isinstance(self.agreements, Features)
        assert isinstance(self.percolation, Percolation)

    def to_nltk(self) -> str:
        """Return an NLTK FeatureGrammar-style string for this production.

        Returns:
            str: A string parseable by NLTK FeatureGrammar.fromstring.

        """
        template = "{lhs}[{features}] -> {rhs}"
        features = self.percolation.to_nltk()
        rhs = [
            f"{nt}[{feats}]" if nt.isupper() else nt
            for nt, feats in zip(self.phrases, self.agreements.to_nltk(), strict=True)
        ]
        return template.format(lhs=self.lhs, features=features, rhs=" ".join(rhs))

    def add_translation(self, indices: list[int]) -> None:
        """Add translation for the given phrase indices into agreements and percolation.

        Args:
            indices: List of phrase indices (0-based) to add translation for.

        """
        assert min(indices) >= 0
        assert max(indices) < len(self.phrases)

        self.agreements.add_translation(self.phrases)
        trads = self.agreements.get_translations()
        self.percolation.add_translation([trads[x] for x in indices])

    def update(self, production: Production, indices: list[int]) -> None:
        """Merge morphosyntactic information from the destination production into this one.

        Args:
            production: The destination production to merge from.
            indices: Phrase indices mapping source positions to destination for translation.

        """
        # Merge destination agreements
        for i_idx, value in enumerate(indices):
            self.agreements[value].update(production.agreements[i_idx])
        # Merge destination percolation
        self.percolation.update(production.percolation)

        # Add translation
        self.add_translation(indices)

    @classmethod
    def from_yaml(cls, data: dict, target: Literal["S", "D"]):
        """Build a Production from YAML dict (e.g. from MorphoSyntax.yaml).

        Args:
            data: Dict with keys lhs, phrases, agreements, percolations (and
                translations for target "S").
            target: "S" for source or "D" for destination.

        Returns:
            Production: A new Production instance.

        """
        return cls(
            lhs=data["lhs"],
            phrases=data["phrases"],
            agreements=Features.from_string(
                data=data["agreements"],
                target=target,
                phrase_len=len(data["phrases"]),
            ),
            percolation=Percolation.from_string(
                data=data["percolations"],
                target=target,
                phrase_len=len(data["phrases"]),
            ),
        )
