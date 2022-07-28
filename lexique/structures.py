"""
    Structures nécessaires au bon fonctionnement de la grammaire.

    Un lexeme est une Forme abstraite.
    La forme est la réalisation d'un lexème.
    Les morphèmes 'composent' une forme.
"""

from dataclasses import dataclass
from typing import List, Match, Optional, Union, Tuple, Dict, TypedDict, Set, Literal

from frozendict import frozendict  # type: ignore


@dataclass
class Morpheme:
    """
    Base DatClass pour représenter un morphème.

    :param rule : Résultat d'une regex (un Match)
    :param sigma : Informations morphosyntaxiques d'un morphème
    """
    rule: Optional[Match]
    sigma: Optional[frozendict]


TypeBlock = List[Morpheme]
TypeBlocks = List[TypeBlock]
TypeStem = str
TypeStems = Tuple[TypeStem, ...]
TypeSigma = frozendict


@dataclass
class Prefix(Morpheme):
    """
    Un préfixe encode une règle affixale précédant le Radical.
    """


@dataclass
class Suffix(Morpheme):
    """
    Un suffixe encode une règle affixale succédant le Radical.
    """


@dataclass
class Circumfix(Morpheme):
    """
    Un circonfixe encode une règle affixale préfixant ET suffixant le Radical simultanément.
    """


@dataclass
class Radical(Morpheme):
    """
    Le radical est la partie non réalisée du Morphème.

    :param stem : Radicaux dont le lexème aura besoin pour être réalisé.
    """
    stem: Tuple[str, ...]


@dataclass
class Gabarit(Morpheme):
    """
    Le gabarit encode une règle affixale qui touche la structure du Radical.
    Dans la règle gabaritique, les consonnes comme les voyelles peuvent subir des modifications phonologiques.
    """


@dataclass
class Realisation:
    """
    Base DataClass pour les Formes.

    :param pos : Catégorie syntaxique
    :param morphemes : Liste des morphèmes dont la forme est composée
    :param sigma : Informations morphosyntaxiques de la forme
    """
    pos: str
    morphemes: List[Morpheme]
    sigma: frozendict


@dataclass
class Forme(Realisation):
    """
    La forme est la réalisation d'un lexème.

    :param traduction : Réalisation du lexème de la traduction
    """
    traduction: Optional[Realisation] = None


@dataclass
class LexSign:
    """
    Base DataClass pour les Lexèmes.

    :param stem : radicaux disponibles
    :param pos : catégorie syntaxique
    :param sigma : Informations morphosyntaxiques inhérentes au lexème
    """
    stem: Union[str, Tuple[str, ...]]
    pos: str
    sigma: frozendict


@dataclass
class Lexeme(LexSign):
    """
    Représentation abstraite d'une Forme.

    :param traduction : Lexeme
    """
    traduction: Optional[LexSign] = None


TypeCategories = List[str]
TypeCategoriesPositions = List[int]


@dataclass
class Selection(Morpheme):
    """
    Pseudo-Morpheme qui permet de construire une règle de sélection de radical.
    """


@dataclass
class Condition(Morpheme):
    """
    Pseudo-morpheme permettant d'encoder la règle ternaire au sein des règles morphologiques.

    :param cond : Construction du morphème
    :param true : Si la construction de la condition réussie, on récupère true.
    :param false : Si la construction de la condition échoue, on récupère false.
    """
    cond: Morpheme
    true: Morpheme
    false: Morpheme


@dataclass
class MorphoSyntax:
    """
    DataClass encodant les éléments syntaxiques.

    :param contractions : mots du français qui doivent être délié lors du parsing.
    :param syntagmes : Règles syntaxiques de la grammaire.
                       Uniquement les parties gauche et droite des règles.
    :param start : Non-terminal considéré comme étant la tête de la grammaire.
    :param accords : Contexte des éléments de la partie droite.
                     Encodage des règles d'accord au sin de la partie droite de la règle.
    :param percolations : Contexte de la partie gauche de la règle.
    :param traduction : Structure identique à celle de syntagmes.
                        Elle permet de réordonner les éléments pour la traduction.
                        La traduction sera encodée dans la partie gauche des règles.
    """
    contractions: frozendict
    start: str
    syntagmes: Dict[str, List[TypeCategories]]
    accords: Dict[str, List[List[Dict[str, str]]]]
    percolations: Dict[str, List[Dict[str, str]]]
    traductions: Dict[str, List[TypeCategoriesPositions]]


class MorphoSyntaxConfig(TypedDict):
    """
    Structure de données contenant :
        - les contractions
        - la description des syntagmes avec clé le noeaud syntaxique et en valeur la liste de ses constituants
        - le "point de départ" : Le noeud
    """
    contractions: Dict[str, str]
    syntagmes: Dict[str, List[TypeCategories]]
    start: str
    accords: Dict[str, List[Dict[str, Dict[str, str]]]]
    percolations: Dict[str, List[Dict[str, str]]]
    traductions: Dict[str, List[TypeCategoriesPositions]]


TypeSigmaRule = Dict[str, str]
TypeBlockConfig = Dict[str, TypeSigmaRule]
TypeCatBlockConfig = Dict[str, TypeBlockConfig]
TypeBlocksConfig = Dict[Literal["source", "destination"], TypeCatBlockConfig]


class PhonologyConfig(TypedDict):
    """
    Structure de données contenant :
        - Les consonnes et les voyelles
        - Les règles de transformation apophoniques
        - Les règles des dérivés
        - Les règles des mutations
        - Les règles syllabiques
    """
    apophonies: Dict[str, str]
    derives: Dict[str, str]
    mutations: Dict[str, str]
    consonnes: Set[str]
    voyelles: Set[str]
    syllabes: Dict[str, str]


@dataclass
class Phonology:
    """
    DataClass encodant les informations phonologiques

    :param apophonies : modifications phonétiques des voyelles
    :param derives : TODO: je ne sais pas quoi mettre comme docstring...
    :param mutations : modifications phonétiques des consonnes
    :param consonnes : ensemble des consonnes
    :param voyelles : ensemble des voyelles
    """
    apophonies: frozendict
    derives: frozendict
    mutations: frozendict
    consonnes: frozenset
    voyelles: frozenset


__all__ = ["TypeBlocksConfig",
           "Circumfix",
           "Condition",
           "Forme",
           "Gabarit",
           "Lexeme",
           "LexSign",
           "Morpheme",
           "MorphoSyntax",
           "MorphoSyntaxConfig",
           "Phonology",
           "PhonologyConfig",
           "Prefix",
           "Radical",
           "Realisation",
           "Selection",
           "Suffix",
           "TypeBlock",
           "TypeBlocks",
           "TypeCategories",
           "TypeCategoriesPositions",
           "TypeSigma",
           "TypeStem",
           "TypeStems"]
