"""Mixin that dispatches to_glose to type-specific implementations."""

from pfmg.external.gloser.ABCGloser import ABCGloser
from pfmg.lexique.stem_space.StemSpace import StemSpace


class MixinGloser(ABCGloser):
    """Mixin that routes to_glose(term) to _to_glose__<type>(term)."""

    def to_glose(self, term: StemSpace | str | None = None) -> str:
        """Dispatch to the appropriate _to_glose__* method based on term type."""
        return getattr(self, f"_to_glose__{term.__class__.__name__.lower()}")(
            term=term,
        )

    def _to_glose__nonetype(self, term: None = None) -> str:
        """Return glose when term is None. Override in subclasses."""
        raise NotImplementedError

    def _to_glose__stemspace(self, term: StemSpace) -> str:
        """Return glose for a StemSpace term. Override in subclasses."""
        raise NotImplementedError

    def _to_glose__str(self, term: str) -> str:
        """Return glose for a single str term. Override in subclasses."""
        raise NotImplementedError
