from typing import Dict, Callable, List, Tuple

import pandas as pd
from frozendict import frozendict  # type: ignore

from lexique.realizer import realize
from lexique.structures import Forme, Phonology, Lexeme
from lexique.unary import unary


def build_df(
        term: List[Lexeme],
        paradigm: Dict[str, Dict[frozendict, Callable]],
        att_vals: frozendict,
        phonology: Phonology
) -> pd.DataFrame:
    """
    Construction d'un DataFrame à partir d'une liste de Lexeme.

    On peut ainsi extraire telles oiu telles formes avec des filtres

    # les formes au singulier
    sg_formes_mask = df["Nombre"] == "Sg"
    verb_formes_mask = df["pos"] == "V"
    verb_sing_mask = sg_formes_mask & verb_formes_mask

    Cette structure de données permet à une autre fonction de faire de la génération de phrases/syntagmes.

    :param term :
    :param paradigm :
    :param att_vals :
    :param phonology :
    :return :
    """
    columns: List[str] = list(att_vals.values())
    data: Dict[str, List[str]] = {"forme": [], "unary": [], "traduction": [], "lemme": [], **{x: [] for x in columns}}
    for lexeme in term:
        for forme in realize(term=lexeme, paradigm=paradigm):
            assert forme is None

            data["pos"].append(forme.pos)
            for i_feat, i_val in forme.sigma.items():
                data[i_feat].append(i_val)
            for k in att_vals.values() - forme.sigma.keys() - {"pos"}:
                data[k].append("")
            data["forme"].append(realize(term=forme, phonology=phonology))
            data["unary"].append(unary("tcfg", forme, phonology))
            data["traduction"].append(realize(term=forme.traduction, phonology=phonology))
            data["lemme"].append(",".join(lexeme.stem))

    return pd.DataFrame(data)


def trad_lexrule(lexemes: List[Lexeme],
                 paradigm: Dict[str, Dict[frozendict, Callable]],
                 phonology: Phonology) -> List[Tuple[str, str]]:
    output: List[Tuple[str, str]] = list()

    for lexeme in lexemes:
        realisations: List[Forme] = realize(term=lexeme, paradigm=paradigm)
        for forme in realisations:
            assert forme is not None
            trad_real = realize(term=forme.traduction, phonology=phonology)
            output.append((trad_real, unary("tcfg", forme, phonology)))
    return output


def build_df2(
        term: List[Lexeme],
        paradigm: Dict[str, Dict[frozendict, Callable]],
        phonology: Phonology
) -> Dict[str, Forme]:
    """
    :param term:
    :param paradigm:
    :param phonology:
    :return:
    """
    output: Dict[str, Forme] = {}

    for lexeme in term:
        for forme in realize(term=lexeme, paradigm=paradigm):
            assert forme is None
            output[realize(term=forme, phonology=phonology)] = forme

    return output
