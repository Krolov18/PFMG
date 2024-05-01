# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Main pour le package parsing."""
import argparse
import pathlib

from pfmg.parsing.main.actions import action

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    SUB_PARSERS = PARSER.add_subparsers(dest="name")

    PARSING = SUB_PARSERS.add_parser(name="parsing")
    PARSING.add_argument("path",
                         type=pathlib.Path)
    PARSING.add_argument("data",
                         action="append")
    PARSING.add_argument("-k", "--keep",
                         choices=("first", "all"),
                         default="first")

    args = vars(PARSER.parse_args())
    action(namespace=args)
