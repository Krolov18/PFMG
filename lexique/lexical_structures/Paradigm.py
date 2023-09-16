from dataclasses import dataclass
from pathlib import Path

from lexique.lexical_structures.interfaces.Reader import Reader
from lexique.lexical_structures.Blocks import Blocks
from lexique.lexical_structures.Forme import Forme
from lexique.lexical_structures.Gloses import Gloses
from lexique.lexical_structures.Lexeme import Lexeme
from lexique.lexical_structures.Morphemes import Morphemes
from lexique.lexical_structures.interfaces.Realizer import Realizer


@dataclass
class Paradigm(Realizer, Reader):
    """
    Classe qui permet de réaliser un paradigme.
    """
    gloses: Gloses
    blocks: Blocks

    def __realise(self, lexeme: LexemeEntry, blocks: BlockEntry) -> list[Entry]:
        entries: list[FormeEntry] = list()

        for i_sigma in sigmas:
            if lexeme.sigma.items() <= i_sigma.items():
                entries.append(
                    Entry(
                        pos=lexeme.pos,
                        sigma=i_sigma,
                        morphemes=Morphemes(
                            radical=lexeme.to_radical(),
                            others=blocks.select_morphemes(
                                pos=lexeme.pos,
                                sigma=i_sigma
                            )
                        )
                    )
                )
        return entries

    def realize(self, lexeme: Lexeme) -> list[Forme]:
        """
        Méthode qui permet de réaliser un lexème donné.

        :param lexeme: Lexème à réaliser.
        :return: Liste des réalisations du lexème.
        """
        return [Forme(source=s,
                      destination=d)
                for s, d in zip(self.__realise(lexeme=lexeme.source,
                                               blocks=self.blocks.source),
                                self.__realise(lexeme=lexeme.destination,
                                               blocks=self.blocks.destination))]

    @classmethod
    def from_disk(cls, path: Path) -> 'Paradigm':
        """
        Méthode permettant de charger un paradigme à partir d'un chemin donné.

        :param path: Chemin à partir duquel charger le paradigme.
        :return: Instance de Paradigm.
        """
        return cls(gloses=Gloses.from_disk(
            path=path / "Gloses.yaml"),
                   blocks=Blocks.from_disk(
                       path=path / "Blocks.yaml")
        )
