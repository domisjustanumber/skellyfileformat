"""Golden folder G11 (recording-files/SPEC.md Appendix A): header and row error vectors.

Each case is a copy of the case `take` of G1 in which only the sidecar of camera 1 has a change. A
reader refuses that sidecar (the state `invalid`). A changed row has a correct CRC, so the row has
only one fault.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from goldgen import capture_cases, common, g01

ROW = 1  # the position of the changed row
SOURCE, ARRIVAL = 1, 2  # the fields of a row


def _header(key: str, value: str | None):
    """Give a header key another value, or remove its line."""

    def change(lines: list[str]) -> None:
        (index,) = [i for i, line in enumerate(lines) if line.startswith(f"# {key}=")]
        lines[index : index + 1] = [] if value is None else [f"# {key}={value}"]

    return change


def _row(field: int, edit):
    def change(lines: list[str]) -> None:
        index = next(i for i, line in enumerate(lines) if not line.startswith("#")) + 1 + ROW
        fields = lines[index].split(",")[:-1]
        fields[field] = edit(fields[field])
        lines[index] = common.csv_row(fields)[:-1]

    return change


# The case, the change of the sidecar and the reason of the reader, with its requirement.
CASES = {
    "leading_zero": (_row(SOURCE, lambda text: "0" + text), "bad_metadata"),  # SFF-701
    "plus_sign": (_row(ARRIVAL, lambda text: "+" + text), "bad_metadata"),  # SFF-701
    "row_integer_2_53": (_row(SOURCE, lambda text: str(2**53)), "bad_metadata"),  # SFF-701
    "rate_0_1": (_header("nominal_rate", "0/1"), "bad_rate"),  # SFF-750
    "rate_2_20_plus_1": (_header("nominal_rate", f"{2**20 + 1}/1"), "bad_rate"),  # SFF-750
    "rotation_45": (_header("display_rotation", "45"), "bad_rotation"),  # SFF-751
    "bad_label": (_header("camera_label", "nothex"), "bad_label"),  # SFF-753
    "missing_key": (_header("nominal_rate", None), "missing_metadata"),  # SFF-748
    "unknown_clock": (_header("clock", "fake_clock"), "bad_metadata"),  # SFF-772
}


def build(out: Path) -> None:
    first = next(iter(CASES))
    facts = common.write_take(out / first, g01.TAKE, g01.cameras(), g01.audio())
    for case in list(CASES)[1:]:
        shutil.copytree(out / first, out / case)
    good = facts["files"][1]
    for case, (change, reason) in CASES.items():
        sidecar = (out / case / good["name"]).with_suffix(".csv")
        lines = sidecar.read_bytes().decode().split("\n")
        change(lines)
        sidecar.write_bytes("\n".join(lines).encode())
        refused = good | {
            "state": "invalid", "reason": reason, "rows": None, "torn_bytes": None, "fit": None,  # SFF-885
            "camera_label": None if case == "bad_label" else good["camera_label"],  # SFF-885
            "warnings": ["prerelease"], "records": None,  # no usable row, so no `gap` (SFF-887)
        }  # fmt: skip
        capture_cases.write_results(out, case, facts | {"files": [facts["files"][0], refused, facts["files"][2]]})
