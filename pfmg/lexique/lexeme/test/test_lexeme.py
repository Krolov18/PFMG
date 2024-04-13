from frozendict import frozendict
from pfmg.lexique.lexeme.Lexeme import Lexeme
from pfmg.lexique.lexeme.LexemeEntry import LexemeEntry
from pfmg.lexique.stem_space.StemSpace import StemSpace


def test_lexeme() -> None:
    source = LexemeEntry(
        stems=StemSpace(("gitun",)),
        pos="N",
        sigma=frozendict(genre="f"),
    )
    destination = LexemeEntry(
        stems=StemSpace(("banane",)),
        pos="N",
        sigma=frozendict(cf=1),
    )
    lexeme = Lexeme(
        source=source,
        destination=destination,
    )
    assert lexeme.source == source
    assert lexeme.destination == destination
