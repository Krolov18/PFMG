# pylint: disable=missing-module-docstring,line-too-long,missing-function-docstring
from pathlib import Path

import pytest
import yaml
from nltk import FeatStruct, Variable, Production
from nltk.featstruct import FeatureValueTuple
from nltk.grammar import FeatStructNonterminal

import lexique_2.lexical_structures.Syntax as syn


@pytest.mark.parametrize("term", [
    "",
    "PP{",
    "PP}",
    "PP{}",  # Dans une regex classique, c'est valide, mais ne mène à rien. Permissif !
    "PP/{}",
    "PP/{,}",
    "PP/{2,}",  # Équivalent en regex : 2 ou plus. L'infini est permissif !
])
def test_syntax_assertions(term) -> None:
    with pytest.raises(AssertionError):
        _ = syn.repeat(term)


@pytest.mark.parametrize("term", [
    "PP/*",  # Équivalent en regex 0 ou plus. L'infini est permissif.
    "PP/+",  # Équivalent en regex 1 ou plus. L'infini est permissif.
])
def test_syntax_raising(term) -> None:
    with pytest.raises(NotImplementedError):
        _ = syn.repeat(term)


@pytest.mark.parametrize("term, expected", [
    ("VER", [["VER"]]),
    ("PP/?", [[""], ["PP"]]),
    ("PP/{,0}", [[""]]),
    ("PP/{,1}", [[""], ["PP"]]),
    ("PP/{,2}", [[""], ["PP"], ["PP", "PP"]]),
    ("PP/{0,2}", [[""], ["PP"], ["PP", "PP"]]),
    ("PP/{1,2}", [["PP"], ["PP", "PP"]]),
    ("PP/{2,2}", [["PP", "PP"]]),
    ("PP/{0, 2}", [[""], ["PP"], ["PP", "PP"]]),
    ("PP/{0 ,2}", [[""], ["PP"], ["PP", "PP"]]),
    ("PP/{0 , 2}", [[""], ["PP"], ["PP", "PP"]]),
    ("PP/{, 2}", [[""], ["PP"], ["PP", "PP"]]),
    ("PP/{0,1}", [[""], ["PP"]]),
    ("PP/{0 ,1}", [[""], ["PP"]]),
    ("PP/{0, 1}", [[""], ["PP"]]),
    ("PP/{0 , 1}", [[""], ["PP"]]),
    ("PP/{ 0,1 }", [[""], ["PP"]]),
])
def test_syntax(term, expected):
    actual = syn.repeat(term)
    assert actual == expected


@pytest.mark.parametrize("term, expected", [
    (["PP/{,2}", "NP", "PP/{,2}", "VER"],
     [["", "NP", "", "VER"],  # 0 0
      ["", "NP", "PP", "VER"],  # 0 1
      ["", "NP", "PP", "PP", "VER"],  # 0 2
      ["PP", "NP", "", "VER"],  # 1 0
      ["PP", "NP", "PP", "VER"],  # 1 1
      ["PP", "NP", "PP", "PP", "VER"],  # 1 2
      ["PP", "PP", "NP", "", "VER"],  # 2 0
      ["PP", "PP", "NP", "PP", "VER"],  # 2 1
      ["PP", "PP", "NP", "PP", "PP", "VER"]]),  # 2 2

])
def test_develop(term, expected) -> None:
    actual = list(syn.develop(term))
    assert actual == expected




parametrize = pytest.mark.parametrize("accords, accumulator, expected", [
    ("",
     [],
     []),

    (";",
     [FeatStruct(), FeatStruct()],
     [FeatStruct(), FeatStruct()]),

    (";;",
     [FeatStruct(), FeatStruct(), FeatStruct()],
     [FeatStruct(), FeatStruct(), FeatStruct()]),

    (";;;",
     [FeatStruct(), FeatStruct(), FeatStruct(), FeatStruct()],
     [FeatStruct(), FeatStruct(), FeatStruct(), FeatStruct()]),

    ("Genre",
     [FeatStruct(Source=FeatStruct())],
     [FeatStruct(Source=FeatStruct(SGenre=Variable("SGenre")))]),

    ("Genre",
     [FeatStruct(Destination=FeatStruct())],
     [FeatStruct(Destination=FeatStruct(DGenre=Variable("DGenre")))]),

    ("Genre=m",
     [FeatStruct(Source=FeatStruct())],
     [FeatStruct(Source=FeatStruct(SGenre="m"))]),

    ("Genre=m",
     [FeatStruct(Destination=FeatStruct())],
     [FeatStruct(Destination=FeatStruct(DGenre="m"))]),

    ("Genre=m;",
     [FeatStruct(Source=FeatStruct()), FeatStruct(Source=FeatStruct())],
     [FeatStruct(Source=FeatStruct(SGenre="m")), FeatStruct(Source=FeatStruct())]),

    ("Genre=m;",
     [FeatStruct(Destination=FeatStruct()), FeatStruct(Destination=FeatStruct())],
     [FeatStruct(Destination=FeatStruct(DGenre="m")), FeatStruct(Destination=FeatStruct())]),

    ("Genre=m;;",
     [FeatStruct(Source=FeatStruct()), FeatStruct(Source=FeatStruct()), FeatStruct(Source=FeatStruct())],
     [FeatStruct(Source=FeatStruct(SGenre="m")), FeatStruct(Source=FeatStruct()), FeatStruct(Source=FeatStruct())]),

    ("Genre=m;;",
     [FeatStruct(Destination=FeatStruct()), FeatStruct(Destination=FeatStruct()), FeatStruct(Destination=FeatStruct())],
     [FeatStruct(Destination=FeatStruct(DGenre="m")), FeatStruct(Destination=FeatStruct()),
      FeatStruct(Destination=FeatStruct())]),

    ("Genre=m;;Cas=Nom",
     [FeatStruct(Source=FeatStruct()), FeatStruct(Source=FeatStruct()), FeatStruct(Source=FeatStruct())],
     [FeatStruct(Source=FeatStruct(SGenre="m")), FeatStruct(Source=FeatStruct()),
      FeatStruct(Source=FeatStruct(SCas="Nom"))]),

    ("Genre=m;;Cas=Nom",
     [FeatStruct(Destination=FeatStruct()), FeatStruct(Destination=FeatStruct()), FeatStruct(Destination=FeatStruct())],
     [FeatStruct(Destination=FeatStruct(DGenre="m")), FeatStruct(Destination=FeatStruct()),
      FeatStruct(Destination=FeatStruct(DCas="Nom"))]),

    ("Genre,Nombre;Genre,Nombre;Genre,Nombre",
     [FeatStruct(Source=FeatStruct()),
      FeatStruct(Source=FeatStruct()),
      FeatStruct(Source=FeatStruct())],
     [FeatStruct(Source=FeatStruct(SGenre=Variable("SGenre"), SNombre=Variable("SNombre"))),
      FeatStruct(Source=FeatStruct(SGenre=Variable("SGenre"), SNombre=Variable("SNombre"))),
      FeatStruct(Source=FeatStruct(SGenre=Variable("SGenre"), SNombre=Variable("SNombre")))]),

    ("Genre,Nombre;Genre,Nombre;Genre,Nombre",
     [FeatStruct(Destination=FeatStruct()),
      FeatStruct(Destination=FeatStruct()),
      FeatStruct(Destination=FeatStruct())],
     [FeatStruct(Destination=FeatStruct(DGenre=Variable("DGenre"), DNombre=Variable("DNombre"))),
      FeatStruct(Destination=FeatStruct(DGenre=Variable("DGenre"), DNombre=Variable("DNombre"))),
      FeatStruct(Destination=FeatStruct(DGenre=Variable("DGenre"), DNombre=Variable("DNombre")))]),

])


@parametrize
def test_parse_features(accords, accumulator, expected):
    syn.parse_features(accords, accumulator)
    assert accumulator == expected


parametrize = pytest.mark.parametrize("accords, accumulator, error", [
    ("Genre=m", [FeatStruct(), FeatStruct()], TypeError),
    ("Genre", [FeatStruct(), FeatStruct()], TypeError),
    ("Genre;", [], IndexError),
    ("Genre=", [FeatStruct()], TypeError),
    ("=m", [FeatStruct()], TypeError),
    ("=", [FeatStruct()], TypeError),
])


@parametrize
def test_parse_features_erreurs(accords, accumulator, error):
    with pytest.raises(error):
        syn.parse_features(accords, accumulator)


parametrize = pytest.mark.parametrize("percolation, accords, accumulator, expected", [
    ("",
     [FeatStruct(Source=FeatStruct(SGenre="m")), FeatStruct(Source=FeatStruct()),
      FeatStruct(Source=FeatStruct(SCas="Nom"))],
     FeatStruct(Source=FeatStruct()),
     FeatStruct(Source=FeatStruct())),

    ("",
     [FeatStruct(Destination=FeatStruct(DGenre="m")), FeatStruct(Destination=FeatStruct()),
      FeatStruct(Destination=FeatStruct(DCas="Nom"))],
     FeatStruct(Destination=FeatStruct()),
     FeatStruct(Destination=FeatStruct())),

    (";",
     [FeatStruct(Source=FeatStruct(SGenre="m")), FeatStruct(Source=FeatStruct(SCas="Nom"))],
     FeatStruct(Source=FeatStruct()),
     FeatStruct(Source=FeatStruct())),

    (";",
     [FeatStruct(Destination=FeatStruct(SGenre="m")), FeatStruct(Destination=FeatStruct(SCas="Nom"))],
     FeatStruct(Destination=FeatStruct()),
     FeatStruct(Destination=FeatStruct())),

    (";;",
     [FeatStruct(Source=FeatStruct(SGenre="m")), FeatStruct(), FeatStruct(Source=FeatStruct(SCas="Nom"))],
     FeatStruct(Source=FeatStruct()),
     FeatStruct(Source=FeatStruct())),

    (";;",
     [FeatStruct(Destination=FeatStruct(DGenre="m")), FeatStruct(), FeatStruct(Destination=FeatStruct(DCas="Nom"))],
     FeatStruct(Destination=FeatStruct()),
     FeatStruct(Destination=FeatStruct())),

    (";;;",
     [FeatStruct(Source=FeatStruct(SGenre="m")), FeatStruct(Source=FeatStruct()),
      FeatStruct(Source=FeatStruct(SCas="Nom")), FeatStruct(Source=FeatStruct())],
     FeatStruct(Source=FeatStruct()),
     FeatStruct(Source=FeatStruct())),

    (";;;",
     [FeatStruct(Destination=FeatStruct(DGenre="m")), FeatStruct(Destination=FeatStruct()),
      FeatStruct(Destination=FeatStruct(DCas="Nom")), FeatStruct(Destination=FeatStruct())],
     FeatStruct(Destination=FeatStruct()),
     FeatStruct(Destination=FeatStruct())),

    ("Genre",
     [FeatStruct(Source=FeatStruct(SGenre=Variable("SGenre")))],
     FeatStruct(Source=FeatStruct()),
     FeatStruct(Source=FeatStruct(SGenre=Variable("SGenre")))),

    ("Genre",
     [FeatStruct(Destination=FeatStruct(DGenre=Variable("DGenre")))],
     FeatStruct(Destination=FeatStruct()),
     FeatStruct(Destination=FeatStruct(DGenre=Variable("DGenre")))),

    ("Genre=m",
     [FeatStruct(Source=FeatStruct(SGenre="m"))],
     FeatStruct(Source=FeatStruct()),
     FeatStruct(Source=FeatStruct(SGenre="m"))),

    ("Genre=m",
     [FeatStruct(Destination=FeatStruct(DGenre="m"))],
     FeatStruct(Destination=FeatStruct()),
     FeatStruct(Destination=FeatStruct(DGenre="m"))),

    ("Genre=m;",
     [FeatStruct(Source=FeatStruct(SGenre="m")), FeatStruct(Source=FeatStruct())],
     FeatStruct(Source=FeatStruct()),
     FeatStruct(Source=FeatStruct(SGenre="m"))),

    ("Genre=m;",
     [FeatStruct(Destination=FeatStruct(DGenre="m")), FeatStruct(Destination=FeatStruct())],
     FeatStruct(Destination=FeatStruct()),
     FeatStruct(Destination=FeatStruct(DGenre="m"))),

    ("Genre=m;;",
     [FeatStruct(Source=FeatStruct(SGenre="m")), FeatStruct(Source=FeatStruct()), FeatStruct(Source=FeatStruct())],
     FeatStruct(Source=FeatStruct()),
     FeatStruct(Source=FeatStruct(SGenre="m"))),

    ("Genre=m;;",
     [FeatStruct(Destination=FeatStruct(DGenre="m")), FeatStruct(Destination=FeatStruct()),
      FeatStruct(Destination=FeatStruct())],
     FeatStruct(Destination=FeatStruct()),
     FeatStruct(Destination=FeatStruct(DGenre="m"))),

    ("Genre=m;;Cas=Nom",
     [FeatStruct(Source=FeatStruct(SGenre="m")), FeatStruct(Source=FeatStruct()),
      FeatStruct(Source=FeatStruct(SCas="Nom"))],
     FeatStruct(Source=FeatStruct()),
     FeatStruct(Source=FeatStruct(SGenre="m", SCas="Nom"))),

    ("Genre=m;;Cas=Nom",
     [FeatStruct(Destination=FeatStruct(DGenre="m")), FeatStruct(Destination=FeatStruct()),
      FeatStruct(Destination=FeatStruct(DCas="Nom"))],
     FeatStruct(Destination=FeatStruct()),
     FeatStruct(Destination=FeatStruct(DGenre="m", DCas="Nom"))),

    ("Genre,Nombre",
     [FeatStruct(Source=FeatStruct(SGenre=Variable("SGenre"), SNombre=Variable("SNombre")))],
     FeatStruct(Source=FeatStruct()),
     FeatStruct(Source=FeatStruct(SGenre=Variable("SGenre"), SNombre=Variable("SNombre")))),

    ("Genre,Nombre",
     [FeatStruct(Destination=FeatStruct(DGenre=Variable("DGenre"), DNombre=Variable("DNombre")))],
     FeatStruct(Destination=FeatStruct()),
     FeatStruct(Destination=FeatStruct(DGenre=Variable("DGenre"), DNombre=Variable("DNombre")))),

    ("Genre,Nombre;Genre,Nombre",
     [FeatStruct(Source=FeatStruct(SGenre=Variable("SGenre"), SNombre=Variable("SNombre"))),
      FeatStruct(Source=FeatStruct(SGenre=Variable("SGenre"), SNombre=Variable("SNombre")))],
     FeatStruct(Source=FeatStruct()),
     FeatStruct(Source=FeatStruct(SGenre=Variable("SGenre"), SNombre=Variable("SNombre")))),

    ("Genre,Nombre;Genre,Nombre",
     [FeatStruct(Destination=FeatStruct(DGenre=Variable("DGenre"), DNombre=Variable("DNombre"))),
      FeatStruct(Destination=FeatStruct(DGenre=Variable("DGenre"), DNombre=Variable("DNombre")))],
     FeatStruct(Destination=FeatStruct()),
     FeatStruct(Destination=FeatStruct(DGenre=Variable("DGenre"), DNombre=Variable("DNombre")))),

])


@parametrize
def test_parse_percolation(percolation, accords, accumulator, expected):
    syn.parse_percolation(percolation, accords, accumulator)
    assert accumulator == expected


parametrize = pytest.mark.parametrize("percolation, accords, accumulator, error", [
    ("Genre=m", [FeatStruct(Source=FeatStruct()), FeatStruct(Source=FeatStruct())], FeatStruct(Source=FeatStruct()),
     TypeError),
    ("Genre=m", [FeatStruct(Destination=FeatStruct()), FeatStruct(Destination=FeatStruct())],
     FeatStruct(Destination=FeatStruct()), TypeError),
    ("Genre", [FeatStruct(Source=FeatStruct()), FeatStruct(Source=FeatStruct())], FeatStruct(Source=FeatStruct()),
     TypeError),
    ("Genre", [FeatStruct(Destination=FeatStruct()), FeatStruct(Destination=FeatStruct())],
     FeatStruct(Destination=FeatStruct()), TypeError),
    ("Genre;", [], FeatStruct(Source=FeatStruct()), IndexError),
    ("Genre;", [], FeatStruct(Destination=FeatStruct()), IndexError),
    ("Genre=", [FeatStruct(Source=FeatStruct())], FeatStruct(Source=FeatStruct()), TypeError),
    ("Genre=", [FeatStruct(Destination=FeatStruct())], FeatStruct(Destination=FeatStruct()), TypeError),
    ("=m", [FeatStruct(Source=FeatStruct())], FeatStruct(Source=FeatStruct()), TypeError),
    ("=m", [FeatStruct(Destination=FeatStruct())], FeatStruct(Destination=FeatStruct()), TypeError),
    ("=", [FeatStruct(Source=FeatStruct())], FeatStruct(Source=FeatStruct()), TypeError),
    ("=", [FeatStruct(Destination=FeatStruct())], FeatStruct(Destination=FeatStruct()), TypeError),
    ("Genre=m", [FeatStruct(Source=FeatStruct(SGenre="f"))], FeatStruct(Source=FeatStruct(SGenre="f")), TypeError),
    ("Genre=m", [FeatStruct(Destination=FeatStruct(DGenre="f"))], FeatStruct(Destination=FeatStruct(DGenre="f")),
     TypeError)
])


@parametrize
def test_parse_percolation_erreurs(percolation, accords, accumulator, error):
    with pytest.raises(error):
        syn.parse_percolation(percolation, accords, accumulator)


parametrize = pytest.mark.parametrize("accords, len_rhs, expected", [
    ("", 0, ""),
    ("", 1, ""),
    ("", 2, ""),
    (";", 0, ";"),
    (";", 1, ";"),
    (";", 2, ";"),
    (";;", 0, ";;"),
    (";;", 1, ";;"),
    (";;", 2, ";;"),
    ("Genre", 0, "Genre"),
    ("Genre", 1, "Genre"),
    ("Genre", 2, "Genre;Genre"),
    ("Genre", 3, "Genre;Genre;Genre"),
])


@parametrize
def test_broadcast(accords, len_rhs, expected) -> None:
    actual = syn.broadcast(accords=accords, len_rhs=len_rhs)
    assert actual == expected


parametrize = pytest.mark.parametrize("syntagme, traduction, f_accords, f_percolation, expected", [

    (["D", "N"],
     [0, 1],
     [FeatStruct(Source=FeatStruct(Genre=Variable("Genre"))), FeatStruct(Source=FeatStruct(Genre=Variable("Genre")))],
     FeatStruct(Source=FeatStruct(Genre=Variable("Genre"))),
     ([FeatStruct(Source=FeatStruct(Genre=Variable("Genre"), Traduction=Variable("0"))),
       FeatStruct(Source=FeatStruct(Genre=Variable("Genre"), Traduction=Variable("1")))],
      FeatStruct(
          Source=FeatStruct(Genre=Variable("Genre"), Traduction=FeatureValueTuple([Variable("0"), Variable("1")]))))),

    (["D", "N"],
     [1, 0],
     [FeatStruct(Source=FeatStruct(Genre=Variable("Genre"))),
      FeatStruct(Source=FeatStruct(Genre=Variable("Genre")))],
     FeatStruct(Source=FeatStruct(Genre=Variable("Genre"))),
     ([FeatStruct(Source=FeatStruct(Genre=Variable("Genre"), Traduction=Variable("0"))),
       FeatStruct(Source=FeatStruct(Genre=Variable("Genre"), Traduction=Variable("1")))],
      FeatStruct(
          Source=FeatStruct(Genre=Variable("Genre"), Traduction=FeatureValueTuple([Variable("1"), Variable("0")]))))),

    (["D", "N"],
     [0, 1, 0],
     [FeatStruct(Source=FeatStruct(Genre=Variable("Genre"))),
      FeatStruct(Source=FeatStruct(Genre=Variable("Genre")))],
     FeatStruct(Source=FeatStruct(Genre=Variable("Genre"))),
     ([FeatStruct(Source=FeatStruct(Genre=Variable("Genre"), Traduction=Variable("0"))),
       FeatStruct(Source=FeatStruct(Genre=Variable("Genre"), Traduction=Variable("1")))],
      FeatStruct(Source=FeatStruct(Genre=Variable("Genre"),
                                   Traduction=FeatureValueTuple([Variable("0"), Variable("1"), Variable("0")]))))),

    (["D", "N"],
     [1],
     [FeatStruct(Source=FeatStruct(Genre=Variable("Genre"))),
      FeatStruct(Source=FeatStruct(Genre=Variable("Genre")))],
     FeatStruct(Source=FeatStruct(Genre=Variable("Genre"))),
     ([FeatStruct(Source=FeatStruct(Genre=Variable("Genre"), Traduction=Variable("0"))),
       FeatStruct(Source=FeatStruct(Genre=Variable("Genre"), Traduction=Variable("1")))],
      FeatStruct(Source=FeatStruct(Genre=Variable("Genre"), Traduction=FeatureValueTuple([Variable("1")]))))),
])


@parametrize
def test_parse_traduction(syntagme, traduction, f_accords, f_percolation, expected) -> None:
    syn.parse_traduction(syntagme=syntagme, traduction=traduction, f_accords=f_accords, f_percolation=f_percolation)
    assert f_accords == expected[0]
    assert f_percolation == expected[1]


parametrize = pytest.mark.parametrize("lhs, syntagme, accords, percolation, traduction, expected", [
    ("NP", ["D", "N"], "Genre,Nombre", "Genre,Nombre", None,
     Production(
         lhs=FeatStructNonterminal("NP",
                                   Destination=FeatStruct(DGenre=Variable("DGenre"),
                                                          DNombre=Variable("DNombre"))),
         rhs=[FeatStructNonterminal("D",
                                    Destination=FeatStruct(DGenre=Variable("DGenre"),
                                                           DNombre=Variable("DNombre"))),
              FeatStructNonterminal("N",
                                    Destination=FeatStruct(DGenre=Variable("DGenre"),
                                                           DNombre=Variable("DNombre")))])),

    ("NP", ["D", "N"], "Genre,Nombre", "Genre,Nombre", [0],
     Production(lhs=FeatStructNonterminal("NP",
                                          Source=FeatStruct(SGenre=Variable("SGenre"),
                                                            SNombre=Variable("SNombre"),
                                                            Traduction=FeatureValueTuple([Variable("0")]))),
                rhs=[FeatStructNonterminal("D",
                                           Source=FeatStruct(SGenre=Variable("SGenre"),
                                                             SNombre=Variable("SNombre"),
                                                             Traduction=Variable("0"))),
                     FeatStructNonterminal("N",
                                           Source=FeatStruct(SGenre=Variable("SGenre"),
                                                             SNombre=Variable("SNombre"),
                                                             Traduction=Variable("1")))])),

    ("NP", ["D", "N"], "Genre,Nombre", "Genre,Nombre", [0, 1],
     Production(lhs=FeatStructNonterminal("NP",
                                          Source=FeatStruct(SGenre=Variable("SGenre"),
                                                            SNombre=Variable("SNombre"),
                                                            Traduction=FeatureValueTuple([Variable("0"),
                                                                                          Variable("1")]))),
                rhs=[FeatStructNonterminal("D",
                                           Source=FeatStruct(SGenre=Variable("SGenre"),
                                                             SNombre=Variable("SNombre"),
                                                             Traduction=Variable("0"))),
                     FeatStructNonterminal("N",
                                           Source=FeatStruct(SGenre=Variable("SGenre"),
                                                             SNombre=Variable("SNombre"),
                                                             Traduction=Variable("1")))])),

    ("NP", ["D", "N"], "Genre,Nombre", "Genre,Nombre", [1],
     Production(lhs=FeatStructNonterminal("NP",
                                          Source=FeatStruct(SGenre=Variable("SGenre"),
                                                            SNombre=Variable("SNombre"),
                                                            Traduction=FeatureValueTuple([Variable("1")]))),
                rhs=[FeatStructNonterminal("D",
                                           Source=FeatStruct(SGenre=Variable("SGenre"),
                                                             SNombre=Variable("SNombre"),
                                                             Traduction=Variable("0"))),
                     FeatStructNonterminal("N",
                                           Source=FeatStruct(SGenre=Variable("SGenre"),
                                                             SNombre=Variable("SNombre"),
                                                             Traduction=Variable("1")))])),

    ("NP", ["D", "N"], "Genre,Nombre", "Genre,Nombre", [1, 0],
     Production(lhs=FeatStructNonterminal("NP",
                                          Source=FeatStruct(SGenre=Variable("SGenre"),
                                                            SNombre=Variable("SNombre"),
                                                            Traduction=FeatureValueTuple([Variable("1"),
                                                                                          Variable("0")]))),
                rhs=[FeatStructNonterminal("D",
                                           Source=FeatStruct(SGenre=Variable("SGenre"),
                                                             SNombre=Variable("SNombre"),
                                                             Traduction=Variable("0"))),
                     FeatStructNonterminal("N",
                                           Source=FeatStruct(SGenre=Variable("SGenre"),
                                                             SNombre=Variable("SNombre"),
                                                             Traduction=Variable("1")))])),
])


@parametrize
def test_parse_one_rule(lhs, syntagme, accords, percolation, traduction, expected) -> None:
    actual = syn.parse_one_rule(lhs, syntagme, accords, percolation, traduction)
    assert actual == expected


parametrize = pytest.mark.parametrize("p1, p2, expected", [

    (Production(lhs=FeatStructNonterminal("NP",
                                          Source=FeatStruct(SGenre=Variable("SGenre"),
                                                            SNombre=Variable("SNombre"),
                                                            Traduction=FeatureValueTuple([Variable("0"),
                                                                                          Variable("1")]))),
                rhs=[FeatStructNonterminal("D",
                                           Source=FeatStruct(SGenre=Variable("SGenre"),
                                                             SNombre=Variable("SNombre"),
                                                             Traduction=Variable("0"))),
                     FeatStructNonterminal("N",
                                           Source=FeatStruct(SGenre=Variable("SGenre"),
                                                             SNombre=Variable("SNombre"),
                                                             Traduction=Variable("1")))]),
     Production(lhs=FeatStructNonterminal("NP",
                                          Destination=FeatStruct(DGenre=Variable("DGenre"),
                                                                 DNombre=Variable("DNombre"))),
                rhs=[FeatStructNonterminal("D",
                                           Destination=FeatStruct(DGenre=Variable("DGenre"),
                                                                  DNombre=Variable("DNombre"))),
                     FeatStructNonterminal("N",
                                           Destination=FeatStruct(DGenre=Variable("DGenre"),
                                                                  DNombre=Variable("DNombre")))]),
     Production(lhs=FeatStructNonterminal("NP",
                                          Source=FeatStruct(SGenre=Variable("SGenre"),
                                                            SNombre=Variable("SNombre"),
                                                            Traduction=FeatureValueTuple([Variable("0"),
                                                                                          Variable("1")])
                                                            ),
                                          Destination=FeatStruct(DGenre=Variable("DGenre"),
                                                                 DNombre=Variable("DNombre"))),
                rhs=[FeatStructNonterminal("D",
                                           Source=FeatStruct(SGenre=Variable("SGenre"),
                                                             SNombre=Variable("SNombre"),
                                                             Traduction=Variable("0")),
                                           Destination=FeatStruct(DGenre=Variable("DGenre"),
                                                                  DNombre=Variable("DNombre"))),
                     FeatStructNonterminal("N",
                                           Source=FeatStruct(SGenre=Variable("SGenre"),
                                                             SNombre=Variable("SNombre"),
                                                             Traduction=Variable("1")),
                                           Destination=FeatStruct(DGenre=Variable("DGenre"),
                                                                  DNombre=Variable("DNombre")))])),

    (Production(lhs=FeatStructNonterminal("NP",
                                          Source=FeatStruct(SGenre=Variable("SGenre"),
                                                            SNombre=Variable("SNombre"),
                                                            Traduction=FeatureValueTuple([Variable("1"),
                                                                                          Variable("0")]))),
                rhs=[FeatStructNonterminal("D",
                                           Source=FeatStruct(SGenre=Variable("SGenre"),
                                                             SNombre=Variable("SNombre"),
                                                             Traduction=Variable("0"))),
                     FeatStructNonterminal("N",
                                           Source=FeatStruct(SGenre=Variable("SGenre"),
                                                             SNombre=Variable("SNombre"),
                                                             Traduction=Variable("1")))]),
     Production(lhs=FeatStructNonterminal("NP",
                                          Destination=FeatStruct(DGenre=Variable("DGenre"),
                                                                 DNombre=Variable("DNombre"))),
                rhs=[FeatStructNonterminal("N",
                                           Destination=FeatStruct(DGenre=Variable("DGenre"),
                                                                  DNombre=Variable("DNombre"))),
                     FeatStructNonterminal("D",
                                           Destination=FeatStruct(DGenre=Variable("DGenre"),
                                                                  DNombre=Variable("DNombre")))]),
     Production(lhs=FeatStructNonterminal("NP",
                                          Source=FeatStruct(SGenre=Variable("SGenre"),
                                                            SNombre=Variable("SNombre"),
                                                            Traduction=FeatureValueTuple([Variable("1"),
                                                                                          Variable("0")])),
                                          Destination=FeatStruct(DGenre=Variable("DGenre"),
                                                                 DNombre=Variable("DNombre"))),
                rhs=[FeatStructNonterminal("D",
                                           Source=FeatStruct(SGenre=Variable("SGenre"),
                                                             SNombre=Variable("SNombre"),
                                                             Traduction=Variable("0")),
                                           Destination=FeatStruct(DGenre=Variable("DGenre"),
                                                                  DNombre=Variable("DNombre"))),
                     FeatStructNonterminal("N",
                                           Source=FeatStruct(SGenre=Variable("SGenre"),
                                                             SNombre=Variable("SNombre"),
                                                             Traduction=Variable("1")),
                                           Destination=FeatStruct(DGenre=Variable("DGenre"),
                                                                  DNombre=Variable("DNombre")))]))

])


@parametrize
def test_concatenate_rule_features(p1, p2, expected) -> None:
    actual = syn.concatenate_rule_features(p1, p2)
    assert actual == expected


# @pytest.mark.skip(reason="en cours de construction")
def test_parse_config() -> None:
    yaml_filename = Path(__file__).parent / "data_for_test" / "MorphoSyntax.yaml"
    with open(yaml_filename) as fh:
        config = yaml.safe_load(fh)
    result = syn.parse_config(config)
    assert False
