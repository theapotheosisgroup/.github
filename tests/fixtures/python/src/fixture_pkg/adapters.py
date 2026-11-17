"""Fixture adapter. It may depend on the core; the reverse is forbidden."""

from fixture_pkg.core import greet


def greet_loudly(name: str) -> str:
    return greet(name).upper()
