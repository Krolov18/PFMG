"""Interface d'un Parseur de strings.

On dévie légèrement de la logique de NLTK pour manipuler nos propres structures.
Un parseur renverra donc des Sentences et non des Trees.
"""

import enum
from abc import ABC, abstractmethod
from collections.abc import Iterator

from factory.factory import (  # type: ignore reportMissingImports
    factory_self_object,  # type: ignore reportMissingImports
)
from nltk.grammar import FeatureGrammar

from pfmg.lexique.sentence.Sentence import Sentence


class ABCParser(ABC):
    """Même sémantique que NLTK."""

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

        :param sents: PLusieurs phrases à parser
        :return:
        """


class IdParserEnum(enum.Enum):
    """Tous les identifiants possibles pour les parseurs."""

    kalaba = "Kalaba"
    validator = "Validator"
    translator = "Translator"


def create_parser(
    id_parser: IdParserEnum,
    fcfg: FeatureGrammar,
) -> ABCParser:
    """Factory pour construire un parseur.

    Contraint par IdParserEnum.

    :return: instance d'un Parser
    """
    return factory_self_object(
        concrete_product=f"{id_parser.value}Parser",
        package=__package__,
        fcfg=fcfg,
    )
