import pytest


from pfmg.parsing.tokenizer import new_tokenizer


@pytest.mark.parametrize("id_tokenizer, data, expected", [

    ("Space", "a b c", ["a", "b", "c"]),

    ("Space", "abc", ["abc"]),

    ("Space", "b  c", ["b", "", "c"]),

    pytest.param(
        "Space", "", None,
        marks=pytest.mark.xfail(raises=AssertionError)),

    pytest.param(
        "Space", [], None,
        marks=pytest.mark.xfail(raises=AssertionError)),

    pytest.param(
        "Space", set(), None,
        marks=pytest.mark.xfail(raises=AssertionError)),
])
def test_tokenizer(id_tokenizer, data, expected) -> None:
    actual = (new_tokenizer(id_tokenizer=id_tokenizer)
              .__call__(sentence=data))
    assert actual == expected
