"""Mixin that dispatches parse() to _parse_* methods by data type and keep mode."""

from typing import Literal, overload

from pfmg.parsing.parsable import ABCParsable


class MixinParseParsable(ABCParsable):
    """Mixin that routes parse(data, keep) to _parse_<type(data)>_<keep>(data)."""

    @overload
    def parse(self, data: str, keep: Literal["first"]) -> str: ...

    @overload
    def parse(self, data: str | list[str], keep: Literal["all"]) -> list[str]: ...

    @overload
    def parse(self, data: list[str], keep: Literal["first", "all"]) -> list[str]: ...

    def parse(self, data, keep):
        """Dispatch to _parse_str_first, _parse_list_all, etc. based on data type and keep.

        Args:
            data: String or list of strings to parse.
            keep: "first" or "all".

        Returns:
            str | list[str]: Result from the dispatched _parse_* method.

        """
        name = f"_parse_{type(data).__name__}_{keep}"
        return getattr(self, name)(data=data)
