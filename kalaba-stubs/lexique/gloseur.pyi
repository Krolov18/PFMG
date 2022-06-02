from typing import overload

from lexique.structures import Forme, Prefix, Suffix, Circumfix, Radical, Gabarit


@overload
def glose(term: Forme) -> str: ...


@overload
def glose(term: Prefix, accumulator: str) -> str: ...


@overload
def glose(term: Suffix, accumulator: str) -> str: ...


@overload
def glose(term: Circumfix, accumulator: str) -> str: ...


@overload
def glose(term: Radical, accumulator: str) -> str: ...


@overload
def glose(term: Gabarit, accumulator: str) -> str: ...
