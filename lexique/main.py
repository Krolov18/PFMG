import argparse
import pathlib

from lexique.actions import action

if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()

    SUB_PARSERS = PARSER.add_subparsers(dest="name")

    LEXICON = SUB_PARSERS.add_parser(name="lexicon")
    # un argument pour le chemin des fichiers de config d'une grammaire (Phonology, Stems, Blocks et Gloses)
    LEXICON.add_argument("datapath", type=pathlib.Path)

    args = PARSER.parse_args([
        "lexicon", "/home/korantin/projects/PycharmProjects/PFMG/lexique/test/data_for_test/grammar"
    ])

    action(namespace=args)
