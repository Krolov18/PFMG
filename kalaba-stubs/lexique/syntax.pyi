from typing import Dict, Iterator, List, overload

from nltk import ParserI

from lexique.structures import MorphoSyntax


def _is_accolade(term: str) -> bool: ...


def _is_q_mark(term: str) -> bool: ...


@overload
def repeat(term: str) -> List[str]: ...


@overload
def develop(rhs: Dict[str, List[List[str]]]) -> Iterator[List[str]]: ...


@overload
def develop(rhs: List[str]) -> Iterator[List[str]]: ...


@overload
def develop(rhs: List[List[str]]) -> Iterator[List[str]]: ...


@overload
def cleave(word: str, contractions: MorphoSyntax) -> List[str]: ...


@overload
def cleave(word: List[str], contractions: MorphoSyntax) -> List[str]: ...


@overload
def cleave(word: List[List[str]], morpho: MorphoSyntax) -> List[List[str]]: ...
