import sys
from typing import List, Tuple, Iterator, Dict

from frozendict import frozendict
from multimethod import multimethod
from nltk import ParserI, Feature, Variable, parse, grammar, Tree
from nltk.grammar import FeatStructNonterminal, Production

from lexique.structures import MorphoSyntax
from lexique.syntax import cleave


def _validate(term: FeatStructNonterminal, att_vals: frozendict) -> None:
    """
    :param term:
    :param att_vals:
    :return:
    """
    _term = term.copy()
    _term.pop(Feature("type"), None)
    assert _term.keys() <= set(att_vals.values()), list(_term.keys())
    for i_x, i_y in list(_term.items()):
        if isinstance(i_y, Variable):
            _term.pop(i_x)
    assert set(_term.values()) <= att_vals.keys(), list(_term.values())


@multimethod
def validate(term: List[Production], att_values: frozendict) -> None:
    """
    :param term:
    :param att_values:
    :return:
    """
    for prod in term:
        validate(prod, att_values)


# pylint: disable=function-redefined
@multimethod  # type: ignore
def validate(term: Production, att_values: frozendict) -> None:
    """
    :param term:
    :param att_values:
    :return:
    """
    validate(term.lhs(), att_values)
    validate(term.rhs(), att_values)


# pylint: disable=function-redefined
@multimethod  # type: ignore
def validate(term: FeatStructNonterminal, att_values: frozendict) -> None:
    """
    :param term:
    :param att_values:
    :return:
    """
    _validate(term, att_values)


# # pylint: disable=function-redefined
# @multimethod  # type: ignore
# def validate(term: Tuple[str], att_values: frozendict) -> None:
#     pass


# pylint: disable=function-redefined
@multimethod  # type: ignore
def validate(term: Tuple[FeatStructNonterminal, ...], att_values: frozendict) -> None:
    """
    :param term:
    :param att_values:
    :return:
    """
    for i_nt in term:
        validate(i_nt, att_values)


# pylint: disable=function-redefined
@multimethod  # type: ignore
def validate(term: str, att_vals: frozendict) -> None:
    """
    On vérifie une règle passée sous forme de chaine de caractère
    On la transforme en Production NLTK et on vérifie ses membres
    :param term:
    :param att_vals:
    :return:
    """
    lhs, rhs = term.split(" -> ")
    prod = Production(lhs=FeatStructNonterminal(lhs), rhs=tuple(map(FeatStructNonterminal, rhs.split(" "))))
    validate(prod, att_vals)


@multimethod  # type: ignore
def validate(parser: ParserI, sentences: List[List[str]]) -> None:
    """
    Parcourt une série de phrases et print la phrase qui n'est pas reconnue par la grammaire
    On affiche à la fin, le nombre de phrases n'ayant pas été reconnues.
    :param parser : un parseur enfant de ParserI
    :param sentences : une liste de string encodant les phrases à tester
    """
    i = 0
    for sentence in sentences:
        try:
            [*parser.parse(sentence)][0]
        except IndexError:
            i += 1
            print(sentence)
    print(f"{i} n'ont pas pu être parsées.")


def validate_sentences(parser: parse.FeatureEarleyChartParser,
                       sentences: List[List[str]]) -> Iterator[Tuple[bool, str]]:
    """
    :param parser : parser syntaxique de type Earley et att/val pour gérer les grammaires semi-contextuelles
    :param sentences : liste de phrases découpées en tokens
    :return : itérateur de phrase avec indicateur si la phrase est valide
    """
    for sentence in sentences:
        trees = [*parser.parse(sentence)]
        if not trees:
            yield False, " ".join(sentence)
            continue
        yield True, " ".join(sentence)


def validate_sentence(sentence: List[str],
                      rules: str,
                      lexicon: Dict[str, List[str]],
                      morpho: MorphoSyntax,
                      start_nt: str) -> Iterator[str]:
    assert start_nt

    sentence_unzip: List[str] = [x.lower() if x not in ["Nicole", "Nabil", "Katisha", "Des"] else x for x in sentence]
    sentence_unzip = cleave(sentence_unzip, morpho)
    lex_rules: List[str] = [x[1]
                            for word in sentence_unzip
                            for x in lexicon
                            if ((word not in ("à", "deux")) and (word == x[0]))]
    # [lex_rules.extend(lexicon[word]) for word in sentence_unzip if word not in ("à", "deux")]
    _lex_rules: str = "\n".join(lex_rules)
    # print(_lex_rules)
    _rules: str = "% start " + start_nt + "\n\n" + rules.split("\n", 1)[1] + "\n" + _lex_rules
    parser = parse.FeatureEarleyChartParser(grammar=grammar.FeatureGrammar.fromstring(_rules))
    trees = parser.parse(sentence_unzip)
    _trees = set()
    for tree in trees:
        _trees.add(" ".join(i_glose for i_glose in tree.label()["Source", "Traduction"] if not isinstance(i_glose, Variable)))
    yield from _trees


def validate_tree(rules: str,
                  lexicon: Dict[str, List[str]],
                  sentences: List[List[str]],
                  morpho: MorphoSyntax,
                  start_nt: str
                  ) -> Iterator[Tuple[bool, str]]:
    for sentence in sentences:
        yield validate_sentence(sentence=sentence,
                                rules=rules,
                                lexicon=lexicon,
                                morpho=morpho,
                                start_nt=start_nt)


def validate_tree2(parser: parse.FeatureEarleyChartParser,
                   sentences: List[List[str]]) -> Iterator[Tuple[bool, str]]:
    """
    :param parser :
    :param sentences :
    :return :
    """
    for sentence in sentences:
        tree = next(parser.parse(sentence))
        if tree is None:
            yield False, " ".join(sentence)
            continue
        yield True, " ".join(i_glose for i_glose in tree.label()["TRAD"]
                             if not isinstance(i_glose, Variable))


def validate_translation(parser: parse.FeatureEarleyChartParser,
                         sentences: List[List[str]]) -> Iterator[Tuple[bool, str]]:
    for sentence in sentences:
        trees: List[Tree] = [*parser.parse(sentence)]
        if not trees:
            yield False, ""
            continue
        translation = " ".join(trees[0].label()["TRAD"])
        translation = translation[0].capitalize() + translation[1:] + "."
        yield True, translation
