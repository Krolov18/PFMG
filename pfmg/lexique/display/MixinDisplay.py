"""Mixin pour la représentation des objects."""
from pfmg.lexique.display.ABCDisplay import ABCDisplay
from pfmg.lexique.stem_space.StemSpace import StemSpace


class MixinDisplay(ABCDisplay):
    """Mixin qui implémente la factory to_string."""

    def to_string(self, term: StemSpace | str | None = None) -> str:
        """Transforme un objet en un string le décrivant.

        :param term: radical utiliser pour représenter un objet
            StemSpace: objet avec plusieurs radicaux
            str: objet avec un seul radical
            None: objet sans radical
        :return: une string décrivant l'objet
        """
        return getattr(self, f"_to_string__{term.__class__.__name__.lower()}")(
            term=term,
        )

    def _to_string__str(self, term: str) -> str:
        raise NotImplementedError

    def _to_string__nonetype(self, term: None = None) -> str:
        raise NotImplementedError

    def _to_string__stemspace(self, term: StemSpace) -> str:
        raise NotImplementedError
