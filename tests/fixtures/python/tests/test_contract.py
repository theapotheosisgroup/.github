import inspect

import pytest

import fixture_pkg.core


@pytest.mark.contract
def test_core_public_surface() -> None:
    public = sorted(n for n in vars(fixture_pkg.core) if not n.startswith("_"))
    assert public == ["greet"]
    assert str(inspect.signature(fixture_pkg.core.greet)) == "(name: str) -> str"
