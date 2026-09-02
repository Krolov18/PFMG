"""Realizes Lexemes as Forme (paradigm: gloses + blocks)."""

import itertools
from collections.abc import Generator, Iterator
from dataclasses import dataclass, field
from pathlib import Path

from pfmg.external.reader.ABCReader import ABCReader
from pfmg.external.realizable.ABCRealizable import ABCRealizable
from pfmg.lexique.block.BlockEntry import BlockEntry
from pfmg.lexique.forme.Forme import Forme
from pfmg.lexique.forme.FormeEntry import FormeEntry
from pfmg.lexique.lexeme.Lexeme import Lexeme
from pfmg.lexique.morpheme.Morphemes import Morphemes
from pfmg.lexique.sigma import new_gloses
from pfmg.lexique.sigma.Sigma import Sigma
from pfmg.lexique.sigma.StraightPos2Sigmas import StraightPos2Sigmas


@dataclass(repr=False)
class Paradigm(ABCRealizable, ABCReader):
    """Realizes Lexemes as Forme using gloses (POS -> Sigmas) and blocks (Desinence).

    Attributes:
        gloses: POS -> Sigmas mapping.
        blocks: Desinence blocks.
        counter: Per-instance source of Forme indexes. It is deliberately *not*
            shared between Paradigm instances: the indexes it produces are the
            terminals of the generated NLTK grammars, so a counter shared
            process-wide would make those terminals depend on how many
            realizations happened earlier in the process.

    """

    gloses: StraightPos2Sigmas
    blocks: BlockEntry
    counter: Iterator[int] = field(
        default_factory=itertools.count, repr=False, compare=False
    )

    def _next_index(self) -> int:
        """Return the next Forme index of this Paradigm."""
        return next(self.counter)

    def realize(self, lexeme: Lexeme) -> Generator[Forme]:
        """Yield all Forme realizations of the given lexeme (matching sigma and desinence)."""
        gloses = self.gloses(lexeme.source.pos)
        lexeme_pos = lexeme.source.pos
        for i_sigma in gloses:
            if Sigma(lexeme.source.sigma, lexeme.destination.sigma) <= i_sigma:
                desinence = self.blocks(lexeme_pos, i_sigma)
                yield Forme(
                    source=FormeEntry(
                        index=self._next_index(),
                        pos=lexeme_pos,
                        sigma=i_sigma.source,
                        morphemes=Morphemes(
                            radical=lexeme.source.to_radical(),
                            others=desinence.source,
                        ),
                    ),
                    destination=FormeEntry(
                        index=self._next_index(),
                        pos=lexeme_pos,
                        sigma=i_sigma.destination,
                        morphemes=Morphemes(
                            radical=lexeme.destination.to_radical(),
                            others=desinence.destination,
                        ),
                    ),
                )

    @classmethod
    def from_yaml(cls, path: Path) -> Paradigm:
        """Load Paradigm from a directory (Gloses.yaml, Blocks.yaml, etc.)."""
        assert (path / "Gloses.yaml").exists()
        return cls(
            gloses=new_gloses(path=path / "Gloses.yaml"),
            blocks=BlockEntry.from_yaml(path=path / "Blocks.yaml"),
        )
