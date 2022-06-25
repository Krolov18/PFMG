import pytest
from frozendict import frozendict

from lexique.ruler import ruler
from lexique.structures import Forme, Radical
from lexique.unary import unary


@pytest.mark.parametrize("term, expected", [  # Genre=A,Nombre=Du: 1A8V2i6
    (Forme(pos="N",
           morphemes=[Radical(rule=None, sigma=frozendict(Genre="A"), stem=("padaN",)),
                      ruler(id_ruler="all", rule="1A8V2i6", sigma=frozendict(Genre="A", Nombre="Du"),
                            voyelles=frozenset("aeiou")),
                      ruler(id_ruler="all", rule="re+X", sigma=frozendict(Cas="Erg"), voyelles=frozenset("aeiou"))],
           sigma=frozendict(Genre="A", Nombre="Du", Cas="Erg"),
           traduction=Forme(pos="N",
                            morphemes=[Radical(rule=None, sigma=frozendict(þGenre="þF"), stem=("plaine",)),
                                       ruler(id_ruler="all", rule="X+s", sigma=frozendict(þNombre="þPl"),
                                             voyelles=frozenset())],
                            sigma=frozendict(þGenre="þF", þNombre="þPl"),
                            traduction=None)),
     "N[Genre='A',Nombre='Du',Cas='Erg',Traduction='plaines'] -> 'repupadin'"),
    (Forme(pos="V",
           morphemes=[Radical(rule=None, sigma=None, stem=("briN",)),
                      ruler(id_ruler="all", rule="X+i", sigma=frozendict(type="VI"), voyelles=frozenset("aeiou")),
                      ruler(id_ruler="all", rule="A1i2a5V3u", sigma=frozendict(temps="PRS", genre="A"),
                            voyelles=frozenset("aeiou")),
                      ruler(id_ruler="all", rule="p+X", sigma=frozendict(nombre="sg"), voyelles=frozenset("aeiou"))],
           sigma=frozendict(type="VI", temps="PRS", genre="A", nombre="sg"),
           traduction=Forme(pos="V",
                            morphemes=[Radical(rule=None, sigma=frozendict(), stem=("laver",)),
                                       ruler(id_ruler="all", rule="X+g", sigma=frozendict(), voyelles=frozenset("aeiou"))],
                            sigma=frozendict(),
                            traduction=None)),
     "V[type='VI',temps='PRS',genre='A',nombre='sg',Traduction='laverg'] -> 'pabirawiNu'"),
])
def test_unary(phonology, term, expected) -> None:
    actual = unary("fcfg", term, phonology)
    assert actual == expected
