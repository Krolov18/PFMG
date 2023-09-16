from lexique.lexical_structures.Lexeme import Lexeme
from lexique.lexical_structures.Radical import Radical
from lexique.lexical_structures.StemSpace import StemSpace


def test_lexeme() -> None:
    lexeme = Lexeme(stem=StemSpace(("stem",)),
                    pos="pos",
                    sigma={"sigma": "sigma"})
    assert lexeme.stem == StemSpace(("stem",))
    assert lexeme.pos == "pos"
    assert lexeme.sigma == {"sigma": "sigma"}
    assert lexeme.to_radical() == Radical(stems=StemSpace(("stem",)))



def test_lexeme2() -> None:
    pass
