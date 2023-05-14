from abc import ABC, abstractmethod
from typing import Match

from frozendict import frozendict


class Equality(ABC):
    @abstractmethod
    def __eq__(self, other) -> bool:
        """
        :param other:
        :return:
        """

    @abstractmethod
    def get_rule(self) -> str:
        """
        :return:
        """

    @abstractmethod
    def get_sigma(self) -> frozendict:
        """
        :return:
        """
