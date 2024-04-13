"""Sentence."""
from dataclasses import dataclass

from pfmg.lexique.forme.Forme import Forme


@dataclass
class Sentence:
    """Représente une phrase dans notre système.

    :param words: une liste de formes
    """

    words: list[Forme]

