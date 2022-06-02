from typing import Dict, List

import numpy as np
import pandas as pd

from lexique.structures import Forme


def format_forme(word: str, term: Forme) -> str:
    return f"{word}(pos={term.pos},{dict(term.sigma)})"


def format_sentence(sentence_: str, real2forme: Dict[str, Forme]) -> List[str]:
    return [format_forme(word, real2forme[word]) for word in sentence_.split(" ")]
