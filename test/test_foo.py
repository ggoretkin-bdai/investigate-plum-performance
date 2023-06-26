# Copyright (c) 2023 Boston Dynamics AI Institute, Inc.  All rights reserved.
import example_py_multiple_dispatch.foo
import plum  # type: ignore
import pytest


def test_trivial() -> None:
    assert 1 + 1 == 2


@pytest.mark.xfail
def test_trivial_fail() -> None:
    assert 1 + 1 == 3


def test_foo_defined() -> None:
    assert "This is an integer!" == example_py_multiple_dispatch.foo.f(3)
    assert "This is a string!" == example_py_multiple_dispatch.foo.f("three")


def test_foo_undefined() -> None:
    with pytest.raises(plum.resolver.NotFoundLookupError):
        example_py_multiple_dispatch.foo.f(3.0)
