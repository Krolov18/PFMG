"""TODO : Write some doc."""


class FeatureMixin:
    """TODO : Write some doc."""

    @staticmethod
    def broadcast(data: str, i: int) -> str:
        """TODO : Write some doc."""
        assert (data.count(";") == 0) or (data.count(";") != (i - 1))
        return ((data + ";") * i).rstrip(";")
