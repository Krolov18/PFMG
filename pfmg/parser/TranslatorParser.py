# Copyright (c) <year>, <copyright holder>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""TranslatorParser."""

from collections.abc import Iterator

from nltk import ParserI
from nltk.grammar import FeatureGrammar
from nltk.parse.earleychart import FeatureEarleyChartParser

from pfmg.lexique.sentence.Sentence import Sentence
from pfmg.parser.ABCParser import ABCParser


class TranslatorParser(ABCParser):
    """Parseur de traduction."""

    __parser: ParserI

    def __init__(self, fcfg: FeatureGrammar) -> None:
        """Initialise la fcfg.

        :param fcfg: Une grammaire faiblement contextuelle
        """
        self.__parser = FeatureEarleyChartParser(grammar=fcfg)

    def parse_one(self, sent: str) -> Sentence | None:
        """Récupère le premier arbre trouvé pour 'sent'.

        :param sent: une phrase quelconque.
        :return: le premiera arbre trouvé
        """
        raise NotImplementedError

    def parse_all(
        self,
        sent: str,
    ) -> Iterator[Sentence]:
        """Récupère tous les arbres pour 'sent'.

        :param sent: une phrase quelconque
        :return: tous les arbres pour cette phrase
        """
        return (x for x in self.__parser.parse_all(sent))

    def parse_sents(
        self,
        sents: Iterator[str],
    ) -> Iterator[Iterator[Sentence]]:
        """Récupère tous les arbres de toutes les 'sents'.

        :param sents: des phrases quelconques
        :return: tous les arbres de toutes les 'sents'
        """
        raise NotImplementedError
