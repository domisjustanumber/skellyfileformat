"""Golden folder G9 (spec/SPEC.md Appendix A): link mismatch vectors, one case for each vector.

Each case is a copy of G3 with one fault, and each other file agrees with the fault: when a case
changes a file, the hashes that point at that file get the new value (SFF-723, SFF-838), unless the
hash is the vector. So each case gives `mismatch` in exactly one check of SFF-872, or, for
`recording_id`, an `invalid` Parquet (SFF-824). golden/G07_G09_CHOICES.md gives each value that the
spec does not give. The camera of each camera vector is camera 1 (`group_position` 1).
"""

from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path

from goldgen import common, g01, g03
from goldgen import folder_common as fc
from goldgen.g07 import MANIFEST, link, load_json, replace_file, replace_json, write_results

OTHER_TAKE_UUID = "00000000000040008000000000000901"  # a take that is in no golden folder
OTHER_CALIBRATION_UUID = "00000000000040008000000000000902"  # a calibration that is in no golden folder
WRONG_HASH = common.sha256_hex(b"")  # the SHA-256 of a file with no bytes
WRONG_RECORDING_ID = "g09_other_take"
LARGER_IMAGE = {"width": 128, "height": 96}  # 2 x the stored 64 x 48
# Camera 0 of `row_counts` lost its last frame; camera 1 keeps 90 rows. Camera 1 has the last arrival,
# so the manifest summary does not change (SFF-728).
SHORT_CAMERA, SHORT_ROWS = 0, 89
CAMERA = 1

# The check that shows each vector (SFF-872), and true when the scope `player` evaluates a part of
# it: the vector is in a JSON file, not in the TOML or the Parquet (SFF-892).
CHECKS = {
    "take_uuid": ("take_uuid", True), "camera_key": ("camera_key", True), "frame_range": ("frames", False),
    "row_counts": ("frames", False), "dimensions": ("dimensions", False), "rotation_in_configs": ("rotation", True),
    "unresolved_file": ("files", False), "stale_parquet_sha256": ("hashes", False),
    "calibration_hash": ("hashes", False), "calibration_uuid": ("calibration", False), "recording_id": (None, False),
}  # fmt: skip


def replace_parquet(folder: Path, facts: dict, cameras: list[dict], files: list[dict], change_run=None, recording_id=None):
    """Write the Parquet again from these `files` records, then the processing info JSON (SFF-838).

    `change_run(run)` changes run 0. `recording_id` is a wrong `recording_id` of the Parquet alone.
    """
    import pyarrow.parquet as pq

    rec = facts["recording_name"]
    path = folder / f"{rec}_data.parquet"
    descriptor = json.loads(pq.read_schema(path).metadata[fc.DESCRIPTOR_KEY.encode()])
    run, rows = g03.run_and_rows(cameras, files)
    if change_run:
        change_run(run)
    descriptor["runs"] = {"0": run}
    fc.write_parquet(path, descriptor | {"recording_id": recording_id or rec}, rows)
    replace_file(folder, f"{rec}_recording_info.json", fc.processing_info(descriptor, path.read_bytes(), 0))


def short_take(folder: Path, facts: dict) -> list[dict]:
    """`row_counts`: camera 0 of G3 with 89 rows. Return the new `files` items (SFF-746)."""
    cameras = g01.cameras()
    camera = cameras[SHORT_CAMERA]
    camera |= {"rows": camera["rows"][:SHORT_ROWS], "flash_positions": [p for p in camera["flash_positions"] if p < SHORT_ROWS]}
    with tempfile.TemporaryDirectory() as temporary:
        other = Path(temporary) / "take"
        items = common.write_take(other, g01.TAKE, cameras, g01.audio())["files"]
        short, g3 = load_json(other / MANIFEST)["summary"], load_json(folder / MANIFEST)["summary"]
        assert all(short[k] == g3[k] for k in ("duration_s", "cameras")), "the manifest of G3 stays correct"
        for suffix in (".mkv", ".csv"):
            name = Path(items[SHORT_CAMERA]["name"]).with_suffix(suffix)
            shutil.copyfile(other / name, folder / name)
    # SFF-754: the multi-camera frames are 0 to the smallest count minus 1, so the Parquet has 89 frames.
    replace_parquet(folder, facts, cameras, [item | {"records": item["records"][:SHORT_ROWS]} for item in items[:2]])
    return items


def write_vector(case: str, folder: Path) -> dict:
    """Write G3 into `folder` with the fault of `case`. Return the facts for `folder_common.expected_result`."""
    facts, cameras, _ = g03.write_case(folder)
    rec, files = facts["recording_name"], facts["files"][:2]
    label, key = files[CAMERA]["camera_label"], files[CAMERA]["camera_key"]
    capture, processing = f"{rec}_info.json", f"{rec}_recording_info.json"

    if case == "take_uuid":
        replace_json(folder, processing, lambda v: v.update(take_uuid=OTHER_TAKE_UUID))
    elif case == "camera_key":
        # The capture info JSON holds another key for camera 1, with the same 6 first characters.
        new = key[:-1] + ("1" if key[-1] == "0" else "0")
        replace_json(folder, capture, lambda v: v.update(camera_configs={new if k == key else k: c for k, c in v["camera_configs"].items()}))

        def privacy(m: dict) -> None:  # SFF-881: `<key>` is a key of `camera_configs`
            for item in m["privacy"]["fields"]:
                item["field"] = item["field"].replace(f"/camera_configs/{key}/", f"/camera_configs/{new}/")
            m["privacy"]["fields"].sort(key=lambda item: (item["file"].encode(), item["field"].encode()))

        replace_json(folder, MANIFEST, privacy)
    elif case == "frame_range":
        # The Parquet has one frame more than each camera file: `frame_number` 90 (SFF-827).
        extra = [item | {"records": item["records"] + [[None] * 4 + [2 * item["records"][-1][4] - item["records"][-2][4]]]} for item in files]
        replace_parquet(folder, facts, cameras, extra)
    elif case == "row_counts":
        facts = facts | {"files": short_take(folder, facts)}
    elif case == "dimensions":
        replace_parquet(folder, facts, cameras, files, lambda run: run["reference_frames"][f"camera:{label}:image"].update(LARGER_IMAGE))
    elif case == "rotation_in_configs":
        replace_json(folder, capture, lambda v: v["camera_configs"][key].update(rotation=90))  # SFF-800
    elif case == "unresolved_file":
        name = f"{WRONG_RECORDING_ID}.{label}.mkv"
        replace_parquet(folder, facts, cameras, files, lambda run: run["sources"][f"camera:{label}"]["definition"].update(video_filename=name))
    elif case == "stale_parquet_sha256":
        replace_json(folder, processing, lambda v: v["processed"].update(parquet_sha256=WRONG_HASH))
    elif case == "calibration_hash":
        replace_json(folder, MANIFEST, lambda m: m["calibration"].update(sha256=WRONG_HASH))
    elif case == "calibration_uuid":
        # Only the manifest changes. Its summary keeps the values of the TOML (SFF-728).
        replace_json(folder, MANIFEST, lambda m: m["calibration"].update(calibration_uuid=OTHER_CALIBRATION_UUID))
    else:
        replace_parquet(folder, facts, cameras, files, recording_id=WRONG_RECORDING_ID)
    return facts


def expected_result(case: str, facts: dict, scope: str) -> dict:
    result = fc.expected_result(facts, scope)
    (take,) = result["takes"]
    check, in_player = CHECKS[case]
    if check and (scope == "full" or in_player):
        link(take, check)["state"] = "mismatch"  # SFF-872: an evaluated part fails
    if scope == "player":
        return result  # SFF-892: no `stale_processing_info`, and the Parquet is `not_checked`
    if case == "stale_parquet_sha256":
        take["warnings"] = ["stale_processing_info"]  # SFF-874
    if case == "recording_id":
        (item,) = [item for item in take["folder_files"] if item["role"] == "tracking"]
        item |= {"state": "invalid", "reason": "take_fact_mismatch"}  # SFF-824; `prerelease` stays (SFF-891)
        # SFF-872: no part that needs the Parquet is evaluated. `dimensions` has no other part. Each
        # other check has a part that passes.
        link(take, "dimensions")["state"] = "not_checked"
    return result


def build(out: Path) -> None:
    for case in CHECKS:
        facts = write_vector(case, out / case)
        write_results(out, case, lambda scope: expected_result(case, facts, scope))
