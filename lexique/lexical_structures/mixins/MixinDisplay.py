from lexique.lexical_structures.interfaces.Display import Display
from lexique.lexical_structures.StemSpace import StemSpace


class MixinDisplay(Display):
    """
    Classe
    """

    def to_string(self, term: StemSpace | str | None = None) -> str:
        return getattr(
            self,
            f"_to_string__{term.__class__.__name__.lower()}"
        )(
            term=term
        )

    def _to_string__str(self, term: str) -> str:
        raise NotImplementedError(
            "Pas disponible pour se réaliser avec un 'str'"
        )

    def _to_string__nonetype(self, term: None = None) -> str:
        raise NotImplementedError(
            "Pas disponible pour se réaliser avec un 'None'"
        )

    def _to_string__stemspace(self, term: StemSpace) -> str:
        raise NotImplementedError(
            "Pas disponible pour se réaliser avec un 'StemSpace'"
        )
