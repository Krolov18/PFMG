import pytest

from lexique.glose_reader import (gridify,
                                  cuefy,
                                  cuefy2,
                                  read_glose,
                                  cuefy_block,
                                  cuefy_blocks,
                                  read_stems, choose_rule)


@pytest.mark.parametrize("gloses, expected", [

    pytest.param({}, None, marks=pytest.mark.xfail(raises=AssertionError)),

    pytest.param([], None, marks=pytest.mark.xfail(raises=AssertionError)),

    ({"Genre": ["m"]},
     [[("Genre", "m")]]),

    ({"Genre": ["m"], "Nombre": ["sg"]},
     [[("Genre", "m"), ("Nombre", "sg")]]),

    ({"Genre": ["m", "f"], "Nombre": ["sg", "pl"]},
     [[("Genre", "m"), ("Nombre", "sg")],
      [("Genre", "m"), ("Nombre", "pl")],
      [("Genre", "f"), ("Nombre", "sg")],
      [("Genre", "f"), ("Nombre", "pl")]]),

    ([{"Genre": ["m"]}],
     [[("Genre", "m")]]),

    ([{"Genre": ["m"], "Nombre": ["sg"]}],
     [[("Genre", "m"), ("Nombre", "sg")]]),

    ([{"Genre": ["m"]}, {"Nombre": ["sg"]}],
     [[("Genre", "m")],
      [("Nombre", "sg")]]),

    ([{"Genre": ["m"], "Nombre": ["sg", "pl"]}],
     [[("Genre", "m"), ("Nombre", "sg")],
      [("Genre", "m"), ("Nombre", "pl")]]),

    ([{"Genre": ["m"], "Nombre": ["sg", "pl"]}, {"Mode": ["inf"]}],
     [[("Genre", "m"), ("Nombre", "sg")],
      [("Genre", "m"), ("Nombre", "pl")],
      [("Mode", "inf")]]),

    pytest.param({1, 2, 3, 4}, None, marks=pytest.mark.xfail(raises=TypeError))
])
def test_gridify(gloses, expected) -> None:
    actual = [*gridify(gloses)]
    assert actual == expected


@pytest.mark.parametrize("attribute, values, expected", [
    pytest.param("", [], None, marks=pytest.mark.xfail(raises=AssertionError)),
    pytest.param("A", [], None, marks=pytest.mark.xfail(raises=AssertionError)),
    pytest.param("", ["val"], None, marks=pytest.mark.xfail(raises=AssertionError)),
    pytest.param("A", [""], None, marks=pytest.mark.xfail(raises=AssertionError)),
    pytest.param("A", ["", "val"], None, marks=pytest.mark.xfail(raises=AssertionError)),

    ("Genre", ["m"],
     ['#Genre: "m"',
      '#GenreM: {#Genre, "m"}']),  # Cas d'alias... problème ?

    ("Genre", ["m", "f"],
     ['#Genre: =~"^[fm]$"',
      '#GenreM: {#Genre, "m"}',
      '#GenreF: {#Genre, "f"}']),

    ("Cas", ["erg", "nom", "abs"],
     ['#Cas: =~"^(?:abs|erg|nom)$"',
      '#CasErg: {#Cas, "erg"}',
      '#CasNom: {#Cas, "nom"}',
      '#CasAbs: {#Cas, "abs"}']),

    ("Cas", ["e", "ee", "eee", "eeee"],
     ['#Cas: =~"^e(?:e(?:ee?)?)?$"',
      '#CasE: {#Cas, "e"}',
      '#CasEe: {#Cas, "ee"}',
      '#CasEee: {#Cas, "eee"}',
      '#CasEeee: {#Cas, "eeee"}']),

])
def test_cuefy(attribute, values, expected) -> None:
    actual = cuefy(attribute, values)
    assert actual == expected


@pytest.mark.parametrize("attribute, values, expected", [
    pytest.param("", [], None, marks=pytest.mark.xfail(raises=AssertionError)),
    pytest.param("A", [], None, marks=pytest.mark.xfail(raises=AssertionError)),
    pytest.param("", ["val"], None, marks=pytest.mark.xfail(raises=AssertionError)),
    pytest.param("A", [""], None, marks=pytest.mark.xfail(raises=AssertionError)),
    pytest.param("A", ["", "val"], None, marks=pytest.mark.xfail(raises=AssertionError)),

    ("N", ["Nombre"], ['#SigmaN: {#Sigma, nombre: #Nombre}']),
    ("N", ["Genre", "Nombre"], ['#SigmaN: {#Sigma, genre: #Genre, nombre: #Nombre}'])
])
def test_cuefy2(attribute, values, expected) -> None:
    actual = cuefy2(attribute, values)
    assert actual == expected


@pytest.mark.parametrize("glose, expected", [
    pytest.param({}, None, marks=pytest.mark.xfail(raises=AssertionError)),

    ({"N": {"Genre": ["m"]}},
     ['#Category: =~"^N$"',
      '#Genre: "m"',
      '#GenreM: {#Genre, "m"}',
      '#SigmaN: {#Sigma, genre: #Genre}',
      '#FormeN: #Forme & {lexeme: #LexemeN, pos: "N", sigma: #SigmaN}',
      '#SigmaNM: #SigmaN & {Genre: #GenreM}',
      '#FormeNM: #FormeN & {sigma: #SigmaNM}']),

    ({"N": {"Genre": ["m", "f"]}},
     ['#Category: =~"^N$"',
      '#Genre: =~"^[fm]$"',
      '#GenreM: {#Genre, "m"}',
      '#GenreF: {#Genre, "f"}',
      '#SigmaN: {#Sigma, genre: #Genre}',
      '#FormeN: #Forme & {lexeme: #LexemeN, pos: "N", sigma: #SigmaN}',
      '#SigmaNM: #SigmaN & {Genre: #GenreM}',
      '#FormeNM: #FormeN & {sigma: #SigmaNM}',
      '#SigmaNF: #SigmaN & {Genre: #GenreF}',
      '#FormeNF: #FormeN & {sigma: #SigmaNF}']),

    ({"N": {"Genre": ["m", "f"],
            "Nombre": ["sg", "pl"]}},
     ['#Category: =~"^N$"',
      '#Genre: =~"^[fm]$"',
      '#GenreM: {#Genre, "m"}',
      '#GenreF: {#Genre, "f"}',
      '#Nombre: =~"^(?:pl|sg)$"',
      '#NombreSg: {#Nombre, "sg"}',
      '#NombrePl: {#Nombre, "pl"}',
      '#SigmaN: {#Sigma, genre: #Genre, nombre: #Nombre}',
      '#FormeN: #Forme & {lexeme: #LexemeN, pos: "N", sigma: #SigmaN}',
      '#SigmaNMSg: #SigmaN & {Genre: #GenreM, Nombre: #NombreSg}',
      '#FormeNMSg: #FormeN & {sigma: #SigmaNMSg}',
      '#SigmaNMPl: #SigmaN & {Genre: #GenreM, Nombre: #NombrePl}',
      '#FormeNMPl: #FormeN & {sigma: #SigmaNMPl}',
      '#SigmaNFSg: #SigmaN & {Genre: #GenreF, Nombre: #NombreSg}',
      '#FormeNFSg: #FormeN & {sigma: #SigmaNFSg}',
      '#SigmaNFPl: #SigmaN & {Genre: #GenreF, Nombre: #NombrePl}',
      '#FormeNFPl: #FormeN & {sigma: #SigmaNFPl}']),

    ({"N": {"Genre": ["m", "f"],
            "Nombre": ["sg", "pl"]},
      "ADJ": {"Genre": ["m", "f"]}},
     ['#Category: =~"^(?:ADJ|N)$"',
      '#Genre: =~"^[fm]$"',
      '#GenreM: {#Genre, "m"}',
      '#GenreF: {#Genre, "f"}',
      '#Nombre: =~"^(?:pl|sg)$"',
      '#NombreSg: {#Nombre, "sg"}',
      '#NombrePl: {#Nombre, "pl"}',
      '#SigmaN: {#Sigma, genre: #Genre, nombre: #Nombre}',
      '#FormeN: #Forme & {lexeme: #LexemeN, pos: "N", sigma: #SigmaN}',
      '#SigmaNMSg: #SigmaN & {Genre: #GenreM, Nombre: #NombreSg}',
      '#FormeNMSg: #FormeN & {sigma: #SigmaNMSg}',
      '#SigmaNMPl: #SigmaN & {Genre: #GenreM, Nombre: #NombrePl}',
      '#FormeNMPl: #FormeN & {sigma: #SigmaNMPl}',
      '#SigmaNFSg: #SigmaN & {Genre: #GenreF, Nombre: #NombreSg}',
      '#FormeNFSg: #FormeN & {sigma: #SigmaNFSg}',
      '#SigmaNFPl: #SigmaN & {Genre: #GenreF, Nombre: #NombrePl}',
      '#FormeNFPl: #FormeN & {sigma: #SigmaNFPl}',
      '#Genre: =~"^[fm]$"',
      '#GenreM: {#Genre, "m"}',
      '#GenreF: {#Genre, "f"}',
      '#SigmaADJ: {#Sigma, genre: #Genre}',
      '#FormeADJ: #Forme & {lexeme: #LexemeADJ, pos: "ADJ", sigma: #SigmaADJ}',
      '#SigmaADJM: #SigmaADJ & {Genre: #GenreM}',
      '#FormeADJM: #FormeADJ & {sigma: #SigmaADJM}',
      '#SigmaADJF: #SigmaADJ & {Genre: #GenreF}',
      '#FormeADJF: #FormeADJ & {sigma: #SigmaADJF}']),

    ({"N": [{"Mode": ["inf"]},
            {"Genre": ["m", "f"],
             "Nombre": ["sg", "pl"]}]},
     ['#Category: =~"^N$"',
      '#Mode: "inf"',
      '#ModeInf: {#Mode, "inf"}',
      '#Genre: =~"^[fm]$"',
      '#GenreM: {#Genre, "m"}',
      '#GenreF: {#Genre, "f"}',
      '#Nombre: =~"^(?:pl|sg)$"',
      '#NombreSg: {#Nombre, "sg"}',
      '#NombrePl: {#Nombre, "pl"}',
      '#SigmaN: {#Sigma, mode: #Mode, genre: #Genre, nombre: #Nombre}',
      '#FormeN: #Forme & {lexeme: #LexemeN, pos: "N", sigma: #SigmaN}',
      '#SigmaNInf: #SigmaN & {Mode: #ModeInf}',
      '#FormeNInf: #FormeN & {sigma: #SigmaNInf}',
      '#SigmaNMSg: #SigmaN & {Genre: #GenreM, Nombre: #NombreSg}',
      '#FormeNMSg: #FormeN & {sigma: #SigmaNMSg}',
      '#SigmaNMPl: #SigmaN & {Genre: #GenreM, Nombre: #NombrePl}',
      '#FormeNMPl: #FormeN & {sigma: #SigmaNMPl}',
      '#SigmaNFSg: #SigmaN & {Genre: #GenreF, Nombre: #NombreSg}',
      '#FormeNFSg: #FormeN & {sigma: #SigmaNFSg}',
      '#SigmaNFPl: #SigmaN & {Genre: #GenreF, Nombre: #NombrePl}',
      '#FormeNFPl: #FormeN & {sigma: #SigmaNFPl}'])
])
def test_read_glose(glose, expected) -> None:
    actual = read_glose(glose)
    assert actual == expected


@pytest.mark.parametrize("block, expected", [
    pytest.param({}, None, marks=pytest.mark.xfail(raises=AssertionError)),

    ({"Nombre=Sg": "X+s"}, "#Suffix & {sigma: {Nombre: \"Sg\"}, _sigma: {Nombre: \"Sg\"}, rule: \"X+s\"}"),
    ({"Nombre=Sg": "s+X"}, "#Prefix & {sigma: {Nombre: \"Sg\"}, _sigma: {Nombre: \"Sg\"}, rule: \"s+X\"}"),
    ({"Nombre=Sg": "s+X+s"}, "#Circumfix & {sigma: {Nombre: \"Sg\"}, _sigma: {Nombre: \"Sg\"}, rule: \"s+X+s\"}"),

    ({"Nombre=Sg,Genre=M": "X+s"},
     "#Suffix & {sigma: {Nombre: \"Sg\",Genre: \"M\"}, _sigma: {Nombre: \"Sg\",Genre: \"M\"}, rule: \"X+s\"}"),
    ({"Nombre=Sg,Genre=M": "s+X"},
     "#Prefix & {sigma: {Nombre: \"Sg\",Genre: \"M\"}, _sigma: {Nombre: \"Sg\",Genre: \"M\"}, rule: \"s+X\"}"),
    ({"Nombre=Sg,Genre=M": "s+X+s"},
     "#Circumfix & {sigma: {Nombre: \"Sg\",Genre: \"M\"}, _sigma: {Nombre: \"Sg\",Genre: \"M\"}, rule: \"s+X+s\"}"),

    ({"Nombre=Sg": "X+a", "Nombre=Du": "X+b", "Nombre=Pl": "X+c"},
     ("#Suffix & {sigma: {Nombre: \"Sg\"}, _sigma: {Nombre: \"Sg\"}, rule: \"X+a\"} | "
      "#Suffix & {sigma: {Nombre: \"Du\"}, _sigma: {Nombre: \"Du\"}, rule: \"X+b\"} | "
      "#Suffix & {sigma: {Nombre: \"Pl\"}, _sigma: {Nombre: \"Pl\"}, rule: \"X+c\"}")),
    ({"Nombre=Sg": "a+X", "Nombre=Du": "b+X", "Nombre=Pl": "c+X"},
     ("#Prefix & {sigma: {Nombre: \"Sg\"}, _sigma: {Nombre: \"Sg\"}, rule: \"a+X\"} | "
      "#Prefix & {sigma: {Nombre: \"Du\"}, _sigma: {Nombre: \"Du\"}, rule: \"b+X\"} | "
      "#Prefix & {sigma: {Nombre: \"Pl\"}, _sigma: {Nombre: \"Pl\"}, rule: \"c+X\"}")),
    ({"Nombre=Sg": "a+X+a", "Nombre=Du": "b+X+b", "Nombre=Pl": "c+X+c"},
     ("#Circumfix & {sigma: {Nombre: \"Sg\"}, _sigma: {Nombre: \"Sg\"}, rule: \"a+X+a\"} | "
      "#Circumfix & {sigma: {Nombre: \"Du\"}, _sigma: {Nombre: \"Du\"}, rule: \"b+X+b\"} | "
      "#Circumfix & {sigma: {Nombre: \"Pl\"}, _sigma: {Nombre: \"Pl\"}, rule: \"c+X+c\"}"))
])
def test_read_block(block, expected) -> None:
    actual = cuefy_block(block)
    assert actual == expected


@pytest.mark.parametrize("blocks, expected", [
    pytest.param({}, None, marks=pytest.mark.xfail(raises=AssertionError)),

    ({"NOM": [{"Nombre=Sg": "a+X+a", "Nombre=Du": "b+X+b", "Nombre=Pl": "c+X+c"}]},
     [(
             "#LexemeNOM: #Lexeme & {pos: \"NOM\", morphemes: [#Circumfix & {sigma: {Nombre: \"Sg\"}, _sigma: {Nombre: \"Sg\"}, rule: \"a+X+a\"} | "
             "#Circumfix & {sigma: {Nombre: \"Du\"}, _sigma: {Nombre: \"Du\"}, rule: \"b+X+b\"} | "
             "#Circumfix & {sigma: {Nombre: \"Pl\"}, _sigma: {Nombre: \"Pl\"}, rule: \"c+X+c\"}]}")]),

    ({"NOM": [{"Nombre=Sg": "a+X+a", "Nombre=Du": "b+X+b", "Nombre=Pl": "c+X+c"}],
      "VER": [{"Nombre=Sg": "a+X+a", "Nombre=Du": "b+X+b", "Nombre=Pl": "c+X+c"}]},
     [(
             "#LexemeNOM: #Lexeme & {pos: \"NOM\", morphemes: [#Circumfix & {sigma: {Nombre: \"Sg\"}, _sigma: {Nombre: \"Sg\"}, rule: \"a+X+a\"} | "
             "#Circumfix & {sigma: {Nombre: \"Du\"}, _sigma: {Nombre: \"Du\"}, rule: \"b+X+b\"} | "
             "#Circumfix & {sigma: {Nombre: \"Pl\"}, _sigma: {Nombre: \"Pl\"}, rule: \"c+X+c\"}]}"),
         (
                 "#LexemeVER: #Lexeme & {pos: \"VER\", morphemes: [#Circumfix & {sigma: {Nombre: \"Sg\"}, _sigma: {Nombre: \"Sg\"}, rule: \"a+X+a\"} | "
                 "#Circumfix & {sigma: {Nombre: \"Du\"}, _sigma: {Nombre: \"Du\"}, rule: \"b+X+b\"} | "
                 "#Circumfix & {sigma: {Nombre: \"Pl\"}, _sigma: {Nombre: \"Pl\"}, rule: \"c+X+c\"}]}")])

])
def test_read_blocks(blocks, expected) -> None:
    actual = cuefy_blocks(blocks)
    assert actual == expected


@pytest.mark.parametrize("stems, expected", [
    pytest.param({}, None, marks=pytest.mark.xfail(raises=AssertionError)),

    ({"NOM": {"katiSa": ""}}, ["#katiSaNOM: #LexemeNOM & {stems: \"katiSa\"}"]),

    ({"NOM": {"Genre=A": {"katiSa": ""}}}, ["#katiSaNOMA: #LexemeNOM & {sigma: {Genre: \"A\"}, stems: \"katiSa\"}"]),

    ({"NOM": {"Genre=A": {"katiSa": "", "padaN": "", "toSik": ""}}},
     ["#katiSaNOMA: #LexemeNOM & {sigma: {Genre: \"A\"}, stems: \"katiSa\"}",
      "#padaNNOMA: #LexemeNOM & {sigma: {Genre: \"A\"}, stems: \"padaN\"}",
      "#toSikNOMA: #LexemeNOM & {sigma: {Genre: \"A\"}, stems: \"toSik\"}"]),

    ({"NOM": {"Genre=A": {"katiSa": ""}, "Genre=B": {"minet": ""}}},
     ["#katiSaNOMA: #LexemeNOM & {sigma: {Genre: \"A\"}, stems: \"katiSa\"}",
      "#minetNOMB: #LexemeNOM & {sigma: {Genre: \"B\"}, stems: \"minet\"}"]),

    ({"NOM": {"Genre=A": {"katiSa": ""}},
      "ADJ": {"Cf=1": {"meN": ""}}},
     ["#katiSaNOMA: #LexemeNOM & {sigma: {Genre: \"A\"}, stems: \"katiSa\"}",
      "#meNADJ1: #LexemeADJ & {sigma: {Cf: \"1\"}, stems: \"meN\"}"]),
])
def test_read_stems(stems, expected) -> None:
    actual = read_stems(stems)
    assert actual == expected


@pytest.mark.parametrize("rule, expected", [
    pytest.param("1AU4125", None, marks=pytest.mark.xfail()),
    ("X+o", "Suffix"),
    ("X+mo", "Suffix"),
    ("o+X", "Prefix"),
    ("oo+X", "Prefix"),
    ("o+X+r", "Circumfix"),
    ("od+X+dr", "Circumfix"),
])
def test_choose_rule(rule, expected) -> None:
    actual = choose_rule(rule)
    assert actual == expected
