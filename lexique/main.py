import argparse
import pathlib

from lexique.actions import action

if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()

    # remplir l'option 'dest' permet d'avoir un champ supplémentaire
    # quand le Namespace est généré soit 'name'
    # Ce champ sera utilisé pour lier une commande à une action
    SUB_PARSERS = PARSER.add_subparsers(dest="name")

    STARTPROJECT = SUB_PARSERS.add_parser(
        name="startproject",
        description="Initialise un projet Kalaba"
    )
    STARTPROJECT.add_argument("-p", "--project-path", type=pathlib.Path)
    STARTPROJECT.add_argument("-n", "--project-name", type=str)

    VALIDATE = SUB_PARSERS.add_parser(
        name="validate",
        description="\n  Vérifie les arguments de la grammaire."
        )
    VALIDATE_GROUP = VALIDATE.add_mutually_exclusive_group()
    VALIDATE.add_argument("datapath", type=pathlib.Path)
    VALIDATE.add_argument("-S", "--start-nt", type=str)
    VALIDATE.add_argument("-l", "--print-lexicon", action="store_true")
    VALIDATE_GROUP.add_argument("-w", "--words", type=str)
    VALIDATE_GROUP.add_argument("-s", "--sentences", type=pathlib.Path)
    VALIDATE.add_argument("-v", "--verbose", action='count', default=1)

    LEXICON = SUB_PARSERS.add_parser(name="lexicon")
    LEXICON.add_argument("datapath", type=pathlib.Path)
    LEXICON.add_argument("-e", "--exclude", nargs="*", type=str)

    # args = PARSER.parse_args(["lexicon", "/home/korantin/Documents/Kalaba/lexique/test/data_for_test/avec_traduction"])
    args = PARSER.parse_args()

    print("\n", args, "\n")

    action(id_action=args.name, namespace=args)
