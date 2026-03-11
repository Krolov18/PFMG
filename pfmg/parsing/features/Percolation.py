"""Percolation (unified feature dict) for grammar productions."""

from dataclasses import dataclass

from pfmg.parsing.features.FeatureMixin import FeatureMixin
from pfmg.parsing.features.utils import FeatureReader


@dataclass
class Percolation(FeatureMixin):
    """Unified feature dict for a production (NLTK-style percolation).

    Attributes:
        data: Unified feature dict for the production.

    """

    data: dict

    @staticmethod
    def unify(data: list[dict]) -> dict:
        """Unify a list of feature dicts into one using NLTK unify.

        Args:
            data: List of feature dicts to unify.

        Returns:
            dict: Single unified feature dict.

        """
        import functools as ft

        import nltk

        return ft.reduce(nltk.unify, data)

    def to_nltk(self) -> str:
        """Return NLTK-style percolation string (key=value, comma-separated).

        Returns:
            str: Comma-separated key=value string.

        """
        return ",".join(f"{key}={value}" for key, value in self.data.items())

    @classmethod
    def from_string(cls, data: str, target: str, phrase_len: int) -> Percolation:
        """Build Percolation from string (broadcast, parse, unify).

        Args:
            data: Feature specification string.
            target: Prefix for feature names.
            phrase_len: Number of phrases (for broadcast).

        Returns:
            Percolation: New Percolation instance.

        """
        data = Percolation.broadcast(data, phrase_len)
        features = FeatureReader().parse(data=data, target=target)
        return cls(data=cls.unify(features))

    def add_translation(self, translations: list[str]) -> None:
        """Add a single 'translation' key with comma-joined values.

        Args:
            translations: List of translation values to join.

        """
        values = ",".join(translations)
        self.data["translation"] = f"({values})"

    def update(self, other: Percolation) -> None:
        """Merge the other Percolation's data into this one.

        Args:
            other: Percolation whose data is merged into self.data.

        """
        self.data.update(other.data)
