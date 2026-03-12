"""Tests for tokenizer (new_tokenizer)."""

import pytest

from pfmg.conftest import _assert_compare
from pfmg.parsing.tokenizer import new_tokenizer


@pytest.mark.parametrize(
    "params, expected",
    [
        ({"id_tokenizer": "Space", "sentence": "a b c"}, ["a", "b", "c"]),
        ({"id_tokenizer": "Space", "sentence": "abc"}, ["abc"]),
        ({"id_tokenizer": "Space", "sentence": "b  c"}, ["b", "", "c"]),
    ],
)
def test_tokenizer(params, expected) -> None:
    result = new_tokenizer(id_tokenizer=params["id_tokenizer"])(sentence=params["sentence"])
    _assert_compare(result, expected)


@pytest.mark.parametrize(
    "params, expected",
    [
        ({"id_tokenizer": "Space", "sentence": ""}, AssertionError),
        ({"id_tokenizer": "Space", "sentence": []}, AssertionError),
        ({"id_tokenizer": "Space", "sentence": set()}, AssertionError),
    ],
)
def test_tokenizer_raises(params, expected) -> None:
    with pytest.raises(expected):
        new_tokenizer(id_tokenizer=params["id_tokenizer"])(sentence=params["sentence"])
