# pylint: disable=missing-function-docstring,missing-module-docstring
import re
from pathlib import Path
from argparse import Namespace

import pytest

from lexique.actions import validate_action
from lexique.errors import Errors


@pytest.mark.parametrize("data_path,message", [
    ("data_for_test/blocks/translation/[E002]_vide", Errors.E002),
    ("data_for_test/blocks/translation/[E003]_bloc_kalaba_manquant", Errors.E003),
    ("data_for_test/blocks/translation/[E003]_bloc_translation_manquant", Errors.E003),
    ("data_for_test/blocks/translation/[E004]_blocs_vides", Errors.E004),
    ("data_for_test/blocks/translation/[E004]_kalaba_vide", Errors.E004),
    ("data_for_test/blocks/translation/[E004]_translation_vide", Errors.E004),
    ("data_for_test/blocks/translation/[E005]_categorie_vide", Errors.E005),
    ("data_for_test/blocks/translation/[E005]_bloc_vide", Errors.E005),
    ("data_for_test/blocks/translation/[E006]_attribut_inconnu", Errors.E006.format(attribute="þInconnu",
                                                                                    attributes=["Genre", "pos",
                                                                                                "þGenre"])),
    ("data_for_test/blocks/translation/[E007]_valeur_inconnue", Errors.E007.format(value="þInconnu",
                                                                                   values=["DET", "F",
                                                                                           "M", "N",
                                                                                           "þF", "þM"])),
    ("data_for_test/blocks/translation/[E008]_rule/circumfix", Errors.E008.format(rule="a+X1a")),
    ("data_for_test/blocks/translation/[E008]_rule/ternary", Errors.E008.format(rule="X2X2:X1")),
    ("data_for_test/blocks/translation/[E008]_rule/gabarit", Errors.E008.format(rule="4U2AX9u3u")),
    ("data_for_test/blocks/translation/[E008]_rule/prefix", Errors.E008.format(rule="eX")),
    ("data_for_test/blocks/translation/[E008]_rule/suffix", Errors.E008.format(rule="Xe")),

])
def test_validate_action_scenarii_with_errors(data_path, message) -> None:
    namespace = Namespace(name="validate",
                          datapath=Path(data_path),
                          sentences=None, words=None, start_nt=None, verbose=0)
    with pytest.raises(ValueError, match=re.escape(message)):
        validate_action(namespace)


@pytest.mark.parametrize("data_path", [
    "data_for_test/avec_traduction"
])
def test_validate_action_valid_scenarii(data_path) -> None:
    namespace = Namespace(name="validate",
                          datapath=Path(data_path),
                          sentences=None,
                          words="les chasseurs mange un coyote",
                          start_nt=None,
                          print_lexicon=False,
                          verbose=0)
    validate_action(namespace)
