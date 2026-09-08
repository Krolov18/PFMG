"""End-to-end tests of the example grammars shipped in `examples/`."""

import pytest

from pfmg.parsing.parser import KParser
from pfmg.utils.paths import get_project_path

CORPUS = get_project_path() / "examples" / "phrases_data3.txt"


def _corpus() -> list[str]:
    """Return the benchmark corpus, skipping blank and '#' lines."""
    lines = CORPUS.read_text(encoding="utf8").splitlines()
    return [x.strip() for x in lines if x.strip() and not x.startswith("#")]


@pytest.fixture(scope="module")
def fx_kparser() -> KParser:
    """KParser built from the `examples/data` grammar."""
    return KParser.from_yaml(get_project_path() / "examples" / "data")


@pytest.fixture(scope="module")
def fx_kparser3() -> KParser:
    """KParser built from the `examples/data3` sentence grammar."""
    return KParser.from_yaml(get_project_path() / "examples" / "data3")


def test_parse_all(fx_kparser) -> None:
    """"des garçons" translates to the Kalaba noun phrases of the example.

    Both translations are the dual and the plural: the source plural aligns
    with two destination numbers, which is the morphological ambiguity the
    example is built around.
    """
    actual = fx_kparser.parse(data="des garçons", keep="all")

    assert sorted(actual) == [
        "tulo zo",
        "tulol zoj",
    ]


def test_parse_prenominal_adjective(fx_kparser) -> None:
    """"D ADJ NOM" is reordered as "NOM ADJ D" in Kalaba."""
    actual = fx_kparser.parse(data="des petites autruches", keep="all")

    assert sorted(actual) == [
        "sipru kizi zi",
        "siprug kizin zij",
    ]


def test_parse_postnominal_adjective(fx_kparser) -> None:
    """"D NOM ADJ" reaches the same Kalaba order as "D ADJ NOM"."""
    actual = fx_kparser.parse(data="les autruches vertes", keep="all")

    assert sorted(actual) == [
        "sipru regi ri",
        "siprug regin rij",
    ]


def test_parse_agrees_on_destination_gender(fx_kparser) -> None:
    """The determiner takes the inherent gender of the Kalaba noun.

    "bruit" is masculine in French but its Kalaba counterpart is feminine, so
    the determiner is realized as "ri-", not "ro-".
    """
    actual = fx_kparser.parse(data="le bruit", keep="all")

    assert actual == ["apsanv ris"]


def test_parse_first(fx_kparser) -> None:
    """keep="first" returns one of the translations, as a string."""
    actual = fx_kparser.parse(data="des garçons", keep="first")

    assert isinstance(actual, str)
    assert actual in fx_kparser.parse(data="des garçons", keep="all")


def test_parse_list(fx_kparser) -> None:
    """A list of sentences is parsed sentence by sentence."""
    actual = fx_kparser.parse(data=["des garçons", "le bruit"], keep="all")

    assert "tulol zoj" in actual
    assert "apsanv ris" in actual


def test_parse_unknown_word(fx_kparser) -> None:
    """A word outside the lexicon is reported as untranslatable."""
    with pytest.raises(ValueError, match="n'est pas reconnu par le traducteur"):
        fx_kparser.parse(data="des zzzz", keep="all")


def test_sentence_grammar_nests_noun_phrases(fx_kparser3) -> None:
    """A full French sentence becomes a verb-final Kalaba clause.

    Both translations differ only by the number of the subject: French "les"
    is plural where Kalaba distinguishes a dual from a plural. The object is
    dual on both because "deux" is lexically dual.
    """
    actual = fx_kparser3.parse(
        data="les petits enfants mangent deux autruches jaunes", keep="all"
    )

    assert sorted(actual) == [
        "telaazi kizerak rek sipruazi gelirak duz nagetak",
        "telag kizen rej sipruazi gelirak duz nagetan",
    ]


@pytest.mark.parametrize(
    "sentence, expected",
    [
        ("le petit enfant dort", ["telaj kizer res zomta"]),
        ("la fille voit deux autruches", ["grij ris sipruazi duz sepita"]),
        (
            "la maman donne une banane à la fille",
            ["mimav ris ninov zes grij ris ka mizuta"],
        ),
    ],
)
def test_sentence_grammar_valences(fx_kparser3, sentence, expected) -> None:
    """Intransitive, direct transitive and ditransitive clauses each parse."""
    assert fx_kparser3.parse(data=sentence, keep="all") == expected


def test_sentence_grammar_indirect_transitive(fx_kparser3) -> None:
    """The French preposition becomes a Kalaba postposition."""
    actual = fx_kparser3.parse(data="les enfants parlent à la maman", keep="all")

    assert sorted(actual) == [
        "telaazi rek mimav ris ka lubitak",
        "telag rej mimav ris ka lubitan",
    ]


@pytest.mark.parametrize(
    "sentence",
    [
        "les enfants mangent",
        "le garçon dort la banane",
        "les enfants parlent la maman",
        "le enfant mangent deux autruches",
    ],
)
def test_sentence_grammar_rejects(fx_kparser3, sentence) -> None:
    """Valence and subject agreement leave these sentences without a parse."""
    assert fx_kparser3.parse(data=sentence, keep="all") == []


def test_corpus_is_well_formed() -> None:
    """The benchmark corpus holds 50 distinct sentences."""
    sentences = _corpus()

    assert len(sentences) == 50
    assert len(set(sentences)) == 50


@pytest.mark.parametrize("sentence", _corpus()[::5])
def test_corpus_still_parses(fx_kparser3, sentence) -> None:
    """A sample of the benchmark corpus still translates.

    `scripts/bench_parsing.py` runs the whole file; this keeps the suite fast
    while still catching a grammar change that would silently break it.
    """
    assert fx_kparser3.parse(data=sentence, keep="first")


@pytest.fixture(scope="module")
def fx_kparser4() -> KParser:
    """KParser built from the `examples/data4` templatic grammar."""
    return KParser.from_yaml(get_project_path() / "examples" / "data4")


def test_template_noun_carries_number_and_case(fx_kparser4) -> None:
    """The root consonants stay put; the vocalic scheme carries the inflection.

    "livre" is the root k-t-b: the first vowel is the number (sg a, dual o,
    plural i, trial u, quadral e) and the second one the case (here absolutive
    a). A bare French plural covers the four non-singular numbers.
    """
    singular = fx_kparser4.parse(data="le livre dort", keep="all")
    plural = fx_kparser4.parse(data="les livres dorment", keep="all")

    assert singular == ["takataban fanzkot"]
    assert sorted(plural) == [
        "taketaban fanzkoz",
        "takitaban fanzkol",
        "takotaban fanzkon",
        "takutaban fanzkom",
    ]


@pytest.mark.parametrize(
    "sentence, expected",
    [
        ("les deux livres dorment", "takotaban fanzkon"),
        ("les trois livres dorment", "takutaban fanzkom"),
        ("les quatre livres dorment", "taketaban fanzkoz"),
    ],
)
def test_numeral_is_a_morpheme_not_a_word(fx_kparser4, sentence, expected) -> None:
    """The French numeral leaves no word behind: it selects a vocalic scheme.

    It fixes the source-only `Compte` feature, which the noun's alignments turn
    into a grammatical number. The translation is as long as the one without a
    numeral — only the noun's scheme changed.
    """
    actual = fx_kparser4.parse(data=sentence, keep="all")

    assert actual == [expected]
    assert len(actual[0].split()) == 2


def test_numeral_requires_a_plural_noun_phrase(fx_kparser4) -> None:
    """The numeral is inherently plural on the French side."""
    assert fx_kparser4.parse(data="le deux livre dort", keep="all") == []
    assert fx_kparser4.parse(data="les deux livre dort", keep="all") == []


def test_determiner_is_a_circumfix_on_the_noun(fx_kparser4) -> None:
    """The invented language has no determiner word: it wraps the noun.

    The prefix carries the determination and the suffix carries it together
    with the noun's inherent gender.
    """
    forms = [
        fx_kparser4.parse(data=f"{d} livre dort", keep="first") for d in ("le", "un", "ce")
    ]

    assert forms == ["takataban fanzkot", "mukatabun fanzkot", "sikatabin fanzkot"]
    assert all(len(x.split()) == 2 for x in forms)


@pytest.mark.parametrize(
    "sentence, expected",
    [
        # intransitif : sujet absolutif, verbe à l'absolutif
        ("le livre dort", "takataban fanzkot"),
        # transitif : sujet ergatif, objet accusatif, verbe à l'ergatif
        ("la femme voit le chien", "tagazomar tatasukas sepkket"),
        # ditransitif : sujet nominatif, objet absolutif, second objet datif
        (
            "la femme donne un livre à un enfant",
            "tagazimar mukatabun mumaredun mizdkat",
        ),
    ],
)
def test_case_follows_the_valence(fx_kparser4, sentence, expected) -> None:
    """The valence assigns a case to every argument, and the verb agrees on the subject's."""
    assert fx_kparser4.parse(data=sentence, keep="all") == [expected]


def test_genitive_complement(fx_kparser4) -> None:
    """"de" disappears: the genitive scheme carries the relation."""
    actual = fx_kparser4.parse(data="le livre de la femme dort", keep="all")

    assert actual == ["takataban tagazaimar fanzkot"]


def test_adposition_sits_right_of_the_noun_phrase(fx_kparser4) -> None:
    """The French preposition becomes a postposition governing the absolutive."""
    actual = fx_kparser4.parse(data="le livre dort sur la maison", keep="all")

    assert actual == ["tasalafal mirim takataban fanzkot"]


def test_circumstantials_wrap_the_clause(fx_kparser4) -> None:
    """Circumstantial complements stay at the edges, never inside the clause."""
    actual = fx_kparser4.parse(
        data="pour la femme le livre dort sous un arbre", keep="all"
    )

    assert actual == ["tagazamar talat takataban fanzkot mupanakul dolod"]
    core = actual[0].split()[2:4]
    assert core == ["takataban", "fanzkot"]


def test_opposing_adpositions_are_palindromes(fx_kparser4) -> None:
    """Adpositions that come in opposing pairs have a palindromic form."""
    opposed = {"pro", "anti", "sup", "sub"}
    forms = {
        f.source.to_string(): (dict(f.source.get_sigma())["Rel"], f.destination.to_string())
        for f in fx_kparser4.translator.lexique
        if f.source.pos == "ADP"
    }

    assert {r for r, _ in forms.values()} >= opposed
    for word, (rel, form) in forms.items():
        if rel in opposed:
            assert form == form[::-1], f"{word} -> {form} n'est pas un palindrome"


@pytest.mark.parametrize(
    "sentence",
    [
        "la femme dort le chien",
        "le livre voit",
        "le livre dort de la maison",
    ],
)
def test_data4_rejects(fx_kparser4, sentence) -> None:
    """Valence and adposition type leave these without a parse."""
    assert fx_kparser4.parse(data=sentence, keep="all") == []


def test_ditransitive_with_numerals(fx_kparser4) -> None:
    """Numerals on both arguments leave exactly one translation.

    Subject nominative dual, object absolutive quadral, second object dative
    singular, and the verb agrees on the subject's case and number.
    """
    actual = fx_kparser4.parse(
        data="les deux femmes donnent les quatre livres à la rivière", keep="all"
    )

    assert actual == ["tagozimar taketaban tadaretar mizdkan"]


def test_numeral_only_filters(fx_kparser4) -> None:
    """A numbered noun phrase is one of the readings of the bare plural.

    Nothing distinguishes "les deux livres" from "les livres" understood as
    two: the numeral narrows the French input, it does not add a word.
    """
    bare = fx_kparser4.parse(data="les livres dorment", keep="all")
    two = fx_kparser4.parse(data="les deux livres dorment", keep="all")

    assert len(bare) == 4
    assert two[0] in bare
