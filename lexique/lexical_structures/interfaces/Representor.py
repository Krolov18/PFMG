from abc import ABC, abstractmethod


class Representor(ABC):
    @abstractmethod
    def __repr__(self) -> str:
        """
        :return:
        """

    @abstractmethod
    def __str__(self) -> str:
        """
        :return:
        """
