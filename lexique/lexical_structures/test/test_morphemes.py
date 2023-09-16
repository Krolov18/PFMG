from frozendict import frozendict

from lexique.lexical_structures.Factory import create_morpheme
from lexique.lexical_structures.Morphemes import Morphemes
from lexique.lexical_structures.Phonology import Phonology


def test_morpheme() -> None:
    phonology = Phonology(apophonies=frozendict(Ø="i", i="a", a="u", u="u", e="o", o="o"),
                          mutations=frozendict(p="p", t="p", k="t", b="p", d="b",
                                               g="d", m="m", n="m", N="n", f="f",
                                               s="f", S="s", v="f", z="v", Z="z",
                                               r="w", l="r", j="w", w="w"),
                          derives=frozendict(A="V", D="C"),
                          consonnes=frozenset("ptkbdgmnNfsSvzZrljw"),
                          voyelles=frozenset("iueoa"))
    morpheme = Morphemes(radical="radical",
                         others=[
                             create_morpheme(
                                 rule="a+X",
                                 sigma=frozendict({"Genre": "m"}),
                                 phonology=phonology),
                             create_morpheme(
                                 rule="b+X",
                                 sigma=frozendict({"Nombre": "s"}),
                                 phonology=phonology)])
    assert morpheme.radical == "radical"
    assert morpheme.others == [create_morpheme(rule="a+X",
                                               sigma=frozendict({"Genre": "m"}),
                                               phonology=phonology),
                               create_morpheme(rule="b+X",
                                               sigma=frozendict({"Nombre": "s"}),
                                               phonology=phonology)]
