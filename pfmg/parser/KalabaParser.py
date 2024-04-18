# Copyright (c) <year>, <copyright holder>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""KalabaParser."""

from collections.abc import Iterator

from nltk.grammar import FeatureGrammar

from pfmg.lexique.sentence.Sentence import Sentence
from pfmg.parser.ABCParser import ABCParser, IdParserEnum, create_parser


class KalabaParser(ABCParser):
    """Parseur en deux étapes.

    On traduit la phrase donnée avec un premier parseur
    puis onvalide la traduction avec un second parseur.
    """

    __validator: ABCParser
    __translator: ABCParser

    def __init__(self, fcfg: FeatureGrammar) -> None:
        """Initialise la fcfg.

        :param fcfg: Une grammaire faiblement contextuelle (NLTK)
        """
        self.__validator = create_parser(
            id_parser=IdParserEnum.validator,
            fcfg=fcfg,
        )
        self.__translator = create_parser(
            id_parser=IdParserEnum.translator,
            fcfg=fcfg,
        )

    def parse_one(self, sent: str) -> Sentence | None:
        """Calcule le premier arbre trouvé.

        :param sent: une chaine de caractères
        :return:
        """
        return next(self.parse_all(sent), None)

    def parse_all(
        self,
        sent: str,
    ) -> Iterator[Sentence]:
        """Calcule tous les arbres couverts par la grammaire sur cette phrase.

        :param sent:
        :return:
        """
        translation_trees = self.__translator.parse_all(sent)
        for translation_tree in translation_trees:
            match translation_tree:
                case None:
                    # la phrase en français n'est pas reconnue pas la grammaire
                    return None
                case Sentence():
                    translation: tuple[str, ...]
                    translation = translation_tree.get("Source", "Traduction")  # type: ignore reportAttributeAccessIssue
                    validation = self.__validator.parse_one(list(translation))  # type: ignore reportArgumentType
                    match validation:
                        case None:
                            # La traduction n'est pas reconnue par la grammaire
                            return None
                        case Sentence():
                            yield translation_tree

    def parse_sents(
        self,
        sents: Iterator[str],
    ) -> Iterator[Iterator[Sentence]]:
        """Calcule tous les arbres pour chaucune des phrases données.

        :param sents:
        :return:
        """
        return (self.parse_all(sent) for sent in sents)
