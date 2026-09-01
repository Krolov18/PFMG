import re

import pytest

from pfmg.conftest import _assert_compare
from pfmg.utils.trie import add_word, add_words, dict2str, to_pattern


@pytest.mark.parametrize(
    "params, expected",
    [
        ({"tree": {}, "word": ""}, {"": 1}),
        ({"tree": {}, "word": "a"}, {"a": {"": 1}}),
        ({"tree": {}, "word": "aa"}, {"a": {"a": {"": 1}}}),
        (
            {"tree": {"a": {"a": {"": 1}}}, "word": "ab"},
            {"a": {"a": {"": 1}, "b": {"": 1}}},
        ),
    ],
)
def test_add_word(params, expected) -> None:
    tree = params["tree"]
    add_word(tree, params["word"])
    _assert_compare(tree, expected)


@pytest.mark.parametrize(
    "params, expected",
    [
        ({"tree": {}, "words": [""]}, {"": 1}),
        ({"tree": {}, "words": ["a"]}, {"a": {"": 1}}),
        ({"tree": {}, "words": ["aa"]}, {"a": {"a": {"": 1}}}),
        (
            {"tree": {"a": {"a": {"": 1}}}, "words": ["ab"]},
            {"a": {"a": {"": 1}, "b": {"": 1}}},
        ),
        (
            {"tree": {"a": {"a": {"": 1}}}, "words": ["ab", "ac"]},
            {"a": {"a": {"": 1}, "b": {"": 1}, "c": {"": 1}}},
        ),
    ],
)
def test_add_words(params, expected) -> None:
    tree = params["tree"]
    add_words(tree, params["words"])
    _assert_compare(tree, expected)


@pytest.mark.parametrize(
    "params, expected",
    [
        ({"tree": {}}, ""),
        ({"tree": {"": 1}}, None),
        ({"tree": {"a": {"": 1}}}, "a"),
        ({"tree": {"a": {"": 1}, "": 1}}, "a?"),
        ({"tree": {"a": {"": 1}, "b": {"": 1}, "": 1}}, "[ab]?"),
        (
            {
                "tree": {
                    "a": {
                        "b": {"": 1},
                        "c": {"": 1},
                        "d": {"": 1},
                    }
                }
            },
            "a[bcd]",
        ),
        (
            {
                "tree": {
                    "b": {
                        "a": {
                            "t": {"": 1},
                            "n": {"": 1},
                            "g": {"": 1},
                        }
                    }
                }
            },
            "ba[gnt]",
        ),
        (
            {
                "tree": {
                    "b": {
                        "a": {
                            "n": {
                                "a": {
                                    "n": {
                                        "e": {
                                            "s": {
                                                "": 1,
                                            }
                                        }
                                    }
                                },
                                "n": {
                                    "i": {
                                        "r": {
                                            "": 1,
                                        }
                                    }
                                },
                            }
                        }
                    }
                }
            },
            "ban(?:anes|nir)",
        ),
        (
            {
                "tree": {
                    "b": {
                        "a": {
                            "n": {
                                "a": {
                                    "n": {
                                        "e": {
                                            "s": {
                                                "": 1,
                                            }
                                        }
                                    }
                                },
                                "n": {
                                    "i": {
                                        "r": {"": 1},
                                        "e": {"": 1},
                                    }
                                },
                            }
                        }
                    }
                }
            },
            "ban(?:anes|ni[er])",
        ),
    ],
)
def test_dict2str(params, expected) -> None:
    result = dict2str(params["tree"])
    _assert_compare(result, expected)


def test_dict2str_applies_escape_at_every_depth() -> None:
    # the escape function must be propagated through the recursion,
    # not only applied to the characters of the first level
    result = dict2str({"a": {"b": {"": 1}}}, lambda char: f"<{char}>")
    _assert_compare(result, "<a><b>")


@pytest.mark.parametrize(
    "words, expected",
    [
        ([], ""),
        (["a"], "a"),
        (["a", "b"], "[ab]"),
        (["chat", "chien"], "ch(?:at|ien)"),
        (["le", "la", "les"], "l(?:es?|a)"),
    ],
)
def test_to_pattern(words, expected) -> None:
    _assert_compare(to_pattern(words), expected)


@pytest.mark.parametrize(
    "words",
    [
        ["chat", "chien", "chevre"],
        ["le", "la", "les"],
        ["banane", "bannir"],
        ["a", "ab", "abc"],
    ],
)
def test_to_pattern_matches_exactly_the_words(words) -> None:
    pattern = re.compile(to_pattern(words))
    for word in words:
        assert pattern.fullmatch(word) is not None, word
    for absent in ("", "zzz", "chatte", "l"):
        if absent not in words:
            assert pattern.fullmatch(absent) is None, absent


@pytest.mark.parametrize(
    "words, literal, lookalike",
    [
        # metacharacter on the first level of the trie
        (["a.b"], "a.b", "axb"),
        # metacharacter nested deeper: regression test for the escape
        # function being lost in the recursion of __build_pattern
        (["ab.c", "ab+d"], "ab.c", "abxc"),
        (["x(y)"], "x(y)", "xy"),
    ],
)
def test_to_pattern_escapes_metacharacters(words, literal, lookalike) -> None:
    pattern = re.compile(to_pattern(words))
    assert pattern.fullmatch(literal) is not None
    assert pattern.fullmatch(lookalike) is None


def test_to_pattern_rejects_the_empty_word() -> None:
    # a trie holding only the empty word has no pattern to build
    with pytest.raises(AssertionError):
        to_pattern([""])
