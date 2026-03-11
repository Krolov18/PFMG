"""TODO : Doc à écrire."""

from pfmg.external.decoupeur.ABCDecoupeur import ABCDecoupeur
from pfmg.lexique.stem_space.StemSpace import StemSpace


class MixinDecoupeur(ABCDecoupeur):
    """TODO : Doc à écrire."""

    def to_decoupe(self, term: StemSpace | str | None = None) -> str:
        """TODO : Doc à écrire."""
        return getattr(self, f"_to_decoupe__{term.__class__.__name__.lower()}")(
            term=term,
        )

    def _to_decoupe__str(self, term: str) -> str:
        """TODO : Doc à écrire."""
        raise NotImplementedError

    def _to_decoupe__nonetype(self, term: None = None) -> str:
        """TODO : Doc à écrire."""
        raise NotImplementedError

    def _to_decoupe__stemspace(self, term: StemSpace) -> str:
        """TODO : Doc à écrire."""
        raise NotImplementedError
