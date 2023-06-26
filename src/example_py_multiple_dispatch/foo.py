from plum import dispatch  # type: ignore

# We need to tell both `ruff` and `mypy` to get out of the way


@dispatch  # type: ignore[no-redef]
def f(x: str):  # noqa: F811
    return "This is a string!"


@dispatch  # type: ignore[no-redef]
def f(x: int):  # noqa: F811
    return "This is an integer!"
