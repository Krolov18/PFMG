"""TODO : Write some doc."""

from collections.abc import Iterator

from pfmg.lexique.sentence.Sentence import Sentence
from pfmg.parsing.parsable import ABCParsable


class MixinParse2Parsable(ABCParsable):
    """TODO : Write some doc."""

    def _parse_first_str(self, data: str) -> Sentence:
        """TODO : Write some doc.

        :param data:
        :return:
        """
        raise NotImplementedError

    def _parse_first_list(self, data: list[str]) -> Iterator[Sentence]:
        """TODO : Write some doc.

        :param data:
        :return:
        """
        raise NotImplementedError

    def _parse_all_str(self, data: str) -> Iterator[Sentence]:
        """TODO : Write some doc.

        :param data:
        :return:
        """
        raise NotImplementedError

    def _parse_all_list(self, data: list[str]) -> Iterator[Sentence]:
        """TODO : Write some doc.

        :param data:
        :return:
        """
        raise NotImplementedError
