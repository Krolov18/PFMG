"""Desinence: source and destination morpheme lists for a word form."""

from dataclasses import dataclass


@dataclass
class Desinence:
    """Pair of morpheme lists: one for source, one for destination."""

    source: list["Morpheme"]  # noqa # type: ignore
    destination: list["Morpheme"]  # noqa # type: ignore
