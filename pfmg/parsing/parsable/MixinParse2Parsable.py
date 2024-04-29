# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
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
