import pytest
from frozendict import frozendict

from lexique.structures import Phonology


@pytest.fixture(scope="module")
def phonology() -> Phonology:
    return Phonology(
        mutations=frozendict({'p': 'p', 't': 'p', 'k': 't', 'b': 'p',
                              'd': 'b', 'g': 'd', 'm': 'm', 'n': 'm',
                              'N': 'n', 'f': 'f', 's': 'f', 'S': 's',
                              'v': 'f', 'z': 'v', 'Z': 'z', 'r': 'w',
                              'l': 'r', 'j': 'w', 'w': 'w'}),
        apophonies=frozendict({'Ø': 'i', 'i': 'a', 'a': 'u',
                               'u': 'u', 'e': 'o', 'o': 'o'}),
        derives=frozendict({'A': 'V', 'D': 'C'}),
        consonnes=frozenset("ptkbdgmnNfsSvzZrljw"),
        voyelles=frozenset("iueoa")
    )
