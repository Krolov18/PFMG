"""Mixin for feature broadcast (repeat string for phrase count)."""


class FeatureMixin:
    """Mixin providing broadcast() to repeat feature data per phrase."""

    @staticmethod
    def broadcast(data: str, i: int) -> str:
        """Repeat data i times, joined by ';' (semicolon-separated per phrase).

        Args:
            data: Feature string to repeat.
            i: Number of repetitions (phrase count).

        Returns:
            str: data repeated i times, separated by ';'.

        """
        assert (data.count(";") == 0) or (data.count(";") != (i - 1))
        return ((data + ";") * i).rstrip(";")
