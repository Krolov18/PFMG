"""Parser for feature strings (semicolon/comma/equal-separated) into dict(s)."""


class FeatureReader:
    """Parses feature specification strings into a list of feature dicts."""

    def parse(self, data: str, target: str = "") -> list[dict]:
        """Parse data into feature dict(s); target prefixes feature names (e.g. S/D).

        Args:
            data: Feature specification string (semicolon/comma/equal-separated).
            target: Prefix for feature names (e.g. "S" or "D"). Defaults to "".

        Returns:
            list[dict]: One or more feature dicts.

        """
        assert data

        nb_c = data.count(";") + 1 if data.count(";") > 0 else 1
        accumulator: list[dict] = [{} for _ in range(nb_c)]
        self.__read(
            data,
            target=target,
            accumulator=accumulator if nb_c > 1 else accumulator[0],
            separators=("scolon", "comma", "equal", "char"),
        )
        return accumulator

    def __read(
        self,
        data: str,
        *,
        target: str,
        accumulator: list[dict] | dict,
        separators: tuple[str, ...],
    ) -> None:
        """Recursively parse using the first matching separator (scolon, comma, equal, char)."""
        for name in separators:
            try:
                name = f"_{self.__class__.__name__}__read_{name}"
                result = getattr(self, name)(
                    data=data,
                    target=target,
                    accumulator=accumulator,
                    separators=separators,
                )
            except AssertionError:
                continue
            else:
                return result
        return None

    def __read_scolon(
        self,
        data: str,
        *,
        target: str,
        accumulator: list[dict],
        separators: tuple[str, ...],
    ) -> None:
        """Split on ';' and parse each segment into the corresponding accumulator slot."""
        assert ";" in data

        tmp_ = data.split(";")
        for i_idx, i_x in enumerate(tmp_):
            assert isinstance(accumulator[i_idx], dict)
            self.__read(
                i_x,
                target=target,
                accumulator=accumulator[i_idx],
                separators=separators[1:],
            )

    def __read_comma(
        self,
        data: str,
        *,
        target: str,
        accumulator: dict,
        separators: tuple[str, ...],
    ) -> None:
        """Split on ',' and parse each segment into the same accumulator."""
        assert "," in data
        assert isinstance(accumulator, dict)

        tmp_ = data.split(",")
        for x in tmp_:
            self.__read(
                x,
                target=target,
                accumulator=accumulator,
                separators=separators[1:],
            )

    @staticmethod
    def __read_equal(data: str, *, target: str, accumulator: dict, **_kwargs) -> None:
        """Parse key=value and store in accumulator with target-prefixed key."""
        assert "=" in data

        if not all(lhs_rhs := data.partition("=")):
            raise TypeError(lhs_rhs)

        match accumulator:
            case [a]:
                a[f"{target}{lhs_rhs[0]}"] = lhs_rhs[2]
            case dict():
                accumulator[f"{target}{lhs_rhs[0]}"] = lhs_rhs[2]

    @staticmethod
    def __read_char(data: str, target: str, accumulator: dict, **_kwargs) -> None:
        """Store a single feature name as key with a variable placeholder as value."""
        assert ";" not in data
        assert "," not in data
        assert "=" not in data

        if not data:
            return

        match accumulator:
            case [a]:
                a[f"{target}{data}"] = f"?{target}{data}"
            case dict():
                accumulator[f"{target}{data}"] = f"?{target}{data}"
