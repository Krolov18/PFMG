"""Structure that yields Desinence (source/destination morpheme lists) per POS and Sigma."""

from dataclasses import dataclass
from pathlib import Path

import yaml

from pfmg.lexique.block.Blocks import Blocks
from pfmg.lexique.block.Desinence import Desinence
from pfmg.lexique.phonology.Phonology import Phonology
from pfmg.lexique.sigma.Sigma import Sigma


@dataclass
class BlockEntry:
    """Maps POS to source/destination Blocks; (pos, sigma) -> Desinence.

    Attributes:
        source: POS -> Blocks for source language.
        destination: POS -> Blocks for destination language.

    """

    source: dict[str, Blocks]
    destination: dict[str, Blocks]

    def __post_init__(self) -> None:
        """Ensure source and destination are non-empty."""
        assert self.source
        assert self.destination

    def __call__(self, pos: str, sigma: Sigma) -> Desinence:
        """Build a Desinence for the given pos and sigma if the pair is valid.

        Args:
            pos: A POS present in both source and destination Blocks.
            sigma: A valid Sigma instance.

        Returns:
            Desinence: Source and destination morpheme lists for that pos/sigma.

        """
        return Desinence(
            source=self.source[pos](sigma.source),
            destination=self.destination[pos](sigma.destination),
        )

    @classmethod
    def from_yaml(cls, path: Path) -> BlockEntry:
        """Load BlockEntry from a Blocks.yaml file.

        Args:
            path: Path to Blocks.yaml (Phonology.yaml must be in same parent dir).

        Returns:
            BlockEntry: New BlockEntry instance.

        """
        assert path.name.endswith("Blocks.yaml")

        phonology = Phonology.from_yaml(
            path.parent / "Phonology.yaml",
        )

        with open(path, encoding="utf8") as file_handler:
            data: dict = yaml.safe_load(file_handler)

        sources = {}
        destinations = {}
        for pos, blocks in data.items():
            sources[pos] = Blocks.from_list(blocks["source"], phonology)
            destinations[pos] = Blocks.from_list(blocks["destination"], phonology)
        return cls(sources, destinations)
