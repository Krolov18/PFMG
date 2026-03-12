import pytest

from pfmg.conftest import _assert_compare
from pfmg.utils.trie import add_word, add_words, dict2str


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
