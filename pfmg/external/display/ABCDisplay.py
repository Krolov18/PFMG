"""Interface for string representation of objects."""

from abc import ABC, abstractmethod

from frozendict import frozendict

from pfmg.lexique.stem_space.StemSpace import StemSpace


class ABCDisplay(ABC):
    """Abstract base for objects that can be represented as strings."""

    @abstractmethod
    def to_string(self, term: StemSpace | str | None = None) -> str:
        """Return a string representation of this object.

        Args:
            term: Optional stem (StemSpace, str, or None) for the representation.

        Returns:
            str: String representation of the object.

        """

    @abstractmethod
    def get_sigma(self) -> frozendict:
        """Return the object's sigma (feature/property) mapping.

        Returns:
            frozendict: Immutable dict of properties.

        """
