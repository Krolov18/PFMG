"""Mixin providing default __str__ and __repr__ (class name + _repr_params())."""

from pfmg.external.representor.ABCRepresentor import ABCRepresentor


class MixinRepresentor(ABCRepresentor):
    """Mixin that implements __repr__ as ClassName(params) and __str__ as repr(self)."""

    def __repr__(self) -> str:
        """Return ClassName(_repr_params()) for any library object."""
        return f"{self.__class__.__name__}({self._repr_params()})"

    def __str__(self) -> str:
        """Default __str__ delegates to repr(self)."""
        return repr(self)

    def _repr_params(self) -> str:
        raise NotImplementedError
