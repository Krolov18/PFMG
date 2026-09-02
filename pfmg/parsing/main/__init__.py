"""Main pour le package parsing."""

import argparse
import pathlib

from pfmg.parsing.main.actions import action


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser of the parsing CLI.

    Returns:
        argparse.ArgumentParser: Parser exposing the "parsing" sub-command.

    """
    parser = argparse.ArgumentParser()
    sub_parsers = parser.add_subparsers(dest="name")

    parsing = sub_parsers.add_parser(name="parsing")
    parsing.add_argument("path", type=pathlib.Path)
    parsing.add_argument("data", action="append")
    parsing.add_argument("-k", "--keep", choices=("first", "all"), default="first")

    lexical_grammar = sub_parsers.add_parser(name="lexical_grammar")
    lexical_grammar.add_argument("datapath", type=pathlib.Path)

    return parser


def main(argv: list[str] | None = None) -> None:
    """Run the parsing CLI.

    Args:
        argv: Command-line arguments; defaults to sys.argv[1:].

    """
    action(namespace=vars(build_parser().parse_args(argv)))


__all__ = ["build_parser", "main"]
