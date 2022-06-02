""" Commandes pour charger les différentes données d'une grammaire """
import collections
import itertools
import re
from typing import Dict, List, Optional, Union, Callable, Tuple, NoReturn, Iterator, Set
from typing_extensions import TypeAlias

from frozendict import frozendict  # type: ignore
from multimethod import multimethod, DispatchError

from lexique.errors import Errors
from lexique.ruler import ruler
from lexique.structures import (Morpheme, Forme,
                                Radical, Lexeme,
                                Phonology, MorphoSyntax,
                                MorphoSyntaxConfig, PhonologyConfig,
                                TypeBlock, TypeBlocks,
                                TypeStems, TypeSigma, BlocksConfig, TypeCatBlockConfig)
from lexique.syntax import develop
from utils.functions import static_vars


def split(sequence: str) -> List[str]:
    """
    :param sequence : phrase d'entrée au kalabiste
    :return : chaine de caractère découpée sur les espaces, les apostrophes et les points.
    """
    sequence = sequence.replace("'", "' ").replace(".", " .").replace("   ", " ").replace("  ", " ")
    return sequence.split(" ") if sequence else []


def _str2sigma(str_sigma: str) -> frozendict:
    """
    :param str_sigma:
    :return:
    """

    try:
        result = frozendict([att_val.strip().split("=") for att_val in str_sigma.strip().split(",")])
    except ValueError:
        result = frozendict()
    return result


@multimethod
def _select(block: TypeBlock, sigma: frozendict) -> Morpheme:
    """
    Sélectionne la règle plus spécifique par rapport aux traits présents dans la glose
    :param block : dictionnaire ordonné de règles de la plus générale à la plus spécifique
    :param sigma : cellule d'un paradigme
    :return : l'instance d'un morphème
    """
    assert block

    winner: Optional[Morpheme] = None
    for morpheme in block:
        if morpheme.sigma.items() <= sigma.items():
            winner = morpheme

    assert winner
    return winner


@multimethod  # type: ignore
def _select(blocks: TypeBlocks, sigma: frozendict) -> List[Morpheme]:
    """
    Pour qu'une forme existe, il se doit d'appliquer tous les blocks dans le bon ordre
    :param blocks : liste de dictionnaire ordonné de règles du plus général au plus spécifique
    :param sigma : cellule d'un paradigme
    :return : liste de morphèmes
    """
    output: List[Morpheme] = []

    for block in blocks:
        try:
            output.append(_select(block, sigma))
        except AssertionError:
            continue
    return output


@multimethod
def _sigmas(glose: Dict[str, List[str]]) -> List[frozendict]:
    """
    :param glose:
    :return:
    """
    if not glose:
        raise ValueError()

    output: List[frozendict] = []

    keys, values = zip(*glose.items())
    for value in itertools.product(*values):
        params = frozendict(zip(keys, value))
        output.append(params)
    return output


@multimethod  # type: ignore
def _sigmas(glose: List[Dict[str, List[str]]]) -> List[frozendict]:
    """
    :param glose:
    :return:
    """
    return [*itertools.chain.from_iterable(_sigmas(g) for g in glose)]


def _value2attributes(glose: Dict[str, Union[Dict[str, List[str]],
                                             List[Dict[str, List[str]]]]]) -> frozendict:
    """
    :param glose:
    :return:
    """
    output: Dict[str, str] = {}

    for category, gloses in glose.items():
        output[category] = "pos"
        output.update(_value2attribute(gloses))

    return frozendict(output)


def _value2attribute(glose: Dict[str, Dict[str, List[str]]]) -> frozendict:
    """
    :param glose:
    :return:
    """
    result = {}

    for category in glose:
        result[category] = "pos"

        if not glose[category]:
            continue

        for attribute, values in glose[category].items():
            for val in values:
                result[val] = attribute

    return frozendict(result)


@multimethod  # type: ignore
def _value2attribute(glose: Dict[str, List[str]]) -> frozendict:
    """
    :param glose:
    :return:
    """
    output: Dict[str, str] = {}

    for attribute, values in glose.items():
        for i_value in values:
            output[i_value] = attribute

    return frozendict(output)


@multimethod  # type: ignore
def _value2attribute(glose: List[Dict[str, List[str]]]) -> frozendict:
    """
    :param glose:
    :return:
    """
    output: Dict[str, str] = {}

    for i_glose in glose:
        output.update(_value2attribute(i_glose))

    return frozendict(output)


def _format_dict(struct: Dict[str, str]) -> str:
    return ",".join(f"{x}={y if y != '*' else f'?{x.lower()}'}" for x, y in struct.items())


@static_vars(REG=re.compile(r",?Traduction=\??\w+"))
def _retire_traduction(feature_nonterminal: str) -> str:
    return _retire_traduction.REG.sub("", feature_nonterminal)


def filter_grid(grid: Dict, constraints: Dict) -> Dict[str, List[frozendict]]:
    """
    :param grid:
    :param constraints:
    :return:
    """
    return {k: _filter_grid(i_glose, constraints[k]) for k, i_glose in grid.items()}


@multimethod
def _filter_grid(grid: List[frozendict], constraints: Dict[str, str]) -> List[frozendict]:
    """
    :param grid:
    :param constraints:
    :return:
    """
    for i in range(len(grid) - 1, -1, -1):
        for i_key, i_val in constraints.items():
            k_val, t_val = i_val.split(">")
            # try:
            if grid[i][f'þ{i_key}'] != f"þ{grid[i][i_key]}":
                if (grid[i][i_key] == k_val) and (grid[i][f"þ{i_key}"] == f"þ{t_val}"):
                    continue
                del grid[i]
                break
            # except KeyError:
            #     continue

    return grid


@multimethod  # type: ignore
def _filter_grid(grid: List[frozendict], constraints: Set[str]) -> List[frozendict]:
    """
    Pivot morphologique
    si trait dans grille, mais pas de valeurs :
        on cherche une égalité entre la langue source et la langue cible
    :param grid : liste de sigma
    :param constraints : trait > valeur
    :return : liste de sigma réduit suivant les contraintes
    """
    for i in range(len(grid) - 1, -1, -1):
        for constraint in constraints:
            if grid[i][f'þ{constraint}'] != f"þ{grid[i][constraint]}":
                del grid[i]
                break

    return grid


TypeGlosesConfig = Dict[str, Union[List[Dict[str, List[str]]], Dict[str, List[str]]]]
TypeGloses = Dict[str, List[frozendict]]
TypeAttVals: TypeAlias = frozendict


def read_glose(glose: TypeGlosesConfig) -> Tuple[TypeGloses, TypeAttVals]:
    """
    Lit le fichier de gloses et le met au format décrit ci-dessous :

        input : {N: genre: [m, f], nombre: [sg, pl]}
        output: {N: [{'genre': 'm', 'nombre': 'sg'},
                     {'genre': 'm', 'nombre': 'pl'},
                     {'genre': 'f', 'nombre': 'sg'},
                     {'genre': 'f', 'nombre': 'pl'}]}
    :param glose:
    :return: les gloses au format décrit ci-dessus ET un dictionnaire figé valeur → attribut
    """
    if not glose:
        raise ValueError(Errors.E001)

    return {key: _sigmas(value) if value is not None else [] for key, value in glose.items()}, _value2attributes(glose)


def _read_blocks(data: TypeCatBlockConfig, att_vals: TypeAttVals, voyelles: frozenset) -> Dict[str, TypeBlocks]:
    """

    input: {N: {1: {genre=f: X+e}, 2: {nombre=pl: X+s}}}
    output: {N: [[Suffix(sigma={genre: f}, rule=Match(group=e))], [Suffix(sigma={genre: pl}, rule=Match(group=s))]]}

    input: {N: {1: {genre=f: X+e, genre=m: a+X}, 2: {nombre=pl: X+s, nombre=sg: a+X+a}}}
    output: {N: [[Suffix(sigma={genre: f}, rule=Match(...)), Prefix(sigma={genre: m}, rule=Match(...))],
                 [Suffix(sigma={nombre: pl}, rule=Match(...)), Circumfix(sigma={nombre: sg}, rule=Match(...))]]}

    :param data:
    :param att_vals : structure de données qui permet de valider les attributs et les valeurs utilisés ici.
                     Cette structure est générée après avoir parcouru GLoses.
    :return : les blocs structurés sous forme de listes de morphemes pour chaque catégorie.
    """
    if not data:
        raise ValueError(Errors.E004)

    output: Dict[str, TypeBlocks] = {}
    for category, _blocks in data.items():
        validate_attribute(category, att_vals)

        blocks: TypeBlocks = []
        for sigma_rule in _blocks.values():
            block: TypeBlock = []
            for str_sigma, rule in sigma_rule.items():
                str_sigmas = _str2sigma(str_sigma)

                validate_attribute(str_sigmas, att_vals)

                block.append(
                    ruler(id_ruler="all", rule=rule, sigma=str_sigmas, voyelles=voyelles)
                )
            blocks.append(block)
        output[category] = blocks
    return output


def read_blocks(data: BlocksConfig, att_vals: TypeAttVals, voyelles: frozenset) -> Dict[str, Dict[str, TypeBlocks]]:
    """
    Lit les informations de configurations concernant les blocs de morphèmes
    aussi bien pour la traduction que pour le kalaba.

    Attention, toute information autre que les champs kalaba et translation ne seront pas pris en compte.
    :param data:
    :param att_vals: Structure validant les attributs/valuers utilisés dans Blocks.yaml
    :return: un dictionnaire à deux clés 'kalaba' et 'translation'
    """
    try:
        kalaba, translation = data["kalaba"], data["translation"]
    except TypeError as ex:
        raise ValueError(Errors.E002) from ex
    except KeyError as ex:
        raise ValueError(Errors.E003) from ex

    return {"kalaba": _read_blocks(kalaba, att_vals, voyelles),
            "translation": _read_blocks(translation, att_vals, frozenset())}


def read_traduction(stem: str, att_vals: frozendict) -> Tuple[TypeStems, TypeSigma]:
    """
    :param stem:
    :param att_vals:
    :return:
    """
    assert stem

    try:
        stems, values = stem.split("-")
        sigma = frozendict({att_vals[val]: val for val in [f"þ{x}" for x in values.split(".")]})
    except ValueError:
        stems = stem
        sigma = frozendict()

    _stems = tuple(stems.split(","))

    return _stems, sigma


def read_stems(data: Dict[str, Dict], att_vals: frozendict, accumulator: str = "") -> Iterator[Lexeme]:
    """

     input : {N: {banan: [turc,turcs,turcque,turques]}}
    output : [Lexeme(pos=N, stem=banan, sigma={}, traductions=[turc,turcs,turcque,turques])]

     input : {N: {f: {banan: [turc,turcs,turcque,turques]}}}
    output : [Lexeme(pos=N, stem=banan, sigma={genre: f}, traductions=[turc,turcs,turcque,turques])]

     input : {N: {f: {sg: {banan: [turc,turcs,turcque,turques]}}}}
    output : [Lexeme(pos=N, stem=banan, sigma={genre: f, nombre: sg}, traductions=[turc,turcs,turcque,turques])]

    :param data:
    :param accumulator:
    :param att_vals:
    :return:
    """
    if isinstance(data, str):
        valeurs = eval(f"dict({accumulator})")
        pos = valeurs.pop("pos")
        k_stems = tuple(valeurs.pop("stem").split(","))
        t_stems, t_sigma = read_traduction(stem=data, att_vals=att_vals)
        yield Lexeme(stem=k_stems,
                     pos=pos,
                     sigma=frozendict(valeurs),
                     traduction=Lexeme(stem=t_stems,
                                       pos=pos,
                                       sigma=t_sigma,
                                       traduction=None))
    else:
        for i_key in data:
            try:
                search = att_vals[i_key]
            except KeyError:
                search = "stem"
            yield from read_stems(data[i_key], att_vals, accumulator + f"{search}='{i_key}',")


def read_phonology(data: PhonologyConfig) -> Phonology:
    """
    Le format de Phonology.yaml n'est pas très stabilisé. J'ai donc choisi de figer
    apophonies, derives, mutations, consonnes et voyelles.
    :param data : structure de configuration pour créer un Phonology
    :return : une data class Phonology
    precondition : la structure de configuration ne doit pas être vide
    """
    assert data

    return Phonology(
        apophonies=frozendict(data["apophonies"]),
        derives=frozendict(data["derives"]),
        mutations=frozendict(data["mutations"]),
        consonnes=frozenset(data["consonnes"]),
        voyelles=frozenset(data["voyelles"])
    )


def read_morphosyntax(data: MorphoSyntaxConfig) -> MorphoSyntax:
    """
    Constructeur de MorphoSyntax
    :param data : un dictionnaire respectant les clés de MorphoSyntax
    :return : une DataClass MorphoSyntax
    pre-condition: la structure ne peut pas être vide
    """
    assert data
    return MorphoSyntax(**data)


def __(_sigma: frozendict, k_morphemes: List[Morpheme], t_morphemes: List[Morpheme]) -> Callable[[Lexeme], Forme]:
    """
    Il faut "bind" ces deux paramètres sinon cela ne donnera pas l'effet escompté...
    :param _sigma:
    :param k_morphemes:
    :param t_morphemes:
    :return:
    """

    def _(lexeme: Lexeme) -> Forme:
        """
        :param lexeme:
        :return:
        """
        return Forme(pos=lexeme.pos,
                     morphemes=[Radical(stem=lexeme.stem,
                                        rule=None,
                                        sigma=lexeme.sigma),
                                *k_morphemes],
                     sigma=_sigma,
                     traduction=Forme(pos=lexeme.traduction.pos,
                                      morphemes=[Radical(stem=lexeme.traduction.stem,
                                                         rule=None,
                                                         sigma=lexeme.traduction.sigma),
                                                 *t_morphemes],
                                      sigma=_sigma,
                                      traduction=None))

    return _


def build_paradigm(
        glose: Dict[str, Dict[str, List[frozendict]]],
        blocks: Dict[str, Dict[str, TypeBlocks]]
) -> Dict[str, Dict[frozendict, Callable[[Lexeme], Forme]]]:
    """
    output : {N: {{genre: m, nombre: sg}: lambda lexeme: Forme(morphemes=[Radical(stem=lexeme.stem)...])
                  {genre: m, nombre: pl}: lambda lexeme: Forme(morphemes=[Radical(stem=lexeme.stem)...])
                  {genre: f, nombre: sg}: lambda lexeme: Forme(morphemes=[Radical(stem=lexeme.stem)...])
                  {genre: f, nombre: pl}: lambda lexeme: Forme(morphemes=[Radical(stem=lexeme.stem)...])}}

    :param glose :
    :param blocks :
    :return :
    """
    assert glose
    assert blocks
    assert all(blocks.values())

    output: Dict[str, Dict[frozendict, Callable[[Lexeme], Forme]]] = {}

    for i_category, i_sigmas in glose.items():
        assert i_sigmas

        for i_sigma in i_sigmas:
            try:
                k_morphemes = _select(blocks["kalaba"][i_category], i_sigma)
            except KeyError:
                k_morphemes = []
            except DispatchError as ex:
                raise ValueError(Errors.E005) from ex
            try:
                t_morphemes = _select(blocks["translation"][i_category], i_sigma)
            except KeyError:
                t_morphemes = []
            except DispatchError as ex:
                raise ValueError(Errors.E005) from ex
            output.setdefault(i_category, {}).setdefault(i_sigma, __(i_sigma, k_morphemes, t_morphemes))
    return output


def read_rules(morphosyntax: MorphoSyntax) -> Tuple[List[str], List[str]]:
    """
    Construit deux grammaires FCFG à partir d'un MorphoSyntax
    La G1 générée est la grammaire du français qui traduit en kalaba
    La G2 générée est la grammaire du kalaba qui vérifie que le kalaba généré est valide
    :param morphosyntax : Structure encodant la tête de la grammaire,
                         ses syntagmes, les informations d'accord et de traduction
    :return : un itérateur de règles non lexicales
              Le premier élément de l'itérateur est la tête de la grammaire.
    TODO : clairement à refactorer... beaucoup trop complexe pour pas grand chose
    """
    # gestion de start
    G1: List[str]
    G2: List[str]
    G1, G2 = [f"% start {morphosyntax.start}"], [f"% start {morphosyntax.start}"]

    for lhs, rhs in morphosyntax.syntagmes.items():
        # Accord : gestion de la partie droite
        for i_idx, i_rhs in enumerate(rhs):
            for j_rhs in develop(i_rhs):
                count = {k: (x for x in range(0, v))  # type: ignore
                         for k, v in collections.Counter(j_rhs).items()}

                __traduction = [""] * len(j_rhs)
                __trad_perco = [""] * len(j_rhs)

                for i_pos, i_cat in enumerate(j_rhs):
                    if not i_cat:
                        continue
                    if i_cat.startswith("'"):
                        continue
                    try:
                        accord = _format_dict(morphosyntax.accords[lhs][i_idx][i_pos])
                    except KeyError:
                        accord = ""

                    next_id = next(count[i_cat])
                    traduction = f"{i_cat.lower()}{str(next_id) if next_id > 0 else ''}"
                    __trad_perco[i_pos] = traduction
                    j_rhs[i_pos] = f"{i_cat}[{accord + ',' if accord else accord}Traduction=?{traduction}]"

                __traduction = [_retire_traduction(j_rhs[k_idx]) for k_idx in morphosyntax.traductions[lhs][i_idx] if
                                j_rhs[k_idx]]
                __trad_perco = [__trad_perco[k_idx] for k_idx in morphosyntax.traductions[lhs][i_idx] if j_rhs[k_idx]]

                # Percolation : gestion de la partie gauche
                try:
                    accord = ",".join([f"{x}={y if y != '*' else f'?{x.lower()}'}" for x, y in
                                       morphosyntax.percolations[lhs][i_idx].items()])
                except KeyError:
                    accord = ""

                _traduction = "+".join([f"?{x}" for x in __trad_perco if x])
                traduction = ("," if accord else "") + (
                    f"Traduction=({_traduction})" if "+" in _traduction else f"Traduction={_traduction}")
                G1.append(f"{lhs}[{accord}{traduction}] -> {' '.join(x for x in j_rhs if x)}")
                G2.append(f"{lhs}[{accord}] -> {' '.join(x for x in __traduction if x)}")
    return G1, G2


@multimethod
def validate_attribute(values: str, attributes: frozendict) -> NoReturn:
    """
    :param values:
    :param attributes:
    :return:
    """
    if values not in attributes:
        raise AttributeError(f"'{values}' n'est pas une valeur disponible.")


@multimethod  # type: ignore
def validate_attribute(values: frozendict, att_vals: frozendict) -> NoReturn:
    """
    :param values:
    :param att_vals:
    :return:
    """
    for i_attribute, i_value in values.items():
        try:
            if i_attribute != att_vals[i_value]:
                raise ValueError(Errors.E006.format(attribute=i_attribute, attributes=sorted(set(att_vals.values()))))
        except KeyError as ex:
            raise ValueError(Errors.E007.format(value=i_value, values=sorted(set(att_vals.keys())))) from ex


__all__ = ["read_glose",
           "read_phonology",
           "read_stems",
           "read_traduction",
           "read_rules",
           "read_blocks",
           "read_morphosyntax",
           "filter_grid"]

# TypeBlocks, TypeGloses, TypeMorphoSyntax, TypePhonology, TypeStems, TypeTraduction
