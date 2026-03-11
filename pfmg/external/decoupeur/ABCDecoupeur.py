"""TODO : Doc à écrire."""

from abc import ABC, abstractmethod

from pfmg.lexique.stem_space.StemSpace import StemSpace


class ABCDecoupeur(ABC):
    """TODO : Doc à écrire."""

    @abstractmethod
    def to_decoupe(self, term: StemSpace | str | None = None) -> str:
        """TODO : Doc à écrire."""
