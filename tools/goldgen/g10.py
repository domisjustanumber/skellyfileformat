"""Golden folder G10 (recording-files/SPEC.md Appendix A): version vectors (SPEC.md section 3).

The cases are `higher_minor` (G3 with `2.1`), `unknown_major_sidecar` and `unknown_major_folder_file`
(G1 with `3.0` in one file), `higher_minor_journal` (G13 with a journal of `2.1`) and `prerelease_0`
(G1 with `format_prerelease` 0). recording-files/golden/G10_G13_G14_CHOICES.md gives each value that the spec does not
give.
"""

from __future__ import annotations

import contextlib
import json
from pathlib import Path

from goldgen import capture_cases, common, g01, g03, g13
from goldgen import folder_common as fc

FLAG_ROW, FLAG_BIT_7 = 10, 128  # the row of camera 0 of `higher_minor` with the unknown flag bit 7


@contextlib.contextmanager
def versions(version: str = common.FORMAT_VERSION, prerelease: int = common.FORMAT_PRERELEASE):
    """Write the files of the block with other version fields.

    shortcut: this changes the globals of `common` for the block, because the shared writers read
    them at each call; upgrade to a parameter of the shared writers when a second user needs it.
    """
    old = common.FORMAT_VERSION, common.FORMAT_PRERELEASE
    common.FORMAT_VERSION, common.FORMAT_PRERELEASE = version, prerelease
    try:
        yield
    finally:
        common.FORMAT_VERSION, common.FORMAT_PRERELEASE = old


def _replace_once(path: Path, old: bytes, new: bytes) -> bytes:
    data = path.read_bytes()
    assert data.count(old) == 1, (path, old)
    path.write_bytes(data.replace(old, new))
    return path.read_bytes()


def _add_x_future_to_sidecar(path: Path, flag_row: int | None) -> None:
    """`x_future` as the last header key and as a column before `crc32` (SFF-709). Each row gets a new CRC."""
    lines = path.read_bytes().decode().split("\n")
    column = next(i for i, line in enumerate(lines) if not line.startswith("#"))
    assert lines[column].endswith(",crc32")
    lines[column] = lines[column][: -len("crc32")] + "x_future,crc32"
    for i in range(column + 1, len(lines)):
        if lines[i].startswith("#") or not lines[i]:
            break  # the footer
        fields = lines[i].rsplit(",", 1)[0].split(",")
        if i - column - 1 == flag_row:
            assert fields[4] == "0"
            fields[4] = str(FLAG_BIT_7)  # SFF-709: a reader ignores a flag bit that it does not know
        lines[i] = common.csv_row([*fields, 1])[:-1]
    lines.insert(column, "# x_future=1")
    path.write_bytes("\n".join(lines).encode())


def _add_member(path: Path) -> bytes:
    data = common.file_json(json.loads(path.read_bytes()) | {"x_future": 1})  # the last member
    path.write_bytes(data)
    return data


def higher_minor(case: Path) -> dict:
    with versions("2.1"):
        facts, _, _ = g03.write_case(case)
    for item in facts["files"]:
        _add_x_future_to_sidecar(case / Path(item["name"]).with_suffix(".csv"), FLAG_ROW if item is facts["files"][0] else None)
    rec = facts["recording_name"]
    hashes = {path: common.sha256_hex(_add_member(case / path)) for path in (f"{rec}_info.json", f"{rec}_recording_info.json")}
    label = facts["files"][0]["camera_label"]
    toml = case / f"{rec}_camera_calibration.toml"
    _replace_once(toml, b"\n[metadata.board]\n", b"x_future = 1\n\n[metadata.board]\n")
    toml_bytes = _replace_once(toml, f"\n[{label}.controls_at_calibration]\n".encode(), f"x_future = 1\n\n[{label}.controls_at_calibration]\n".encode())
    # The manifest gets the hashes of the changed files (SFF-723) and its own `x_future`.
    manifest_path = case / capture_cases.MANIFEST
    manifest = json.loads(manifest_path.read_bytes())
    for item in manifest["files"]:
        item["sha256"] = hashes.get(item["path"], item["sha256"])
    manifest["calibration"]["sha256"] = common.sha256_hex(toml_bytes)
    manifest_path.write_bytes(common.file_json(manifest | {"x_future": 1}))
    return facts


def refused(item: dict) -> dict:
    """A file with a `major` that the reader does not know (SFF-708), with the conventions of an `invalid` file."""
    return item | {
        "state": "unsupported_version", "reason": None, "rows": None, "torn_bytes": None, "fit": None,  # SFF-885
        "records": None,
    }  # fmt: skip


def build(out: Path) -> None:
    # higher_minor: each version field is 2.1; the reader gives the result of G3 (SFF-709).
    facts = higher_minor(out / "higher_minor")
    for scope in ("full", "player"):
        (out / f"higher_minor.{scope}.json").write_bytes(common.canonical_json(fc.expected_result(facts, scope)))

    # unknown_major_sidecar: the sidecar of camera 1 has 3.0.
    case = out / "unknown_major_sidecar"
    facts = common.write_take(case, g01.TAKE, g01.cameras(), g01.audio())
    _replace_once((case / facts["files"][1]["name"]).with_suffix(".csv"), b"# format_version=2.0\n", b"# format_version=3.0\n")
    files = [facts["files"][0], refused(facts["files"][1] | {"warnings": ["prerelease"]}), facts["files"][2]]
    capture_cases.write_results(out, case.name, facts | {"files": files})  # SFF-872: `frames` has one finished file

    # unknown_major_folder_file: the capture info JSON has 3.0.
    case = out / "unknown_major_folder_file"
    facts = common.write_take(case, g01.TAKE, g01.cameras(), g01.audio())
    info = _replace_once(case / facts["info_path"], b'"format_version": "2.0"', b'"format_version": "3.0"')
    manifest_path = case / capture_cases.MANIFEST
    manifest = json.loads(manifest_path.read_bytes())
    manifest["files"][0]["sha256"] = common.sha256_hex(info)
    manifest_path.write_bytes(common.file_json(manifest))
    for scope in ("full", "player"):
        result = common.expected_result(facts, scope)
        result["takes"][0]["folder_files"][0] |= {"state": "unsupported_version", "reason": None}  # SFF-886
        (out / f"{case.name}.{scope}.json").write_bytes(common.canonical_json(result))

    # higher_minor_journal: G13 with a journal header of 2.1 and one good record of the type 200.
    g13.write_results(out, "higher_minor_journal", g13.write_case(out / "higher_minor_journal", "2.1", unknown_record=True))

    # prerelease_0: each file has `format_prerelease` 0, so no file has the warning `prerelease` (SFF-891).
    with versions(prerelease=0):
        facts = common.write_take(out / "prerelease_0", g01.TAKE, g01.cameras(), g01.audio())
    for scope in ("full", "player"):
        result = common.expected_result(facts, scope)
        (take,) = result["takes"]
        for item in take["files"] + take["folder_files"]:
            item["warnings"] = [code for code in item["warnings"] if code != "prerelease"]
        (out / f"prerelease_0.{scope}.json").write_bytes(common.canonical_json(result))
