"""Interface for equality (rule + sigma)."""

from abc import ABC, abstractmethod
from re import Match

from frozendict import frozendict


class ABCEquality(ABC):
    """Abstract base for objects that support equality via rule and sigma."""

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        """Return True if this object is equal to other (same rule and compatible sigma).

        Args:
            other: Object to compare with.

        Returns:
            bool: True if equal.

        """

    @abstractmethod
    def get_rule(self) -> Match:
        """Return the regex match object for the rule.

        Returns:
            Match: The compiled rule match object.

        """

    @abstractmethod
    def get_sigma(self) -> frozendict:
        """Return the element's sigma (feature/property dict).

        Returns:
            frozendict: Feature/property mapping.

        """
