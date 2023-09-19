from frozendict import frozendict

from lexique.lexical_structures.Lexeme import Lexeme
from lexique.lexical_structures.LexemeEntry import LexemeEntry
from lexique.lexical_structures.StemSpace import StemSpace


def test_lexeme() -> None:
    source = LexemeEntry(
        stems=StemSpace(("gitun",)),
        pos="N",
        sigma=frozendict(genre="f")
    )
    destination = LexemeEntry(
        stems=StemSpace(("banane",)),
        pos="N",
        sigma=frozendict(cf=1)
    )
    lexeme = Lexeme(
        source=source,
        destination=destination
    )
    assert lexeme.source == source
    assert lexeme.destination == destination
