from argparse import Namespace

import pytest

from lexique_2.actions import action
from lexique_2.paths import get_data_test_grammar


@pytest.mark.parametrize("namespace", [
    Namespace(name="lexicon",
              datapath=get_data_test_grammar()),
])
def test_actions(namespace):
    action(namespace=namespace)
