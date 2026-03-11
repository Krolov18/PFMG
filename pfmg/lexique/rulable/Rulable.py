"""Abstract base for objects that can be expressed as a lexical production."""

from abc import ABC, abstractmethod


class Rulable(ABC):
    """Abstract base for objects convertible to an NLTK lexical production string."""

    @abstractmethod
    def to_lexical(self) -> str:
        """Return this object as an NLTK-style lexical production rule.

        Returns:
            str: Lexical production string (NLTK format).

        """
