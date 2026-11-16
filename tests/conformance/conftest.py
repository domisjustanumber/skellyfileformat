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


@pytest.fixture
def reader():
    """The Python reader: `read_folder`, `canonical_json` and the detail functions."""
    return _package()


@pytest.fixture
def writer():
    """The Python writer: `TakeWriter`, `repair_take` and `release_check`."""
    return _package()


@pytest.fixture
def js_reader():
    """A function that runs the JavaScript reader on a folder and returns the bytes of its standard output."""
    node = shutil.which("node")
    if node is None or not JS_COMMAND.is_file():
        pytest.fail("the JavaScript reader `js/bin/read-folder.mjs`, or `node`, does not exist", pytrace=False)

    def run(folder: Path, records: bool = False) -> bytes:
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
