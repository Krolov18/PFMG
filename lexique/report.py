import argparse
import sys
from typing import Iterator, Tuple, Any, Dict, Union, List, Callable

import pandas as pd
import tabulate
from frozendict import frozendict
from nltk.grammar import Production

from lexique.etl import (read_glose, read_stems,
                         build_paradigm, read_blocks,
                         read_phonology, read_morphosyntax, read_rules)
from lexique.structures import Lexeme, Forme, Phonology, MorphoSyntax
from lexique.validate import validate
from utils.abstract_factory import factory_function


def report(id_report: str, **kwargs) -> Any:
    """
    Rapport d'erreurs d'une grammaire, d'un parsing ou autre
    :param id_report: identifiant du rapport
    :param kwargs: paramètres pour le rapport
    :return:
    """
    try:
        _verbose = f"_{kwargs.pop('verbose', 0)}"
    except KeyError:
        _verbose = "_0"

    return factory_function(
        concrete_product=f"{id_report}_report{_verbose}",
        package=__name__,
        **kwargs
    )


def rules_report_0(morphosyntax: MorphoSyntax) -> Tuple[List[str], List[str]]:
    return read_rules(morphosyntax=morphosyntax)


def rules_report_1(morphosyntax: MorphoSyntax) -> Tuple[List[str], List[str]]:
    print("Chargement des règles syntaxiques", file=sys.stderr)
    values = read_rules(morphosyntax=morphosyntax)
    print("Règles syntaxiques chargées", file=sys.stderr)
    return values


def parsing_report_0(sentences: Iterator[Tuple[bool, str]]) -> None:
    pass


def parsing_report_1(sentences: Iterator[Tuple[bool, str]]) -> None:
    data = dict(zip(["CORRECTNESS", "SENTENCE"], map(list, zip(*sentences))))
    df = pd.DataFrame(data)
    print(tabulate.tabulate(df), file=sys.stderr)
    print(df["CORRECTNESS"].value_counts(), file=sys.stderr)


def gloses_report_0(gloses: Dict[str, Union[List[Dict[str, List[str]]], Dict[str, List[str]]]]) -> Tuple[
    Dict[str, List[frozendict]], frozendict]:
    return read_glose(gloses)


def gloses_report_1(gloses: Dict[str, Union[List[Dict[str, List[str]]], Dict[str, List[str]]]]) -> Tuple[
    Dict[str, List[frozendict]], frozendict]:
    print("Chargement des gloses", file=sys.stderr)
    gloses_, att_vals = read_glose(gloses)
    print("Gloses chargées", file=sys.stderr)
    return gloses_, att_vals


# def translation_report_0(
#         gloses: Dict[str, List[frozendict]],
#         constraints: Dict[str, Dict[str, str]]) -> Dict[str, List[frozendict]]:
#     return filter_grid(grid=gloses, constraints=constraints)
#
#
# def translation_report_1(
#         gloses: Dict[str, List[frozendict]],
#         constraints: Dict[str, Dict[str, str]]) -> Dict[str, List[frozendict]]:
#     print("Application du filtre pour la traduction", file=sys.stderr)
#     output = filter_grid(grid=gloses, constraints=constraints)
#     print("Filtre appliqué", file=sys.stderr)
#     return output


def lexemes_report_0(data: Dict[str, Dict], accumulator: str, att_vals: frozendict) -> List[Lexeme]:
    return [*read_stems(data=data, accumulator=accumulator, att_vals=att_vals)]


def lexemes_report_1(data: Dict[str, Dict], accumulator: str, att_vals: frozendict) -> List[Lexeme]:
    print("Chargement du lexique", file=sys.stderr)
    lexemes = [*read_stems(data=data, accumulator=accumulator, att_vals=att_vals)]
    print("Lexique chargé", file=sys.stderr)
    return lexemes


def paradigm_report_0(
        gloses: Dict[str, List[frozendict]],
        blocks: Dict[str, Dict[str, Dict[str, Dict[str, str]]]],
        att_vals: frozendict,
        voyelles: frozenset
) -> Dict[str, Dict[frozendict, Callable[[Lexeme], Forme]]]:
    return build_paradigm(
        glose=gloses,
        blocks=read_blocks(
            data=blocks,
            att_vals=att_vals,
            voyelles=voyelles
        )
    )


def paradigm_report_1(
        gloses: Dict[str, List[frozendict]],
        blocks: Dict[str, Dict[str, Dict[str, Dict[str, str]]]],
        att_vals: frozendict,
        voyelles: frozenset
) -> Dict[str, Dict[frozendict, Callable[[Lexeme], Forme]]]:
    print("Chargement des paradigmes", file=sys.stderr)
    paradigm = build_paradigm(
        glose=gloses,
        blocks=read_blocks(
            data=blocks,
            att_vals=att_vals,
            voyelles=voyelles
        )
    )
    print("Paradigmes chargés", file=sys.stderr)
    return paradigm


def phonology_report_0(data: Dict[str, Union[Dict[str, str], str]]) -> Phonology:
    return read_phonology(data)


def phonology_report_1(data: Dict[str, Union[Dict[str, str], str]]) -> Phonology:
    print("Chargement de la phonologie", file=sys.stderr)
    phonology = read_phonology(data)
    print("Phonologie chargée", file=sys.stderr)
    return phonology


def productions_report_0(productions: List[Production], att_vals: frozendict) -> None:
    validate(productions, att_vals)


def productions_report_1(productions: List[Production], att_vals: frozendict) -> None:
    print("Vérification des productions de la grammaire", file=sys.stderr)
    validate(productions, att_vals)
    print("Productions valides", file=sys.stderr)
    print(f"La grammaire est composée de '{len(productions)}' règles de production.", file=sys.stderr)
    print(*productions, sep="\n", file=sys.stderr)


def morphosyntax_report_0(morphosyntax: Dict) -> MorphoSyntax:
    return read_morphosyntax(morphosyntax)


def morphosyntax_report_1(morphosyntax: Dict) -> MorphoSyntax:
    print("Chargement des informations morphosyntaxiques", file=sys.stderr)
    morpho = read_morphosyntax(morphosyntax)
    print("Informations morphosyntaxiques chargées", file=sys.stderr)
    return morpho
