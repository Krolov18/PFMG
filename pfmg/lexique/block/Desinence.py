"""Désinence."""

from dataclasses import dataclass


@dataclass
class Desinence:
    """Ensemble de morphèmes pour source/destination."""

    source: list["Morpheme"]  # noqa # type: ignore
    destination: list["Morpheme"]  # noqa # type: ignore
