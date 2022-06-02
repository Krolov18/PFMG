from typing import overload, List, Tuple, Iterator, Dict

from frozendict import frozendict
from nltk import Production, ParserI, parse
from nltk.grammar import FeatStructNonterminal

from lexique.structures import MorphoSyntax


def _validate(term: FeatStructNonterminal, att_values: frozendict) -> None: ...


@overload
def validate(term: Production, att_values: frozendict) -> None: ...


@overload
def validate(term: List[Production], att_values: frozendict) -> None: ...


@overload
def validate(term: FeatStructNonterminal, att_values: frozendict) -> None: ...


@overload
def validate(term: Tuple[FeatStructNonterminal], att_values: frozendict) -> None: ...


@overload
def validate(term: str, att_vals: frozendict) -> None: ...


@overload
def validate(term: Tuple[str], att_vals: frozendict) -> None: ...


@overload
def validate(parser: ParserI, sentences: List[List[str]]) -> None: ...


def validate_tree(rules: str,
                  lexicon: Dict[str, List[str]],
                  sentences: List[List[str]],
                  morpho: MorphoSyntax,
                  start_nt: str
                  ) -> Iterator[Tuple[bool, str]]: ...


def validate_translation(parser: parse.FeatureEarleyChartParser,
                         sentences: List[List[str]]) -> Iterator[Tuple[bool, str]]: ...


def validate_sentence(sentence: List[str],
                      rules: str,
                      lexicon: Dict[str, List[str]],
                      morpho: MorphoSyntax,
                      start_nt: str) -> Iterator[str]: ...
