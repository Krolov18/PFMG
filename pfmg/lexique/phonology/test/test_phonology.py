# Copyright (c) <year>, <copyright holder>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. 
import yaml
from frozendict import frozendict

from pfmg.lexique.phonology.Phonology import Phonology


def fx_phonology() -> Phonology:
    return Phonology(
        apophonies=frozendict(Ø="i", i="a", a="u", u="u", e="o", o="o"),
        mutations=frozendict(p="p", t="p", k="t", b="p", d="b",
                             g="d", m="m", n="m", N="n", f="f",
                             s="f", S="s", v="f", z="v", Z="z",
                             r="w", l="r", j="w", w="w"),
        derives=frozendict(A="V", D="C"),
        consonnes=frozenset("ptkbdgmnNfsSvzZrljw"),
        voyelles=frozenset("iueoa"),
    )


def test_phonology_from_disk(tmp_path) -> None:
    phono_path = tmp_path / "Phonology.yaml"
    with open(phono_path, mode="w", encoding="utf8") as file_handler:
        yaml.safe_dump(fx_phonology().to_json(), file_handler)

    actual = Phonology.from_disk(phono_path)
    assert actual == fx_phonology()
