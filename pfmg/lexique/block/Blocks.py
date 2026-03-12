"""Blocks: list of morpheme groups, one of which is chosen per sigma."""

from dataclasses import dataclass

from frozendict import frozendict

from pfmg.lexique.morpheme.Factory import create_morpheme
from pfmg.lexique.phonology.Phonology import Phonology
from pfmg.parsing.features.utils import FeatureReader


@dataclass
class Blocks:
    """List of morpheme lists (blocks); __call__(sigma) returns matching morphemes."""

    data: list[list["Morpheme"]]  # noqa # type: ignore

    def __post_init__(self) -> None:
        """Ensure all blocks are non-empty."""
        assert self.data
        assert all(x for x in self.data)

    def __call__(self, sigma: frozendict) -> list["Morpheme"]:  # noqa # type: ignore
        """Return the list of morphemes that match the given sigma (one per block)."""
        assert sigma

        output: list["Morpheme"] = []  # noqa # type: ignore
        for morphemes in self.data:
            winner: "Morpheme | None" = None  # noqa # type: ignore
            for morpheme in morphemes:
                if morpheme.get_sigma().items() <= sigma.items():
                    winner = morpheme
            if winner is not None:
                output.append(winner)
        return output

    @classmethod
    def from_list(cls, data: list[dict], phonology: Phonology) -> Blocks:
        """Build Blocks from a list of block dicts (sigma spec -> rule) and a Phonology."""
        output: list[list["Morpheme"]] = []  # noqa # type: ignore

        fr = FeatureReader()
        for block in data:
            _tmp = []
            for key, value in block.items():
                _sigma = frozendict(fr.parse(key)[0])
                _tmp.append(
                    create_morpheme(
                        rule=value,
                        sigma=_sigma,
                        phonology=phonology,
                    ),
                )
            output.append(_tmp)

        assert output
        return cls(output)
