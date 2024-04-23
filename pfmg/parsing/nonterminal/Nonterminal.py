from dataclasses import dataclass


@dataclass
class Nonterminal[T]:
    symbol: T
