"""Interface pour les tokenizers."""

from abc import ABC, abstractmethod


class ABCTokenizer(ABC):
    """Interface pour ce qui est toknisable."""

    @abstractmethod
    def tokenize(self, sentence: str) -> list[str]:
        """Split some sentence into tokens.

        :param sentence:
        :return:
        """
