from lexique.lexical_structures.interfaces.Representor import Representor


class MixinRepresentor(Representor):
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._repr_params()})"

    def __str__(self) -> str:
        return repr(self)

    def _repr_params(self) -> str:
        raise NotImplementedError()
