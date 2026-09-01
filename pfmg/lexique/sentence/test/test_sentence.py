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


class SigmaForme(Forme):
    """Forme whose sigma is readable.

    Forme.get_sigma() is left to subclasses, so Sentence.get_sigma() can only
    be exercised through one of them.
    """

    def get_sigma(self) -> frozendict:
        """Return the sigma of the source entry."""
        return self.source.get_sigma()


def make_sigma_forme(pos: str, sigma: frozendict, index: int) -> SigmaForme:
    morphemes = Morphemes(
        radical=Radical(stems=StemSpace(("toto",)), sigma=frozendict()),
        others=[]
    )
    return SigmaForme(
        source=FormeEntry(pos=pos, morphemes=morphemes, sigma=sigma, index=index),
        destination=FormeEntry(
            pos=pos,
            morphemes=morphemes,
            sigma=frozendict(),
            index=index
        )
    )


def test_get_sigma_merges_every_word() -> None:
    sentence = Sentence([
        make_sigma_forme("D", frozendict(Genre="m"), 1),
        make_sigma_forme("N", frozendict(Nombre="pl"), 2),
    ])
    actual = sentence.get_sigma()
    assert actual == frozendict(Genre="m", Nombre="pl")
    assert isinstance(actual, frozendict)


def test_get_sigma_last_word_wins_on_conflict() -> None:
    sentence = Sentence([
        make_sigma_forme("D", frozendict(Genre="m", Nombre="sg"), 1),
        make_sigma_forme("N", frozendict(Genre="f"), 2),
    ])
    assert sentence.get_sigma() == frozendict(Genre="f", Nombre="sg")


def test_get_sigma_without_word() -> None:
    assert Sentence([]).get_sigma() == frozendict()


def test_get_sigma_is_not_implemented_on_plain_forme() -> None:
    sentence = Sentence([
        Forme(
            source=FormeEntry(
                pos="N",
                morphemes=Morphemes(
                    radical=Radical(
                        stems=StemSpace(("toto",)),
                        sigma=frozendict()
                    ),
                    others=[]
                ),
                sigma=frozendict(Genre="m"),
                index=1
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
                index=1
            )
        )
    ])
    with pytest.raises(NotImplementedError):
        sentence.get_sigma()
