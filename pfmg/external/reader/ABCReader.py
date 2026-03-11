"""Abstract base for types loadable from YAML on disk."""

from abc import ABC, abstractmethod
from pathlib import Path


class ABCReader[T](ABC):
    """Abstract base for types that can be built from YAML (or directory) on disk."""

    @classmethod
    @abstractmethod
    def from_yaml(cls, path: Path) -> T:
        """Build an instance of T from a file or directory at path.

        Args:
            path: Path to the YAML file or directory to load from.

        Returns:
            T: An instance of the concrete reader type.

        """
