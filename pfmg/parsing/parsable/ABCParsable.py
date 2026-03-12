"""Interface for parsers that consume strings.

Slightly diverges from NLTK's flow to work with our own structures;
a parser will eventually return Sentence instances rather than Trees.
"""

import enum
from abc import ABC, abstractmethod
from typing import Literal, overload

from pfmg.utils.abstract_factory import factory_method


class ABCParsable(ABC):
    """Interface for parsable objects.

    Implementations parse one or more sentences and produce an underlying Sentence structure.
    """

    @overload
    @abstractmethod
    def parse(self, data: str, keep: Literal["first"]) -> str: ...

    @overload
    @abstractmethod
    def parse(self, data: str | list[str], keep: Literal["all"]) -> list[str]: ...

    @overload
    @abstractmethod
    def parse(self, data: list[str], keep: Literal["first", "all"]) -> list[str]: ...

    @abstractmethod
    def parse(self, data, keep):
        """Parse input; return first or all results according to keep.

        Args:
            data: String or list of strings to parse.
            keep: "first" for one result, "all" for all parses.

        Returns:
            str | list[str]: Parsed result(s).

        """
        raise NotImplementedError


class IdParsableEnum(enum.Enum):
    """All possible identifiers for parsable implementations."""


def create_parsable(id_parsable: IdParsableEnum) -> ABCParsable:
    """Factory to build a parsable instance constrained by IdParsableEnum.

    Args:
        id_parsable: Which parser variant to create.

    Returns:
        ABCParsable: A parsable instance.

    """
    assert __package__ is not None
    return factory_method(
        concrete_product=f"{id_parsable.value}Parser", package=__package__
    )
