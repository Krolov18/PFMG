import pytest
from frozendict import frozendict

from lexique.ruler import ruler
from lexique.structures import Forme, Radical
from lexique.unary import unary


@pytest.mark.parametrize("term, expected", [  # Genre=A,Nombre=Du: 1A8V2i6
    (Forme(pos="N",
           morphemes=[Radical(rule=None, sigma=frozendict(Genre="A"), stem=("padaN",)),
                      ruler(id_ruler="all", rule="1A8V2i6", sigma=frozendict(Genre="A", Nombre="Du"),
                            voyelles=frozenset()),
                      ruler(id_ruler="all", rule="re+X", sigma=frozendict(Cas="Erg"), voyelles=frozenset())],
           sigma=frozendict(Genre="A",
                            Nombre="Du",
                            Cas="Erg"),
           traduction=Forme(pos="N",
                            morphemes=[Radical(rule=None, sigma=frozendict(þGenre="þF"), stem=("plaine",)),
                                       ruler(id_ruler="all", rule="X+s", sigma=frozendict(þNombre="þPl"),
                                             voyelles=frozenset())],
                            sigma=frozendict(þGenre="þF", þNombre="þPl"),
                            traduction=None)),
     "N[Genre='A',Nombre='Du',Cas='Erg',TRAD='plaines'] -> 'repupadin'"),
    # (Forme(pos="V",
    #        morphemes=[Radical(rule=None, sigma=None, stem=("briN",)),
    #                   ruler(id_ruler="all", rule="X+i", sigma=frozendict(type="VI")),
    #                   ruler(id_ruler="all", rule="A1i2a5V3u", sigma=frozendict(temps="PRS", genre="A")),
    #                   ruler(id_ruler="all", rule="p+X", sigma=frozendict(nombre="sg"))],
    #        sigma=frozendict(type="VI", temps="PRS", genre="A", nombre="sg")),
    #  "V[type='VI',temps='PRS',genre='A',nombre='sg'] -> 'pabirawiNu'"),
])
def test_unary(phonology, term, expected) -> None:
    actual = unary("fcfg", term, phonology)
    assert actual == expected
