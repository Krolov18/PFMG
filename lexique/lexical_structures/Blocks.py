from dataclasses import dataclass
from pathlib import Path

import yaml
from frozendict import frozendict

from lexique.lexical_structures.BlockEntry import BlockEntry
from lexique.lexical_structures.interfaces.Display import Display
from lexique.lexical_structures.interfaces.Reader import Reader
from lexique.lexical_structures.Phonology import Phonology


@dataclass
class Blocks(Reader):
    source: BlockEntry
    destination: BlockEntry

    def __post_init__(self):
        assert self.source
        assert self.destination

    @classmethod
    def from_disk(cls, path: Path):
        assert path.name.endswith("Blocks.yaml")

        with open(path, mode="r", encoding="utf8") as file_handler:
            data: dict[str, list[dict[str, str]]] = yaml.load(
                file_handler,
                Loader=yaml.Loader
            )

        assert data

        phonology_from_disk = Phonology.from_disk(
            path.parent / "Phonology.yaml"
        )

        source = BlockEntry.from_dict(
            data=data["source"],
            phonology=phonology_from_disk
        )

        destination = BlockEntry.from_dict(
            data=data["destination"],
            phonology=phonology_from_disk
        )

        return cls(source=source, destination=destination)

    def __call__(
        self,
        pos: str,
        sigma: frozendict
    ) -> tuple[list[Display], list[Display]]:
        """
        :param pos:
        :param sigma:
        :return:
        """
        return {key: getattr(self, key)(pos, sigma[key])
                for key, value in sigma.items()}
