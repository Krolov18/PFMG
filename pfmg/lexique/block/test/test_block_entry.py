# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. 
import pytest
from collections.abc import Generator
from frozendict import frozendict

from pfmg.lexique.block.BlockEntry import BlockEntry
from pfmg.lexique.phonology.Phonology import Phonology
from pfmg.lexique.morpheme.Suffix import Suffix


@pytest.fixture(scope="module")
def fx_phonology() -> Generator[Phonology, None, None]:
    yield phonology()


def phonology():
    return Phonology(
        apophonies=frozendict(
            Ø="i", i="a", a="u",
            u="u", e="o", o="o"
        ),
        mutations=frozendict(
            p="p", t="p", k="t", b="p", d="b",
            g="d", m="m", n="m", N="n", f="f",
            s="f", S="s", v="f", z="v", Z="z",
            r="w", l="r", j="w", w="w"
        ),
        derives=frozendict(A="V", D="C"),
        consonnes=frozenset("ptkbdgmnNfsSvzZrljw"),
        voyelles=frozenset("iueoa")
    )


@pytest.mark.parametrize(
    "blocks, expected", [
        ({"N": [{"CF=N1,Nombre=Sg": "X+v"}]},
         {"N": [[Suffix(
             rule="X+v",
             sigma=frozendict(CF="N1", Nombre="Sg"),
             phonology=phonology()
         )]]})
    ]
)
def test_from_dict(fx_phonology, blocks, expected) -> None:
    actual = BlockEntry.from_dict(blocks, fx_phonology)
    assert isinstance(actual, BlockEntry)
    assert actual.data == expected


def test___call__() -> None:
    blocks = BlockEntry(
        data={"N": [[Suffix(
            rule="X+v",
            sigma=frozendict(Genre="m", Nombre="sg"),
            phonology=phonology()
        )]]}
    )
    actual = blocks(pos="N", sigma=frozendict())
    expected = []
    assert actual == expected

    actual = blocks(pos="N", sigma=frozendict(Genre="f", Nombre="sg"))
    expected = []
    assert actual == expected

    actual = blocks(pos="N", sigma=frozendict(Genre="m", Nombre="sg"))
    expected = [Suffix(
        rule="X+v",
        sigma=frozendict(Genre="m", Nombre="sg"),
        phonology=phonology()
    )]
    assert actual == expected

    actual = blocks(
        pos="N",
        sigma=frozendict(Genre="m", Nombre="sg", Cas="erg")
    )
    expected = [Suffix(
        rule="X+v",
        sigma=frozendict(Genre="m", Nombre="sg"),
        phonology=phonology()
    )]
    assert actual == expected


def test_raise_errors():
    with pytest.raises(AssertionError):
        _ = BlockEntry(data={})

    with pytest.raises(AssertionError):
        _ = BlockEntry(data={"N": []})

    with pytest.raises(AssertionError):
        _ = BlockEntry(data={"N": [[], [{"qqch"}]]})  # type: ignore

    with pytest.raises(KeyError):
        _ = BlockEntry(
            data={"N": [[Suffix(
                rule="X+v",
                sigma=frozendict(Genre="m", Nombre="sg"),
                phonology=phonology()
            )]]}
        )(pos="NOUN", sigma=frozendict())
        
    with pytest.raises(KeyError):
        _ = BlockEntry(
            data={"N": [[Suffix(
                rule="X+v",
                sigma=frozendict(Genre="m", Nombre="sg"),
                phonology=phonology()
            )]]}
        )(pos="NOUN", sigma=frozendict(Genre="m", Nombre="sg"))
        
    with pytest.raises(ValueError):
        _ = BlockEntry.from_dict(data={"N": []}, phonology=phonology())

    with pytest.raises(ValueError):
        _ = BlockEntry.from_dict(data={"N": [{}]}, phonology=phonology())


# @pytest.mark.parametrize(
#     "blocks, phonology, expected", [
#         ({"N": []},
#          dict(
#              apophonies=frozendict(Ø="i", i="a", a="u",
#                                    u="u", e="o", o="o"),
#              mutations=frozendict(
#                  p="p", t="p", k="t", b="p", d="b",
#                  g="d", m="m", n="m", N="n", f="f",
#                  s="f", S="s", v="f", z="v", Z="z",
#                  r="w", l="r", j="w", w="w"
#              ),
#              derives=frozendict(A="V", D="C"),
#              consonnes=frozenset("ptkbdgmnNfsSvzZrljw"),
#              voyelles=frozenset("iueoa")
#          ),
#          {}),
# 
#         ({"N": [{}]},
#          dict(
#              apophonies=frozendict(Ø="i", i="a", a="u",
#                                    u="u", e="o", o="o"),
#              mutations=frozendict(
#                  p="p", t="p", k="t", b="p", d="b",
#                  g="d", m="m", n="m", N="n", f="f",
#                  s="f", S="s", v="f", z="v", Z="z",
#                  r="w", l="r", j="w", w="w"
#              ),
#              derives=frozendict(A="V", D="C"),
#              consonnes=frozenset("ptkbdgmnNfsSvzZrljw"),
#              voyelles=frozenset("iueoa")
#          ),
#          {}),
#     ]
# )
# def test_from_disk_errors(
#     tmp_path,
#     blocks,
#     phonology,
#     expected
# ) -> None:
#     blocks_path = tmp_path / "Blocks.yaml"
#     with open(blocks_path, mode="w", encoding="utf8") as file_handler:
#         yaml.dump(blocks, file_handler)
# 
#     phono_path = tmp_path / "Phonology.yaml"
#     with open(phono_path, mode="w", encoding="utf8") as file_handler:
#         yaml.dump(phonology, file_handler)
# 
#     with pytest.raises(ValueError):
#         _ = BlockEntry.from_disk(blocks_path)
# 
# 
# @pytest.mark.parametrize(
#     "blocks, pos, sigma, expected", [
# 
#         # Aucun morpheme trouvé : le sigma est totalement différent.
#         ({"N": [{"Genre=m,Nombre=pl": "X+s"}]},
#          "N", frozendict(Genre="f"), []),
# 
#         # Aucun morphème trouvé : le sigma n'inclut pas celui 
#         # d'un des sigmas des morphèmes de Blocks.N
#         ({"N": [{"Genre=m,Nombre=pl": "X+s"}]},
#          "N", frozendict(Genre="m"), []),
# 
#         # Un morphème trouvé : le sigma correspond exactement 
#         # à l'un des sigmas des morphèmes de Blocks.N.
#         ({"N": [{"Genre=m,Nombre=pl": "X+s"}]},
#          "N", frozendict(Genre="m", Nombre="pl"),
#          [create_morpheme(
#              rule="X+s",
#              sigma=frozendict(Genre="m", Nombre="pl", Cas="erg"),
#              phonology=fx_phonology()
#          )]),
# 
#         # Un morphème trouvé : le sigma inclut un des morphèmes de Blocks.N.
#         ({"N": [{"Genre=m,Nombre=pl": "X+s"}]},
#          "N",
#          frozendict(Genre="m", Nombre="pl", Cas="erg"),
#          [create_morpheme(
#              rule="X+s",
#              sigma=frozendict(Genre="m", Nombre="pl", Cas="erg"),
#              phonology=fx_phonology()
#          )]),
# 
#     ]
# )
# def test_select_morphemes(tmp_path, blocks, pos, sigma, expected) -> None:
#     blocks_path = tmp_path / "Blocks.yaml"
#     with open(blocks_path, mode="w", encoding="utf8") as file_handler:
#         yaml.dump(blocks, file_handler)
# 
#     phono_path = tmp_path / "Phonology.yaml"
#     with open(phono_path, mode="w", encoding="utf8") as file_handler:
#         yaml.dump(fx_phonology().__dict__, file_handler)
# 
#     _blocks = BlockEntry.from_dict(blocks_path)
#     actual = _blocks(pos=pos, sigma=sigma)
#     assert actual == expected
# 
# 
# def test_select_morphemes_errors(tmp_path) -> None:
#     blocks_path = tmp_path / "Blocks.yaml"
#     with open(blocks_path, mode="w", encoding="utf8") as file_handler:
#         yaml.dump({}, file_handler)
# 
#     phono_path = tmp_path / "Phonology.yaml"
#     with open(phono_path, mode="w", encoding="utf8") as file_handler:
#         yaml.dump(fx_phonology().__dict__, file_handler)
# 
#     _blocks = BlockEntry.from_disk(blocks_path)
#     with pytest.raises(KeyError):
#         # POS n'est pas dans blocks
#         _ = _blocks(
#             pos="N",
#             sigma=frozendict(Genre="m", Nombre="pl")
#         )
# 
#     with pytest.raises(KeyError):
#         # POS est dans blocks, mais sigma n'est pas dans blocks[POS]
#         _ = _blocks(
#             pos="N",
#             sigma=frozendict(Genre="m", Nombre="pl")
#         )
# 
#     with pytest.raises(KeyError):
#         # POS est dans blocks, mais sigma n'est pas dans blocks[POS]
#         _ = _blocks(
#             pos="N",
#             sigma=frozendict(Genre="m", Nombre="pl", Cas="erg")
#         )
