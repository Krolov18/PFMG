"""
    Structures nécessaires au bon fonctionnement de la grammaire.

    Un lexeme est une Forme abstraite.
    La forme est la réalisation d'un lexème.
    Les morphèmes 'composent' une forme.
"""

from dataclasses import dataclass
from typing import Literal, Match, TypedDict, Any

from frozendict import frozendict  # type: ignore


@dataclass
class Term:
    pass


@dataclass
class Morpheme(Term):
    """
    Base DatClass pour représenter un morphème.

    :param rule : Résultat d'une regex (un Match)
    :param sigma : Informations morphosyntaxiques d'un morphème
    """
    rule: Match | None
    sigma: frozendict


# TypeBlock = list[Morpheme]
# TypeBlocks = list[TypeBlock]
# TypeStem = str
# TypeStems = tuple[TypeStem, ...]
# TypeSigma = frozendict


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
    rule = None
    stem: str | tuple[str, ...]


@dataclass
class Gabarit(Morpheme):
    """
    Le gabarit encode une règle affixale qui touche la structure du Radical.
    Dans la règle gabaritique, les consonnes comme les voyelles peuvent subir des modifications phonologiques.
    """


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
class Realisation(Term):
    """
    Base DataClass pour les Formes.

    :param pos : Catégorie syntaxique
    :param morphemes : Liste des morphèmes dont la forme est composée
    :param sigma : Informations morphosyntaxiques de la forme
    """
    pos: str
    morphemes: list[Morpheme]
    sigma: frozendict


@dataclass
class Forme(Realisation):
    """
    La forme est la réalisation d'un lexème.

    :param traduction : Réalisation du lexème de la traduction
    """
    traduction: Realisation | None = None


@dataclass
class LexSign(Term):
    """
    Base DataClass pour les Lexèmes.

    :param stem : radicaux disponibles
    :param pos : catégorie syntaxique
    :param sigma : Informations morphosyntaxiques inhérentes au lexème
    """
    stem: str | tuple[str, ...]
    pos: str
    sigma: frozendict


@dataclass
class Lexeme(LexSign):
    """
    Représentation abstraite d'une Forme.

    :param traduction : Lexeme
    """
    traduction: LexSign | None = None


##########################################################################


@dataclass
class SDConfig:
    pass


@dataclass
class CategoryAnyConfig(SDConfig):
    pass


@dataclass
class CategoryFeaturesConfig(CategoryAnyConfig):
    pass


@dataclass
class CategoryBlocksConfig(CategoryAnyConfig):
    pass


@dataclass
class MorphoSyntaxParametersConfig(SDConfig):
    syntagmes: list[list[str]]
    accords: list[list[str]]
    percolations: list
    translations: list[list[int]]


@dataclass
class Config:
    source: Any
    destination: Any


@dataclass
class GlosesConfig(Config):
    source: dict[str, dict[str, str]]
    destination: dict[str, dict[str, str]]


class FeaturesConfig(Config):
    source: dict[str, str]
    destination: dict[str, str]


Numbers = Literal["1", "2", "3", "4", "5", "6", "7", "8", "9"]


@dataclass
class BlocksConfig(Config):
    source: dict[str, dict[Numbers, dict[str, str]]]


@dataclass
class MorphoSyntaxConfig(Config):
    source: MorphoSyntaxParametersConfig
    destination: MorphoSyntaxParametersConfig
    contractions: frozendict


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
    consonnes: frozenset[str]
    voyelles: frozenset[str]


__all__ = ["Circumfix",
           "Condition",
           "Forme",
           "Gabarit",
           "Lexeme",
           "LexSign",
           "Morpheme",
           "MorphoSyntaxConfig",
           "Phonology",
           "Prefix",
           "Radical",
           "Realisation",
           "Selection",
           "Suffix"]
