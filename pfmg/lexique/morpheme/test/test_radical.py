from pfmg.lexique.morpheme.Radical import Radical
from pfmg.lexique.stem_space.StemSpace import StemSpace


def test_radical() -> None:
    actual = str(Radical(stems=StemSpace(stems=("jaune",))))
    assert actual == "Radical(jaune)"
    actual = str(Radical(stems=StemSpace(stems=("petit", "petite")), ))
    assert actual == "Radical(petit::petite)"
