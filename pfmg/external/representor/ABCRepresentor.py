"""Abstract base for objects with string representation (repr/str)."""

from abc import ABC, abstractmethod


class ABCRepresentor(ABC):
    """Abstract base for objects that can be represented as strings (repr, str, _repr_params)."""

    @abstractmethod
    def __repr__(self) -> str:
        """Return a string representation of the object."""

    @abstractmethod
    def __str__(self) -> str:
        """Return a string form of the object."""

    @abstractmethod
    def _repr_params(self) -> str:
        """Return the parameter part used in repr (e.g. for ClassName(params))."""
