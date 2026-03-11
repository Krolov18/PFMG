"""Phonological data: apophonies, derives, mutations, consonants, vowels."""

from dataclasses import dataclass
from pathlib import Path

import yaml
from frozendict import frozendict

from pfmg.external.reader.ABCReader import ABCReader


@dataclass
class Phonology(ABCReader):
    """Encodes phonological information: apophonies (vowel changes), derives, mutations (consonant changes), consonants and vowels sets."""

    apophonies: frozendict
    derives: frozendict
    mutations: frozendict
    consonnes: frozenset
    voyelles: frozenset

    @classmethod
    def from_yaml(cls, path: Path) -> Phonology:
        """Build a Phonology from a Phonology.yaml file."""
        assert path.name.endswith("Phonology.yaml")

        with open(path, encoding="utf8") as file_handler:
            data = yaml.safe_load(file_handler)

        return cls(**Phonology.from_dict(data))

    def to_dict(self) -> dict:
        """Return internal structure as a JSON-serializable dict."""
        return {
            "apophonies": dict(self.apophonies),
            "derives": dict(self.derives),
            "mutations": dict(self.mutations),
            "consonnes": list(self.consonnes),
            "voyelles": list(self.voyelles),
        }

    @staticmethod
    def from_dict(data: dict) -> dict:
        """Build internal structure from a dict (e.g. from JSON/YAML)."""
        return {
            "apophonies": frozendict(data["apophonies"]),
            "derives": frozendict(data["derives"]),
            "mutations": frozendict(data["mutations"]),
            "consonnes": frozenset(data["consonnes"]),
            "voyelles": frozenset(data["voyelles"]),
        }
