from typing import overload, List, Dict, Callable, Tuple

import numpy as np
from frozendict import frozendict

from lexique.structures import Lexeme, Forme, Prefix, Suffix, Circumfix, Gabarit, Radical, Phonology, Morpheme


@overload
def realize(term: Lexeme, paradigm: Dict[str, Dict[frozendict, Callable]]) -> List[Forme]: ...


@overload
def realize(term: Forme, phonology: Phonology) -> str: ...


@overload
def realize(term: Morpheme, accumulator: Tuple[str, ...]) -> np.ndarray: ...


@overload
def realize(term: Morpheme, accumulator: str) -> np.ndarray: ...


@overload
def realize(term: Prefix, accumulator: str) -> np.ndarray: ...


@overload
def realize(term: Suffix, accumulator: str) -> np.ndarray: ...


@overload
def realize(term: Circumfix, accumulator: str) -> np.ndarray: ...


@overload
def realize(term: Gabarit, accumulator: str, phonology: Phonology) -> np.ndarray: ...


@overload
def realize(term: Radical) -> np.ndarray: ...
