from typing import Dict, List, Callable, Tuple

import pandas as pd
from frozendict import frozendict

from lexique.structures import Lexeme, Phonology


def build_df(
        term: List[Lexeme],
        paradigm: Dict[str, Dict[frozendict, Callable]],
        att_vals: frozendict,
        phonology: Phonology
) -> pd.DataFrame: ...


def trad_lexrule(term: List[Lexeme],
                 paradigm: Dict[str, Dict[frozendict, Callable]],
                 phonology: Phonology) -> List[Tuple[str, str]]: ...
