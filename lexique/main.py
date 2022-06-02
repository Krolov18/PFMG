import argparse
import pathlib
import sys

from lexique.actions import action

# L'objet de cette ligne est d'effacer le traceback, quand une erreur survient.
# Le message d'erreur doit suffir à l'utilisateur.
sys.tracebacklimit = 0


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(
        prog="main.py",
        description="""
Commands:
    validate        Valide les éléments de la grammaire.
    generate        Génère les phrases licites reconnues par la grammaire.
""",
        usage="\n   %(prog)s <commands> [options]",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # remplir l'option 'dest' permet d'avoir un champ supplémentaire
    # quand le Namespace est généré soit 'name'
    # Ce champ sera utilisé pour lier une commande à une action
    SUB_PARSERS = PARSER.add_subparsers(dest="name")

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
    VALIDATE.add_argument("-v", "--verbose", action='count', default=0)

    args = PARSER.parse_args()

    # print("\n", args, "\n")

    # l'action est automatiquement liée à args.name qui correspond au nom de la commande
    action(id_action=args.name,
           namespace=args)
