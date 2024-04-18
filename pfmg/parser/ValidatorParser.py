# Copyright (c) <year>, <copyright holder>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""ValidatorParser."""

from collections.abc import Iterator

from nltk import ParserI
from nltk.grammar import FeatureGrammar
from nltk.parse.earleychart import FeatureEarleyChartParser

from pfmg.lexique.sentence.Sentence import Sentence
from pfmg.parser.ABCParser import ABCParser


class ValidatorParser(ABCParser):
    """Parseur de validation à effectuer après la traduction."""

    __parser: ParserI

    def __init__(self, fcfg: FeatureGrammar) -> None:
        """Initialise la fcfg.

        :param fcfg: Une grammaire faiblement contextuelle
        """
        self.__parser = FeatureEarleyChartParser(grammar=fcfg)

    def parse_one(self, sent: str) -> Sentence | None:
        """Récupère le premier arbre qui vient.

        :param sent: une phrase quelconque
        :return: le premier arbre qui vient
        """
        raise NotImplementedError

    def parse_all(
        self,
        sent: str,
    ) -> Iterator[Sentence]:
        """Récupère tous les arbres possibles pour 'sent'.

        :param sent: Une phrase quelconque
        """
        raise NotImplementedError

    def parse_sents(
        self,
        sents: Iterator[str],
    ) -> Iterator[Iterator[Sentence]]:
        """Renvoie tous les arbres pour toutes les 'sents'.

        :param sents: Set de phrases
        """
        raise NotImplementedError
