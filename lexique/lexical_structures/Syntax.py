"""
    Fonctions permettant de valider les productions d'une grammaire.
    Fonctions permettant de séparer les contractions.
    Fonctions permettant de générer les productions non lexicales fournies dans Rules.yaml
"""
import itertools as it
import re
from functools import reduce
from operator import add
from typing import Iterator, Iterable, Literal

from nltk import Production, FeatStruct, Variable, Feature
from nltk.featstruct import FeatureValueTuple
from nltk.grammar import FeatureGrammar, FeatStructNonterminal

from utils.functions import static_vars


def _is_q_mark(term: str) -> bool:
    """
    :param term:
    :return:
    """
    return term.endswith("?")


def _is_star(term: str) -> bool:
    """
    :param term:
    :return:
    """
    return term.endswith("*")


def _is_plus(term: str) -> bool:
    """
    :param term:
    :return:
    """
    return term.endswith("+")


def _is_accolade(term: str) -> bool:
    """
    :param term:
    :return:
    """
    return ("{" in term) or ("}" in term)


@static_vars(  # type: ignore
    REG=re.compile(r"{(?: (\d+),(\d+) }|,(?: (\d+)}|(\d+)})|(\d+)(?: ,(?: (\d+)}|(\d+)})|,(?: (\d+)}|(\d+)})))")
)
def repeat(term: str) -> list[list[str]]:
    match term:
        case c if _is_q_mark(c):
            assert len(term.split("/")[1]) == 1
            return [[""], [term.split("/")[0]]]
        case c if _is_accolade(c):
            reg = getattr(repeat, "REG").search(term)
            deb: str
            fin: Iterable[str]
            assert reg
            deb, *fin = filter(None, reg.groups())
            term = term.rsplit("/", 1)[0]
            if not fin:
                return [([term] * i or [""]) for i in range(int(deb) + 1)]
            return [([term] * i or [""]) for i in range(int(deb), int(fin[0]) + 1)]
        case c if _is_star(c):
            raise NotImplementedError("Fonctionnalité non développée pour éviter l'infini")
        case c if _is_plus(c):
            raise NotImplementedError("Fonctionnalité non développée pour éviter l'infini")
        case _:
            assert term
            return [[term]]


def develop(rhs: list[str]) -> Iterator[list[str]]:
    """
    :param rhs: partie droite d'une règle de production d'une CFG.
    :return: Développe le nombre de règles suivant
             si dans la règle un ou plusieurs constituants
             peut apparaitre plusieurs fois.
    par exemple:
        input : [D, N, A/?]
        output : [[D, N], [D, N, A]]

        input: [D/?, N, A/?]
        output: [[D, N], [D, N, A], [D, A, N], [D, A, N, A]]
    """
    for i_x in it.product(*(repeat(t) for t in rhs)):
        yield [f"'{i_y}'" if (i_y and i_y.islower()) else i_y for i_y in reduce(add, i_x)]


# def cleave(word: str | list[str] | list[list[str]], morpho) -> list[str] | list[list[str]]:
#     match word:
#         case str() as c if c in morpho.contractions:
#             return morpho.contractions[word]
#         case str():
#             return [word]
#         case [str(), *_]:
#             res: list[str] = []
#             for i_w in word:
#                 res += cleave(i_w, morpho)
#             return res
#         case [list(), *_]:
#             result: list[list[str]] = []
#             for i_sent in word:
#                 result.append(cleave(i_sent, morpho))
#             return result


def parse_config(config: dict) -> tuple[FeatureGrammar, FeatureGrammar]:
    for lhs, rhss in config.items():
        _s_prods = [parse_one_rule(lhs, *i_config) for i_config in zip(*rhss["Source"].values())]
        d_prods = [parse_one_rule(lhs, *i_config) for i_config in zip(*rhss["Destination"].values())]
        assert len(_s_prods) == len(d_prods)
        s_prods = [concatenate_rule_features(p1, p2) for p1, p2 in zip(_s_prods, d_prods)]
        assert len(s_prods) == len(d_prods)
        start = FeatStructNonterminal("S")
        return FeatureGrammar(start, s_prods), FeatureGrammar(start, d_prods)


def parse_one_rule(lhs: str,
                   syntagmes: list[str],
                   accords: str,
                   percolation: str,
                   traduction: list[int] | None = None) -> Production:
    source: Literal["Source", "Destination"] = "Destination" if traduction is None else "Source"
    match source:
        case "Destination":
            f_accords = [FeatStruct(Destination=FeatStruct()) for _ in range(len(syntagmes))]
        case "Source":
            f_accords = [FeatStruct(Source=FeatStruct()) for _ in range(len(syntagmes))]

    parse_features(broadcast(accords, len(syntagmes)), f_accords)
    f_percolation = FeatStruct(FeatStruct({source: FeatStruct()}))
    parse_percolation(broadcast(percolation, len(syntagmes)), f_accords, f_percolation)
    if traduction is not None:
        parse_traduction(syntagmes, traduction, f_accords, f_percolation)
    return Production(
        lhs=FeatStructNonterminal(lhs, **f_percolation),
        rhs=[i_s if i_s.islower() else FeatStructNonterminal(i_s, **i_a)
             for i_s, i_a in zip(syntagmes, f_accords)]
    )


def concatenate_rule_features(p1: Production, p2: Production) -> Production:
    assert "Traduction" in p1.lhs()["Source"]
    assert all(["Traduction" in x["Source"] for x in p1.rhs() if isinstance(x, FeatStructNonterminal)])
    assert "Traduction" not in p2.lhs()["Destination"]
    assert not any(["Traduction" in x["Destination"] for x in p2.rhs()])

    p1.lhs().update(p2.lhs())

    for i_idx, i_x in enumerate(p1.lhs()["Source", "Traduction"]):
        p1.rhs()[int(i_x.name)].update(p2.rhs()[i_idx])

    return p1


def broadcast(accords: str, len_rhs: int) -> str:
    if accords.count(";") != 0:
        return accords
    if len_rhs < 1:
        return accords
    return ((accords + ";") * len_rhs).rstrip(";")


def parse_traduction(syntagme: list[str],
                     traduction: list[int],
                     f_accords: list[FeatStruct],
                     f_percolation: FeatStruct) -> None:
    for i in range(len(syntagme)):
        f_accords[i]["Source", "Traduction"] = Variable(str(i))  # type: ignore
    f_percolation["Source", "Traduction"] = FeatureValueTuple([f_accords[i_trad]["Source", "Traduction"]  # type: ignore
                                                               for i_trad in traduction])


def parse_features(accords: str,
                   accumulator: list[FeatStruct] | FeatStruct) -> None:
    if not accords:
        return

    if ";" in accords:
        # il y a plusieurs ensemble de features
        for i_idx, i_x in enumerate(accords.split(";")):
            parse_features(i_x, accumulator[i_idx])
    elif "," in accords:
        # il y a plusieurs traits
        for x in accords.split(","):
            parse_features(x, accumulator)
    elif "=" in accords:
        # un trait à une valeur de spécifiée
        if not all(lhs_rhs := accords.partition("=")):
            raise TypeError(lhs_rhs)
        match accumulator:
            case [a]:
                match a:
                    case {"Source": values}:  # type: ignore
                        values[f"S{lhs_rhs[0]}"] = lhs_rhs[2]
                    case {"Destination": values}:  # type: ignore
                        values[f"D{lhs_rhs[0]}"] = lhs_rhs[2]
            case {"Source": values}:  # type: ignore
                values[f"S{lhs_rhs[0]}"] = lhs_rhs[2]
            case {"Destination": values}:  # type: ignore
                values[f"D{lhs_rhs[0]}"] = lhs_rhs[2]
            case _:
                raise TypeError(accords, accumulator)
    else:
        # un trait n'a pas de valeur de spécifiée
        # On en fait alors une Variable

        match accumulator:
            case [a]:
                match a:
                    case {"Source": values}:  # type: ignore
                        values[f"S{accords}"] = Variable(f"S{accords}")  # type: ignore
                    case {"Destination": values}:  # type: ignore
                        values[f"D{accords}"] = Variable(f"D{accords}")  # type: ignore
            case {"Source": values}:  # type: ignore
                values[f"S{accords}"] = Variable(f"S{accords}")  # type: ignore
            case {"Destination": values}:  # type: ignore
                values[f"D{accords}"] = Variable(f"D{accords}")  # type: ignore
            case _:
                raise TypeError(accords, accumulator)


def parse_percolation(percolation: str,
                      accords: list[FeatStruct] | FeatStruct,
                      accumulator: FeatStruct) -> None:
    """
    La différence entre parse_features et parse_percolation est la sémantique des ";"
    Ici, "Genre;Nombre" signifie qu'on percole le genre du premier élément du syntagme et le nombre du second.
    ATTENTION: on peut tomber dans des pièges.
    "Genre=m;Nombre" si le premier élément comporte un Genre avec une autre valeur, il y aua conflit.
    :param percolation:
    :param accords:
    :param accumulator:
    :return:
    """
    assert "Destination" in accumulator or "Source" in accumulator

    if not percolation:
        return

    source = [x for x in accumulator.keys() if x != Feature("type")][0]
    source_init = source[0]

    if ";" in percolation:
        for i_idx, i_x in enumerate(percolation.split(";")):
            parse_percolation(i_x, accords[i_idx], accumulator)
    elif "," in percolation:
        for i_x in percolation.split(","):
            parse_percolation(i_x, accords, accumulator)
    elif "=" in percolation:
        # TODO: cas très douteux, je pense qu'il permet plus de faire des bêtises qu'autre chose
        #  NP[Genre='m'] -> D[Genre=?genre] N[Genre=?genre] A[Genre=?genre]
        #  La situation précédente peut faire pointer '?genre' vers 'f' et percoler 'm'
        if not all(lhs_rhs := percolation.partition("=")):
            raise TypeError(lhs_rhs)
        match accords:
            case [a] if (m := a[source].get(f"{source_init}{lhs_rhs[0]}", None)) and m == lhs_rhs[2]:
                # cas de stricte égalité entre ce qu'on cherche à percoler et ce qu'il y a dans la partie du rhs
                accumulator[source][f"{source_init}{lhs_rhs[0]}"] = m
            case [a] if (m := a[source].get(f"{source_init}{lhs_rhs[0]}", None)):
                # Cas à débattre.
                # Soit raise une erreur puisqu'il y a dissonance entre la partie du rhs et ce qu'on veut percoler,
                # Soit on laisse et c'est à l'utilisateur de gérer cela et de faire attention à cela.#
                raise TypeError(percolation, accords, accumulator)
            case [_]:
                accumulator[source][f"{source_init}{lhs_rhs[0]}"] = lhs_rhs[2]
            case FeatStruct():  # type: ignore
                accumulator[source][f"{source_init}{lhs_rhs[0]}"] = lhs_rhs[2]
            case _:
                raise TypeError(percolation, accords, accumulator)

    else:
        match accords:
            case FeatStruct():  # type: ignore
                accumulator[source][f"{source_init}{percolation}"] = accords[source][f"{source_init}{percolation}"]
            case [FeatStruct()]:  # type: ignore
                accumulator[source][f"{source_init}{percolation}"] = accords[0][source][f"{source_init}{percolation}"]
            case _:
                raise TypeError(percolation, accumulator)
