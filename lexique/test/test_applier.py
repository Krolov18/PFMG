from frozendict import frozendict
import pytest

from lexique.applier import verify, apply, format_stem


@pytest.mark.parametrize("t, stem, expected", [
    pytest.param("", frozendict(), "", marks=pytest.mark.xfail(reason="cas extrême", raises=AssertionError)),
    ("A", frozendict({"1": "b", "2": "r", "3": "N", "V": "a"}), "u"),
    ("U", frozendict({"1": "b", "2": "r", "3": "N", "V": "a"}), "u"),
    ("V", frozendict({"1": "b", "2": "r", "3": "N", "V": "a"}), "a"),

    ("b", frozendict({"1": "b", "2": "r", "3": "N", "V": "a"}), "b"),
    ("r", frozendict({"1": "b", "2": "r", "3": "N", "V": "a"}), "r"),
    ("a", frozendict({"1": "b", "2": "r", "3": "N", "V": "a"}), "a"),
    ("N", frozendict({"1": "b", "2": "r", "3": "N", "V": "a"}), "N"),

    ("1", frozendict({"1": "b", "2": "r", "3": "N", "V": "a"}), "b"),
    ("2", frozendict({"1": "b", "2": "r", "3": "N", "V": "a"}), "r"),
    ("3", frozendict({"1": "b", "2": "r", "3": "N", "V": "a"}), "N"),
    ("4", frozendict({"1": "b", "2": "r", "3": "N", "V": "a"}), "p"),
    ("5", frozendict({"1": "b", "2": "r", "3": "N", "V": "a"}), "w"),
    ("6", frozendict({"1": "b", "2": "r", "3": "N", "V": "a"}), "n"),
    ("7", frozendict({"1": "b", "2": "r", "3": "N", "V": "a"}), "p"),
    ("8", frozendict({"1": "b", "2": "r", "3": "N", "V": "a"}), "w"),
    ("9", frozendict({"1": "b", "2": "r", "3": "N", "V": "a"}), "m"),
])
def test_verify(phonology, t, stem, expected) -> None:
    actual = verify(t, stem, phonology)
    assert actual == expected


@pytest.mark.parametrize("stem, expected", [
    pytest.param("", "", marks=pytest.mark.xfail(reason="cas extrême dans lequel le stem est vide", raises=AssertionError)),
    ("bran", frozendict({"1": "b", "2": "r", "3": "n", "V": "a"})),
])
def test_format_stem(phonology, stem, expected) -> None:
    actual = format_stem(stem, phonology)
    assert actual == expected


@pytest.mark.parametrize("rule, stem, expected", [
    ("", frozendict(), ""),
    ("1A8V2i6", frozendict({"1": "b", "2": "r", "3": "n", "V": "a"}), "buwarim"),
    ("1A8V2i6i", frozendict({"1": "b", "2": "r", "3": "n", "V": "a"}), "buwarimi"),
    ("1A8V2i6a", frozendict({"1": "b", "2": "r", "3": "n", "V": "a"}), "buwarima"),
    ("1A8V2i6u", frozendict({"1": "b", "2": "r", "3": "n", "V": "a"}), "buwarimu"),
    ("4U2A9u3i", frozendict({"1": "b", "2": "r", "3": "n", "V": "a"}), "purumuni"),
    ("4U2A9u3a", frozendict({"1": "b", "2": "r", "3": "n", "V": "a"}), "purumuna"),
    ("4U2A9u3u", frozendict({"1": "b", "2": "r", "3": "n", "V": "a"}), "purumunu"),

])
def test_apply(phonology, rule, stem, expected) -> None:
    actual = apply(rule, stem, phonology)
    assert len(actual) == len(rule)
    assert actual == expected
