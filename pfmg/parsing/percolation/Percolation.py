# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""TODO : Write some doc."""

from dataclasses import dataclass

from pfmg.parsing.features.utils import FeatureReader


@dataclass
class Percolation:
    """TODO : Write some doc."""

    data: dict

    @staticmethod
    def unify(data: list[dict]) -> dict:
        """TODO : Write some doc."""
        import functools as ft

        import nltk

        return ft.reduce(nltk.unify, data)  # type: ignore

    def to_nltk(self) -> str:
        """TODO : Write some doc."""
        return ",".join(f"{key}={value}" for key, value in self.data.items())

    @classmethod
    def from_string(cls, data: str, target: str) -> "Percolation":
        """TODO : Write some doc."""
        features = FeatureReader().parse(data=data, target=target)
        return cls(data=cls.unify(features))

    def add_translation(self, translations: list[str]) -> None:
        """TODO : Write some doc."""
        values = ",".join(translations)
        self.data["Traduction"] = f"({values})"
