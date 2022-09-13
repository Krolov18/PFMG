""" Commandes pour charger les différentes données d'une grammaire """
import collections
import itertools as it
import re
from ast import literal_eval
from typing import Any, Literal, Iterator, Callable

from frozendict import frozendict  # type: ignore

from lexique.errors import Errors
from lexique.ruler import ruler
from lexique.structures import Term, FeaturesConfig, GlosesConfig, Morpheme, Lexeme, Phonology, Forme, Radical
from lexique.syntax import develop
from utils.abstract_factory import factory_function
from utils.functions import static_vars


def split(sequence: str) -> list[str]:
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
        result: frozendict = frozendict([att_val.strip().split("=")  # type: ignore
                                         for att_val in str_sigma.strip().split(",")])
    except ValueError:
        result = frozendict()
    return result


def select(blocks: list[Morpheme] | list[list[Morpheme]], sigma: frozendict) -> Morpheme | list[Morpheme]:
    match blocks:
        case []:
            pass
        case [Morpheme(), *_] as morphemes:
            winner: Morpheme | None = None
            for morpheme in morphemes:
                assert morpheme.sigma is not None
                if morpheme.sigma.items() <= sigma.items():
                    winner = morpheme
            assert winner
            return winner
        case [list(), *_] as morphemes:
            output: list[Morpheme] = []

            for block in morphemes:
                try:
                    output.append(select(block, sigma))
                except AssertionError:
                    continue
            return output
        case _:
            raise TypeError()


def sigmas(glose: dict[str, list[str]] | list[dict[str, list[str]]]) -> list[frozendict]:
    match glose:
        case {}:
            return []
        case dict() as g:
            return [*it.chain.from_iterable([frozendict(zip(keys, value)) for value in it.product(*values)]
                                            for keys, values in zip(*g.items()))]
        case list():
            return [*it.chain.from_iterable(map(sigmas, glose))]
        case _:
            TypeError()


def _value2attributes(glose: dict[str, dict[str, list[str]]]) -> frozendict:
    """
    :param glose:
    :return:
    """
    output: dict[str, str] = {}

    for category, gloses in glose.items():
        output[category] = "pos"
        output.update(_value2attribute(gloses))

    return frozendict(output)


def _value2attribute(glose: dict[str, Any]) -> frozendict:
    try:
        return factory_function(concrete_product=f"_value2attribute_k_{type(list(glose.values())[0]).__name__.lower()}",
                                package=__name__,
                                glose=glose)
    except (NameError, AttributeError):
        return factory_function(concrete_product=f"_value2attribute_{type(glose).__name__.lower()}",
                                package=__name__,
                                glose=glose)


def _value2attribute_k_dict(glose: dict[str, dict[str, list[str]]]) -> frozendict:
    """
    :param glose:
    :return:
    """
    assert isinstance(glose, dict)
    result = {}

    for category in glose:
        result[category] = "pos"

        if not glose[category]:
            continue

        for attribute, values in glose[category].items():
            for val in values:
                result[val] = attribute

    return frozendict(result)


def _value2attribute_k_list(glose: dict[str, list[str]]) -> frozendict:
    """
    :param glose:
    :return:
    """
    assert isinstance(glose, dict)
    output: dict[str, str] = {}

    for attribute, values in glose.items():
        for i_value in values:
            output[i_value] = attribute

    return frozendict(output)


def _value2attribute_list(glose: list[dict[str, list[str]]]) -> frozendict:
    """
    :param glose:
    :return:
    """
    assert isinstance(glose, list)
    output: dict[str, str] = {}

    for i_glose in glose:
        output.update(_value2attribute(i_glose))

    return frozendict(output)


def _value2attribute_nonetype(glose: list[dict[str, list[str]]]) -> frozendict:
    assert glose is None
    return frozendict()


def _format_dict(struct: dict[str, str], pokayoke: str = "") -> str:
    return ",".join(f"{x}={y if y != '*' else f'?{pokayoke}{x.lower()}'}" for x, y in struct.items())


def _format_dict2(struct: dict[str, str]) -> tuple[dict[str, str], dict[str, str]]:
    source: dict[str, str] = {}
    destination: dict[str, str] = {}

    for key, value in struct.items():
        if key.startswith("s"):
            source[key[1:]] = value
        elif key.startswith("d"):
            destination[key[1:]] = value

    return source, destination


@static_vars(REG=re.compile(r",?Traduction=\??\w+"))
def _retire_traduction(feature_nonterminal: str) -> str:
    return _retire_traduction.REG.sub("", feature_nonterminal)


# TypeAttribute = str
# TypeValue = str
# TypeCategory = str
# TypeValues = list[str]
# TypeAttVals = dict[TypeAttribute, TypeValues]
# TypeAttVal = frozendict[TypeAttribute, TypeValue]
# TypeAttVals2: TypeAlias = frozendict
#
# TypeGlosesConfig = dict[Literal["source", "destination"], dict[TypeCategory, TypeAttVals]]
# TypeGloses = dict[Literal["source", "destination"], TypeAttVals2]
# TypeSigmaVerification = dict[Literal["source", "destination"], TypeAttVal]


def read_glose(glose) -> tuple:
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

    output_gloses = {"source": frozendict({key: _sigmas(value) if value is not None else frozendict()
                                           for key, value in glose["source"].items()}),
                     "destination": frozendict({key: _sigmas(value) if value is not None else frozendict()
                                                for key, value in glose["destination"].items()})}

    output_sigma_validation = {"source": _value2attributes(glose["source"]),
                               "destination": _value2attributes(glose["destination"])}

    return output_gloses, output_sigma_validation


def read_gloses2(gloses_data: dict) -> tuple[GlosesConfig, FeaturesConfig]:
    pass


def to_sd(l: frozendict) -> frozendict[Literal["source", "destination"], frozendict]:
    output = {"source": {}, "destination": {}}
    for key, value in l.items():
        if key.startswith("d"):
            output["destination"].setdefault(key[1:], value)
        else:
            output["source"].setdefault(key, value)
    return frozendict({"source": frozendict(output["source"]),
                       "destination": frozendict(output["destination"])})


def read_gloses(gloses) -> tuple:
    """
    source:
        N:
            Nombre: [SG, PL]
    """
    pre_source = {}

    for category, att_vals in gloses["source"].items():
        if att_vals is None:
            pre_source[category] = []
            continue
        copy_att_vals = att_vals.copy()
        copy_att_vals.update({f"d{key}": value for key, value in gloses["destination"][category].items()})
        pre_source[category] = list(map(to_sd, _sigmas(copy_att_vals)))

    output_sigma_validation = {"source": _value2attributes(gloses["source"]),
                               "destination": _value2attributes(gloses["destination"])}

    return pre_source, output_sigma_validation


def _read_blocks(data, att_vals, voyelles: frozenset) -> dict[str, Any]:
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

    output: dict[str, Any] = {}
    for category, _blocks in data.items():
        validate_attribute(category, att_vals)

        if _blocks is None:
            output[category] = [[ruler(id_ruler="selection", rule="X1", sigma=frozendict(), voyelles=voyelles)]]
            continue

        blocks = []
        for sigma_rule in _blocks.values():
            block = []
            for str_sigma, rule in sigma_rule.items():
                str_sigmas = _str2sigma(str_sigma)

                validate_attribute(str_sigmas, att_vals)

                block.append(
                    ruler(rule=rule, sigma=str_sigmas, voyelles=voyelles)
                )
            blocks.append(block)
        output[category] = blocks
    return output


def read_blocks(data,
                att_vals,
                voyelles: frozenset) -> dict[str, dict[str, Any]]:
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

    return {"source": _read_blocks(data=source, att_vals=att_vals["source"], voyelles=voyelles),
            "destination": _read_blocks(destination, att_vals["destination"], voyelles=voyelles)}


def read_traduction(stem: str, att_vals: frozendict) -> tuple:
    """
    :param stem:
    :param att_vals:
    :return:
    """
    assert stem

    if "-" in stem:
        stems, values = stem.split("-")
        _values = frozendict({att_vals[x]: x for x in values.split(".")})
        return tuple(stems.split(",")) if "," in stems else stems, _values

    if "." in stem:
        raise ValueError(Errors.E014)

    return tuple(stem.split(",")) if "," in stem else stem, frozendict()


def read_stems(data: dict[str, dict],
               att_vals: dict[Literal["source", "destination"], frozendict],
               accumulator: str = "") -> Iterator[Lexeme]:
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
            valeurs: dict[str, str] = literal_eval(f"{{{accumulator}}}")
        except SyntaxError:
            message: str = ",".join([x.split("=")[1] for x in accumulator.strip(",").split(",")])
            raise ValueError(Errors.E009.format(valeurs=message)) from None
        try:
            pos = valeurs.pop("pos")
        except KeyError:
            print(valeurs)
            raise
        stem = valeurs.pop("stem")
        k_stems = tuple(stem.split(",")) if "," in stem else stem
        try:
            t_stems, t_sigma = read_traduction(stem=data, att_vals=att_vals["destination"])
        except AssertionError as exc:
            raise ValueError(Errors.E012) from exc

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

            yield from read_stems(data[i_key], att_vals, accumulator + f"'{search}': '{i_key}',")


def read_phonology(data):
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


def read_morphosyntax(data):
    """
    Constructeur de MorphoSyntax
    :param data : un dictionnaire respectant les clés de MorphoSyntax
    :return : une DataClass MorphoSyntax
    pre-condition: la structure ne peut pas être vide
    """
    assert data
    return MorphoSyntax(
        contractions=frozendict(data["contractions"]),
        start=data["start"],
        syntagmes=data["syntagmes"],
        accords=data["accords"],
        percolations=data["percolations"],
        traductions=data["traductions"]
    )


def __(_sigma: frozendict, k_morphemes: list[Morpheme], t_morphemes: list[Morpheme]) -> Callable[[Lexeme], Forme]:
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
        assert lexeme.traduction is not None
        return Forme(pos=lexeme.pos,
                     morphemes=[Radical(stem=lexeme.stem,
                                        rule=None,
                                        sigma=lexeme.sigma),
                                *k_morphemes],
                     sigma=_sigma.get("source", frozendict()),
                     traduction=Forme(pos=lexeme.traduction.pos,
                                      morphemes=[Radical(stem=lexeme.traduction.stem,
                                                         rule=None,
                                                         sigma=lexeme.traduction.sigma),
                                                 *t_morphemes],
                                      sigma=_sigma.get("destination", frozendict()),
                                      traduction=None))

    return _


def build_paradigm(
        glose: dict[str, dict[str, list[frozendict]]],
        blocks: dict[str, dict[str, Any]]
) -> dict[str, dict[frozendict, Callable[[Lexeme], Forme]]]:
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

    output: dict[str, dict[frozendict, Callable[[Lexeme], Forme]]] = {}

    for i_category, i_sigmas in glose.items():
        if not i_sigmas:
            output.setdefault(i_category, {}).setdefault(frozendict(), __(frozendict(), [], []))
            continue

        for i_sigma in i_sigmas:
            try:
                k_morphemes = _select(blocks["source"][i_category], i_sigma["source"])
            except (KeyError, TypeError):
                k_morphemes = []
            try:
                t_morphemes = _select(blocks["destination"][i_category], i_sigma["destination"])
            except (KeyError, TypeError):
                t_morphemes = []
            output.setdefault(i_category, {}).setdefault(i_sigma, __(i_sigma, k_morphemes, t_morphemes))
    return output


def dict2str(dico: dict[str, str]) -> str:
    result = ""

    for key, value in dico.items():
        result += f"{key}={('?' + key.lower()) if value == '*' else value},"

    return result.rstrip(",")


def rule2str(syntagmes: list[str], accords: list[dict[str, str]],
             percolations: dict[str, str]):
    # todo: ajouter preconditions
    output: list[str] = []

    for i_rhs in develop(syntagmes):
        # gestion du champ 'syntagmes'
        assert any(x for x in i_rhs)

        for i_idx, i_category in enumerate(i_rhs):
            if i_category:
                i_rhs[i_idx] = f"{i_category}[{dict2str(accords[i_idx])}]"

    return output


def number_elements(elements: list[str]) -> list[str]:
    dico: dict[str, int] = {}
    output: list[str] = []

    for i_element in elements:
        if i_element not in dico:
            dico[i_element] = 1
        else:
            dico[i_element] += 1
        output.append(f"{i_element}{dico[i_element]}")
    return output


def read_rules2(morphosyntax):
    output: list[str] = [f"% start {morphosyntax.start_nt}"]

    for lhs, rhs in morphosyntax.source["syntagmes"].items():
        for source_idx, source_rhs in enumerate(rhs):
            destination_rhs = morphosyntax.destination["syntagmes"][lhs][source_idx]
            for i_source_rhs, i_destination_rhs in it.zip_longest(develop(source_rhs), develop(destination_rhs)):
                source_counter = {k: (x for x in range(1, v + 1)) for k, v in collections.Counter(i_source_rhs).items()
                                  if k}
                destination_counter = {k: (x for x in range(1, v + 1)) for k, v in
                                       collections.Counter(i_source_rhs).items() if k}

                traduction_percolation = number_elements(i_destination_rhs)

                for i_pos, i_cat in enumerate(i_source_rhs):
                    if not i_cat:
                        continue
                    if i_cat.startswith("'"):
                        continue
                    try:
                        _source = _format_dict(morphosyntax.source["accords"][lhs][source_idx][i_pos])
                        _destination = _format_dict(morphosyntax.destination["accords"][lhs][source_idx][i_pos], "d")
                    except KeyError:
                        _source = ""
                        _destination = ""

                    next_source_id = next(source_counter[i_cat])
                    next_destination_id = next(destination_counter[i_cat])
                    traduction = f"{i_cat.lower()}{str(next_source_id) if next_source_id > 0 else ''}"

                    i_source_rhs[
                        i_pos] = f"{i_cat}[SOURCE=[{_source},TRADUCTION=?{traduction}],DESTINATION=[{_destination}]]"

                # __traduction = [j_rhs_copy[k_idx] for k_idx in morphosyntax.traductions[lhs][i_idx] if
                #                 j_rhs_copy[k_idx]]
                # __trad_perco = [__trad_perco[k_idx] for k_idx in morphosyntax.traductions[lhs][i_idx] if j_rhs[k_idx]]

                # Percolation : gestion de la partie gauche
                # source, destination = _format_dict2(morphosyntax.percolations[lhs][i_idx])
                _source = _format_dict(morphosyntax.source["percolations"][lhs][source_idx])
                _destination = _format_dict(morphosyntax.destination["percolations"][lhs][source_idx], "d")

                _traduction = "+".join([f"?{x.lower()}" for x in traduction_percolation if x])

                output.append(
                    f"{lhs}[SOURCE=[{_source},TRADUCTION=({_traduction})],DESTINATION=[{_destination}]] -> {' '.join(x for x in i_source_rhs if x)}")

    return output


def read_rules(morphosyntax) -> tuple[list[str], list[str]]:
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
    G1: list[str]
    G2: list[str]
    G1, G2 = [f"% start {morphosyntax.start}"], [f"% start {morphosyntax.start}"]

    for lhs, rhs in morphosyntax.syntagmes.items():
        for i_idx, i_rhs in enumerate(rhs):
            for j_rhs in develop(i_rhs):
                j_rhs_copy = j_rhs.copy()
                count = {k: (x for x in range(0, v))
                         for k, v in collections.Counter(j_rhs).items()}

                __traduction = [""] * len(j_rhs)
                __trad_perco = [""] * len(j_rhs)

                for i_pos, i_cat in enumerate(j_rhs):
                    if not i_cat:
                        continue
                    if i_cat.startswith("'"):
                        continue
                    try:
                        source, destination = _format_dict2(
                            morphosyntax.accords[lhs][i_idx][i_pos])
                        _source = _format_dict(source, "s")
                        _destination = _format_dict(destination, "d")
                    except KeyError:
                        _source = ""
                        _destination = ""

                    next_id = next(count[i_cat])
                    traduction = f"{i_cat.lower()}{str(next_id) if next_id > 0 else ''}"
                    __trad_perco[i_pos] = traduction

                    j_rhs[
                        i_pos] = f"{i_cat}[SOURCE=[{_source},TRADUCTION=?{traduction}],DESTINATION=[{_destination}]]"
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

                G1.append((f"{lhs}[SOURCE=[{_source},TRADUCTION=({_traduction})],DESTINATION=[{_destination}]]"
                           f" -> {' '.join(x for x in j_rhs if x)}"))
                G2.append(f"{lhs}[{_destination}] -> {' '.join(x for x in __traduction if x)}")
    return G1, G2


def validate_attribute(values: str, att_vals: str) -> None:
    factory_function(concrete_product=f"validate_attribute_{type(values).__name__.lower()}",
                     package=__name__,
                     values=values,
                     att_vals=att_vals)


def validate_attribute_str(values: str, att_vals: frozendict) -> None:
    """
    :param values:
    :param att_vals:
    :return:
    """
    assert att_vals
    if values not in att_vals:
        raise AttributeError(f"'{values}' n'est pas une valeur disponible.")


def validate_attribute_frozendict(values: frozendict, att_vals: frozendict) -> None:
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


def read_morphosyntax2(morpho) -> list[str]:
    output: list[str] = []

    for lhs, rhs in morpho["source"]["syntagmes"].items():
        for rule in develop(rhs):
            pass

    return output
