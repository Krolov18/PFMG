# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""TODO : Write some doc."""


class FeatureReader:
    """TODO : Write some doc."""

    def parse(self, data: str, target: str = "") -> list[dict]:
        """TODO : Write some doc."""
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
        """TODO : Write some doc."""
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
        """TODO : Write some doc."""
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
        """TODO : Write some doc."""
        assert "," in data
        assert isinstance(accumulator, dict)

        tmp_ = data.split(",")
        for x in tmp_:
            self.__read(
                x,
                target=target,
                accumulator=accumulator,
                separators=separators[2:],
            )

    @staticmethod
    def __read_equal(
        data: str, *, target: str, accumulator: dict, **_kwargs
    ) -> None:
        """TODO : Write some doc."""
        assert "=" in data

        if not all(lhs_rhs := data.partition("=")):
            raise TypeError(lhs_rhs)

        match accumulator:
            case [a]:
                a[f"{target}{lhs_rhs[0]}"] = lhs_rhs[2]
            case dict():
                accumulator[f"{target}{lhs_rhs[0]}"] = lhs_rhs[2]

    @staticmethod
    def __read_char(
        data: str, target: str, accumulator: dict, **_kwargs
    ) -> None:
        """TODO : Write some doc."""
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
