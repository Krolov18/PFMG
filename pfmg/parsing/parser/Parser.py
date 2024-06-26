# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""TODO : Write some doc."""

from dataclasses import dataclass
from pathlib import Path

import nltk.grammar
from nltk import FeatureEarleyChartParser, Tree

from pfmg.lexique.lexicon import Lexicon
from pfmg.parsing.grammar import Grammar
from pfmg.parsing.parsable.MixinParseParsable import MixinParseParsable
from pfmg.parsing.tokenizer import ABCTokenizer, new_tokenizer


@dataclass
class Parser(MixinParseParsable):
    """TODO : Write some doc."""

    lexique: Lexicon
    grammar: Grammar
    how: str

    def __post_init__(self):
        """TODO : Write some doc."""
        g = self.grammar.to_nltk()
        grammar = nltk.grammar.FeatureGrammar.fromstring(
            "\n\n".join((g, getattr(self.lexique, f"to_{self.how}")()))
        )

        self.tokenizer: ABCTokenizer = new_tokenizer(id_tokenizer="Space")
        self.parserj = FeatureEarleyChartParser(grammar)

    def to_file(self, path: str | Path) -> None:
        """Enregistre le contenu de la grammaire dans un fichier texte.

        :param path: Chemin de sortie pour la grammaire.
        """
        path = Path(path)
        with open(path, mode="w") as fh:
            fh.write(str(self.parserj.grammar()))

    def __tokenize(self, data: str | list[str]) -> list[str] | list[list[str]]:
        """Méthode temporaire pour tokéniser du texte."""
        match data:
            case str():
                return self.tokenizer(data)
            case list():
                return [self.tokenizer(d) for d in data]

    def _parse_str_first(self, data: str) -> Tree:
        """Retourne le premier arbre disponible.

        :param data: Une phrase
        :return: Une Sentence
        """
        return self._parse_str_all(data)[0]

    def _parse_list_first(self, data: list[str]) -> list[Tree]:
        """Pour chaque phrase de data, retourne le premier arbre disponible.

        :param data: une liste de phrases
        :return: Une liste de Sentence
        """
        return [
            result
            for x in self.__tokenize(data)
            if (result := self.parserj.parse_one(x)) is not None
        ]

    def _parse_str_all(self, data: str) -> list[Tree]:
        """Retourne tous les arbres disponibles de data.

        :param data: Une phrase
        :return: une Sentence
        """
        return list(self.parserj.parse_all(self.__tokenize(data)))

    def _parse_list_all(self, data: list[str]) -> list[Tree]:
        """Pour chaque phrase, retourne tous les arbres disponibles.

        :param data: liste de phrases
        :return: liste de Sentence
        """
        output = []
        for parsing in self.parserj.parse_sents(self.__tokenize(data)):
            output.extend(parsing)
        return output
