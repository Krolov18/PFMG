"""Mixin that dispatches to_decoupe to type-specific implementations."""

from pfmg.external.decoupeur.ABCDecoupeur import ABCDecoupeur
from pfmg.lexique.stem_space.StemSpace import StemSpace


class MixinDecoupeur(ABCDecoupeur):
    """Mixin that routes to_decoupe(term) to _to_decoupe__<type>(term)."""

    def to_decoupe(self, term: StemSpace | str | None = None) -> str:
        """Dispatch to the appropriate _to_decoupe__* method based on term type."""
        return getattr(self, f"_to_decoupe__{term.__class__.__name__.lower()}")(
            term=term,
        )

    def _to_decoupe__str(self, term: str) -> str:
        """Return segmentation for a single string term. Override in subclasses."""
        raise NotImplementedError

    def _to_decoupe__nonetype(self, term: None = None) -> str:
        """Return segmentation when term is None. Override in subclasses."""
        raise NotImplementedError

    def _to_decoupe__stemspace(self, term: StemSpace) -> str:
        """Return segmentation for a StemSpace term. Override in subclasses."""
        raise NotImplementedError
