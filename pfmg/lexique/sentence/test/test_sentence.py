# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import pytest
from frozendict import frozendict

from pfmg.conftest import get_default_phonology
from pfmg.lexique.forme import Forme, FormeEntry
from pfmg.lexique.morpheme.Factory import create_morpheme
from pfmg.lexique.morpheme.Morphemes import Morphemes
from pfmg.lexique.morpheme.Radical import Radical
from pfmg.lexique.sentence.Sentence import Sentence
from pfmg.lexique.stem_space.StemSpace import StemSpace


@pytest.mark.parametrize(
    "formes, expected", [
        ([
             Forme(
                 source=FormeEntry(
                     pos="D",
                     morphemes=Morphemes(
                         radical=Radical(
                             stems=StemSpace(("DEF", "le", "la", "les")),
                             sigma=frozendict()
                         ),
                         others=[
                             create_morpheme(
                                 rule="X4",
                                 sigma=frozendict(Genre="m", Nombre="pl"),
                                 phonology=get_default_phonology()
                             )
                         ]
                     ),
                     sigma=frozendict(Genre="m", Nombre="pl"),
                     index=1
                 ),
                 destination=FormeEntry(
                     pos="D",
                     morphemes=Morphemes(
                         radical=Radical(
                             stems=StemSpace(("toto",)),
                             sigma=frozendict()
                         ),
                         others=[]
                     ),
                     sigma=frozendict(),
                     index=1
                 )
             ),
             Forme(
                 source=FormeEntry(
                     pos="N",
                     morphemes=Morphemes(
                         radical=Radical(
                             stems=StemSpace(("chat",)),
                             sigma=frozendict(Genre="m")
                         ),
                         others=[
                             create_morpheme(
                                 rule="X+s",
                                 sigma=frozendict(Nombre="pl"),
                                 phonology=get_default_phonology()
                             )
                         ]
                     ),
                     sigma=frozendict(),
                     index=2
                 ),
                 destination=FormeEntry(
                     pos="N",
                     morphemes=Morphemes(
                         radical=Radical(
                             stems=StemSpace(("toto",)),
                             sigma=frozendict()
                         ),
                         others=[]
                     ),
                     sigma=frozendict(),
                     index=2
                 )
             )],
         "les chats")
    ]
)
def test_to_string(fx_df_phonology, formes, expected) -> None:
    sentence = Sentence(formes)
    actual = sentence.to_string()
    assert actual == expected


@pytest.mark.parametrize(
    "formes, expected", [
        ([
             Forme(
                 source=FormeEntry(
                     pos="D",
                     morphemes=Morphemes(
                         radical=Radical(
                             stems=StemSpace(("DEF", "le", "la", "les")),
                             sigma=frozendict()
                         ),
                         others=[
                             create_morpheme(
                                 rule="X4",
                                 sigma=frozendict(Genre="m", Nombre="pl"),
                                 phonology=get_default_phonology()
                             )
                         ]
                     ),
                     sigma=frozendict(Genre="m", Nombre="pl"),
                     index=1
                 ),
                 destination=FormeEntry(
                     pos="D",
                     morphemes=Morphemes(
                         radical=Radical(
                             stems=StemSpace(("toto",)),
                             sigma=frozendict()
                         ),
                         others=[]
                     ),
                     sigma=frozendict(),
                     index=1
                 )
             ),
             Forme(
                 source=FormeEntry(
                     pos="N",
                     morphemes=Morphemes(
                         radical=Radical(
                             stems=StemSpace(("chat",)),
                             sigma=frozendict(Genre="m")
                         ),
                         others=[
                             create_morpheme(
                                 rule="X+s",
                                 sigma=frozendict(Nombre="pl"),
                                 phonology=get_default_phonology()
                             )
                         ]
                     ),
                     sigma=frozendict(),
                     index=2
                 ),
                 destination=FormeEntry(
                     pos="N",
                     morphemes=Morphemes(
                         radical=Radical(
                             stems=StemSpace(("toto",)),
                             sigma=frozendict()
                         ),
                         others=[]
                     ),
                     sigma=frozendict(),
                     index=2
                 )
             )],
         "les chat-s")
    ]
)
def test_to_decoupe(fx_df_phonology, formes, expected) -> None:
    sentence = Sentence(formes)
    actual = sentence.to_decoupe()
    assert actual == expected


@pytest.mark.parametrize(
    "formes, expected", [
        ([
             Forme(
                 source=FormeEntry(
                     pos="D",
                     morphemes=Morphemes(
                         radical=Radical(
                             stems=StemSpace(("DEF", "le", "la", "les")),
                             sigma=frozendict()
                         ),
                         others=[
                             create_morpheme(
                                 rule="X4",
                                 sigma=frozendict(Genre="m", Nombre="pl"),
                                 phonology=get_default_phonology()
                             )
                         ]
                     ),
                     sigma=frozendict(Genre="m", Nombre="pl"),
                     index=1
                 ),
                 destination=FormeEntry(
                     pos="D",
                     morphemes=Morphemes(
                         radical=Radical(
                             stems=StemSpace(("toto",)),
                             sigma=frozendict()
                         ),
                         others=[]
                     ),
                     sigma=frozendict(),
                     index=1
                 )
             ),
             Forme(
                 source=FormeEntry(
                     pos="N",
                     morphemes=Morphemes(
                         radical=Radical(
                             stems=StemSpace(("chat",)),
                             sigma=frozendict(Genre="m")
                         ),
                         others=[
                             create_morpheme(
                                 rule="X+s",
                                 sigma=frozendict(Nombre="pl"),
                                 phonology=get_default_phonology()
                             )
                         ]
                     ),
                     sigma=frozendict(),
                     index=2
                 ),
                 destination=FormeEntry(
                     pos="N",
                     morphemes=Morphemes(
                         radical=Radical(
                             stems=StemSpace(("toto",)),
                             sigma=frozendict()
                         ),
                         others=[]
                     ),
                     sigma=frozendict(),
                     index=2
                 )
             )],
         "DEF.m.pl chat.m-pl")
    ]
)
def test_to_glose(fx_df_phonology, formes, expected) -> None:
    sentence = Sentence(formes)
    actual = sentence.to_glose()
    assert actual == expected
