from abc import ABC, abstractmethod

from frozendict import frozendict

from lexique.lexical_structures.interfaces.Display import Display


class Selector(ABC):
    @abstractmethod
    def __call__(self, pos: str, sigma: frozendict) -> list[Display]:
        """
        :param pos:
        :param sigma:
        :return:
        """
