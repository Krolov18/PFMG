from abc import ABC, abstractmethod


class Searchable(ABC):
    @abstractmethod
    def search(self, pos: str, value: str) -> str:
        """
        :param pos:
        :param value:
        :return:
        """

    @abstractmethod
    def is_pos(self, pos: str) -> bool:
        """
        :param pos: clé de premier niveau
        :return: si oui ou non cette clé dans la structure
        """
