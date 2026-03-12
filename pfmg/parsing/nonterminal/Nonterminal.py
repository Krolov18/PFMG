"""Nonterminal symbol for grammar rules."""

from dataclasses import dataclass


@dataclass
class Nonterminal[T]:
    """A nonterminal symbol (generic type T, e.g. str).

    Attributes:
        symbol: The nonterminal symbol (e.g. str).

    """

    symbol: T
