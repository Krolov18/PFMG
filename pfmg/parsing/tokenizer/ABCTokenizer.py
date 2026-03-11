"""Interface pour les tokenizers."""
from abc import ABC, abstractmethod

from pfmg.utils.abstract_factory import factory_method


class ABCTokenizer(ABC):
    """Interface pour ce qui est toknisable."""

    @abstractmethod
    def __call__(self, sentence: str) -> list[str]:
        """Split some sentence into tokens.

        :param sentence:
        :return:
        """


def new_tokenizer(id_tokenizer: str) -> ABCTokenizer:
    """Factory qui construit n'importe quel tokenizer.

    Args:
    ----
        id_tokenizer: Identifiant unique d'un tokenizer
                      présent dans le même package

    Returns:
    -------
        ABCTokenizer: Une instance de tokenizer

    """
    assert __package__ is not None

    return factory_method(
        concrete_product=f"{id_tokenizer}Tokenizer", package=__package__
    )
