import argparse
import functools
import pathlib

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


def validate_action(namespace: argparse.Namespace) -> None:
    """
    Valide les composantes d'une grammaire.

    :param namespace : namespace généré par ArgumentParser.parse_args():
    """
    grammar_path: pathlib.Path = namespace.datapath

    gloses, att_vals = read_gloses(gloses=preprocess(grammar_path / "Gloses.yaml"))

    lexemes = list(read_stems(data=preprocess(grammar_path / "Stems.yaml"),
                              accumulator="",
                              att_vals=att_vals))
    phonology = read_phonology(data=preprocess(grammar_path / "Phonology.yaml"))

    blocks = read_blocks(data=preprocess(grammar_path / "Blocks.yaml"),
                         att_vals=att_vals,
                         voyelles=phonology.voyelles)

    paradigm = build_paradigm(glose=gloses,
                              blocks=blocks)

    morphosyntax = read_morphosyntax(data=preprocess(grammar_path / "MorphoSyntax.yaml"))

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
    gloses, att_vals = read_gloses(gloses=preprocess(grammar_path / "Gloses.yaml"))
    lexemes = list(read_stems(data=preprocess(grammar_path / "Stems.yaml"),
                              accumulator="",
                              att_vals=att_vals))
    phonology = read_phonology(data=preprocess(grammar_path / "Phonology.yaml"))
    blocks = read_blocks(data=preprocess(grammar_path / "Blocks.yaml"),
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
