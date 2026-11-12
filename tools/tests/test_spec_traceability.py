"""The traceability check links each spec requirement to a conformance test (AGENTS.md section 4)."""

from __future__ import annotations

from pathlib import Path

import check_spec_traceability as cst

ROOT = Path(__file__).resolve().parents[2]


def write(tmp_path: Path, spec: str, conformance: str) -> tuple[Path, Path]:
    s = tmp_path / "SPEC.md"
    c = tmp_path / "conformance.md"
    s.write_text(spec, encoding="utf-8")
    c.write_text(conformance, encoding="utf-8")
    return s, c


GOOD_SPEC = """# Spec

**SFF-001** A reader MUST reject an unknown major version.

**SFF-002** A writer MUST write `header_size` as a multiple of 8.

**SFF-003** (withdrawn)
"""

GOOD_CONFORMANCE = """# Conformance

**SFT-001** Unknown major version.
Checks: SFF-001
Pass: the reader raises an error.

**SFT-002** Header size.
Checks: SFF-002, SFF-001
Pass: every golden header has `header_size % 8 == 0`.

**SFT-003** (withdrawn)
"""


def test_linked_files_pass(tmp_path: Path) -> None:
    assert cst.check(*write(tmp_path, GOOD_SPEC, GOOD_CONFORMANCE)) == []


def test_files_with_no_ids_pass(tmp_path: Path) -> None:
    assert cst.check(*write(tmp_path, "# Spec\n", "# Conformance\n")) == []


def test_the_repository_files_pass() -> None:
    assert cst.check(ROOT / "spec" / "SPEC.md", ROOT / "spec" / "conformance.md") == []


def test_requirement_with_no_test(tmp_path: Path) -> None:
    spec = GOOD_SPEC + "\n**SFF-004** A new rule.\n"
    errors = cst.check(*write(tmp_path, spec, GOOD_CONFORMANCE))
    assert errors == ["SFF-004 has no test in conformance.md"]


def test_test_cites_unknown_requirement(tmp_path: Path) -> None:
    conformance = GOOD_CONFORMANCE + "\n**SFT-004** Extra.\nChecks: SFF-009\n"
    errors = cst.check(*write(tmp_path, GOOD_SPEC, conformance))
    assert errors == ["SFT-004 cites SFF-009, which SPEC.md does not define"]


def test_test_cites_withdrawn_requirement(tmp_path: Path) -> None:
    conformance = GOOD_CONFORMANCE + "\n**SFT-004** Extra.\nChecks: SFF-003\n"
    errors = cst.check(*write(tmp_path, GOOD_SPEC, conformance))
    assert errors == ["SFT-004 cites SFF-003, which is withdrawn"]


def test_test_with_no_checks_line(tmp_path: Path) -> None:
    conformance = GOOD_CONFORMANCE + "\n**SFT-004** Extra.\nPass: something.\n"
    errors = cst.check(*write(tmp_path, GOOD_SPEC, conformance))
    assert errors == ["SFT-004 has no 'Checks:' line"]


def test_test_with_two_checks_lines(tmp_path: Path) -> None:
    conformance = GOOD_CONFORMANCE + "\n**SFT-004** Extra.\nChecks: SFF-001\nChecks: SFF-002\n"
    errors = cst.check(*write(tmp_path, GOOD_SPEC, conformance))
    assert errors == ["SFT-004 has more than one 'Checks:' line"]


def test_duplicate_requirement_id(tmp_path: Path) -> None:
    spec = GOOD_SPEC + "\n**SFF-002** The same number again.\n"
    errors = cst.check(*write(tmp_path, spec, GOOD_CONFORMANCE))
    assert "SFF-002 is defined more than once in SPEC.md" in errors


def test_duplicate_test_id(tmp_path: Path) -> None:
    conformance = GOOD_CONFORMANCE + "\n**SFT-002** Again.\nChecks: SFF-001\n"
    errors = cst.check(*write(tmp_path, GOOD_SPEC, conformance))
    assert "SFT-002 is defined more than once in conformance.md" in errors


def test_ids_out_of_order(tmp_path: Path) -> None:
    spec = "**SFF-002** B.\n\n**SFF-001** A.\n"
    conformance = "**SFT-001** T.\nChecks: SFF-001, SFF-002\n"
    errors = cst.check(*write(tmp_path, spec, conformance))
    assert errors == ["SFF-001 comes after SFF-002 in SPEC.md; define IDs in number order"]


def test_malformed_id_in_a_definition(tmp_path: Path) -> None:
    spec = GOOD_SPEC + "\n**SFF-4** Short number.\n"
    errors = cst.check(*write(tmp_path, spec, GOOD_CONFORMANCE))
    assert errors == ["SPEC.md line 9: 'SFF-4' is not a valid ID (SFF-NNN, three digits)"]


def test_requirement_id_in_conformance_is_not_a_definition(tmp_path: Path) -> None:
    """A test line that mentions SFF-001 in prose does not define a requirement there."""
    conformance = GOOD_CONFORMANCE.replace("Unknown major version.", "Unknown major version (SFF-001).")
    assert cst.check(*write(tmp_path, GOOD_SPEC, conformance)) == []


def test_main_exit_codes(tmp_path: Path) -> None:
    s, c = write(tmp_path, GOOD_SPEC, GOOD_CONFORMANCE)
    assert cst.main(["--spec", str(s), "--conformance", str(c)]) == 0
    s.write_text(GOOD_SPEC + "\n**SFF-004** No test.\n", encoding="utf-8")
    assert cst.main(["--spec", str(s), "--conformance", str(c)]) == 1
