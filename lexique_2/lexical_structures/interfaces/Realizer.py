from abc import abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")
E = TypeVar("E")


class Realizer(Generic[T, E]):
    @abstractmethod
    def realize(self, lexeme: T) -> list[E]:
        """
        :param lexeme:
        :return:
        """
