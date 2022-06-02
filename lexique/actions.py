import argparse
import functools
import pathlib
import re

import pandas as pd
from tabulate import tabulate
import yaml
from nltk import parse
from nltk.grammar import FeatureGrammar

from lexique.etl import read_morphosyntax, split
from lexique.lexicon import trad_lexrule, build_df
from lexique.report import report
from lexique.syntax import cleave
from lexique.unary import unary
from lexique.validate import validate_tree, validate_sentence
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


def translate_action(namespace: argparse.Namespace) -> None:
    """
    à partir d'une grammaire et d'un corpus de phrase en français,
    on va traduire ces phrases en Kalaba.
    :param namespace : namespace généré par ArgumentParser.parse_args():
    postcondition: validation des phrases traduites avec une grammaire Kalaba
    """


def validate_action(namespace: argparse.Namespace) -> None:
    """
    Valide les composantes d'une grammaire.

    :param namespace : namespace généré par ArgumentParser.parse_args():
    """
    grammar_path: pathlib.Path = namespace.datapath

    gloses, att_vals = report(id_report="gloses",
                              gloses=preprocess(grammar_path / "Gloses.yaml"),
                              verbose=namespace.verbose)

    gloses = report(id_report="translation",
                    gloses=gloses,
                    constraints=preprocess(grammar_path / "Traduction.yaml"),
                    verbose=namespace.verbose)

    morphosyntax = report(id_report="morphosyntax",
                          morphosyntax=preprocess(grammar_path / "MorphoSyntax.yaml"),
                          verbose=namespace.verbose)

    lexemes = report(id_report="lexemes",
                     data=preprocess(grammar_path / "Stems.yaml"),
                     accumulator="", att_vals=att_vals,
                     verbose=namespace.verbose)

    phonology = report(id_report="phonology",
                       data=preprocess(grammar_path / "Phonology.yaml"),
                       verbose=namespace.verbose)

    paradigm = report(id_report="paradigm",
                      gloses=gloses,
                      blocks=preprocess(grammar_path / "Blocks.yaml"),
                      att_vals=att_vals,
                      voyelles=phonology.voyelles,
                      verbose=namespace.verbose)

    francais2kalaba, _ = report(id_report="rules",
                                morphosyntax=morphosyntax,
                                verbose=namespace.verbose)

    nt_rules = "\n".join(francais2kalaba)

    # lexical_rules = unary("fcfg", lexemes, paradigm, phonology)

    lexicon = trad_lexrule(term=lexemes, paradigm=paradigm, phonology=phonology)

    if namespace.print_lexicon:
        data_frame = build_df(term=lexemes,
                              paradigm=paradigm,
                              att_vals=att_vals,
                              phonology=phonology)
        print(tabulate(data_frame[data_frame.columns[~data_frame.columns.isin(["unary"])]], headers="keys"))
    # df = build_df(
    #     term=lexemes,
    #     paradigm=paradigm,
    #     att_vals=att_vals,
    #     phonology=phonology
    # )
    # df.to_csv("/tmp/lexicon.csv", sep="\t", index=False, na_rep="")
    #
    # lexicon = {}
    # for i_word, i_rule in df[["traduction", "unary"]].values:
    #     if i_word not in lexicon:
    #         lexicon[i_word] = [i_rule]
    #         continue
    #     lexicon[i_word].append(i_rule)

    if namespace.words:
        print("", namespace.words, *validate_sentence(
            sentence=split(namespace.words),
            rules=nt_rules,
            lexicon=lexicon,
            morpho=morphosyntax,
            start_nt=namespace.start_nt or morphosyntax.start
        ), sep="\n")
        return

    if namespace.sentences:
        # parser = parse.FeatureEarleyChartParser(grammar_)
        sents = validate_tree(
            sentences=[re.split(r"(?<=\w')| ", sent) for sent in
                       namespace.sentences.read_text(encoding="utf8").splitlines()],
            rules=nt_rules,
            lexicon=lexicon,
            morpho=morphosyntax,
            start_nt=namespace.start_nt or morphosyntax.start
        )
        total = i = 0
        for val, sent in sents:
            total += 1
            if val:
                i += 1
                print("=", sent, sep="\t")
            else:
                print("-", sent, sep="\t")
        print()
        print(f"{i} phrases valides")
        print(f"{total - i} phrases invalides")
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
    morphosyntax = read_morphosyntax(preprocess(namespace.morphosyntax))
    sentences = cleave([sent.split(" ")
                        for sent in namespace.sentences.read_text(encoding="utf8").splitlines()],
                       morphosyntax)

    df = pd.read_csv(namespace.lexicon, compression="zip", na_values="")
    print(df.columns)
    for i_sentence in sentences:
        print(i_sentence)
        for word in i_sentence:
            print(tabulate.tabulate(df[df["traduction"] == word].fillna("").drop_duplicates()))
