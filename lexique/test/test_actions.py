# pylint: disable=missing-function-docstring,missing-module-docstring
import re
from os.path import dirname
from pathlib import Path
from argparse import Namespace
import jsonschema

import pytest

from lexique.actions import validate_action, lexicon_action
from lexique.errors import Errors


@pytest.mark.parametrize("data_path, message", [
    # f"{dirname(__file__)}/data_for_test/blocks/translation/[E005]_categorie_vide",
    # f"{dirname(__file__)}/data_for_test/blocks/translation/[E005]_bloc_vide",
    # f"{dirname(__file__)}/data_for_test/blocks/translation/[E006]_attribut_inconnu",
    # f"{dirname(__file__)}/data_for_test/blocks/translation/[E007]_valeur_inconnue",
    # f"{dirname(__file__)}/data_for_test/blocks/translation/[E008]_rule/circumfix",
    # f"{dirname(__file__)}/data_for_test/blocks/translation/[E008]_rule/ternary",
    # f"{dirname(__file__)}/data_for_test/blocks/translation/[E008]_rule/gabarit",
    # f"{dirname(__file__)}/data_for_test/blocks/translation/[E008]_rule/prefix",
    # f"{dirname(__file__)}/data_for_test/blocks/translation/[E008]_rule/suffix",
    (f"{dirname(__file__)}/data_for_test/gloses/vide/", "None is not of type 'object'"),
    (f"{dirname(__file__)}/data_for_test/gloses/bloc_source_manquant/", "'source' is a required property"),
    (f"{dirname(__file__)}/data_for_test/gloses/bloc_destination_manquant/", "'destination' is a required property"),
    (f"{dirname(__file__)}/data_for_test/gloses/blocs_source_et_destination_vides", "{} does not have enough properties"),
    (f"{dirname(__file__)}/data_for_test/gloses/bloc_source_vide", "{} does not have enough properties"),
    (f"{dirname(__file__)}/data_for_test/gloses/bloc_destination_vide", "{} does not have enough properties"),
    (f"{dirname(__file__)}/data_for_test/gloses/categorie_vide", "{} does not have enough properties"),
])
def test_validate_action_scenarii_with_errors(data_path, message) -> None:
    namespace = Namespace(name="validate",
                          datapath=Path(data_path),
                          sentences=None, words=None, start_nt=None, verbose=0)
    with pytest.raises(jsonschema.exceptions.ValidationError, match=message):
        validate_action(namespace)


@pytest.mark.parametrize("data_path", [
    f"{dirname(__file__)}/data_for_test/avec_traduction"
])
def test_validate_action_valid_scenarii(data_path) -> None:
    namespace = Namespace(name="lexicon",
                          datapath=Path(data_path),
                          exclude=None)
    lexicon_action(namespace)
