"""Tests for FeatureMixin.broadcast (one feature segment per phrase)."""

import pytest

from pfmg.parsing.features.FeatureMixin import FeatureMixin


@pytest.mark.parametrize(
    "data, phrase_len, expected",
    [
        ("Genre,Nombre", 1, "Genre,Nombre"),
        ("Genre,Nombre", 2, "Genre,Nombre;Genre,Nombre"),
        ("Genre,Nombre", 3, "Genre,Nombre;Genre,Nombre;Genre,Nombre"),
    ],
)
def test_broadcast_repeats_a_single_specification(data, phrase_len, expected) -> None:
    """One specification is repeated for every phrase."""
    assert FeatureMixin.broadcast(data, phrase_len) == expected


@pytest.mark.parametrize(
    "data, phrase_len",
    [
        ("Nombre;Nombre", 2),
        ("Nombre;Nombre,Val=tdir;", 3),
        ("Nombre;;;Nombre", 4),
    ],
)
def test_broadcast_keeps_a_per_phrase_specification(data, phrase_len) -> None:
    """A string that already has one segment per phrase is left alone.

    This is how a rule constrains its constituents unevenly, e.g. making the
    subject agree with the verb while leaving the object free.
    """
    assert FeatureMixin.broadcast(data, phrase_len) == data


def test_broadcast_rejects_a_mismatched_specification() -> None:
    """A partial per-phrase string cannot be broadcast and is a config error."""
    with pytest.raises(AssertionError):
        FeatureMixin.broadcast("Nombre;Nombre", 3)
