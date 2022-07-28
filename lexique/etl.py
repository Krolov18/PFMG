""" Commandes pour charger les différentes données d'une grammaire """
import collections
import itertools
import re
from typing import Dict, List, Optional, Union, Callable, Tuple, NoReturn, Iterator, Set, Literal, Any
from typing_extensions import TypeAlias

from frozendict import frozendict  # type: ignore

from lexique.errors import Errors
from lexique.ruler import ruler
from lexique.structures import (Morpheme, Forme,
                                Radical, Lexeme,
                                Phonology, MorphoSyntax,
                                MorphoSyntaxConfig, PhonologyConfig,
                                TypeBlock, TypeBlocks,
                                TypeStems, TypeSigma, TypeCatBlockConfig, TypeBlocksConfig)
from lexique.syntax import develop
from utils.abstract_factory import factory_function
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


def _select(block, sigma: frozendict) -> Union[Morpheme, List[Morpheme]]:
    if not block:
        block_name = type(block).__name__.lower()
        first = type(block[0]).__name__.lower()
        return factory_function(
            concrete_product=f"_select_{block_name}_{first}",
            package=__name__,
            block=block,
            sigma=sigma
        )
    return []


def _select_list_morpheme(block: TypeBlock, sigma: frozendict) -> Morpheme:
    """
    Sélectionne la règle plus spécifique par rapport aux traits présents dans la glose
    :param block : dictionnaire ordonné de règles de la plus générale à la plus spécifique
    :param sigma : cellule d'un paradigme
    :return : l'instance d'un morphème
    """
    assert block

    winner: Optional[Morpheme] = None
    for morpheme in block:
        assert morpheme.sigma is not None
        if morpheme.sigma.items() <= sigma.items():
            winner = morpheme

    assert winner
    return winner


def _select_list_list(blocks: TypeBlocks, sigma: frozendict) -> List[Morpheme]:
    """
    Pour qu'une forme existe, il se doit d'appliquer tous les blocks dans le bon ordre
    :param blocks : liste de dictionnaire ordonné de règles du plus général au plus spécifique
    :param sigma : cellule d'un paradigme
    :return : liste de morphèmes
    """
    output: List[Morpheme] = []

    for block in blocks:
        try:
            output.append(_select_list_morpheme(block, sigma))
        except AssertionError:
            continue
    return output


def _sigmas(glose) -> List[frozendict]:
    return factory_function(concrete_product=f"_sigmas_{type(glose).__name__.lower()}",
                            package=__name__,
                            glose=glose)


def _sigmas_dict(glose: Dict[str, List[str]]) -> List[frozendict]:
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


def _sigmas_list(glose: List[Dict[str, List[str]]]) -> List[frozendict]:
    """
    :param glose:
    :return:
    """
    return [*itertools.chain.from_iterable(_sigmas(g) for g in glose)]


def _value2attributes(glose: Dict[str, Dict[str, List[str]]]) -> frozendict:
    """
    :param glose:
    :return:
    """
    output: Dict[str, str] = {}

    for category, gloses in glose.items():
        output[category] = "pos"
        output.update(_value2attribute(gloses))

    return frozendict(output)


def _value2attribute(glose: Dict[str, Any]) -> frozendict:
    try:
        return factory_function(concrete_product=f"_value2attribute_k_{type(list(glose.values())[0]).__name__.lower()}", package=__name__, glose=glose)
    except:
        return factory_function(concrete_product=f"_value2attribute_{type(glose).__name__.lower()}", package=__name__, glose=glose)


def _value2attribute_k_dict(glose: Dict[str, Dict[str, List[str]]]) -> frozendict:
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


def _value2attribute_k_list(glose: Dict[str, List[str]]) -> frozendict:
    """
    :param glose:
    :return:
    """
    output: Dict[str, str] = {}

    for attribute, values in glose.items():
        for i_value in values:
            output[i_value] = attribute

    return frozendict(output)


def _value2attribute_list(glose: List[Dict[str, List[str]]]) -> frozendict:
    """
    :param glose:
    :return:
    """
    output: Dict[str, str] = {}

    for i_glose in glose:
        output.update(_value2attribute(i_glose))

    return frozendict(output)


def _format_dict(struct: Dict[str, str], id_var: str) -> str:
    return ",".join(f"{x}={y if y != '*' else f'?{id_var}{x.lower()}'}" for x, y in struct.items())


def _format_dict2(struct: Dict[str, str]) -> Tuple[Dict[str, str], Dict[str, str]]:
    source: Dict[str, str] = {}
    destination: Dict[str, str] = {}

    for key, value in struct.items():
        if key.startswith("s"):
            source[key[1:]] = value
        elif key.startswith("d"):
            destination[key[1:]] = value

    return source, destination


@static_vars(REG=re.compile(r",?Traduction=\??\w+"))
def _retire_traduction(feature_nonterminal: str) -> str:
    return _retire_traduction.REG.sub("", feature_nonterminal)


TypeAttribute = str
TypeValue = str
TypeCategory = str
TypeValues = List[str]
TypeAttVals = Dict[TypeAttribute, TypeValues]
TypeAttVal = Dict[TypeAttribute, TypeValue]
TypeAttVals2: TypeAlias = frozendict

TypeGlosesConfig = Dict[Literal["source", "destination"], Dict[TypeCategory, TypeAttVals]]
TypeGloses = Dict[Literal["source", "destination"], TypeAttVals2]
TypeSigmaVerification = Dict[Literal["source", "destination"], TypeAttVal]


def read_glose(glose: TypeGlosesConfig) -> Tuple[TypeGloses, TypeSigmaVerification]:
    """
        input : {source: {N: genre: [m, f], nombre: [sg, pl]},
                 destination: {N: genre: [m, f], nombre: [sg, pl]}}
        output: {source: {N: [{'genre': 'm', 'nombre': 'sg'},
                     {'genre': 'm', 'nombre': 'pl'},
                     {'genre': 'f', 'nombre': 'sg'},
                     {'genre': 'f', 'nombre': 'pl'}]},
                 destination: {N: [{'genre': 'm', 'nombre': 'sg'},
                     {'genre': 'm', 'nombre': 'pl'},
                     {'genre': 'f', 'nombre': 'sg'},
                     {'genre': 'f', 'nombre': 'pl'}]}}
                {source: {},
                 destination: {}}
    :param glose:
    :return: les gloses au format décrit ci-dessus ET un dictionnaire figé valeur → attribut
    """
    if not glose:
        raise ValueError(Errors.E001)

    output_gloses: TypeGloses = {
        "source": {key: _sigmas(value) if value is not None else frozendict() for key, value in glose["source"].items()},
        "destination": {key: _sigmas(value) if value is not None else frozendict() for key, value in
                        glose["destination"].items()}}

    output_sigma_validation: TypeSigmaVerification = {"source": _value2attributes(glose["source"]),
                                                      "destination": _value2attributes(glose["destination"])}

    return output_gloses, output_sigma_validation


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

        if _blocks is None:
            output[category] = [[ruler(id_ruler="selection", rule="X1", sigma=frozendict(), voyelles=voyelles)]]
            continue

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


def read_blocks(data: TypeBlocksConfig, att_vals: TypeAttVals, voyelles: frozenset) -> Dict[str, Dict[str, TypeBlocks]]:
    """
    Lit les informations de configurations concernant les blocs de morphèmes
    aussi bien pour la traduction que pour le kalaba.

    Attention, toute information autre que les champs kalaba et translation ne seront pas pris en compte.
    :param voyelles:
    :param data:
    :param att_vals: Structure validant les attributs/valuers utilisés dans Blocks.yaml
    :return: un dictionnaire à deux clés 'kalaba' et 'translation'
    """
    try:
        source, destination = data["source"], data["destination"]
    except TypeError as ex:
        raise ValueError(Errors.E002) from ex
    except KeyError as ex:
        raise ValueError(Errors.E003) from ex

    return {"source": _read_blocks(source, att_vals["destination"], voyelles=voyelles),
            "destination": _read_blocks(destination, att_vals["source"], voyelles=voyelles)}


def read_traduction(stem: str, att_vals: frozendict) -> Tuple[TypeStems, TypeSigma]:
    """
    :param stem:
    :param att_vals:
    :return:
    """
    assert stem

    if "-" in stem:
        stems, values = stem.split("-")
        _values = frozendict({att_vals[x]: x for x in values.split(".")})
        return tuple(stems.split(",")), _values

    if "." in stem:
        raise ValueError(Errors.E014)

    return tuple(stem.split(",")), frozendict()


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
    if ("source" not in att_vals) or ("destination" not in att_vals):
        raise ValueError(Errors.E003)

    if isinstance(data, str):
        try:
            valeurs = eval(f"dict({accumulator})")
        except SyntaxError:
            valeurs = ",".join([x.split("=")[1] for x in accumulator.strip(",").split(",")])
            raise ValueError(Errors.E009.format(valeurs=valeurs)) from None

        pos = valeurs.pop("pos")
        k_stems = tuple(valeurs.pop("stem").split(","))
        try:
            t_stems, t_sigma = read_traduction(stem=data, att_vals=att_vals["destination"])
        except AssertionError:
            raise ValueError(Errors.E012)

        yield Lexeme(stem=k_stems,
                     pos=pos,
                     sigma=frozendict(valeurs),
                     traduction=Lexeme(stem=t_stems,
                                       pos=pos,
                                       sigma=t_sigma,
                                       traduction=None))
    else:
        if not data:
            raise ValueError(Errors.E013)

        for i_key in data:
            if not i_key:
                raise ValueError(Errors.E012)
            try:
                search = att_vals["source"][i_key]
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

    for i_category, i_sigmas in glose["source"].items():
        assert i_sigmas

        for i_sigma in i_sigmas:
            try:
                k_morphemes = _select(blocks["source"][i_category], i_sigma)
            except KeyError:
                k_morphemes = []
            try:
                t_morphemes = _select(blocks["destination"][i_category], i_sigma)
            except KeyError:
                t_morphemes = []
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
        for i_idx, i_rhs in enumerate(rhs):
            for j_rhs in develop(i_rhs):
                j_rhs_copy = j_rhs.copy()
                count = {k: (x for x in range(0, v)) for k, v in collections.Counter(j_rhs).items()}

                __traduction = [""] * len(j_rhs)
                __trad_perco = [""] * len(j_rhs)

                for i_pos, i_cat in enumerate(j_rhs):
                    if not i_cat:
                        continue
                    if i_cat.startswith("'"):
                        continue
                    try:
                        source, destination = _format_dict2(morphosyntax.accords[lhs][i_idx][i_pos])
                        _source = _format_dict(source, "s")
                        _destination = _format_dict(destination, "d")
                    except KeyError:
                        _source = ""
                        _destination = ""

                    next_id = next(count[i_cat])
                    traduction = f"{i_cat.lower()}{str(next_id) if next_id > 0 else ''}"
                    __trad_perco[i_pos] = traduction

                    j_rhs[
                        i_pos] = f"{i_cat}[Source=[{_source},Traduction=?{traduction}],Destination=[{_destination}]]"
                    j_rhs_copy[i_pos] = f"{i_cat}[{_destination}]"

                __traduction = [j_rhs_copy[k_idx] for k_idx in morphosyntax.traductions[lhs][i_idx] if
                                j_rhs_copy[k_idx]]
                __trad_perco = [__trad_perco[k_idx] for k_idx in morphosyntax.traductions[lhs][i_idx] if
                                j_rhs[k_idx]]

                # Percolation : gestion de la partie gauche
                source, destination = _format_dict2(morphosyntax.percolations[lhs][i_idx])
                _source = _format_dict(source, "s")
                _destination = _format_dict(destination, "d")
                _traduction = "+".join([f"?{x}" for x in __trad_perco if x])

                G1.append(
                    f"{lhs}[Source=[{_source},Traduction=({_traduction})],Destination=[{_destination}]] -> {' '.join(x for x in j_rhs if x)}")
                G2.append(f"{lhs}[{_destination}] -> {' '.join(x for x in __traduction if x)}")
    return G1, G2


def validate_attribute(values, att_vals):
    return factory_function(concrete_product=f"validate_attribute_{type(values).__name__.lower()}",
                            package=__name__,
                            values=values,
                            att_vals=att_vals)


def validate_attribute_str(values: str, att_vals: frozendict) -> NoReturn:
    """
    :param values:
    :param att_vals:
    :return:
    """
    assert att_vals
    if values not in att_vals:
        raise AttributeError(f"'{values}' n'est pas une valeur disponible.")


def validate_attribute_frozendict(values: frozendict, att_vals: frozendict) -> NoReturn:
    """
    :param values:
    :param att_vals:
    :return:
    """
    assert values
    for i_attribute, i_value in values.items():
        try:
            if i_attribute != att_vals[i_value]:
                raise ValueError(
                    Errors.E006.format(attribute=i_attribute, attributes=sorted(set(att_vals.values()))))
        except KeyError as ex:
            raise ValueError(Errors.E007.format(value=i_value, values=sorted(set(att_vals.keys())))) from ex


__all__ = ["read_glose",
           "read_phonology",
           "read_stems",
           "read_traduction",
           "read_rules",
           "read_blocks",
           "read_morphosyntax"]

# TypeBlocks, TypeGloses, TypeMorphoSyntax, TypePhonology, TypeStems, TypeTraduction
