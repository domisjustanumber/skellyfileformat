"""Golden folder G7 (recording-files/SPEC.md Appendix A): two copies of G3 whose manifest the reader cannot use, in
the cases `no_manifest` and `other_take_manifest`.

`no_manifest` is G3 with no `recording_manifest.json`. `other_take_manifest` is G3 whose manifest holds
another `take_uuid`. In each case, the reader rebuilds the links by a scan (SFF-731, SFF-867).
recording-files/golden/G07_G09_CHOICES.md gives each value that the spec does not give. This module also holds the
small helpers that g08.py and g09.py use.
"""

from __future__ import annotations

import json
from pathlib import Path

from goldgen import common, g03
from goldgen import folder_common as fc

MANIFEST = "recording_manifest.json"
OTHER_TAKE_UUID = "00000000000040008000000000000701"  # a take that is in no golden folder


def write_results(out: Path, case: str, result_of) -> None:
    """Write `<case>.full.json` and `<case>.player.json`. `result_of(scope)` gives the result."""
    for scope in ("full", "player"):
        (out / f"{case}.{scope}.json").write_bytes(common.canonical_json(result_of(scope)))


def link(take: dict, check: str) -> dict:
    (item,) = [item for item in take["links"] if item["check"] == check]
    return item


def load_json(path: Path) -> dict:
    return json.loads(path.read_bytes())


def replace_file(folder: Path, path: str, data: bytes) -> None:
    """Write a file of the take again. When the manifest lists it with a `sha256`, the manifest gets the
    new SHA-256 (SFF-723), so that the change is the only fault of the case."""
    (folder / path).write_bytes(data)
    if path != MANIFEST:
        manifest = load_json(folder / MANIFEST)
        for item in manifest["files"]:
            if item["path"] == path and item["sha256"] is not None:
                item["sha256"] = common.sha256_hex(data)
        (folder / MANIFEST).write_bytes(common.file_json(manifest))


def replace_json(folder: Path, path: str, change) -> None:
    """Change a JSON file of the take with `change(value)` and write it again (SFF-702)."""
    value = load_json(folder / path)
    change(value)
    replace_file(folder, path, common.file_json(value))


def rebuilt_result(facts: dict, scope: str, manifest: str) -> dict:
    """The result of G3 when the reader does not use the manifest (SFF-731, SFF-867, SFF-872, SFF-883)."""
    result = fc.expected_result(facts, scope)
    (take,) = result["takes"]
    take["manifest"] = manifest
    take["warnings"] = ["manifest_missing"]  # SFF-731: also when `manifest` is `invalid`
    # SFF-872: with no manifest, `camera_key` and `calibration` have no part. `files` has only its
    # Parquet part, which the scope `player` does not read (SFF-892).
    for check in ("camera_key", "calibration", *(("files",) if scope == "player" else ())):
        link(take, check)["state"] = "not_checked"
    return result


def build(out: Path) -> None:
    for case in ("no_manifest", "other_take_manifest"):
        folder = out / case
        facts, _, _ = g03.write_case(folder)
        if case == "no_manifest":
            (folder / MANIFEST).unlink()
            write_results(out, case, lambda scope: rebuilt_result(facts, scope, "missing"))
            continue
        replace_json(folder, MANIFEST, lambda m: m.update(take_uuid=OTHER_TAKE_UUID))

        def result_of(scope: str) -> dict:
            result = rebuilt_result(facts, scope, "invalid")
            # SFF-867: no take uses the manifest, and it holds a `take_uuid`. The scope `player`
            # reads it, because it is a JSON file (SFF-892).
            result["other_files"] = [{"name": MANIFEST, "state": "invalid", "reason": "take_fact_mismatch"}]
            result["folder_warnings"] = ["orphan_file"]
            return result

        write_results(out, case, result_of)
