# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import pytest

from frozendict import frozendict

from pfmg.lexique.forme.FormeEntry import FormeEntry
from pfmg.lexique.forme.Forme import Forme
from pfmg.lexique.morpheme.Morphemes import Morphemes
from pfmg.lexique.morpheme.Radical import Radical
from pfmg.lexique.stem_space.StemSpace import StemSpace


@pytest.mark.parametrize(
    "source, destination", [
        (("N", [], frozendict()), ("N", [], frozendict()))
    ]
)
def test_forme(source, destination):
    source_forme = FormeEntry(
        index=4,
        pos=source[0],
        morphemes=Morphemes(
            radical=Radical(
                stems=StemSpace(stems=("source",))
            ),
            others=source[1]
        ),
        sigma=source[2]
    )
    dest_forme = FormeEntry(
        index=4,
        pos=source[0],
        morphemes=Morphemes(
            radical=Radical(
                stems=StemSpace(stems=("destination",))
            ),
            others=source[1]
        ),
        sigma=source[2]
    )
    actual = Forme(
        source=source_forme,
        destination=dest_forme
    )
    assert actual.source == source_forme
    assert actual.destination == dest_forme

    with pytest.raises(NotImplementedError):
        _ = actual.get_sigma()

    assert actual.to_string() == "source"
