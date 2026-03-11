"""Mixin for string representation of objects (to_string)."""

from pfmg.external.display.ABCDisplay import ABCDisplay
from pfmg.lexique.stem_space.StemSpace import StemSpace


class MixinDisplay(ABCDisplay):
    """Mixin that implements the to_string factory by dispatching on term type."""

    def to_string(self, term: StemSpace | str | None = None) -> str:
        """Return a string describing this object.

        Args:
            term: Stem used to represent the object: StemSpace (multiple stems),
                str (single stem), or None (no stem).

        Returns:
            str: String describing the object.

        """
        return getattr(self, f"_to_string__{term.__class__.__name__.lower()}")(
            term=term,
        )

    def _to_string__str(self, term: str) -> str:
        """Return string representation for a single str term. Override in subclasses."""
        raise NotImplementedError

    def _to_string__nonetype(self, term: None = None) -> str:
        """Return string representation when term is None. Override in subclasses."""
        raise NotImplementedError

    def _to_string__stemspace(self, term: StemSpace) -> str:
        """Return string representation for a StemSpace term. Override in subclasses."""
        raise NotImplementedError
