from abc import ABC, abstractmethod

from frozendict import frozendict

from lexique_2.lexical_structures.StemSpace import StemSpace


class Display(ABC):
    @abstractmethod
    def to_string(self, term: StemSpace | str | None = None) -> str:
        """
        :param term:
        :return:
        """

    @abstractmethod
    def get_sigma(self) -> frozendict:
        """
        :return:
        """

    @abstractmethod
    def _to_string__stemspace(self, term: StemSpace) -> str:
        """
        :param term:
        :return:
        """

    @abstractmethod
    def _to_string__str(self, term: str) -> str:
        """
        :param term:
        :return:
        """

    @abstractmethod
    def _to_string__nonetype(self, term: None = None) -> str:
        """
        :param term:
        :return:
        """
