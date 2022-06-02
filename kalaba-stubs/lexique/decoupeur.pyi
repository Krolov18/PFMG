from typing import overload

from structures import Circumfix, Forme, Gabarit, Prefix, Radical, Suffix


@overload
def decoupe(term: Prefix, accumulator: str) -> str: ...


@overload
def decoupe(term: Suffix, accumulator: str) -> str: ...


@overload
def decoupe(term: Circumfix, accumulator: str) -> str: ...


@overload
def decoupe(term: Gabarit, accumulator: str) -> str: ...


@overload
def decoupe(term: Radical, accumulator: str) -> str: ...


@overload
def decoupe(term: Forme) -> str: ...
