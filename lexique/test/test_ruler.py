import pytest
from frozendict import frozendict

from lexique.ruler import (ruler_prefix, ruler_suffix, ruler_circumfix, ruler_condition,
                           ruler_selection, ruler_gabarit, any_ruler)
from lexique.structures import Condition, Selection, Prefix, Suffix, Circumfix, Gabarit


@pytest.mark.parametrize("rule, sigma", [
    ("e+X", frozendict(genre="m", nombre="sg")),
])
def test_ruler_prefix(rule, sigma) -> None:
    actual = ruler_prefix(rule=rule, sigma=sigma)
    assert isinstance(actual, Prefix)
    assert actual.rule is not None
    assert actual.rule.group(1) == rule[0]
    assert actual.sigma == sigma


@pytest.mark.parametrize("rule, sigma", [
    ("X+e", frozendict(genre="m", nombre="sg")),
])
def test_ruler_suffix(rule, sigma) -> None:
    actual = ruler_suffix(rule=rule, sigma=sigma)
    assert isinstance(actual, Suffix)
    assert actual.rule is not None
    assert actual.rule.group(1) == rule[-1]
    assert actual.sigma == sigma


@pytest.mark.parametrize("rule, sigma", [
    ("e+X+a", frozendict(genre="m", nombre="sg")),
])
def test_ruler_circumfix(rule, sigma) -> None:
    actual = ruler_circumfix(rule=rule, sigma=sigma)
    assert isinstance(actual, Circumfix)
    assert actual.rule is not None
    assert actual.rule.group(1) == rule[:rule.find("+")]
    assert actual.rule.group(2) == rule[rule.rfind("+") + 1:]
    assert actual.sigma == sigma


@pytest.mark.parametrize("rule, sigma", [
    ("i4A1o2a3V", frozendict(genre="m", nombre="sg")),
])
def test_ruler_gabarit(phonology, rule, sigma) -> None:
    actual = ruler_gabarit(rule=rule, sigma=sigma)
    assert isinstance(actual, Gabarit)
    assert actual.rule is not None
    assert actual.rule.group(0) == rule
    assert actual.sigma == sigma


@pytest.mark.parametrize("rule, sigma", [
    ("X1", frozendict(genre="m", nombre="sg")),
    ("X2", frozendict(genre="m", nombre="sg")),
])
def test_ruler_selection(rule, sigma) -> None:
    actual = ruler_selection(rule=rule, sigma=sigma)
    assert isinstance(actual, Selection)
    assert actual.rule is not None
    assert int(actual.rule.group(1)) == int(rule[1:])
    assert actual.sigma == sigma


@pytest.mark.parametrize("rule, sigma", [
    ("X2?X2:X1", frozendict(genre="m", nombre="sg")),
    ("X2?X2:X1", frozendict(genre="m", nombre="sg")),
])
def test_ruler_condition(rule, sigma) -> None:
    actual = ruler_condition(rule=rule, sigma=sigma)
    assert isinstance(actual, Condition)
    assert actual.rule is not None
    assert actual.rule[0] == rule
    assert actual.rule[1] == rule[:rule.find("?")]
    assert actual.rule[2] == rule[rule.find("?") + 1:rule.find(":")]
    assert actual.rule[3] == rule[rule.find(":") + 1:]
    assert actual.sigma == sigma


@pytest.mark.parametrize("rule, expected", [
    ("e+X", Prefix),
    ("X+e", Suffix),
    ("a+X+e", Circumfix),
    ("i4A1o2a3V", Gabarit),
    ("X4", Selection),
    ("X2?X2:X1", Condition)
])
def test_rule_any(rule, expected) -> None:
    actual = any_ruler(rule=rule, sigma=frozendict(genre="m", nombre="sg"))
    assert isinstance(actual, expected)


@pytest.mark.parametrize("rule, expected", [
    ("eX", Prefix),
    ("Xe", Suffix),
    ("a+X+e+9", Circumfix),
    ("i4A1o2a3V3R", Gabarit),
    ("X", Selection),
    ("X2X2:X1", Condition)
])
def test_rule_any_errors(rule, expected) -> None:
    with pytest.raises(ValueError):
        _ = any_ruler(rule=rule, sigma=frozendict(genre="m", nombre="sg"))
