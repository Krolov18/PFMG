import argparse
import functools
import json
import os
import pathlib
import pathlib as pl
from typing import Callable, Literal

from tabulate import tabulate
import yaml
from jsonschema import validate
from nltk import parse
from nltk.grammar import FeatureGrammar

from lexique.etl import (split,
                         read_blocks,
                         read_gloses,
                         read_morphosyntax,
                         read_phonology,
                         read_rules,
                         read_stems,
                         build_paradigm)
from lexique.lexicon import trad_lexrule, build_df

# from lexique.validate import validate_tree, validate_sentence
from utils.abstract_factory import factory_function
from utils.compose import compose

preprocess = compose(functools.partial(yaml.load, Loader=yaml.Loader), argparse.FileType("r"))


def validate_yaml(id_schema: Literal['gloses', 'stems', 'morphosyntax', 'blocks'], yaml_abspath: str | pl.Path) -> None:
    with open(yaml_abspath, mode="r", encoding="utf8") as fh:
        instance = yaml.load(fh, Loader=yaml.Loader)

    with open(os.path.join(os.path.dirname(__file__), "schemas", f"{id_schema}.json"), mode="r", encoding="utf8") as fh:
        schema = json.load(fh)

    validate(instance=instance, schema=schema)


def action(id_action: str, namespace: argparse.Namespace) -> None:
    """
    Factory permettant de construire les actions du "main".

    Plutôt que de créer des sous-classes de "argparse.Namespace"
    On choisit d'utiliser le champ

    :param id_action : préfixe correspondant à une commande du "main"
    :param namespace : namespace généré par ArgumentParser.parse_args()
    :return:
    """
    factory_function(
        concrete_product=f"{id_action}_action",
        package=__name__,
        namespace=namespace
    )


def validate_grammar_config_files(args: argparse.Namespace) -> None:
    # validate_yaml(id_schema="gloses", yaml_abspath=args.datapath / "grammar" / "Gloses.yaml")
    validate_yaml(id_schema="blocks", yaml_abspath=args.datapath / "grammar" / "Blocks.yaml")
    # validate_yaml(id_schema="stems", yaml_abspath=args.datapath / "grammar" / "Stems.yaml")
    # validate_yaml(id_schema="morphosyntax", yaml_abspath=args.datapath / "grammar" / "MorphoSyntax.yaml")


def startproject_action(namespace: argparse.Namespace) -> None:
    """
    Initialisation d'un projet.
    On crée une archive Kalaba contenant
    <nom_de_projet>/
        grammar/
            Gloses.yaml
            Blocks.yaml
            Stems.yaml
            MorphoSyntax.yaml

    namespace.project_path détermine où le projet doit être créé

    :param namespace:
    :return:
    """
    assert not (namespace.project_path / namespace.project_name).exists()
    text = "# Fichier généré par la commande startproject\n"

    grammar_dir: pathlib.Path = (namespace.project_path / namespace.project_name / "grammar")
    grammar_dir.mkdir(parents=True)
    for file in ("Gloses", "Blocks", "Stems", "MorphoSyntax"):
        (grammar_dir / f"{file}.yaml").write_text(text)


def validate_action(namespace: argparse.Namespace) -> None:
    """
    Valide les composantes d'une grammaire.

    :param namespace : namespace généré par ArgumentParser.parse_args():
    """
    validate_grammar_config_files(namespace)

    grammar_path: pl.Path = namespace.datapath

    gloses, att_vals = read_gloses(gloses=preprocess(grammar_path / "grammar" / "Gloses.yaml"))

    lexemes = list(read_stems(data=preprocess(grammar_path / "grammar" / "Stems.yaml"),
                              accumulator="",
                              att_vals=att_vals))
    phonology = read_phonology(data=preprocess(grammar_path / "grammar" / "Phonology.yaml"))

    blocks = read_blocks(data=preprocess(grammar_path / "grammar" / "Blocks.yaml"),
                         att_vals=att_vals,
                         voyelles=phonology.voyelles)

    paradigm = build_paradigm(glose=gloses,
                              blocks=blocks)

    morphosyntax = read_morphosyntax(data=preprocess(grammar_path / "grammar" / "MorphoSyntax.yaml"))

    francais2kalaba, _ = read_rules(morphosyntax=morphosyntax)

    nt_rules = "\n".join(francais2kalaba)

    lexicon = trad_lexrule(lexemes=lexemes, paradigm=paradigm, phonology=phonology)

    if namespace.print_lexicon:
        data_frame = build_df(term=lexemes,
                              paradigm=paradigm,
                              att_vals=att_vals,
                              phonology=phonology)
        print(tabulate(data_frame[data_frame.columns[~data_frame.columns.isin(["unary"])]], headers="keys"))

    if namespace.words:
        print(nt_rules.replace("\n", "\n\n"))
        print("", namespace.words, *validate_sentence(
            sentence=split(namespace.words),
            rules=nt_rules,
            lexicon=lexicon,
            morpho=morphosyntax,
            start_nt=namespace.start_nt or morphosyntax.start
        ), sep="\n")

        return


def test_action(namespace: argparse.Namespace) -> None:
    """
    À partir d'une grammaire existante,
    Les phrases (données en option) seront parsées et un rapport d'erreurs sera présenté à l'utilisateur.
    :param namespace:
    :return:
    """
    g_ = namespace.infile.read().split("\n", 1)[1]
    while True:
        try:
            start, syntagme = input("<START> <PHRASE>").split(" ", 1)
        except ValueError:
            break
        grammar_ = FeatureGrammar.fromstring(f"% start {start}\n" + g_)
        parser = parse.FeatureEarleyChartParser(grammar_)
        tree = next(parser.parse(syntagme.split(" ")))
        if tree is not None:
            print(tree)
            print()
        else:
            print("ça marche pas")


def lexicon_action(namespace: argparse.Namespace) -> None:
    grammar_path: pathlib.Path = namespace.datapath
    gloses, att_vals = read_gloses(gloses=preprocess(grammar_path / "grammar" / "Gloses.yaml"))
    lexemes = list(read_stems(data=preprocess(grammar_path / "grammar" / "Stems.yaml"),
                              accumulator="",
                              att_vals=att_vals))
    phonology = read_phonology(data=preprocess(grammar_path / "grammar" / "Phonology.yaml"))
    blocks = read_blocks(data=preprocess(grammar_path / "grammar" / "Blocks.yaml"),
                         att_vals=att_vals,
                         voyelles=phonology.voyelles)
    paradigm = build_paradigm(glose=gloses,
                              blocks=blocks)

    df = build_df(lexemes, paradigm, att_vals, phonology)

    if namespace.exclude is not None:
        print(df.loc[:, ~df.columns.isin(namespace.exclude)].to_markdown(index=None))
    else:
        print(df.to_markdown(index=None))
    # lexicon = trad_lexrule(lexemes=lexemes,
    #                        paradigm=paradigm,
    #                        phonology=phonology)
