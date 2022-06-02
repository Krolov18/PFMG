from typing import List, Callable, Dict, overload

from frozendict import frozendict

from lexique.structures import Phonology, Lexeme, Forme


@overload
def unary(id_unary: str,
          term: List[Lexeme],
          paradigm: Dict[str, Dict[frozendict, Callable]],
          phonology: Phonology) -> List[str]: ...


@overload
def unary(id_unary: str,
          term: Forme,
          phonology: Phonology) -> str: ...
