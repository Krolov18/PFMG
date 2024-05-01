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
            parameters = [
                x for x in target["Source"].keys() if x != "Traduction"
            ]
            for i_idx, i_rule in enumerate(
                zip(*target["Source"].values(), strict=True)
            ):
                production = Production.from_yaml(
                    {
                        "Source": dict(
                            lhs=lhs,
                            **dict(zip(parameters, i_rule[:-1], strict=True)),
                        )
                    }
                )
                production.add_translation(
                    target["Source"]["Traduction"][i_idx]
                )
                sources.append(production)

            for i_rule in zip(*target["Destination"].values(), strict=True):
                destinations.append(
                    Production.from_yaml(
                        {
                            "Destination": dict(
                                lhs=lhs,
                                **dict(zip(parameters, i_rule, strict=True)),
                            )
                        }
                    )
                )

        return cls(
            translator=Grammar(start=start, productions=sources),
            validator=Grammar(start=start, productions=destinations),
        )

    def to_validation(self) -> Grammar:
        """TODO : Write some doc."""
        return self.validator
