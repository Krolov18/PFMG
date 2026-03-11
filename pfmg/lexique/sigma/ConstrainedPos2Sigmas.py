"""Gloses with constraints (filter paradigm by source/destination alignments)."""

from dataclasses import dataclass
from pathlib import Path

import yaml
from frozendict import frozendict

from pfmg.external.reader.ABCReader import ABCReader
from pfmg.lexique.sigma.Sigma import Sigma
from pfmg.lexique.sigma.Sigmas import Sigmas
from pfmg.lexique.sigma.StraightPos2Sigmas import StraightPos2Sigmas
from pfmg.parsing.features.utils import FeatureReader


@dataclass
class ConstrainedPos2Sigmas(ABCReader):
    """Paradigm gloses filtered by alignments (e.g. source Number 'sg' -> destination 'sg').

    Attributes:
        gloses: Standard paradigm gloses (POS -> Sigmas).
        alignments: Constraints between source and destination (filters valid Sigma pairs).

    Examples:
        If source Number is 'sg' then destination Number must be 'sg'; a pair
        (sg, pl) is filtered out.

    """

    gloses: StraightPos2Sigmas
    alignments: StraightPos2Sigmas

    def __call__(self, pos: str) -> Sigmas:
        """Return gloses for pos filtered by alignments.

        Args:
            pos: Part-of-speech key.

        Returns:
            Sigmas: Filtered list of Sigma instances.

        """
        return Sigmas(
            [sigma for sigma in self.gloses(pos) if sigma in self.alignments(pos)]
        )

    @classmethod
    def from_yaml(cls, path: Path) -> ConstrainedPos2Sigmas:
        """Load ConstrainedPos2Sigmas from a YAML file.

        Args:
            path: Path to the YAML file.

        Returns:
            ConstrainedPos2Sigmas: New instance with gloses and alignments.

        """
        with open(path, encoding="utf8") as fh:
            data = yaml.safe_load(fh)
        gloses = StraightPos2Sigmas.from_dict(data)
        alignments = StraightPos2Sigmas(cls.__read_alignments(data))
        return cls(gloses=gloses, alignments=alignments)

    @staticmethod
    def __read_alignments(data: dict) -> dict:
        fr = FeatureReader()
        return {
            pos: Sigmas(
                [
                    Sigma(
                        source=frozendict(fr.parse(key)[0]),
                        destination=frozendict(fr.parse(value)[0]),
                    )
                    for key, values in sigmas["alignments"].items()
                    for value in values
                ]
            )
            for pos, sigmas in data.items()
        }
