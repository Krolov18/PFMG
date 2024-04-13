"""Fonctions permettant de valider les productions d'une grammaire.

Fonctions permettant de séparer les contractions.
Fonctions permettant de générer les productions non lexicales fournies dans Rules.yaml.
"""
import itertools as it
import re
from collections.abc import Iterator, Sequence
from functools import reduce
from operator import add
from typing import Literal

from nltk import FeatStruct, Feature, Production, Variable
from nltk.featstruct import FeatureValueTuple
from nltk.grammar import FeatStructNonterminal

from pfmg.utils.functions import static_vars


def _is_q_mark(term: str) -> bool:
    """Vérifie la présence de ? à la fin de la chaine.

    :param term:
    :return:
    """
    return term.endswith("?")


def _is_star(term: str) -> bool:
    """Vérifie la présence de * à la fin de la chaine.

    :param term:
    :return:
    """
    return term.endswith("*")


def _is_plus(term: str) -> bool:
    """Vérifie la présence de + à la fin de la chaine.

    :param term:
    :return:
    """
    return term.endswith("+")


def _is_accolade(term: str) -> bool:
    """Vérifie la présence de { et } dans la chaine.

    :param term:
    :return:
    """
    return ("{" in term) or ("}" in term)


@static_vars(
    REG=re.compile(
        (r"{(?: (\d+),(\d+) }|,(?: (\d+)}|(\d+)})|(\d+)"
         r"(?: ,(?: (\d+)}|(\d+)})|,(?: (\d+)}|(\d+)})))"),
    ),
)
def repeat(term: str) -> list[list[str]]:
    """Répète un constituant autant de fois que ne l'indique 'term'.

    Suivant la valeur de term, on va répéter:
        * (PROHIBITED): 0 ou n fois le terme
        + (PROHIBITED): 1 ou n fois le terme
        ?: 0 ou 1 fois le terme
        {n}: n fois le terme

    :param term:
    :return:
    """
    match term:
        case c if _is_q_mark(c):
            assert len(term.split("/")[1]) == 1
            return [[""], [term.split("/")[0]]]
        case c if _is_accolade(c):
            reg = repeat.REG.search(term)  # type: ignore reportCallIssue
            deb: str
            fin: Sequence[str]
            assert reg
            deb, *fin = filter(None, reg.groups())
            term = term.rsplit("/", 1)[0]
            if not fin:
                return [([term] * i or [""])
                        for i in range(int(deb) + 1)]
            return [([term] * i or [""])
                    for i in range(int(deb), int(fin[0]) + 1)]
        case c if _is_star(c):
            raise NotImplementedError
        case c if _is_plus(c):
            raise NotImplementedError
        case _:
            assert term
            return [[term]]


def develop(rhs: list[str]) -> Iterator[list[str]]:
    """Décompresse une partie droite de règle.
        
    En association avec la fonction 'repeat',
    develop va générer autant de règles que le produit cartésien
    des membres de rhs fourniront.
    Par exemple:
        input: [D, N, A/?]
        output: [[D, N], [D, N, A]]

        input: [D/?, N, A/?]
        output: [[D, N], [D, N, A], [D, A, N], [D, A, N, A]]

    :param rhs: partie droite d'une règle de production d'une CFG.
    :return: un itérateur de RHSs
    """
    for i_x in it.product(*(repeat(t) for t in rhs)):
        yield [f"'{i_y}'" if (i_y and i_y.islower()) else i_y
               for i_y in reduce(add, i_x)]


# def cleave(
#         word: str | list[str] | list[list[str]],
#         morpho
# ) -> list[str] | list[list[str]]:
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


def parse_config(
    config: dict,
) -> tuple[FeatStructNonterminal, list[Production], list[Production]]:
    """Transforme la config présente dans le YAML en un triplet.

        0: LHS
        1: RHS de la source
        1: RHS de la destination)

    :param config:
    :return:
    """
    for lhs, rhss in config.items():
        _s_prods = [parse_one_rule(lhs, *i_config)
                    for i_config in zip(*rhss["Source"].values(), strict=True)]
        d_prods = [parse_one_rule(lhs, *i_config)
                   for i_config in
                   zip(*rhss["Destination"].values(), strict=True)]
        assert len(_s_prods) == len(d_prods)
        s_prods = [concatenate_rule_features(p1, p2)
                   for p1, p2 in zip(_s_prods, d_prods, strict=True)]
        assert len(s_prods) == len(d_prods)
        start = FeatStructNonterminal("S")
        return start, s_prods, d_prods
    else:
        raise TypeError


def parse_one_rule(
    lhs: str,
    syntagmes: list[str],
    accords: str,
    percolation: str,
    traduction: list[int] | None = None,
) -> Production:
    """Mise au format NLTK.

    :param lhs:
    :param syntagmes:
    :param accords:
    :param percolation:
    :param traduction:
    :return: Une Production
    """
    source: Literal["Source", "Destination"] = ("Destination"
                                                if traduction is None
                                                else "Source")
    match source:
        case "Destination":
            f_accords = [FeatStruct(Destination=FeatStruct())
                         for _ in range(len(syntagmes))]
        case "Source":
            f_accords = [FeatStruct(Source=FeatStruct())
                         for _ in range(len(syntagmes))]
        case _:
            raise KeyError(source)

    parse_features(
        broadcast(
            accords,
            len(syntagmes),
        ),
        f_accords,
    )
    f_percolation = FeatStruct(
        FeatStruct(
            {
                source: FeatStruct(),
            },
        ),
    )
    parse_percolation(
        broadcast(
            percolation,
            len(syntagmes),
        ),
        f_accords,
        f_percolation,
    )
    if traduction is not None:
        parse_traduction(
            syntagmes,
            traduction,
            f_accords,
            f_percolation,
        )
    return Production(
            lhs=FeatStructNonterminal(lhs, **f_percolation),  # type: ignore reportCallIssue
        rhs=[i_s if i_s.islower() else FeatStructNonterminal(i_s, **i_a)  # type: ignore reportCallIssue
             for i_s, i_a in zip(syntagmes, f_accords, strict=True)],
    )


def concatenate_rule_features(p1: Production, p2: Production) -> Production:
    """Intègre les infos de p2 dans p1.

    TODO : Ce sont des infos à intégrer dans une classe
    :param p1:
    :param p2:
    :return: p1 augmenté des infos de p2
    """
    p1_lhs: FeatStructNonterminal = p1.lhs()
    p2_lhs: FeatStructNonterminal = p2.lhs()
    assert "Traduction" in p1_lhs["Source"]
    assert all(
        "Traduction" in x["Source"]
        for x in p1.rhs()
        if isinstance(x, FeatStructNonterminal)
    )
    assert "Traduction" not in p2_lhs["Destination"]
    assert not any("Traduction" in x["Destination"] for x in p2.rhs())

    p1_lhs.update(p2_lhs)

    for i_idx, i_x in enumerate(p1_lhs["Source", "Traduction"]):
        p1.rhs()[int(i_x.name)].update(p2.rhs()[i_idx])

    return p1


def broadcast(accords: str, len_rhs: int) -> str:
    """TODO: écrire la doc de cela.
    
    :param :
    :param :
    :return :
    """
    if accords.count(";") != 0:
        return accords
    if len_rhs < 1:
        return accords
    return ((accords + ";") * len_rhs).rstrip(";")


def parse_traduction(
    syntagme: list[str],
    traduction: list[int],
    f_accords: list[FeatStruct],
    f_percolation: FeatStruct,
) -> None:
    """TODO: écrire doc."""
    for i in range(len(syntagme)):
        f_accords[i]["Source", "Traduction"] = Variable(str(i))  # type: ignore reportIndexIssue
    f_percolation["Source", "Traduction"] = FeatureValueTuple(  # type: ignore reportIndexIssue
        [f_accords[i_trad]["Source", "Traduction"]  # type: ignore reportIndexIssue
         for i_trad in traduction],
    )


def parse_features(  # noqa C901
    accords: str,
    accumulator: list[FeatStruct] | FeatStruct,
) -> None:
    """TODO: écrire doc."""
    if not accords:
        return

    if ";" in accords:
        # il y a plusieurs ensemble de features
        for i_idx, i_x in enumerate(accords.split(";")):
            parse_features(i_x, accumulator[i_idx])  # type: ignore reportIndexIssue
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
                    case {"Source": values}:
                        values[f"S{accords}"] = Variable(f"S{accords}")
                    case {"Destination": values}:
                        values[f"D{accords}"] = Variable(f"D{accords}")
            case {"Source": values}:
                values[f"S{accords}"] = Variable(f"S{accords}")
            case {"Destination": values}:
                values[f"D{accords}"] = Variable(f"D{accords}")
            case _:
                raise TypeError(accords, accumulator)


def parse_percolation(
    percolation: str,
    accords: list[FeatStruct] | FeatStruct,
    accumulator: FeatStruct,
) -> None:
    """Parse la partie percolation d'une règle.
        
        La différence entre parse_features et
        parse_percolation est la sémantique des ";"
        Ici, "Genre;Nombre" signifie qu'on percole
        le genre du premier élément du syntagme et le nombre du second.
        ATTENTION: on peut tomber dans des pièges.
        "Genre=m;Nombre" si le premier élément comporte un Genre
        avec une autre valeur, il y aua conflit.
    
    :param percolation:
    :param accords:
    :param accumulator:
    """
    assert "Destination" in accumulator or "Source" in accumulator  # type: ignore reportOperatorIssue

    if not percolation:
        return

    source = next(x for x in accumulator.keys() if x != Feature("type"))  # type: ignore reportIndexIssue
    source_init = source[0]

    if ";" in percolation:
        for i_idx, i_x in enumerate(percolation.split(";")):
            parse_percolation(i_x, accords[i_idx], accumulator)  # type: ignore reportIndexIssue
    elif "," in percolation:
        for i_x in percolation.split(","):
            parse_percolation(i_x, accords, accumulator)
    elif "=" in percolation:
        # TODO: cas très douteux, je pense qu'il permet
        #  plus de faire des bêtises qu'autre chose
        #  NP[Genre='m'] -> D[Genre=?genre] N[Genre=?genre] A[Genre=?genre]
        #  La situation précédente peut
        #  faire pointer '?genre' vers 'f' et percoler 'm'
        if not all(lhs_rhs := percolation.partition("=")):
            raise TypeError(lhs_rhs)
        match accords:
            case [a] if ((m := a[source].get(  # type: ignore reportIndexIssue
                f"{source_init}{lhs_rhs[0]}",
                None,
            ))
                         and m == lhs_rhs[2]):
                # cas de stricte égalité entre ce qu'on cherche
                # à percoler et ce qu'il y a dans la partie du rhs
                accumulator[source][f"{source_init}{lhs_rhs[0]}"] = m  # type: ignore reportIndexIssue
            case [a] if a[source].get(f"{source_init}{lhs_rhs[0]}", None):  # type: ignore reportIndexIssue
                # Cas à débattre.
                # Soit raise une erreur puisqu'il y a dissonance entre
                # la partie du rhs et ce qu'on veut percoler,
                # Soit on laisse et c'est à l'utilisateur de gérer cela
                # et de faire attention à cela.#
                raise TypeError(percolation, accords, accumulator)
            case [_]:
                accumulator[source][f"{source_init}{lhs_rhs[0]}"] = lhs_rhs[2]  # type: ignore reportIndexIssue
            case FeatStruct():  # type: ignore
                accumulator[source][f"{source_init}{lhs_rhs[0]}"] = lhs_rhs[2]  # type: ignore reportIndexIssue
            case _:
                raise TypeError(percolation, accords, accumulator)

    else:
        match accords:
            case FeatStruct():
                perco = f"{source_init}{percolation}"
                accumulator[source][perco] = accords[source][perco]  # type: ignore reportIndexIssue
            case [FeatStruct()]:
                perco = f"{source_init}{percolation}"
                accumulator[source][perco] = accords[0][source][perco]  # type: ignore reportIndexIssue
            case _:
                raise TypeError(
                    percolation,
                    accumulator,
                )
