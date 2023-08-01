import pytest
import yaml
from frozendict import frozendict

from lexique.lexical_structures.Blocks import Blocks
from lexique.lexical_structures.Factoy import create_morpheme
from lexique.lexical_structures.Phonology import Phonology
from lexique.lexical_structures.Suffix import Suffix


def fx_phonology() -> Phonology:
    return Phonology(apophonies=frozendict(Ø="i", i="a", a="u", u="u", e="o", o="o"),
                     mutations=frozendict(p="p", t="p", k="t", b="p", d="b",
                                          g="d", m="m", n="m", N="n", f="f",
                                          s="f", S="s", v="f", z="v", Z="z",
                                          r="w", l="r", j="w", w="w"),
                     derives=frozendict(A="V", D="C"),
                     consonnes=frozenset("ptkbdgmnNfsSvzZrljw"),
                     voyelles=frozenset("iueoa"))


@pytest.mark.parametrize("blocks, phonology, expected", [

    ({},
     dict(apophonies=frozendict(Ø="i", i="a", a="u", u="u", e="o", o="o"),
          mutations=frozendict(p="p", t="p", k="t", b="p", d="b",
                               g="d", m="m", n="m", N="n", f="f",
                               s="f", S="s", v="f", z="v", Z="z",
                               r="w", l="r", j="w", w="w"),
          derives=frozendict(A="V", D="C"),
          consonnes=frozenset("ptkbdgmnNfsSvzZrljw"),
          voyelles=frozenset("iueoa")),
     {}),

    ({"N": [{"Genre=m,Nombre=pl": "X+s"}]},
     dict(apophonies=frozendict(Ø="i", i="a", a="u", u="u", e="o", o="o"),
          mutations=frozendict(p="p", t="p", k="t", b="p", d="b",
                               g="d", m="m", n="m", N="n", f="f",
                               s="f", S="s", v="f", z="v", Z="z",
                               r="w", l="r", j="w", w="w"),
          derives=frozendict(A="V", D="C"),
          consonnes=frozenset("ptkbdgmnNfsSvzZrljw"),
          voyelles=frozenset("iueoa")),
     {"N": [[Suffix(rule="X+s",
                    sigma=frozendict(Genre="m", Nombre="pl"),
                    phonology=fx_phonology())]]}),

])
def test_from_disk(tmp_path, blocks, phonology, expected) -> None:
    blocks_path = tmp_path / "Blocks.yaml"
    with open(blocks_path, mode="w", encoding="utf8") as file_handler:
        yaml.dump(blocks, file_handler)

    phono_path = tmp_path / "Phonology.yaml"
    with open(phono_path, mode="w", encoding="utf8") as file_handler:
        yaml.dump(phonology, file_handler)

    actual = Blocks.from_disk(blocks_path)
    assert actual.data == expected


@pytest.mark.parametrize("blocks, phonology, expected", [
    ({"N": []},
     dict(apophonies=frozendict(Ø="i", i="a", a="u", u="u", e="o", o="o"),
          mutations=frozendict(p="p", t="p", k="t", b="p", d="b",
                               g="d", m="m", n="m", N="n", f="f",
                               s="f", S="s", v="f", z="v", Z="z",
                               r="w", l="r", j="w", w="w"),
          derives=frozendict(A="V", D="C"),
          consonnes=frozenset("ptkbdgmnNfsSvzZrljw"),
          voyelles=frozenset("iueoa")),
     {}),

    ({"N": [{}]},
     dict(apophonies=frozendict(Ø="i", i="a", a="u", u="u", e="o", o="o"),
          mutations=frozendict(p="p", t="p", k="t", b="p", d="b",
                               g="d", m="m", n="m", N="n", f="f",
                               s="f", S="s", v="f", z="v", Z="z",
                               r="w", l="r", j="w", w="w"),
          derives=frozendict(A="V", D="C"),
          consonnes=frozenset("ptkbdgmnNfsSvzZrljw"),
          voyelles=frozenset("iueoa")),
     {}),
])
def test_from_disk_errors(tmp_path, blocks, phonology, expected) -> None:
    blocks_path = tmp_path / "Blocks.yaml"
    with open(blocks_path, mode="w", encoding="utf8") as file_handler:
        yaml.dump(blocks, file_handler)

    phono_path = tmp_path / "Phonology.yaml"
    with open(phono_path, mode="w", encoding="utf8") as file_handler:
        yaml.dump(phonology, file_handler)

    with pytest.raises(ValueError):
        _ = Blocks.from_disk(blocks_path)


@pytest.mark.parametrize("blocks, pos, sigma, expected", [

    # Aucun morpheme trouvé : le sigma est totalement différent.
    ({"N": [{"Genre=m,Nombre=pl": "X+s"}]},
     "N", frozendict(Genre="f"), []),

    # Aucun morphème trouvé : le sigma n'inclut pas celui d'un des sigmas des morphèmes de Blocks.N
    ({"N": [{"Genre=m,Nombre=pl": "X+s"}]},
     "N", frozendict(Genre="m"), []),

    # Un morphème trouvé : le sigma correspond exactement à l'un des sigmas des morphèmes de Blocks.N.
    ({"N": [{"Genre=m,Nombre=pl": "X+s"}]},
     "N", frozendict(Genre="m", Nombre="pl"),
     [create_morpheme(rule="X+s", sigma=frozendict(Genre="m", Nombre="pl", Cas="erg"), phonology=fx_phonology())]),

    # Un morphème trouvé : le sigma inclut un des morphèmes de Blocks.N.
    ({"N": [{"Genre=m,Nombre=pl": "X+s"}]},
     "N",
     frozendict(Genre="m", Nombre="pl", Cas="erg"),
     [create_morpheme(rule="X+s", sigma=frozendict(Genre="m", Nombre="pl", Cas="erg"), phonology=fx_phonology())]),

])
def test_select_morphemes(tmp_path, blocks, pos, sigma, expected) -> None:
    blocks_path = tmp_path / "Blocks.yaml"
    with open(blocks_path, mode="w", encoding="utf8") as file_handler:
        yaml.dump(blocks, file_handler)

    phono_path = tmp_path / "Phonology.yaml"
    with open(phono_path, mode="w", encoding="utf8") as file_handler:
        yaml.dump(fx_phonology().__dict__, file_handler)

    _blocks = Blocks.from_disk(blocks_path)
    actual = _blocks.select_morphemes(pos=pos, sigma=sigma)
    assert actual == expected


def test_select_morphemes_errors(tmp_path) -> None:
    blocks_path = tmp_path / "Blocks.yaml"
    with open(blocks_path, mode="w", encoding="utf8") as file_handler:
        yaml.dump({}, file_handler)

    phono_path = tmp_path / "Phonology.yaml"
    with open(phono_path, mode="w", encoding="utf8") as file_handler:
        yaml.dump(fx_phonology().__dict__, file_handler)

    _blocks = Blocks.from_disk(blocks_path)
    with pytest.raises(KeyError):
        # POS n'est pas dans blocks
        _ = _blocks.select_morphemes(pos="N", sigma=frozendict(Genre="m", Nombre="pl"))

    with pytest.raises(KeyError):
        # POS est dans blocks, mais sigma n'est pas dans blocks[POS]
        _ = _blocks.select_morphemes(pos="N", sigma=frozendict(Genre="m", Nombre="pl"))

    with pytest.raises(KeyError):
        # POS est dans blocks, mais sigma n'est pas dans blocks[POS]
        _ = _blocks.select_morphemes(pos="N", sigma=frozendict(Genre="m", Nombre="pl", Cas="erg"))
