import pytest
from frozendict import frozendict
from lexique.lexical_structures.LexemeEntry import LexemeEntry
from lexique.lexical_structures.Radical import Radical
from lexique.lexical_structures.StemSpace import StemSpace


@pytest.mark.parametrize("stems, pos, sigma", [
    (("stem",), "pos", frozendict({"sigma": "sigma"})),
])
def test_lexeme(stems, pos, sigma) -> None:
    lexeme = LexemeEntry(stems=StemSpace(stems),
                         pos=pos,
                         sigma=sigma)
    assert lexeme.stems == StemSpace(stems)
    assert lexeme.pos == pos
    assert lexeme.sigma == sigma
    assert lexeme.to_radical() == Radical(stems=StemSpace(stems))
