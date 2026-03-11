import pytest
from pfmg.lexique.stem_space.StemSpace import StemSpace


@pytest.mark.parametrize("stems", [
    (),
    ("", "rad2"),
])
def test_assertions(stems: tuple[str, ...]) -> None:
    with pytest.raises(AssertionError):
        _ = StemSpace(stems=stems)

    with pytest.raises(AssertionError):
        _ = StemSpace.from_string(",".join(stems))


@pytest.mark.parametrize("stems, lemma, expected", [
    ("rad1", "rad1", ("rad1",)),
    ("rad1,rad2", "rad1", ("rad1", "rad2")),
])
def test_from_string(stems, lemma, expected) -> None:
    actual = StemSpace.from_string(stems)
    assert isinstance(actual, StemSpace)
    assert actual.stems == expected
    assert actual.lemma == lemma
