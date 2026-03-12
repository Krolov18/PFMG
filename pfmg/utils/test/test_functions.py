"""Tests for pfmg.utils.functions."""


from pfmg.utils.functions import compose, static_vars


def test_static_vars_attaches_attributes() -> None:
    @static_vars(counter=0)
    def counter() -> int:
        counter.counter += 1
        return counter.counter

    assert counter() == 1
    assert counter() == 2
    assert counter.counter == 2


def test_static_vars_multiple_attrs() -> None:
    @static_vars(a=10, b=20)
    def fn() -> tuple[int, int]:
        return fn.a, fn.b

    assert fn() == (10, 20)


def test_compose_two_functions() -> None:
    def f(x: int) -> int:
        return x + 1

    def g(x: int) -> int:
        return x * 2

    h = compose(f, g)
    assert h(3) == f(g(3)) == 7


def test_compose_three_functions() -> None:
    def f(x: int) -> int:
        return x + 1

    def g(x: int) -> int:
        return x * 2

    def k(x: int) -> int:
        return x - 1

    h = compose(f, g, k)
    assert h(5) == f(g(k(5))) == f(g(4)) == f(8) == 9


def test_compose_single_function() -> None:
    def f(x: int) -> int:
        return x + 1

    h = compose(f)
    assert h(0) == 1


def test_compose_identity_when_empty() -> None:
    id_fn = compose()
    assert id_fn(42) == 42
