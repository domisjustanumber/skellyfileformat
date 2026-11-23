"""The test adapter seam of recording-files/tests/conformance/conftest.py (decision YBT1; its form: decision K4Y1).

The fixtures `reader` and `writer` give the module that `SKELLYSPECS_ADAPTER` names. With no
adapter, a test that calls one fails with one line. The check runs pytest on a copy of the conftest.
"""

from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
CONFTEST = ROOT / "recording-files" / "tests" / "conformance" / "conftest.py"
STUB = "def read_folder(path, records=False, scope='full'):\n    return 'stub result'\n\n\nTakeWriter = 'stub writer'\n"
TESTS = """
def test_sft_701_reader(reader):
    assert reader.read_folder('take') == 'stub result'


def test_sft_702_writer(writer):
    assert writer.TakeWriter == 'stub writer'
"""


def run_pytest(tmp_path: Path, adapter: str | None) -> subprocess.CompletedProcess:
    suite = tmp_path / "suite"
    suite.mkdir()
    shutil.copy(CONFTEST, suite / "conftest.py")
    (suite / "test_stub.py").write_text(TESTS, encoding="utf-8")
    (tmp_path / "stub_adapter.py").write_text(STUB, encoding="utf-8")
    env = {key: value for key, value in os.environ.items() if not key.startswith("SKELLYSPECS_")}
    env["PYTHONPATH"] = str(tmp_path)
    if adapter is not None:
        env["SKELLYSPECS_ADAPTER"] = adapter
    command = [sys.executable, "-m", "pytest", str(suite), "-q", "-p", "no:cacheprovider", "--rootdir", str(suite)]
    return subprocess.run(command, capture_output=True, text=True, env=env, cwd=tmp_path)  # noqa: S603


def test_the_fixtures_give_the_configured_adapter(tmp_path):
    done = run_pytest(tmp_path, "stub_adapter")
    assert done.returncode == 0, done.stdout + done.stderr
    assert "2 passed" in done.stdout


def test_no_adapter_fails_with_one_line(tmp_path):
    done = run_pytest(tmp_path, None)
    assert "2 failed" in done.stdout, done.stdout + done.stderr
    assert done.stdout.count("no test adapter is configured: set SKELLYSPECS_ADAPTER") == 2


def test_the_javascript_command_comes_from_the_adapter_folder(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location("conformance_conftest_adapter", CONFTEST)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module.shutil, "which", lambda name: "node")
    monkeypatch.delenv(module.JS_ADAPTER, raising=False)
    with pytest.raises(pytest.fail.Exception, match="no JavaScript test adapter is configured"):
        module.js_command(Path("take"))
    script = tmp_path / "bin" / "read-folder.mjs"
    script.parent.mkdir()
    script.write_text("", encoding="utf-8")
    monkeypatch.setenv(module.JS_ADAPTER, str(tmp_path))
    assert module.js_command(Path("take"), records=True) == ["node", str(script), "take", "--records"]
