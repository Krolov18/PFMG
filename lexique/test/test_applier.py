from frozendict import frozendict
import pytest

from lexique.applier import verify, apply, format_stem, is_v, is_a, is_u, is_123, is_456, is_789


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


@pytest.mark.parametrize("t, expected", [
    ("1", True),
    ("2", True),
    ("3", True),
    ("kjefrglkijdsqnhf", False),
])
def test_is_123(t, expected) -> None:
    assert is_123(t) == expected


@pytest.mark.parametrize("t, expected", [
    ("4", True),
    ("5", True),
    ("6", True),
    ("sodojusd", False),
])
def test_is_456(t, expected) -> None:
    assert is_456(t) == expected


@pytest.mark.parametrize("t, expected", [
    ("7", True),
    ("8", True),
    ("9", True),
    ("olqefoujehbouier", False),
])
def test_is_789(t, expected) -> None:
    assert is_789(t) == expected


@pytest.mark.parametrize("t, expected", [
    ("A", True),
    ("sdhzhtr", False),
])
def test_is_a(t, expected) -> None:
    assert is_a(t) == expected


@pytest.mark.parametrize("t, expected", [
    ("U", True),
    ("likshdfoihsz", False),
])
def test_is_u(t, expected) -> None:
    assert is_u(t) == expected


@pytest.mark.parametrize("t, expected", [
    ("V", True),
    ("ljurgb", False)
])
def test_is_v(t, expected) -> None:
    assert is_v(t) == expected


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
