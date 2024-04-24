from dataclasses import dataclass
from pathlib import Path

import yaml

from pfmg.external.reader import ABCReader
from pfmg.parsing.grammar import Grammar
from pfmg.parsing.production import Production


@dataclass
class KGrammar(ABCReader):
    trad: Grammar
    val: Grammar

    @classmethod
    def from_yaml(cls, path: Path) -> 'KGrammar':
        assert path.name.endswith("MorphoSyntax.yaml")

        with open(path, encoding="utf8") as file_handler:
            data = yaml.safe_load(file_handler)

        start = data.pop("start", None)

        assert start is not None
        assert data

        sources: list[Production] = []
        destinations: list[Production] = []

        for lhs, target in data.items():
            parameters = [x.lower() for x in target["Source"].keys()]
            for i_rule in zip(*target["Source"].values()):
                sources.append(
                    Production(lhs=lhs, **dict(zip(parameters, i_rule)))
                )

            for i_rule in zip(*target["Destination"].values()):
                destinations.append(
                    Production(lhs=lhs, **dict(zip(parameters, i_rule)))
                )

        return cls(
            trad=Grammar(
                start=start,
                productions=sources
            ),
            val=Grammar(
                start=start,
                productions=destinations
            )
        )
