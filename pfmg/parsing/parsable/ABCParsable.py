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

from nltk.grammar import FeatureGrammar

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
    def parse_one(self, sent: str) -> Sentence | None:
        """Calcule le premier arbre trouvé.

        :param sent: une chaine de caractère quelconque
        :return: Le premier arbre trouvé en parsant 'sent'
        """

    @abstractmethod
    def parse_all(
        self,
        sent: str,
    ) -> Iterator[Sentence]:
        """Calcule tous les arbres couverts par la grammaire sur cette phrase.

        :param sent: une chaine de caractère quelconque
        :return: Tous les arbres
        """

    @abstractmethod
    def parse_sents(
        self,
        sents: Iterator[str],
    ) -> Iterator[Iterator[Sentence]]:
        """Calcule tous les arbres pour chaucune des phrases données.

        :param sents: Plusieurs phrases à parser
        :return:
        """


class IdParsableEnum(enum.Enum):
    """Tous les identifiants possibles pour les objects parsables."""

    kalaba = "Kalaba"
    validator = "Validator"
    translator = "Translator"


def create_parsable(
    id_parsable: IdParserEnum,
    fcfg: FeatureGrammar,
) -> ABCParsable:
    """Factory pour construire un object parsable.

    Contraint par IdParserEnum.

    :return: instance d'un object parsable
    """
    assert __package__ is not None
    return factory_method(
        concrete_product=f"{id_parsable.value}Parser",
        package=__package__,
        fcfg=fcfg,
    )

