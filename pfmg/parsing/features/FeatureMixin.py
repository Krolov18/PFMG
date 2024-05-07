# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""TODO : Write some doc."""


class FeatureMixin:
    """TODO : Write some doc."""

    @staticmethod
    def broadcast(data: str, i: int) -> str:
        """TODO : Write some doc."""
        assert (data.count(";") == 0) or (data.count(";") != (i - 1))
        return ((data + ";") * i).rstrip(";")
