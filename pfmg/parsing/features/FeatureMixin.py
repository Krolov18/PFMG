"""Mixin for feature broadcast (repeat string for phrase count)."""


class FeatureMixin:
    """Mixin providing broadcast() to repeat feature data per phrase."""

    @staticmethod
    def broadcast(data: str, i: int) -> str:
        """Return one ';'-separated feature segment per phrase.

        A string that already holds one segment per phrase is returned
        unchanged: that is how a rule constrains its constituents unevenly
        (``"Nombre;Nombre;"`` makes the first two agree and leaves the third
        free). Anything else is a single specification broadcast to every
        phrase.

        Args:
            data: Feature string, either per-phrase or to be repeated.
            i: Number of phrases.

        Returns:
            str: A string of exactly i ';'-separated segments.

        """
        if data.count(";") == i - 1:
            return data
        assert data.count(";") == 0
        return ((data + ";") * i).rstrip(";")
