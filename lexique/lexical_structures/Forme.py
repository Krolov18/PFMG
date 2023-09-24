from dataclasses import dataclass

from lexique.lexical_structures.FormeEntry import FormeEntry


@dataclass
class Forme:
    source: FormeEntry
    destination: FormeEntry
