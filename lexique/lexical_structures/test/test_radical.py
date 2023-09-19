from lexique.lexical_structures.Radical import Radical
from lexique.lexical_structures.StemSpace import StemSpace


def test_radical() -> None:
    actual = str(Radical(stems=StemSpace(stems=("jaune",))))
    assert actual == "Radical(jaune)"
    actual = str(Radical(stems=StemSpace(stems=("petit", "petite")), ))
    assert actual == "Radical(petit::petite)"
