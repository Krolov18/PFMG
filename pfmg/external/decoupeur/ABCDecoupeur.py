"""Abstract interface for objects that produce a segmentation (decoupe) string."""

from abc import ABC, abstractmethod

from pfmg.lexique.stem_space.StemSpace import StemSpace


class ABCDecoupeur(ABC):
    """Abstract base for objects that can produce a segmentation string from a term."""

    @abstractmethod
    def to_decoupe(self, term: StemSpace | str | None = None) -> str:
        """Return the segmentation string for the given term (StemSpace, str, or None).

        Args:
            term: StemSpace, str, or None to get segmentation for.

        Returns:
            str: Segmentation string.

        """
