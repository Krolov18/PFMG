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
from typing import Literal, overload

from pfmg.utils.abstract_factory import factory_method


class ABCParsable(ABC):
    """Interface pour les objects parsable.

    Chacune des méthode ce-dessous va parser une ou plusieurs phrases
    afin de calculer une structure Sentence sous-jacente.
    """

    @overload
    @abstractmethod
    def parse(self, data: str, keep: Literal["first"]) -> str: ...

    @overload
    @abstractmethod
    def parse(
        self, data: str | list[str], keep: Literal["all"]
    ) -> list[str]: ...

    @overload
    @abstractmethod
    def parse(
        self, data: list[str], keep: Literal["first", "all"]
    ) -> list[str]: ...

    @abstractmethod
    def parse(self, data, keep):
        """TODO : Write some doc.

        :param data:
        :param keep:
        :return:
        """
        raise NotImplementedError


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
