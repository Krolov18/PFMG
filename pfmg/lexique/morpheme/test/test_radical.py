from frozendict import frozendict

from pfmg.lexique.morpheme.Radical import Radical
from pfmg.lexique.stem_space.StemSpace import StemSpace


def test_radical_assertions() -> None:
    # empty stemspace
    with pytest.raises(AssertionError):
        _ = Radical(
            stems=StemSpace(stems=()),
            sigma=frozendict({"Genre": "m"}))

    # empty lemma
    with pytest.raises(AssertionError):
        _ = Radical(
            stems=StemSpace(stems=("", "rad2", "rad3")),
            sigma=frozendict({"Genre": "m"})
        )

    actual = Radical(
        stems=StemSpace(stems=("rad1", "rad2", "rad3")),
        sigma=frozendict({"Genre": "m"})
    )

    assert str(actual) == "Radical(rad1::rad2::rad3,Genre=m)"


def test_to_glose() -> None:
    radical = Radical(
        stems=StemSpace(stems=("rad1", "rad2", "rad3")),
        sigma=frozendict({"Genre": "m"})
    )

    actual = radical.to_glose()
    assert actual == "rad1.m"
