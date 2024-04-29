# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import pytest

from pfmg.lexique.stem_space.StemSpace import StemSpace


@pytest.mark.parametrize("stems", [
    ("truc",),
    ("truc", "machin"),
])
def test_prefix(stems) -> None:
    actual = StemSpace(stems=stems)
    assert actual.stems is stems
