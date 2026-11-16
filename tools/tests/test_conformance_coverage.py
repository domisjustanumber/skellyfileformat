"""Each conformance test of spec/conformance.md has a runnable test in tests/conformance (decision G21H).

This check reads the files as text. It imports no test and needs only the standard library.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFINITION = re.compile(r"^\*\*SFT-(\d{3})\*\*(.*)$", re.MULTILINE)
FUNCTION = re.compile(r"^def test_sft_(\d{3})_\w+\(", re.MULTILINE)


def listed_ids(conformance: str) -> set[str]:
    """The number of each test of conformance.md that is not withdrawn."""
    return {number for number, rest in DEFINITION.findall(conformance) if not rest.strip().startswith("(withdrawn)")}


def covered_ids(folder: Path) -> set[str]:
    """The number of each test ID that a function `test_sft_<NNN>_...` of the folder names."""
    return {number for path in folder.glob("*.py") for number in FUNCTION.findall(path.read_text(encoding="utf-8"))}


def test_each_conformance_test_has_a_runnable_test():
    listed = listed_ids((ROOT / "spec" / "conformance.md").read_text(encoding="utf-8"))
    covered = covered_ids(ROOT / "tests" / "conformance")
    assert listed, "conformance.md lists tests"
    missing = sorted(f"SFT-{number}" for number in listed - covered)
    assert not missing, f"no function `test_sft_<NNN>_...` in tests/conformance for: {', '.join(missing)}"
    unknown = sorted(f"SFT-{number}" for number in covered - listed)
    assert not unknown, f"a test function names an ID that conformance.md does not list, or lists as withdrawn: {', '.join(unknown)}"


def test_the_two_patterns_find_ids(tmp_path):
    conformance = "**SFT-001** (withdrawn) Draft v0.\n\n**SFT-700** Writer: text\nChecks: SFF-700\n\n**SFT-705** (external: freemocap) Names\n"
    assert listed_ids(conformance) == {"700", "705"}
    (tmp_path / "test_a.py").write_text("def test_sft_700_text(reader):\n    pass\n\n\ndef helper_sft_705():\n    pass\n", encoding="utf-8")
    assert covered_ids(tmp_path) == {"700"}
