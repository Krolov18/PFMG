"""Mixin providing default equality (same rule string and sigma subset)."""

from pfmg.external.equality.ABCEquality import ABCEquality


class MixinEquality(ABCEquality):
    """Mixin that implements equality by comparing rule string and sigma items."""

    def __eq__(self, other: object) -> bool:
        """Return True if other is same type, same rule string, and sigma items are compatible.

        Args:
            other: Object to compare with.

        Returns:
            bool: True if equal (same rule string and compatible sigma).

        """
        if not isinstance(other, ABCEquality):
            return False
        eq_rules = self.get_rule().string == other.get_rule().string
        return eq_rules and (
            (self.get_sigma().items() <= other.get_sigma().items())
            or (other.get_sigma().items() <= self.get_sigma().items())
        )
