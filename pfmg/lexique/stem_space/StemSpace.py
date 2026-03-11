"""Stem space: tuple of stem strings and a default lemma (first stem)."""

from dataclasses import dataclass


@dataclass
class StemSpace:
    """A set of stem variants; lemma is the first stem."""

    stems: tuple[str, ...]

    def __post_init__(self) -> None:
        """Ensure stems is non-empty and set lemma to the first stem."""
        assert self.stems
        self.lemma = self.stems[0]
        assert self.lemma

    @classmethod
    def from_string(cls, key: str) -> StemSpace:
        """Build a StemSpace from a comma-separated string of stems."""
        assert key
        return cls(stems=tuple(key.split(",")))
