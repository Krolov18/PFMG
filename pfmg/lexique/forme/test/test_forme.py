import pytest

from lexique.lexical_structures.FormeEntry import FormeEntry
from lexique.lexical_structures.Forme import Forme
from frozendict import frozendict


@pytest.mark.parametrize("source, destination", [
    (("N", [], frozendict()), ("N", [], frozendict()))
])
def test_forme(source, destination):
    source_forme = FormeEntry(pos=source[0],
                              morphemes=source[1],
                              sigma=source[2])
    dest_forme = FormeEntry(pos=source[0],
                            morphemes=source[1],
                            sigma=source[2])
    actual = Forme(source=source_forme,
                   destination=dest_forme)
    assert actual.source == source_forme
    assert actual.destination == dest_forme
