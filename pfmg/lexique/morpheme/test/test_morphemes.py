# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
from frozendict import frozendict

from pfmg.lexique.morpheme.Factory import create_morpheme
from pfmg.lexique.morpheme.Morphemes import Morphemes
from pfmg.lexique.morpheme.Radical import Radical
from pfmg.lexique.stem_space.StemSpace import StemSpace


def test_morpheme(fx_df_phonology) -> None:
    morpheme = Morphemes(
        radical=Radical(
            stems=StemSpace(("radical",)),
            sigma=frozendict(
                {
                    "Genre": "m"
                }
            )
        ),
        others=[
            create_morpheme(
                rule="a+X",
                sigma=frozendict(
                    {
                        "Genre": "m"
                    }
                ),
                phonology=fx_df_phonology
            ),
            create_morpheme(
                rule="b+X",
                sigma=frozendict(
                    {
                        "Nombre": "s"
                    }
                ),
                phonology=fx_df_phonology
            )]
    )
    assert morpheme.radical == Radical(
        stems=StemSpace(("radical",)),
        sigma=frozendict(
            {
                "Genre": "m"
            }
        )
    )
    expected_morphemes = [
        create_morpheme(
            rule="a+X",
            sigma=frozendict(
                {
                    "Genre": "m"
                }
            ),
            phonology=fx_df_phonology
        ),
        create_morpheme(
            rule="b+X",
            sigma=frozendict(
                {
                    "Nombre": "s"
                }
            ),
            phonology=fx_df_phonology
        )
    ]
    assert morpheme.others == expected_morphemes
