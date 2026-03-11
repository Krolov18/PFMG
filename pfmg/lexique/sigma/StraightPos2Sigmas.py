"""Paradigm cells by POS: maps POS to Sigmas (paradigm labels)."""

from dataclasses import dataclass
from pathlib import Path

import yaml

from pfmg.external.reader import ABCReader
from pfmg.lexique.sigma.Sigmas import Sigmas


@dataclass
class StraightPos2Sigmas(ABCReader):
    """Maps POS to Sigmas (paradigm cells / labels for a language)."""

    data: dict[str, Sigmas]

    def __call__(self, pos: str) -> Sigmas:
        """Return the Sigmas for the given POS (raises KeyError if pos missing)."""
        return self.data[pos]

    @classmethod
    def from_yaml(cls, path: Path | str) -> StraightPos2Sigmas:
        """Load StraightPos2Sigmas from a Gloses.yaml file."""
        path = Path(path)
        assert path.name.endswith("Gloses.yaml")
        with open(path, encoding="utf8") as file_handler:
            data = yaml.safe_load(file_handler)
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: dict) -> StraightPos2Sigmas:
        """Build from a dict (each value must have 'source' and 'destination' keys)."""
        return cls(
            data={
                pos: Sigmas.from_dict(sigmas["source"], sigmas["destination"])
                for pos, sigmas in data.items()
            }
        )
