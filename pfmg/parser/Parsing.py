"""Interface d'un Parseur de strings.

On dévie légèrement de la logique de NLTK pour manipuler nos propres structures.
Un parseur renverra donc des Sentences et non des Trees.
"""
import enum
from abc import ABC, abstractmethod
from collections.abc import Generator, Iterator

from factory.factory import factory_self_object
from nltk import ParserI, Tree
from nltk.grammar import FeatureGrammar
from nltk.parse.earleychart import FeatureEarleyChartParser

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
                case Tree():
                    translation: tuple[str, ...]
                    translation = translation_tree["Source", "Traduction"]
                    validation = self.__validator.parse_one(list(translation))
                    match validation:
                        case None:
                            # La traduction n'est pas reconnue par la grammaire
                            return None
                        case Tree():
                            yield translation_tree

    def parse_sents(
        self,
        sents: Iterator[str],
    ) -> Iterator[Iterator[Sentence | None]]:
        """Calcule tous les arbres pour chaucune des phrases données.

        :param sents:
        :return:
        """
        return (sent for sent in sents)


class ValidatorParser(ABCParser):
    """Parseur de validation à effectuer après la traduction."""

    __parser: ParserI

    def __init__(self, fcfg: FeatureGrammar) -> None:
        """Initialise la fcfg.

        :param fcfg: Une grammaire faiblement contextuelle
        """
        self.__parser = FeatureEarleyChartParser(grammar=fcfg)

    def parse_one(self, sent: str) -> Tree | None:
        """Récupère le premier arbre qui vient.

        :param sent: une phrase quelconque
        :return: le premier arbre qui vient
        """
        raise NotImplementedError

    def parse_all(
        self,
        sent: str,
    ) -> Generator[Tree | None, None, None]:
        """Récupère tous les arbres possibles pour 'sent'.

        :param sent: Une phrase quelconque
        """
        raise NotImplementedError

    def parse_sents(
        self,
        sents: Generator[str, None, None],
    ) -> Generator[Generator[Tree | None, None, None], None, None]:
        """Renvoie tous les arbres pour toutes les 'sents'.

        :param sents: Set de phrases
        """
        raise NotImplementedError


class TranslatorParser(ABCParser):
    """Parseur de traduction."""

    __parser: ParserI

    def __init__(self, fcfg: FeatureGrammar) -> None:
        """Initialise la fcfg.

        :param fcfg: Une grammaire faiblement contextuelle
        """
        self.__parser = FeatureEarleyChartParser(grammar=fcfg)

    def parse_one(self, sent: str) -> Tree | None:
        """Récupère le premier arbre trouvé pour 'sent'.

        :param sent: une phrase quelconque.
        :return: le premiera arbre trouvé
        """
        raise NotImplementedError

    def parse_all(
        self,
        sent: str,
    ) -> Generator[Tree | None, None, None]:
        """Récupère tous les arbres pour 'sent'.

        :param sent: une phrase quelconque
        :return: tous les arbres pour cette phrase
        """
        return self.__parser.parse_all(sent)

    def parse_sents(
        self,
        sents: Generator[str, None, None],
    ) -> Generator[Generator[Tree | None, None, None], None, None]:
        """Récupère tous les arbres de toutes les 'sents'.

        :param sents: des phrases quelconques
        :return: tous les arbres de toutes les 'sents'
        """
        raise NotImplementedError
