from fixture_pkg.adapters import greet_loudly
from fixture_pkg.core import greet


def test_greet() -> None:
    assert greet("fixture") == "hello, fixture"


def test_greet_loudly() -> None:
    assert greet_loudly("fixture") == "HELLO, FIXTURE"
