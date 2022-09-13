from typing import Dict, Callable, List, Tuple

import pandas as pd
from frozendict import frozendict  # type: ignore

from lexique.realizer import realize
from lexique.structures import Forme, Phonology, Lexeme
from lexique.unary import unary


def build_df(
        term: List[Lexeme],
        paradigm: Dict[str, Dict[frozendict, Callable]],
        att_vals,
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
    columns: List[str] = [f"s{x}" for x in sorted(set(att_vals["source"].values()) - {"pos"})] +\
                         [f"d{x}" for x in sorted(set(att_vals["destination"].values()) - {"pos"})]
    data: Dict[str, List[str]] = {"forme": [], "unary": [], "traduction": [],
                                  "lemme": [], "pos": [], **{x: [] for x in columns}}
    for lexeme in term:
        for forme in realize(term=lexeme, paradigm=paradigm):
            assert forme is not None

            data["pos"].append(forme.pos)
            # for k in att_vals["source"].values() - forme.sigma.keys() - {"pos"}:
            #     data[k].append("")
            data["forme"].append(realize(term=forme, phonology=phonology))
            data["unary"].append(unary("tcfg", forme, phonology))
            data["traduction"].append(realize(term=forme.traduction, phonology=phonology))
            data["lemme"].append(",".join(lexeme.stem) if not isinstance(lexeme.stem, str) else lexeme.stem)

            for i_feat, i_val in forme.sigma.items():
                data[f"s{i_feat}"].append(i_val)
            for k in att_vals["source"].values() - forme.sigma.keys() - {"pos"}:
                data[f"s{k}"].append("")

            for i_feat, i_val in forme.traduction.sigma.items():
                data[f"d{i_feat}"].append(i_val)
            for k in att_vals["destination"].values() - forme.traduction.sigma.keys() - {"pos"}:
                data[f"d{k}"].append("")

    return pd.DataFrame(data)


def trad_lexrule(lexemes: List[Lexeme],
                 paradigm: Dict[str, Dict[frozendict, Callable]],
                 phonology: Phonology) -> List[Tuple[str, str]]:
    output: List[Tuple[str, str]] = []

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
