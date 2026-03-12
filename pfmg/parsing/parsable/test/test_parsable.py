"""Tests for MixinParseParsable dispatch and ABCParsable."""

from unittest.mock import MagicMock

import pytest

from pfmg.parsing.parsable.ABCParsable import ABCParsable
from pfmg.parsing.parsable.MixinParseParsable import MixinParseParsable


def test_mixin_parse_parsable_dispatch_str_first() -> None:
    class MockParsable(MixinParseParsable):
        def _parse_str_first(self, data: str) -> str:
            return f"first:{data}"

        def _parse_str_all(self, data: str) -> list[str]:
            return [f"all:{data}"]

        def _parse_list_first(self, data: list[str]) -> list[str]:
            return [f"first:{x}" for x in data]

        def _parse_list_all(self, data: list[str]) -> list[str]:
            return [f"all:{x}" for x in data]

    p = MockParsable()
    assert p.parse("hello", keep="first") == "first:hello"


def test_mixin_parse_parsable_dispatch_str_all() -> None:
    class MockParsable(MixinParseParsable):
        def _parse_str_first(self, data: str) -> str:
            return data

        def _parse_str_all(self, data: str) -> list[str]:
            return [data, data.upper()]

        def _parse_list_first(self, data: list[str]) -> list[str]:
            return data

        def _parse_list_all(self, data: list[str]) -> list[str]:
            return data + data

    p = MockParsable()
    assert p.parse("hi", keep="all") == ["hi", "HI"]


def test_mixin_parse_parsable_dispatch_list_first() -> None:
    class MockParsable(MixinParseParsable):
        def _parse_str_first(self, data: str) -> str:
            return data

        def _parse_str_all(self, data: str) -> list[str]:
            return [data]

        def _parse_list_first(self, data: list[str]) -> list[str]:
            return [f"L:{x}" for x in data]

        def _parse_list_all(self, data: list[str]) -> list[str]:
            return data

    p = MockParsable()
    assert p.parse(["a", "b"], keep="first") == ["L:a", "L:b"]


def test_mixin_parse_parsable_dispatch_list_all() -> None:
    class MockParsable(MixinParseParsable):
        def _parse_str_first(self, data: str) -> str:
            return data

        def _parse_str_all(self, data: str) -> list[str]:
            return [data]

        def _parse_list_first(self, data: list[str]) -> list[str]:
            return data

        def _parse_list_all(self, data: list[str]) -> list[str]:
            return [f"A:{x}" for x in data]

    p = MockParsable()
    assert p.parse(["x"], keep="all") == ["A:x"]


def test_abc_parsable_abstract_parse_raises() -> None:
    class Incomplete(ABCParsable):
        pass

    with pytest.raises(TypeError):
        Incomplete()
