"""Grammar loader from MorphoSyntax YAML; holds translator and validator grammars."""

from dataclasses import dataclass
from pathlib import Path
from typing import Self

import yaml

from pfmg.external.reader import ABCReader
from pfmg.parsing.grammar import Grammar
from pfmg.parsing.production import Production


@dataclass
class KGrammar(ABCReader):
    """Pair of grammars (translator and validator) loaded from a MorphoSyntax YAML file.

    Attributes:
        translator: Grammar for translation phase.
        validator: Grammar for validation phase.

    """

    translator: Grammar
    validator: Grammar

    @classmethod
    def from_yaml(cls, path: str | Path) -> Self:
        """Load translator and validator grammars from a MorphoSyntax.yaml file.

        Args:
            path: Path to the MorphoSyntax.yaml file.

        Returns:
            KGrammar: Instance with translator and validator grammars.

        """
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

                s_production.update(production=d_production, indices=s_translation)
                sources.append(s_production)
                destinations.append(d_production)

        return cls(
            translator=Grammar(start=start, productions=sources),
            validator=Grammar(start=start, productions=destinations),
        )

    def to_validation(self) -> Grammar:
        """Return the validator grammar.

        Returns:
            Grammar: The validator grammar.

        """
        return self.validator
