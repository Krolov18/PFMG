# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
from pfmg.lexique.morpheme.Radical import Radical
from pfmg.lexique.stem_space.StemSpace import StemSpace


def test_radical() -> None:
    actual = str(Radical(stems=StemSpace(stems=("jaune",))))
    assert actual == "Radical(jaune)"
    actual = str(Radical(stems=StemSpace(stems=("petit", "petite")), ))
    assert actual == "Radical(petit::petite)"
