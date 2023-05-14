from lexique_2.lexical_structures.Radical import Radical
from lexique_2.lexical_structures.StemSpace import StemSpace


def test_radical() -> None:
    assert str(Radical(stems=StemSpace(stems=("jaune",)))) == "Radical(jaune)"
    assert str(Radical(stems=StemSpace(stems=("petit", "petite")),)) == "Radical(petit::petite)"
