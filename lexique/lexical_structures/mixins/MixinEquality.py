from typing import Match

from frozendict import frozendict

from lexique.lexical_structures.interfaces.Equality import Equality


class MixinEquality(Equality):

    def get_rule(self) -> Match[str]:
        pass

    def get_sigma(self) -> frozendict:
        pass

    def __eq__(self, other):
        eq_rules = self.get_rule().string == other.get_rule().string
        return (eq_rules
                and ((self.get_sigma().items()
                      <= other.get_sigma().items())
                     or (other.get_sigma().items()
                         <= self.get_sigma().items())))
