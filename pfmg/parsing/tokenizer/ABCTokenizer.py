"""Abstract base for tokenizers (sentence -> list of tokens)."""

from abc import ABC, abstractmethod

from pfmg.utils.abstract_factory import factory_method


class ABCTokenizer(ABC):
    """Abstract base for tokenizers: __call__(sentence) -> list of tokens."""

    @abstractmethod
    def __call__(self, sentence: str) -> list[str]:
        """Split sentence into tokens."""


def new_tokenizer(id_tokenizer: str) -> ABCTokenizer:
    """Factory to build a tokenizer by id (e.g. Space -> SpaceTokenizer)."""
    assert __package__ is not None

    return factory_method(
        concrete_product=f"{id_tokenizer}Tokenizer", package=__package__
    )
