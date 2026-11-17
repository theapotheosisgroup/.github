"""Fixture domain core. It must not import ``fixture_pkg.adapters``."""


def greet(name: str) -> str:
    return f"hello, {name}"
