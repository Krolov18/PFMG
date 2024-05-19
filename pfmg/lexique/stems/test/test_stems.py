# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import pytest
import yaml
from frozendict import frozendict
from pfmg.lexique.lexeme.Lexeme import Lexeme
from pfmg.lexique.lexeme.LexemeEntry import LexemeEntry
from pfmg.lexique.stems.Stems import Stems
from pfmg.lexique.stem_space.StemSpace import StemSpace

parametrize = pytest.mark.parametrize(
    "stems, expected", [
        (
            {
                "N": {
                    "pSit": "toto,tutu.Genre=m",
                },
                "A": {
                    "Cas=erg": {
                        "ksit": "kiki,koko",
                    }
                },
            },
            [
                Lexeme(
                    source=LexemeEntry(
                        stems=StemSpace(stems=("kiki", "koko")),
                        pos="A",
                        sigma=frozendict({}),
                    ),
                    destination=LexemeEntry(
                        stems=StemSpace(stems=("ksit",)),
                        pos="A",
                        sigma=frozendict(
                            {
                                "Cas": "erg"
                            }
                        ),
                    ),
                ),
                Lexeme(
                    source=LexemeEntry(
                        stems=StemSpace(stems=("toto", "tutu")),
                        pos="N",
                        sigma=frozendict(Genre="m"),
                    ),
                    destination=LexemeEntry(
                        stems=StemSpace(stems=("pSit",)),
                        pos="N",
                        sigma=frozendict(),
                    ),
                )
            ]
        ),

        (
            {
                "N": {
                    "Genre=f": {
                        "pSit":      "toto,tutu.Genre=m",
                        "pMat":      "karu,karo.Genre=m",
                        "Nombre=pl": {
                            "polk": "nunu"
                        }
                    },
                    "Genre=m": {
                        "pSif": "toto,tutu.Genre=f",
                    }
                },
            },
            [
                Lexeme(
                    source=LexemeEntry(
                        stems=StemSpace(stems=('nunu',)),
                        pos='N',
                        sigma=frozendict({})
                    ),
                    destination=LexemeEntry(
                        stems=StemSpace(stems=('polk',)),
                        pos='N',
                        sigma=frozendict(
                            {
                                'Genre':  'f',
                                'Nombre': 'pl'
                            }
                        )
                    )
                ),
                Lexeme(
                    source=LexemeEntry(
                        stems=StemSpace(stems=('karu', 'karo')),
                        pos='N',
                        sigma=frozendict(
                            {
                                'Genre': 'm'
                            }
                        )
                    ),
                    destination=LexemeEntry(
                        stems=StemSpace(stems=('pMat',)),
                        pos='N',
                        sigma=frozendict(
                            {
                                'Genre': 'f'
                            }
                        )
                    )
                ),
                Lexeme(
                    source=LexemeEntry(
                        stems=StemSpace(stems=('toto', 'tutu')),
                        pos='N',
                        sigma=frozendict(
                            {
                                'Genre': 'm'
                            }
                        )
                    ),
                    destination=LexemeEntry(
                        stems=StemSpace(stems=('pSit',)),
                        pos='N',
                        sigma=frozendict(
                            {
                                'Genre': 'f'
                            }
                        )
                    )
                ),
                Lexeme(
                    source=LexemeEntry(
                        stems=StemSpace(stems=('toto', 'tutu')),
                        pos='N',
                        sigma=frozendict(
                            {
                                'Genre': 'f'
                            }
                        )
                    ),
                    destination=LexemeEntry(
                        stems=StemSpace(stems=('pSif',)),
                        pos='N',
                        sigma=frozendict(
                            {
                                'Genre': 'm'
                            }
                        )
                    )
                )
                ,
            ]
        ),
    ],
)


@parametrize
def test_from_disk(tmp_path, stems, expected):
    stems_path = tmp_path / "Stems.yaml"
    with open(stems_path, mode="w", encoding="utf8") as file_handler:
        yaml.dump(stems, file_handler)

    actual = list(Stems.from_yaml(stems_path))
    assert actual == expected
