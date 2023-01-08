import pytest
import yaml
from frozendict import frozendict

from lexique.readers import gridify, read_gloses, dictify_str, rulify, read_blocks, read_phonology, realize_lexeme
from lexique.ruler import ruler_suffix, ruler_prefix, ruler_circumfix, ruler_gabarit, ruler_selection, ruler_condition
from lexique.structures import Phonology, Lexeme, Forme, Paradigm, Suffix


@pytest.mark.parametrize("grid", [

    {},

    {"": ["trait_1"]},

    {"a": []},
])
def test_gridify_one_errors(grid) -> None:
    with pytest.raises(ValueError):
        _ = list(gridify(grid))


@pytest.mark.parametrize("grid, expected", [

    ({"a": ["1"]}, [{"a": "1"}]),

    ({"a": ["1", "2"]}, [{"a": "1"}, {"a": "2"}]),

    ({"a": ["1", "2"],
      "b": ["3", "4"]},
     [{"a": "1", "b": "3"},
      {"a": "1", "b": "4"},
      {"a": "2", "b": "3"},
      {"a": "2", "b": "4"}]),
])
def test_gridify_one(grid, expected) -> None:
    actual = list(gridify(grid))
    assert actual == expected


@pytest.mark.parametrize("grid", [

    [],

    [{"": ["trait_1"]}],

    [{"a": []}],
])
def test_gridify_all_errors(grid) -> None:
    with pytest.raises(ValueError):
        _ = list(gridify(grid))


@pytest.mark.parametrize("grid, expected", [

    ([{"a": ["1"]}], [{"a": "1"}]),

    ([{"a": ["1", "2"]}], [{"a": "1"}, {"a": "2"}]),

    ([{"a": ["1", "2"],
       "b": ["3", "4"]}],
     [{"a": "1", "b": "3"},
      {"a": "1", "b": "4"},
      {"a": "2", "b": "3"},
      {"a": "2", "b": "4"}]),

    ([{"a": ["1"]},
      {"a": ["2"],
       "b": ["3", "4"]}],
     [{"a": "1"},
      {"a": "2", "b": "3"},
      {"a": "2", "b": "4"}])
])
def test_gridify_all(grid, expected) -> None:
    actual = list(gridify(grid))
    assert actual == expected


@pytest.mark.parametrize("gloses, expected", [

    ({"NOUN": [{"a": ["1"]}]},
     {"NOUN": [frozendict({"a": "1"})]}),

    ({"NOUN": [{"a": ["1", "2"]}]},
     {"NOUN": [frozendict({"a": "1"}),
               frozendict({"a": "2"})]}),

    ({"NOUN": [{"a": ["1", "2"], "b": ["3", "4"]}]},
     {"NOUN": [frozendict({"a": "1", "b": "3"}),
               frozendict({"a": "1", "b": "4"}),
               frozendict({"a": "2", "b": "3"}),
               frozendict({"a": "2", "b": "4"})]}),

    ({"NOUN": [{"a": ["1"]}, {"a": ["2"], "b": ["3", "4"]}]},
     {"NOUN": [frozendict({"a": "1"}),
               frozendict({"a": "2", "b": "3"}),
               frozendict({"a": "2", "b": "4"})]})
])
def test_read_gloses(tmp_path, gloses, expected) -> None:
    path_gloses_yaml_ = tmp_path / "Gloses.yaml"
    with open(path_gloses_yaml_, mode="w", encoding="utf8") as file_handler:
        yaml.dump(gloses, file_handler)

    actual = read_gloses(path_gloses_yaml_)
    assert actual == expected


@pytest.mark.parametrize("s, expected", [

    ("", frozendict()),

    ("case=erg", frozendict(case="erg")),

    ("case=erg,num=sg", frozendict(case="erg", num="sg")),
])
def test_dictify_str(s, expected) -> None:
    actual = dictify_str(s)
    assert actual == expected


@pytest.mark.parametrize("block, expected", [

    ({"Genre=M": "l+X"},
     [[ruler_prefix(rule="l+X", sigma=frozendict(Genre="M"))]]),

    ({"Genre=M": "X+l"},
     [[ruler_suffix(rule="X+l", sigma=frozendict(Genre="M"))]]),

    ({"Genre=M": "q+X+l"},
     [[ruler_circumfix(rule="q+X+l", sigma=frozendict(Genre="M"))]]),

    ({"Genre=M": "i4A1o2a3V"},
     [[ruler_gabarit(rule="i4A1o2a3V", sigma=frozendict(Genre="M"))]]),

    ({"Genre=M": "X4"},
     [[ruler_selection(rule="X4", sigma=frozendict(Genre="M"))]]),

    ({"Genre=M": "X4?X3:X1"},
     [[ruler_condition(rule="X4?X3:X1", sigma=frozendict(Genre="M"))]]),
])
def test_rulify_dict(block, expected) -> None:
    actual = list(rulify(block))[0]
    for i_idx, morpheme in enumerate(actual):
        assert morpheme.rule.string == expected[0][i_idx].rule.string
        assert morpheme.sigma == expected[0][i_idx].sigma


@pytest.mark.parametrize("blocks, expected", [

    ([{"Genre=M": "l+X"}],
     [[ruler_prefix(rule="l+X", sigma=frozendict(Genre="M"))]]),

    ([{"Genre=M": "X+l"}],
     [[ruler_suffix(rule="X+l", sigma=frozendict(Genre="M"))]]),

    ([{"Genre=M": "q+X+l"}],
     [[ruler_circumfix(rule="q+X+l", sigma=frozendict(Genre="M"))]]),

    ([{"Genre=M": "i4A1o2a3V"}],
     [[ruler_gabarit(rule="i4A1o2a3V", sigma=frozendict(Genre="M"))]]),

    ([{"Genre=M": "X4"}],
     [[ruler_selection(rule="X4", sigma=frozendict(Genre="M"))]]),

    ([{"Genre=M": "X4?X3:X1"}],
     [[ruler_condition(rule="X4?X3:X1", sigma=frozendict(Genre="M"))]]),
])
def test_rulify_list(blocks, expected) -> None:
    actual = list(rulify(blocks))
    for i_idx, rules in enumerate(actual):
        for j_idx, rule in enumerate(rules):
            assert rule.rule.string == expected[i_idx][j_idx].rule.string  # type: ignore
            assert rule.sigma == expected[i_idx][j_idx].sigma



@pytest.mark.parametrize("blocks, expected", [
    ({"NOUN": [{"Genre=M": "l+X"}]},
     {"NOUN": [[ruler_prefix(rule="l+X", sigma=frozendict(Genre="M"))]]}),

    ({"NOUN": [{"Genre=M": "X+l"}]},
     {"NOUN": [[ruler_suffix(rule="X+l", sigma=frozendict(Genre="M"))]]}),

    ({"NOUN": [{"Genre=M": "q+X+l"}]},
     {"NOUN": [[ruler_circumfix(rule="q+X+l", sigma=frozendict(Genre="M"))]]}),

    ({"NOUN": [{"Genre=M": "i4A1o2a3V"}]},
     {"NOUN": [[ruler_gabarit(rule="i4A1o2a3V", sigma=frozendict(Genre="M"))]]}),

    ({"NOUN": [{"Genre=M": "X4"}]},
     {"NOUN": [[ruler_selection(rule="X4", sigma=frozendict(Genre="M"))]]}),

    ({"NOUN": [{"Genre=M": "X4?X3:X1"}]},
     {"NOUN": [[ruler_condition(rule="X4?X3:X1", sigma=frozendict(Genre="M"))]]})
])
def test_read_blocks(tmp_path, blocks, expected) -> None:
    path_blocks_yaml_ = tmp_path / "Blocks.yaml"
    with open(path_blocks_yaml_, mode="w", encoding="utf8") as file_handler:
        yaml.dump(blocks, file_handler)

    actual = read_blocks(path_blocks_yaml_)
    for i_category, i_blocks in actual.items():
        for i_idx, rules in enumerate(i_blocks):
            for j_idx, rule in enumerate(rules):
                assert rule.rule.string == expected[i_category][i_idx][j_idx].rule.string  # type: ignore
                assert rule.sigma == expected[i_category][i_idx][j_idx].sigma


@pytest.mark.parametrize("phonology, expected", [
    ({"consonnes": frozenset("zrtpmkl"),
      "voyelles": frozenset("aeiou"),
      "mutations": frozendict(a="b"),
      "derives": frozendict(a="b"),
      "apophonies": frozendict(a="b")},
     Phonology(consonnes=frozenset("zrtpmkl"),
               voyelles=frozenset("aeiou"),
               mutations=frozendict(a="b"),
               derives=frozendict(a="b"),
               apophonies=frozendict(a="b")))
])
def test_read_phonology(tmp_path, phonology, expected) -> None:
    path_phonology_yaml_ = tmp_path / "Phonology.yaml"
    with open(path_phonology_yaml_, mode="w", encoding="utf8") as file_handler:
        yaml.dump(phonology, file_handler)

    actual = read_phonology(path_phonology_yaml_)
    assert actual == expected


