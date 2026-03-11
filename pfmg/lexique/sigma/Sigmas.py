"""Collection of Sigma (feature-structure) instances."""

import itertools as it
from collections.abc import Iterator
from dataclasses import dataclass

from pfmg.lexique.sigma.Sigma import Sigma
from pfmg.lexique.utils import gridify


@dataclass
class Sigmas:
    """A collection of Sigma instances (e.g. from source/destination config).

    Attributes:
        data: List of Sigma instances.

    """

    data: list[Sigma]

    def __contains__(self, item: Sigma) -> bool:
        """Return True if any Sigma in this collection is a superset of item (item <= sigma).

        Args:
            item: Sigma to check for containment.

        Returns:
            bool: True if item is contained in (subset of) some Sigma in data.

        """
        for x in self.data:
            if x <= item:
                return True
        return False

    def __iter__(self) -> Iterator[Sigma]:
        """Iterate over the Sigma instances.

        Yields:
            Sigma: Each Sigma in the collection.

        """
        return iter(self.data)

    @classmethod
    def from_dict(cls, source: dict, destination: dict) -> Sigmas:
        """Build Sigmas from source and destination config dicts (grid product).

        Args:
            source: Source-language config dict.
            destination: Destination-language config dict.

        Returns:
            Sigmas: New Sigmas instance (cartesian product of source and destination).

        """
        return cls([Sigma(*x) for x in it.product(*gridify([source, destination]))])
