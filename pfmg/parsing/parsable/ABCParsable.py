# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Interface d'un Parseur de strings.

On dévie légèrement de la logique de NLTK pour manipuler nos propres structures.
Un parseur renverra donc des Sentences et non des Trees.
"""

import enum
from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import Literal

from pfmg.lexique.sentence.Sentence import Sentence
from pfmg.utils.abstract_factory import (
    factory_method,
)


class ABCParsable(ABC):
    """Interface pour les objects parsable.

    Chacune des méthode ce-dessous va parser une ou plusieurs phrases
    afin de calculer une structure Sentence sous-jacente.
    """

    @abstractmethod
    def parse(
        self, data: str | list[str], keep: Literal["all", "first"]
    ) -> Iterator[Sentence]:
        """TODO : Write some doc.

        :param data:
        :param keep:
        :return:
        """

    @abstractmethod
    def _parse_first_str(self, data: str) -> Sentence:
        """TODO : Write some doc.

        :param data:
        :return:
        """

    @abstractmethod
    def _parse_first_list(self, data: list[str]) -> Iterator[Sentence]:
        """TODO : Write some doc.

        :param data:
        :return:
        """

    @abstractmethod
    def _parse_all_str(self, data: str) -> Iterator[Sentence]:
        """TODO : Write some doc.

        :param data:
        :return:
        """

    @abstractmethod
    def _parse_all_list(self, data: list[str]) -> Iterator[Sentence]:
        """TODO : Write some doc.

        :param data:
        :return:
        """


class IdParsableEnum(enum.Enum):
    """Tous les identifiants possibles pour les objects parsables."""


def create_parsable(id_parsable: IdParsableEnum) -> ABCParsable:
    """Factory pour construire un object parsable.

    Contraint par IdParserEnum.

    :return: instance d'un object parsable
    """
    assert __package__ is not None
    return factory_method(
        concrete_product=f"{id_parsable.value}Parser", package=__package__
    )
