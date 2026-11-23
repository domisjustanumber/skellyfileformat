"""The stage marks of recording-files/tests/conformance/conftest.py agree with recording-files/conformance.md (decisions CPM2 and YBT1).

The section "The stage of each test" of conformance.md has two tables. The conftest holds the same
facts as `STAGES`, `PARTS`, `GOLDEN_RULE` and `GOLDEN_STAGES`. This check compares them.
"""

from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[2]
ORDER = ["1a", "1b", "2", "3", "4"]
COLLECTED = re.compile(r"::test_sft_(\d{3})_((\w+).*)$")
DEFINITION = re.compile(r"^\*\*SFT-(\d{3})\*\*(.*)$", re.MULTILINE)


def conftest():
    spec = importlib.util.spec_from_file_location("conformance_conftest", ROOT / "recording-files" / "tests" / "conformance" / "conftest.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def section(conformance: str) -> str:
    return conformance.split("\n## The stage of each test\n", 1)[1].split("\n## ", 1)[0]


def rows(text: str, first: str) -> list[list[str]]:
    """The cells of each table row whose first cell starts with `first`."""
    return [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in text.splitlines() if line.startswith(f"| {first}")]


def parse_tests(text: str) -> tuple[dict, dict, set]:
    """The tables STAGES, PARTS and GOLDEN_RULE, from the first table."""
    stages, parts, golden = {}, {}, set()
    for test, stage, earlier in rows(text, "SFT-"):
        number = test.removeprefix("SFT-")
        stages[number] = stage
        for group in filter(None, (group.strip() for group in earlier.split(";"))):
            if group == "`<golden case>`":
                golden.add(number)
                continue
            name, patterns = group.split(":", 1)
            parts.setdefault(number, {})[name] = re.findall(r"`([^`]+)`", patterns)
    return stages, parts, golden


def parse_golden(text: str) -> dict:
    """The table GOLDEN_STAGES, from the second table."""
    found = {}
    for folder, cases, full, player in rows(text, "G"):
        key = f"G{int(folder[1:]):02d}"
        names = re.findall(r"`([^`]+)`", cases)
        for name in names or [None]:
            found[f"{key}/{name}" if name else key] = (full, player)
    return found


def test_the_marks_agree_with_conformance_md():
    text = section((ROOT / "recording-files" / "conformance.md").read_text(encoding="utf-8"))
    module = conftest()
    stages, parts, golden = parse_tests(text)
    assert stages == module.STAGES
    assert parts == module.PARTS
    assert golden == module.GOLDEN_RULE
    assert parse_golden(text) == module.GOLDEN_STAGES


def collected() -> list[tuple[str, str, str]]:
    """The number, the function and the name with its parameter ID of each collected conformance test with an SFT ID."""
    command = [sys.executable, "-m", "pytest", "recording-files/tests/conformance", "--collect-only", "-q", "-p", "no:cacheprovider"]
    output = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=True).stdout  # noqa: S603
    return [found.group(1, 3, 2) for line in output.splitlines() if (found := COLLECTED.search(line))]


def test_each_test_has_a_stage_and_each_part_names_a_case():
    conformance = (ROOT / "recording-files" / "conformance.md").read_text(encoding="utf-8")
    listed = {number for number, rest in DEFINITION.findall(conformance) if not rest.strip().startswith("(withdrawn)")}
    module = conftest()
    assert set(module.STAGES) == listed, "each test of conformance.md has one stage"
    assert set(module.STAGES.values()) <= set(ORDER)
    cases = collected()
    for number, groups in module.PARTS.items():
        for stage, patterns in groups.items():
            assert ORDER.index(stage) < ORDER.index(module.STAGES[number]), f"SFT-{number}: a part of stage {stage} is not earlier"
            for pattern in patterns:
                found = any(n == number and module._matches(pattern, function, name) for n, function, name in cases)
                assert found, f"SFT-{number}: no collected case for `{pattern}`"


def test_stage_of():
    module = conftest()

    def item(originalname, params=None, suffix=""):
        call = {"callspec": SimpleNamespace(params=params)} if params else {}
        return SimpleNamespace(originalname=originalname, name=originalname + suffix, nodeid=originalname, **call)

    reads = "test_sft_768_reader_result_of_each_golden_case"
    for kind, stage in (("player", "1a"), ("js", "1a"), ("full", "2")):
        assert module.stage_of(item(reads, {"name": "G03", "case": "take", "kind": kind}, f"[G03-take-{kind}]")) == stage, kind
    assert module.stage_of(item("test_sft_768_committed_results", {"name": "G03", "case": "take"}, "[G03-take]")) == "1a"
    assert module.stage_of(item("test_golden_g01_is_present")) == "1a"
    with pytest.raises(ValueError, match="test_sft_<NNN>_<part>"):
        module.stage_of(item("test_no_sft_id"))


def test_the_parsers():
    text = (
        "| Test | Stage | Earlier parts |\n|---|---|---|\n| SFT-700 | 2 | 1a: `a`, `b[x:y]` |\n| SFT-701 | 1a | |\n"
        "| SFT-734 | 2 | `<golden case>`; 1a: `c[*-js]` |\n\n| Folder | Cases | `full` | `player` |\n|---|---|---|---|\n"
        "| G1 | each | 1a | 1a |\n| G10 | `higher_minor` | 2 | 1a |\n"
    )
    assert parse_tests(text) == ({"700": "2", "701": "1a", "734": "2"}, {"700": {"1a": ["a", "b[x:y]"]}, "734": {"1a": ["c[*-js]"]}}, {"734"})
    assert parse_golden(text) == {"G01": ("1a", "1a"), "G10/higher_minor": ("2", "1a")}
