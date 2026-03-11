"""Feature-structure nonterminal: symbol plus feature dict."""

from dataclasses import dataclass


@dataclass
class FSNonterminal[T]:
    """A nonterminal with an associated feature structure (dict).

    Attributes:
        symbol: The nonterminal symbol.
        features: Feature structure (dict) attached to the symbol.

    """

    symbol: T
    features: dict
