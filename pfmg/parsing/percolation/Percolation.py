# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""TODO : Write some doc."""

from dataclasses import dataclass

from pfmg.parsing.agreement.Agreement import Agreement


@dataclass
class Percolation:
    """TODO : Write some doc."""

    data: str

    @staticmethod
    def __parse_percolation(
        data: str, agreement: Agreement, accumulator: dict
    ) -> None:
        """TODO : Write some doc."""
        assert "Destination" in accumulator or "Source" in accumulator

        if not data:
            return

        source = next(x for x in accumulator.keys())
        source_init = source[0]

        if ";" in data:
            for i_idx, i_x in enumerate(data.split(";")):
                Percolation.__parse_percolation(
                    i_x,
                    agreement[i_idx],  # type: ignore
                    accumulator,
                )
        elif "," in data:
            for i_x in data.split(","):
                Percolation.__parse_percolation(i_x, agreement, accumulator)
        elif "=" in data:
            if not all(lhs_rhs := data.partition("=")):
                raise TypeError(lhs_rhs)
            match agreement.data:
                case [a] if (
                    m := a[source].get(f"{source_init}{lhs_rhs[0]}", None)
                ) and m == lhs_rhs[2]:
                    accumulator[source][f"{source_init}{lhs_rhs[0]}"] = m
                case [a] if a[source].get(f"{source_init}{lhs_rhs[0]}", None):
                    raise TypeError(data, agreement, accumulator)
                case [_]:
                    accumulator[source][f"{source_init}{lhs_rhs[0]}"] = lhs_rhs[
                        2
                    ]
                case dict():
                    accumulator[source][f"{source_init}{lhs_rhs[0]}"] = lhs_rhs[
                        2
                    ]
                case _:
                    raise TypeError(data, agreement, accumulator)
        else:
            perco = f"{source_init}{agreement}"
            match agreement:
                case dict():
                    result = agreement[source][perco]
                case [dict()]:
                    result = agreement[0][source][perco]
                case _:
                    raise TypeError(data, agreement, accumulator)
            accumulator[source][perco] = result
