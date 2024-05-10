# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""TODO : Write some doc."""

from dataclasses import dataclass
from pathlib import Path
from typing import Self

import yaml

from pfmg.external.reader import ABCReader
from pfmg.parsing.grammar import Grammar
from pfmg.parsing.production import Production


@dataclass
class KGrammar(ABCReader):
    """TODO : Write some doc."""

    translator: Grammar
    validator: Grammar

    @classmethod
    def from_yaml(cls, path: str | Path) -> Self:
        """TODO : Write some doc."""
        path = Path(path)
        assert path.name.endswith("MorphoSyntax.yaml")

        with open(path, encoding="utf8") as file_handler:
            data = yaml.safe_load(file_handler)

        start = data.pop("Start", None)

        assert start is not None
        assert data

        sources: list[Production] = []
        destinations: list[Production] = []

        for lhs, target in data.items():
            nb_rules = len(target["Source"]["phrases"])
            for i in range(nb_rules):
                d_phrase = target["Destination"]["phrases"][i]
                d_percolation = target["Destination"]["percolations"][i]
                d_agreement = target["Destination"]["agreements"][i]
                d_production = Production.from_yaml(
                    data={
                        "lhs": lhs,
                        "phrases": d_phrase,
                        "percolations": d_percolation,
                        "agreements": d_agreement,
                    },
                    target="D",
                )

                s_phrase = target["Source"]["phrases"][i]
                s_percolation = target["Source"]["percolations"][i]
                s_agreement = target["Source"]["agreements"][i]
                s_translation = target["Source"]["translations"][i]
                s_production = Production.from_yaml(
                    data={
                        "lhs": lhs,
                        "phrases": s_phrase,
                        "percolations": s_percolation,
                        "agreements": s_agreement,
                        "translations": s_translation,
                    },
                    target="S",
                )

                s_production.update(
                    production=d_production, indices=s_translation
                )
                sources.append(s_production)
                destinations.append(d_production)

        return cls(
            translator=Grammar(start=start, productions=sources),
            validator=Grammar(start=start, productions=destinations),
        )

    def to_validation(self) -> Grammar:
        """TODO : Write some doc."""
        return self.validator
