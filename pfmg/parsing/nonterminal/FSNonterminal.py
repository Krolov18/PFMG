from dataclasses import dataclass


@dataclass
class FSNonterminal[T]:
    symbol: T
    features: dict
