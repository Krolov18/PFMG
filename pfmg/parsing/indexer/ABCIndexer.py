"""Doc."""

from abc import ABC, abstractmethod

from pfmg.lexique.lexicon import Lexicon
from pfmg.utils.abstract_factory import factory_method


class ABCindexer(ABC):
    """Doc de Indexer."""

    @abstractmethod
    def __call__(self, tokens: list[str]) -> list[list[str]]:
        """Doc.

        :param tokens:
        :return:
        """


def new_indexer(id_indexer: str, lexicon: Lexicon) -> ABCindexer:
    """Factory qui construit n'import quel indexer.

    :param id_indexer: identifiant unique d'une implémentation d'indexer
    :param lexicon: instance d'un Lexicon

    Examples
    --------
    >>> from pfmg.lexique.lexicon import Lexicon
    >>> from pfmg.lexique.sentence.Sentence import Sentence
    >>> from pfmg.utils.paths import get_project_path
    >>>
    >>> config_path = get_project_path() / "examples" / "data"
    >>> lexicon = Lexicon.from_yaml(config_path)
    >>> indexer = new_indexer("Desamb", lexicon=lexicon)
    >>> actual = indexer(["le", "bruit"])
    >>> assert isinstance(actual, Sentence)
    >>> assert str(actual) == "Sentence([10, 12])"

    :returns: ABCIndexer: Instance d'indexer

    """
    assert __package__ is not None
    return factory_method(
        concrete_product=f"{id_indexer}Indexer",
        package=__package__,
        lexicon=lexicon,
    )
