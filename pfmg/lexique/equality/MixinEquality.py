"""Mixin définissant l'agalité par défaut."""
from re import Match

from frozendict import frozendict

from pfmg.lexique.equality.Equality import Equality


class MixinEquality(Equality):
    """Mixin définissant l'agalité par défaut."""

    def get_rule(self) -> Match:
        """Récupère la règle.

        :return: la règle
        """

    def get_sigma(self) -> frozendict:
        """Récupère le sigma.

        :returns: le sigma
        """

    def __eq__(self, other: "Equality"):
        """Vérifie l'égalité entre deux objets.
        
        :param other: un autre object
        :return: bool
        """
        eq_rules = self.get_rule().string == other.get_rule().string
        return (eq_rules
                and ((self.get_sigma().items()
                      <= other.get_sigma().items())
                     or (other.get_sigma().items()
                         <= self.get_sigma().items())))
