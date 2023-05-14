from abc import ABC, abstractmethod

from frozendict import frozendict

from lexique_2.lexical_structures.interfaces.Display import Display


class Selector(ABC):
    @abstractmethod
    def select_morphemes(self, pos: str, sigma: frozendict) -> list[Display]:
        """
        :param pos:
        :param sigma:
        :return:
        """
