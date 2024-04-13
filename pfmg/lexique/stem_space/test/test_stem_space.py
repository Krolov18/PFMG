import pytest

from lexique.lexical_structures.StemSpace import StemSpace


@pytest.mark.parametrize("stems", [
    ("truc",),
    ("truc", "machin"),
])
def test_prefix(stems) -> None:
    actual = StemSpace(stems=stems)
    assert actual.stems is stems
