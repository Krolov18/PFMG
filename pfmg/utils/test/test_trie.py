# Copyright (c) <year>, <copyright holder>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. 
import pytest

from pfmg.utils.trie import add_word, add_words, dict2str


@pytest.mark.parametrize("tree, word, tree_true", [
    ({}, "", {"": 1}),
    ({}, "a", {"a": {"": 1}}),
    ({}, "aa", {"a": {"a": {"": 1}}}),
    ({"a": {"a": {"": 1}}}, "ab", {"a": {"a": {"": 1}, "b": {"": 1}}})
])
def test_add_word(tree, word, tree_true) -> None:
    add_word(tree, word)
    assert tree == tree_true


@pytest.mark.parametrize("tree, words, tree_true", [
    ({}, [""], {"": 1}),
    ({}, ["a"], {"a": {"": 1}}),
    ({}, ["aa"], {"a": {"a": {"": 1}}}),
    ({"a": {"a": {"": 1}}}, ["ab"], {"a": {"a": {"": 1}, "b": {"": 1}}}),
    ({"a": {"a": {"": 1}}}, ["ab", "ac"], {"a": {"a": {"": 1},
                                                 "b": {"": 1},
                                                 "c": {"": 1}}}),
])
def test_add_words(tree, words, tree_true) -> None:
    add_words(tree, words)
    assert tree == tree_true


@pytest.mark.parametrize("tree, tree_true", [
    ({}, ""),

    ({"": 1}, None),

    ({"a": {"": 1}}, "a"),

    ({"a": {"": 1},
      "": 1}, "a?"),

    ({"a": {"": 1},
      "b": {"": 1},
      "": 1}, "[ab]?"),

    ({"a": {"b": {"": 1},
            "c": {"": 1},
            "d": {"": 1}}}, "a[bcd]"),

    ({'b': {'a': {'t': {'': 1},
                  'n': {'': 1},
                  'g': {'': 1}}}}, "ba[gnt]"),

    ({"b": {"a": {"n": {"a": {"n": {"e": {"s": {"": 1}}}},
                        "n": {"i": {"r": {"": 1}}}}}}}, "ban(?:anes|nir)"),

    ({"b": {"a": {"n": {"a": {"n": {"e": {"s": {"": 1}}}},
                        "n": {"i": {"r": {"": 1},
                                    "e": {"": 1}}}}}}}, "ban(?:anes|ni[er])")
])
def test_dict2str(tree, tree_true) -> None:
    assert dict2str(tree) == tree_true
