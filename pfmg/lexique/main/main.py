"""Main du lexique."""

import argparse
import pathlib

from pfmg.lexique.main.actions import action


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser of the lexique CLI.

    Returns:
        argparse.ArgumentParser: Parser exposing the "lexicon" sub-command.

    """
    parser = argparse.ArgumentParser()

    sub_parsers = parser.add_subparsers(dest="name")

    lexicon = sub_parsers.add_parser(name="lexicon")
    # un argument pour le chemin des fichiers de config
    # d'une grammaire (Phonology, Stems, Blocks et Gloses)
    lexicon.add_argument("datapath", type=pathlib.Path)
    lexicon.add_argument(
        "-l",
        "--list",
        choices=("to_string", "to_lexical"),
        default="to_string",
    )

    return parser


def main(argv: list[str] | None = None) -> None:
    """Run the lexique CLI.

    Args:
        argv: Command-line arguments; defaults to sys.argv[1:].

    """
    action(namespace=build_parser().parse_args(argv))


if __name__ == "__main__":
    main()
