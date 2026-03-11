"""Morphosyntactic feature structure for a Forme (source + destination)."""

from dataclasses import dataclass

from frozendict import frozendict


@dataclass
class Sigma:
    """Morphosyntactic information for a Forme: source and destination feature dicts.

    Attributes:
        source: Source-language feature dict.
        destination: Destination-language feature dict.

    """

    source: frozendict[str, str]
    destination: frozendict[str, str]

    def __le__(self, other: Sigma) -> bool:
        """Return True if other's source/destination items are subsets of this one's.

        Args:
            other: Another Sigma to compare.

        Returns:
            bool: True if other is a subset (more specific) of self.

        """
        return (self.source.items() <= other.source.items()) and (
            self.destination.items() <= other.destination.items()
        )
