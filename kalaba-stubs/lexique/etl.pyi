from typing import Callable, Dict, Iterator, List, NoReturn, overload, Tuple, Union, Set

import pandas as pd
from frozendict import frozendict

from lexique.structures import Morpheme, Lexeme, Forme, Phonology, MorphoSyntax, BlocksConfig

TypeBlock = List[Morpheme]
TypeBlocks = List[TypeBlock]
TypeStem = str
TypeStems = Tuple[TypeStem]
TypeSigma = frozendict


@overload
def _sigmas(glose: List[Dict[str, List[str]]]) -> List[frozendict]: ...


@overload
def _sigmas(glose: Dict[str, List[str]]) -> List[frozendict]: ...


@overload
def _select(block: TypeBlock, sigma: frozendict) -> Morpheme: ...


@overload
def _select(blocks: TypeBlocks, sigma: frozendict) -> List[Morpheme]: ...


def _value2attribute(glose: Dict[str, Dict[str, List[str]]]) -> frozendict: ...


def read_blocks(data: BlocksConfig,
                att_vals: frozendict,
                voyelles: frozenset) -> Dict[str, Dict[str, TypeBlocks]]: ...


def read_glose(glose: Dict[str, Union[List[Dict[str, List[str]]], Dict[str, List[str]]]]
               ) -> Tuple[Dict[str, List[frozendict]], frozendict]: ...


def read_morphosyntax(data: Dict) -> MorphoSyntax: ...


def read_phonology(data: Dict[str, Union[Dict[str, str], str]]) -> Phonology: ...


def read_rules(morphosyntax: MorphoSyntax) -> Tuple[List[str], List[str]]: ...


def read_stems(data: Dict[str, Dict],
               att_vals: frozendict,
               accumulator: str = ""
               ) -> Iterator[Lexeme]: ...


def read_traduction(stem: str, att_vals: frozendict) -> Tuple[TypeStems, TypeSigma]: ...


def build_paradigm(glose: Dict[str, List[frozendict]],
                   blocks: Dict[str, Dict[str, TypeBlocks]]
                   ) -> Dict[str, Dict[frozendict, Callable[[Lexeme], Forme]]]: ...


@overload
def filter_grid(grid: List[frozendict], constraints: Set[str]) -> List[frozendict]: ...


@overload
def filter_grid(grid: List[frozendict], constraints: Dict[str, str]) -> List[frozendict]: ...


@overload
def filter_grid(grid: Dict, constraints: Dict) -> Dict[str, List[frozendict]]: ...


@overload
def validate_attribute(values: str, att_vals: frozendict) -> NoReturn: ...


@overload
def validate_attribute(values: frozendict, att_vals: frozendict) -> NoReturn: ...
