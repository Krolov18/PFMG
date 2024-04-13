import pytest

from pfmg.lexique.stem_space.StemSpace import StemSpace


@pytest.mark.parametrize("stems", [
    ("truc",),
    ("truc", "machin"),
])
def test_prefix(stems) -> None:
    actual = StemSpace(stems=stems)
    assert actual.stems is stems
