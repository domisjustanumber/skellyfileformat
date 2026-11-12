#!/usr/bin/env python3
"""Check the links between the spec requirements and the conformance tests (AGENTS.md section 4).

Usage::

    python tools/check_spec_traceability.py [--spec spec/SPEC.md] [--conformance spec/conformance.md]

Definitions:

- A requirement is defined by a line in `SPEC.md` that starts with ``**SFF-NNN**``.
- A test is defined by a line in `conformance.md` that starts with ``**SFT-NNN**``.
- ``NNN`` is exactly three digits.
- A definition followed by ``(withdrawn)`` defines a withdrawn requirement or test.
- A test cites requirements on one line that starts with ``Checks:``, for example
  ``Checks: SFF-001, SFF-004``. The line is in the test's block: after its definition line and
  before the next test definition or heading.

Rules:

1. An ID in a definition must match ``SFF-NNN`` or ``SFT-NNN``.
2. An ID is defined only once.
3. IDs are defined in number order in their file.
4. Each test that is not withdrawn has exactly one ``Checks:`` line, with one or more SFF IDs.
5. Each SFF ID that a test cites is defined in `SPEC.md` and is not withdrawn.
6. Each requirement that is not withdrawn is cited by one or more tests.

The tool exits 1 and prints one line for each error. Standard library only.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFINITION = re.compile(r"^\*\*(SF[FT]-[0-9A-Za-z]*)\*\*(.*)$")
VALID_ID = re.compile(r"^SF[FT]-\d{3}$")
CHECKS = re.compile(r"^Checks:\s*(.*)$")
CITED = re.compile(r"\bSFF-\d{3}\b")


@dataclass
class Item:
    id: str
    withdrawn: bool
    checks: list[list[str]] = field(default_factory=list)


def parse(path: Path, prefix: str, errors: list[str]) -> list[Item]:
    items: list[Item] = []
    current: Item | None = None
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        definition = DEFINITION.match(line)
        if definition and definition.group(1).startswith(prefix):
            item_id = definition.group(1)
            if not VALID_ID.match(item_id):
                errors.append(f"{path.name} line {number}: '{item_id}' is not a valid ID ({prefix}-NNN, three digits)")
                current = None
                continue
            current = Item(item_id, definition.group(2).strip().startswith("(withdrawn)"))
            items.append(current)
        elif line.startswith("#"):
            current = None
        elif current is not None and (checks := CHECKS.match(line)):
            current.checks.append(CITED.findall(checks.group(1)))
    return items


def check_ids(items: list[Item], file_name: str, errors: list[str]) -> None:
    seen: set[str] = set()
    last = 0
    for item in items:
        if item.id in seen:
            errors.append(f"{item.id} is defined more than once in {file_name}")
            continue
        seen.add(item.id)
        number = int(item.id[4:])
        if number < last:
            errors.append(f"{item.id} comes after {item.id[:4]}{last:03d} in {file_name}; define IDs in number order")
        last = max(last, number)


def check(spec: Path, conformance: Path) -> list[str]:
    errors: list[str] = []
    requirements = parse(spec, "SFF", errors)
    tests = parse(conformance, "SFT", errors)
    check_ids(requirements, spec.name, errors)
    check_ids(tests, conformance.name, errors)

    defined = {r.id: r for r in requirements}
    cited: set[str] = set()
    for test in tests:
        if test.withdrawn:
            continue
        if not test.checks or not test.checks[0]:
            errors.append(f"{test.id} has no 'Checks:' line")
            continue
        if len(test.checks) > 1:
            errors.append(f"{test.id} has more than one 'Checks:' line")
            continue
        for requirement_id in test.checks[0]:
            requirement = defined.get(requirement_id)
            if requirement is None:
                errors.append(f"{test.id} cites {requirement_id}, which {spec.name} does not define")
            elif requirement.withdrawn:
                errors.append(f"{test.id} cites {requirement_id}, which is withdrawn")
            else:
                cited.add(requirement_id)

    for requirement in requirements:
        if not requirement.withdrawn and requirement.id not in cited and requirement.id in defined:
            if defined[requirement.id] is requirement:
                errors.append(f"{requirement.id} has no test in {conformance.name}")
    return errors


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--spec", type=Path, default=ROOT / "spec" / "SPEC.md")
    parser.add_argument("--conformance", type=Path, default=ROOT / "spec" / "conformance.md")
    args = parser.parse_args(argv)
    errors = check(args.spec, args.conformance)
    for error in errors:
        print(error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
