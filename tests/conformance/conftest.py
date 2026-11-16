"""Fixtures of the conformance tests (decision G21H, spec/conformance.md).

This module imports no implementation at module level, so pytest can collect the tests before the
package exists. A test that needs the package then fails with one line.
"""

from __future__ import annotations

import importlib
import importlib.util
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
JS_COMMAND = ROOT / "js" / "bin" / "read-folder.mjs"


def _package():
    if importlib.util.find_spec("skellyfileformat") is None:
        pytest.fail("the package `skellyfileformat` does not exist: gate 2 has no implementation", pytrace=False)
    return importlib.import_module("skellyfileformat")


class _Lazy:
    """The package, imported at the first use of an attribute.

    So a test with no implementation fails in its body, with one line, and not with a fixture error.
    A test that first asks for a golden folder that is not built is skipped before that.
    """

    def __getattr__(self, name):
        return getattr(_package(), name)


@pytest.fixture
def reader():
    """The Python reader: `read_folder`, `canonical_json` and the detail functions."""
    return _Lazy()


@pytest.fixture
def writer():
    """The Python writer: `TakeWriter`, `repair_take` and `release_check`."""
    return _Lazy()


@pytest.fixture
def js_reader():
    """A function that runs the JavaScript reader on a folder and returns the bytes of its standard output."""

    def run(folder: Path, records: bool = False) -> bytes:
        node = shutil.which("node")
        if node is None or not JS_COMMAND.is_file():
            pytest.fail("the JavaScript reader `js/bin/read-folder.mjs`, or `node`, does not exist", pytrace=False)
        command = [node, str(JS_COMMAND), str(folder), *(["--records"] if records else [])]
        return subprocess.run(command, capture_output=True, check=True).stdout  # noqa: S603

    return run


@pytest.fixture
def golden():
    """A function that returns the folder of a case, for example `golden("G01")` or `golden("G01", "confirmed_key")`.

    The two expected results are beside the folder: `<case>.full.json` and `<case>.player.json`.
    """

    def case_folder(name: str, case: str = "take") -> Path:
        folder = ROOT / "golden" / name / case
        if not folder.is_dir():
            pytest.fail(f"the golden case `golden/{name}/{case}` does not exist", pytrace=False)
        return folder

    return case_folder


# --- Marks (conformance.md, "How to read a test"; decision QH61 item 46) ---


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "external(program): the repository of that program runs the test; it is skipped here"
    )
    config.addinivalue_line(
        "markers", "provisional(open_item): the test waits for an open item; it is skipped until then"
    )


def pytest_collection_modifyitems(items):
    for item in items:
        mark = item.get_closest_marker("external")
        if mark is not None:
            reason = f"external: {mark.args[0]}; the repository of that program runs it"
            item.add_marker(pytest.mark.skip(reason=reason))
        mark = item.get_closest_marker("provisional")
        if mark is not None:
            item.add_marker(pytest.mark.skip(reason=f"provisional: {mark.args[0]}"))


def external(program: str):
    """The mark of an external test: `@external("freemocap")` is `@pytest.mark.external("freemocap")`."""
    return pytest.mark.external(program)


def provisional(open_item: str):
    """The mark of a provisional test: `@provisional("DT5")` is `@pytest.mark.provisional("DT5")`."""
    return pytest.mark.provisional(open_item)


# --- Golden folders (SPEC.md Appendix A, "Layout and cases") ---

GOLDEN = ROOT / "golden"


def golden_or_skip(name: str, case: str = "take") -> Path:
    """Return the case folder `golden/<name>/<case>`. Skip the test when `golden/<name>` is absent."""
    if not (GOLDEN / name).is_dir():
        pytest.skip(f"golden folder {name} is not built yet")
    folder = GOLDEN / name / case
    if not folder.is_dir():
        pytest.fail(f"the golden case `golden/{name}/{case}` does not exist", pytrace=False)
    return folder


def expected(name: str, case: str, scope: str) -> bytes:
    """Return the bytes of `golden/<name>/<case>.<scope>.json`. `scope` is `full` or `player`."""
    golden_or_skip(name, case)
    return (GOLDEN / name / f"{case}.{scope}.json").read_bytes()


def truth(name: str, case: str):
    """Return the parsed `golden/<name>/<case>.truth.json`."""
    import json

    golden_or_skip(name, case)
    return json.loads((GOLDEN / name / f"{case}.truth.json").read_bytes())


@pytest.fixture(name="golden_or_skip")
def _golden_or_skip_fixture():
    """The function `golden_or_skip(name, case="take") -> Path`."""
    return golden_or_skip


@pytest.fixture(name="expected")
def _expected_fixture():
    """The function `expected(name, case, scope) -> bytes`."""
    return expected


@pytest.fixture(name="truth")
def _truth_fixture():
    """The function `truth(name, case) -> dict`."""
    return truth


@pytest.fixture
def variant(tmp_path):
    """A function that copies a golden case to a temporary directory and returns the copy.

    `variant(name, case="take", folder_name=None) -> Path`. The copy keeps the modification times. Its
    folder name is `folder_name`, or the case name. Each call gives a new copy. The test changes the
    copy: a "G3 with X" input is made at test time and is never committed.
    """
    count = 0

    def copy(name: str, case: str = "take", folder_name: str | None = None) -> Path:
        nonlocal count
        source = golden_or_skip(name, case)
        count += 1
        return Path(shutil.copytree(source, tmp_path / f"variant{count}" / (folder_name or case)))

    return copy
