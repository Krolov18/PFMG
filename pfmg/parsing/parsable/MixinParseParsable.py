"""TODO : Write some doc."""

from collections.abc import Iterator
from typing import Literal

from pfmg.lexique.sentence.Sentence import Sentence
from pfmg.parsing.parsable import ABCParsable


class MixinParseParsable(ABCParsable):
    """TODO : Write some doc."""

    def parse(
        self, data: str | list[str], keep: Literal["all", "first"]
    ) -> Iterator[Sentence]:
        """TODO : Write some doc."""
        name = f"_parse_{type(data).__name__}_{keep}"
        return getattr(self, name)(data=data)
