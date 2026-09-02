"""CLI actions for the parsing package main."""

import sys
from pathlib import Path

from pfmg.lexique.lexicon import Lexicon
from pfmg.parsing.lexical_grammar import LexicalGrammarExporter
from pfmg.parsing.parser import KParser
from pfmg.utils.abstract_factory import factory_function


def action(
    namespace: dict,
) -> None:
    """Dispatch to the requested action (name and args taken from namespace).

    Args:
        namespace: Dict from ArgumentParser.parse_args() (must contain "name").

    """
    name = namespace.pop("name")
    assert name is not None

    factory_function(
        concrete_product=f"{name}_action",
        package=__name__,
        namespace=namespace,
    )


def parsing_action(namespace: dict) -> None:
    """Build a KParser from path in namespace and parse; write results to stdout.

    Args:
        namespace: Must contain "path" and parse options (e.g. data, keep).

    """
    parser = KParser.from_yaml(namespace.pop("path"))

    result = parser.parse(**namespace)

    if isinstance(result, str):
        result = [result]

    sys.stdout.write("\n".join(result) + "\n")


def lexical_grammar_action(namespace: dict) -> None:
    """Export translation and validation lexical productions to stdout.

    Args:
        namespace: Must contain ``datapath`` (path to lexicon config directory).

    """
    path = Path(namespace["datapath"])
    lexicon = Lexicon.from_yaml(path)
    exporter = LexicalGrammarExporter()
    for forme in lexicon:
        sys.stdout.write(exporter.export_forme_translation(forme) + "\n")
        sys.stdout.write(exporter.export_forme_validation(forme) + "\n")
