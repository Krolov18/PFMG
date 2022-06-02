from dataclasses import dataclass
from typing import List, Match, Optional, Tuple, Union, Dict, TypedDict, Set

from frozendict import frozendict


@dataclass
class Morpheme:
    rule: Optional[Match]
    sigma: Optional[frozendict]


TypeBlock = List[Morpheme]
TypeBlocks = List[TypeBlock]

TypeStem = str
TypeStems = Tuple[TypeStem]

TypeSigma = frozendict
TypeSigmaRule = Dict[str, str]

TypeBlockConfig = Dict[str, TypeSigmaRule]
TypeCatBlockConfig = Dict[str, TypeBlockConfig]


@dataclass
class Prefix(Morpheme):
    pass


@dataclass
class Suffix(Morpheme):
    pass


@dataclass
class Circumfix(Morpheme):
    pass


@dataclass
class Radical(Morpheme):
    stem: Tuple[str, ...]


@dataclass
class Gabarit(Morpheme):
    pass


@dataclass
class Realisation:
    pos: str
    morphemes: List[Morpheme]
    sigma: frozendict


@dataclass
class Forme(Realisation):
    traduction: Optional[Realisation] = None


@dataclass
class LexSign:
    stem: Union[str, Tuple[str, ...]]
    pos: str
    sigma: frozendict


@dataclass
class Lexeme(LexSign):
    traduction: Optional[LexSign] = None


@dataclass
class Phonology:
    apophonies: frozendict
    derives: frozendict
    mutations: frozendict
    consonnes: frozenset
    voyelles: frozenset


TypeCategories = List[str]
TypeCategoriesPositions = List[int]


class MorphoSyntaxConfig(TypedDict):
    contractions: Dict[str, str]
    syntagmes: Dict[str, List[TypeCategories]]
    start: str
    accords: Dict[str, List[Dict[str, Dict[str, str]]]]
    percolations: Dict[str, List[Dict[str, str]]]
    traductions: Dict[str, List[TypeCategoriesPositions]]


@dataclass
class MorphoSyntax:
    contractions: frozendict
    start: str
    syntagmes: Dict[str, List[TypeCategories]]
    accords: Dict[str, List[List[Dict[str, str]]]]
    percolations: Dict[str, List[Dict[str, str]]]
    traductions: Dict[str, List[TypeCategoriesPositions]]


class BlocksConfig(TypedDict):
    kalaba: TypeCatBlockConfig
    translation: TypeCatBlockConfig


class PhonologyConfig(TypedDict):
    apophonies: Dict[str, str]
    derives: Dict[str, str]
    mutations: Dict[str, str]
    consonnes: Set[str]
    voyelles: Set[str]
    syllabes: Dict[str, str]


@dataclass
class Selection(Morpheme):
    pass


@dataclass
class Condition(Morpheme):
    cond: Morpheme
    true: Morpheme
    false: Morpheme
