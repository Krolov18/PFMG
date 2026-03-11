"""TODO : Write some doc."""
from typing import Literal, overload

from pfmg.parsing.parsable import ABCParsable


class MixinParseParsable(ABCParsable):
    """TODO : Write some doc."""

    @overload
    def parse(self, data: str, keep: Literal["first"]) -> str: ...

    @overload
    def parse(
        self, data: str | list[str], keep: Literal["all"]
    ) -> list[str]: ...

    @overload
    def parse(
        self, data: list[str], keep: Literal["first", "all"]
    ) -> list[str]: ...

    def parse(self, data, keep):
        """TODO : Write some doc."""
        name = f"_parse_{type(data).__name__}_{keep}"
        return getattr(self, name)(data=data)
