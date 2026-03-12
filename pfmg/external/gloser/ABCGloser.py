"""Interface for objects that produce a formatted glose (gloss) string."""

from abc import ABC, abstractmethod

from pfmg.lexique.stem_space.StemSpace import StemSpace


class ABCGloser(ABC):
    """Abstract base for objects that can produce formatted glose strings."""

    @abstractmethod
    def to_glose(self, term: StemSpace | str | None = None) -> str:
        """Return the formatted glose for the given term (StemSpace, str, or None).

        Args:
            term: StemSpace, str, or None to get glose for.

        Returns:
            str: Formatted glose string.

        """
