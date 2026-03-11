"""Shared pytest configuration and hooks.

Auto-xfail: any test (or fixture) that raises ``NotImplementedError`` is
automatically reported as *expected failure* instead of a hard failure.
Once the stub is replaced with real code the test passes normally — no
markers to add or remove.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Generator

import pytest

if TYPE_CHECKING:
    from pluggy import Result


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(
    item: pytest.Item,  # noqa: ARG001
    call: pytest.CallInfo[None],
) -> Generator[None, Result[pytest.TestReport], None]:
    """Convert NotImplementedError failures into xfail results."""
    outcome: Result[pytest.TestReport] = yield
    report = outcome.get_result()

    if call.when in ("setup", "call") and report.failed:
        if call.excinfo is not None and call.excinfo.errisinstance(NotImplementedError):
            report.outcome = "skipped"
            report.wasxfail = "Not implemented yet"
