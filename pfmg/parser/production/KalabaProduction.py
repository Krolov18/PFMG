"""KalabaProduction."""
from dataclasses import dataclass

from nltk.grammar import Production


@dataclass
class KalabaProduction:
    """Production de Kalaba.

    source: Production pour la traduction
    destination: productionpour la validation
    """
    
    source: Production
    destination: Production

