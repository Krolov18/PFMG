from dataclasses import dataclass
from pathlib import Path
from typing import Generator

from lexique.lexical_structures.interfaces.Reader import Reader
from lexique.lexical_structures.Blocks import Blocks
from lexique.lexical_structures.Forme import Forme
from lexique.lexical_structures.FormeEntry import FormeEntry
from lexique.lexical_structures.Gloses import Gloses
from lexique.lexical_structures.Lexeme import Lexeme
from lexique.lexical_structures.Morphemes import Morphemes
from lexique.lexical_structures.interfaces.Realizer import Realizer


class BlockEntry:
    pass


@dataclass
class Paradigm(Realizer, Reader):
    """
    Classe qui permet de réaliser un lexème.
    """
    gloses: Gloses
    blocks: Blocks

    def realize(self, lexeme: Lexeme) -> Generator[Forme, None, None]:
        """
        Méthode qui permet de réaliser un lexème donné.

        :param lexeme: Lexème à réaliser.
        :return: Liste des réalisations du lexème.
        """
        gloses = self.gloses(lexeme.source.pos)
        source_sigma_items = lexeme.source.sigma.items()
        destination_sigma_items = lexeme.destination.sigma.items()
        lexeme_pos = lexeme.source.pos
        for i_sigma in gloses:
            i_sigma_source = i_sigma["source"]
            i_sigma_destination = i_sigma["destination"]
            source_validation = (source_sigma_items <= i_sigma_source.items())
            destination_validation = (destination_sigma_items
                                      <= i_sigma_destination.items())
            if source_validation and destination_validation:
                forme_entry_source = FormeEntry(
                    pos=lexeme_pos,
                    sigma=i_sigma_source,
                    morphemes=Morphemes(
                        radical=lexeme.source.to_radical(),
                        others=self.blocks.source(
                            pos=lexeme_pos,
                            sigma=i_sigma_source
                        )
                    )
                )
                forme_entry_destination = FormeEntry(
                    pos=lexeme_pos,
                    sigma=i_sigma_destination,
                    morphemes=Morphemes(
                        radical=lexeme.destination.to_radical(),
                        others=self.blocks.destination(
                            pos=lexeme_pos,
                            sigma=i_sigma_destination
                        )
                    )
                )
                yield Forme(
                    source=forme_entry_source,
                    destination=forme_entry_destination
                )

    @classmethod
    def from_disk(cls, path: Path) -> 'Paradigm':
        """
        Méthode permettant de charger un paradigme à partir d'un chemin donné.

        :param path: Chemin à partir duquel charger le paradigme.
        :return: Instance de Paradigm.
        """
        assert (path / "Gloses.yaml").exists()
        return cls(
            gloses=Gloses.from_disk(
                path=path / "Gloses.yaml"
            ),
            blocks=Blocks.from_disk(
                path=path / "Blocks.yaml"
            )
        )
