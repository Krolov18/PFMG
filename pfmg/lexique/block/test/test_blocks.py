# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import pytest

from frozendict import frozendict

from pfmg.lexique.block.Blocks import Blocks
from pfmg.lexique.morpheme.Suffix import Suffix


@pytest.mark.parametrize("blocks", [[{"CF=N1,Nombre=Sg": "X+v"}]])
def test_from_dict(fx_df_phonology, blocks) -> None:
    expected = [[Suffix(rule="X+v", sigma=frozendict(CF="N1", Nombre="Sg"),
                        phonology=fx_df_phonology)]]
    actual = Blocks.from_list(blocks, fx_df_phonology)
    assert isinstance(actual, Blocks)
    assert actual.data == expected


def test___call__(fx_df_phonology) -> None:
    blocks = Blocks(
        data=[[Suffix(rule="X+v", sigma=frozendict(Genre="m", Nombre="sg"),
                      phonology=fx_df_phonology)]])

    actual = blocks(sigma=frozendict(Genre="f", Nombre="sg"))
    expected = []
    assert actual == expected

    actual = blocks(sigma=frozendict(Genre="m", Nombre="sg"))
    expected = [Suffix(
        rule="X+v",
        sigma=frozendict(Genre="m", Nombre="sg"),
        phonology=fx_df_phonology
    )]
    assert actual == expected

    actual = blocks(sigma=frozendict(Genre="m", Nombre="sg", Cas="erg"))
    expected = [Suffix(
        rule="X+v",
        sigma=frozendict(Genre="m", Nombre="sg"),
        phonology=fx_df_phonology
    )]
    assert actual == expected


def test_raise_errors(fx_df_phonology):
    with pytest.raises(AssertionError):
        _ = Blocks(data=[])

    with pytest.raises(AssertionError):
        _ = Blocks(data=[[]])

    with pytest.raises(AssertionError):
        _ = Blocks(data=[[], [{"qqch"}]])  # type: ignore

    with pytest.raises(AssertionError):
        _ = Blocks(
            data=[[Suffix(
                rule="X+v",
                sigma=frozendict(Genre="m", Nombre="sg"),
                phonology=fx_df_phonology
            )]]
        )(sigma=frozendict())
        
    with pytest.raises(AssertionError):
        _ = Blocks.from_list(data=[], phonology=fx_df_phonology)

    with pytest.raises(AssertionError):
        _ = Blocks.from_list(data=[{}], phonology=fx_df_phonology)


# @pytest.mark.parametrize(
#     "blocks, expected", [
#         ({"N": []}, {}),
#
#         ({"N": [{}]}, {}),
#     ]
# )
# def test_from_disk_errors(
#     fx_df_phonology,
#     tmp_path,
#     blocks,
#     expected
# ) -> None:
#     blocks_path = tmp_path / "Blocks.yaml"
#     with open(blocks_path, mode="w", encoding="utf8") as file_handler:
#         yaml.safe_dump(blocks, file_handler)
#
#     phono_path = tmp_path / "Phonology.yaml"
#     with open(phono_path, mode="w", encoding="utf8") as file_handler:
#         yaml.safe_dump(fx_df_phonology, file_handler)
#
#     with pytest.raises(ValueError):
#         _ = BlockEntry.from_yaml(blocks_path)
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
# def test_select_morphemes(fx_df_phonology, tmp_path, blocks, pos, sigma, expected) -> None:
#     blocks_path = tmp_path / "Blocks.yaml"
#     with open(blocks_path, mode="w", encoding="utf8") as file_handler:
#         yaml.dump(blocks, file_handler)
#
#     phono_path = tmp_path / "Phonology.yaml"
#     with open(phono_path, mode="w", encoding="utf8") as file_handler:
#         yaml.dump(fx_df_phonology.to_dict(), file_handler)
#
#     _blocks = BlockEntry.from_yaml(blocks_path)
#     actual = _blocks(pos=pos, sigma=sigma)
#     assert actual == expected
#
#
# def test_select_morphemes_errors(fx_df_phonology, tmp_path) -> None:
#     blocks_path = tmp_path / "Blocks.yaml"
#     with open(blocks_path, mode="w", encoding="utf8") as file_handler:
#         yaml.dump({}, file_handler)
#
#     phono_path = tmp_path / "Phonology.yaml"
#     with open(phono_path, mode="w", encoding="utf8") as file_handler:
#         yaml.dump(fx_df_phonology.to_dict(), file_handler)
#
#     _blocks = BlockEntry.from_yaml(blocks_path)
#     with pytest.raises(KeyError):
#         # POS n'est pas dans blocks
#         _ = _blocks(
#             pos="N",
#             sigma=Sigma(
#                 source=frozendict(Genre="m", Nombre="pl"),
#                 destination=frozendict(Genre="m", Nombre="pl")
#             )
#         )
#
#     with pytest.raises(KeyError):
#         # POS est dans blocks, mais sigma n'est pas dans blocks[POS]
#         _ = _blocks(
#             pos="N",
#             sigma=Sigma(
#                 source=frozendict(Genre="m", Nombre="pl"),
#                 destination=frozendict(Genre="m", Nombre="pl")
#             )
#         )
#
#     with pytest.raises(KeyError):
#         # POS est dans blocks, mais sigma n'est pas dans blocks[POS]
#         _ = _blocks(
#             pos="N",
#             sigma=Sigma(
#                 source=frozendict(Genre="m", Nombre="pl"),
#                 destination=frozendict(Genre="m", Nombre="pl")
#             )
#         )
