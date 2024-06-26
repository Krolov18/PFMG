# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Main du lexique."""

import argparse
import pathlib

from pfmg.lexique.main.actions import action

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()

    SUB_PARSERS = PARSER.add_subparsers(dest="name")

    LEXICON = SUB_PARSERS.add_parser(name="lexicon")
    # un argument pour le chemin des fichiers de config
    # d'une grammaire (Phonology, Stems, Blocks et Gloses)
    LEXICON.add_argument("datapath", type=pathlib.Path)
    LEXICON.add_argument(
        "-l",
        "--list",
        choices=("to_string", "to_lexical"),
        default="to_string",
    )

    args = PARSER.parse_args()

    action(namespace=args)
