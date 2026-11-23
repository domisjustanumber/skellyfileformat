"""Shared helpers of the conformance tests SFT-735 to SFT-770 (recording-files/conformance.md, decision G21H).

Each `*_faults(folder)` function is a check on a take folder that needs no implementation: it returns a
list of texts, one for each fault, and `[]` for a folder that obeys the Pass text. freemocap writes the
Parquet, the TOML, the journal and the processing info JSON (decision G21H item 4), so this repository
tests those files with these checks on the golden folders.

This module imports no implementation. It gets pyarrow, numpy and PyAV with `pytest.importorskip`.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import shutil
import struct
import subprocess
import tomllib
import zlib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
GOLDEN = ROOT / "golden"
MEDIA = "synchronized_videos"

# ---------------------------------------------------------------- general


def golden_cases() -> list[tuple[str, str]]:
    """Each case under `recording-files/golden/` at collection time: a folder with `<case>.full.json` beside it."""
    if not GOLDEN.is_dir():
        return []
    return sorted(
        (group.name, case.name)
        for group in GOLDEN.glob("G[0-9][0-9]")
        for case in group.iterdir()
        if case.is_dir() and case.with_name(case.name + ".full.json").is_file()
    )


# The cases of G9 and the member of the result that shows each vector (SPEC.md Appendix A, SFF-872).
G09_CHECKS = {
    "take_uuid": "take_uuid", "camera_key": "camera_key", "frame_range": "frames", "row_counts": "frames",
    "dimensions": "dimensions", "rotation_in_configs": "rotation", "unresolved_file": "files",
    "stale_parquet_sha256": "hashes", "calibration_hash": "hashes", "calibration_uuid": "calibration",
    "recording_id": None,
}  # fmt: skip


def not_run_here() -> None:
    """The body of a test that this repository does not run. Its mark skips it before this line."""
    pytest.fail("this repository does not run this test; its mark must skip it", pytrace=False)


def load_json(path: Path):
    return json.loads(path.read_bytes())


def write_json(path: Path, value) -> None:
    """Write a JSON file of the format with the conventions of the golden folders (indent 2, one LF)."""
    path.write_bytes((json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode())


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest(folder: Path) -> dict:
    return load_json(folder / "recording_manifest.json")


def one(folder: Path, pattern: str) -> Path:
    """The one file of the folder that matches the pattern."""
    found = sorted(folder.glob(pattern))
    assert len(found) == 1, f"{folder.name}: {len(found)} files match {pattern}"
    return found[0]


def capture_info(folder: Path) -> Path:
    """The capture info JSON `<rec>_info.json` of a take folder."""
    (found,) = [path for path in folder.glob("*_info.json") if not path.name.endswith("_recording_info.json")]
    return found


def committed(folder: Path, scope: str = "full") -> dict:
    """The committed reader result beside a golden case folder."""
    return load_json(folder.with_name(f"{folder.name}.{scope}.json"))


# ---------------------------------------------------------------- the readers


def read_bytes(kind: str, reader, js_reader, folder: Path, records: bool = True) -> bytes:
    """The canonical JSON of one reader. `kind` is `full` or `player` (Python) or `js` (JavaScript)."""
    if kind == "js":
        return js_reader(folder, records=records)
    return reader.canonical_json(reader.read_folder(folder, records=records, scope=kind))


def read(reader, folder: Path, scope: str = "full", records: bool = False) -> dict:
    """The reader result of the Python reader, parsed from its canonical JSON."""
    return json.loads(reader.canonical_json(reader.read_folder(folder, records=records, scope=scope)))


def the_take(result: dict) -> dict:
    assert len(result["takes"]) == 1, f"the result has {len(result['takes'])} takes"
    return result["takes"][0]


def link(take: dict, check: str) -> str:
    return {item["check"]: item["state"] for item in take["links"]}[check]


def folder_file(take: dict, suffix: str) -> dict:
    """The `folder_files` item whose path ends with `suffix`."""
    found = [item for item in take["folder_files"] if item["path"].endswith(suffix)]
    assert len(found) == 1, f"{len(found)} folder_files items end with {suffix}"
    return found[0]


def named(items: list[dict], name: str) -> dict:
    found = [item for item in items if item["name"] == name]
    assert len(found) == 1, f"{len(found)} items have the name {name}"
    return found[0]


# ---------------------------------------------------------------- the reader result (section 23)

REASONS = {
    "bad_metadata", "missing_metadata", "bad_rate", "bad_rotation", "bad_label", "bad_time", "crc_mismatch",
    "take_fact_mismatch", "missing_media", "bad_schema", "code_in_file",
}  # fmt: skip
TAKE_WARNINGS = {
    "incomplete_take", "duplicate_label", "take_fact_mismatch", "extra_files", "manifest_missing",
    "camera_key_zero", "stale_processing_info", "summary_stale", "calibration_mismatch", "realtime_run",
}  # fmt: skip
FILE_WARNINGS = {"missing_fit", "encode_skip", "gap", "prerelease"}
FOLDER_WARNINGS = {"multiple_takes", "stray_tmp", "orphan_file"}
LEGACY_WARNINGS = [
    "legacy_calibration_unverified", "legacy_fake_confidence", "legacy_marker_order", "legacy_nonrigid_alignment",
]  # fmt: skip
FILE_STATES = {"unsupported_version", "invalid", "damaged", "unfinished", "repaired", "finished", "not_in_format"}
FOLDER_FILE_STATES = {"present", "missing", "invalid", "not_checked", "unsupported_version", "unfinished", "damaged"}
LINKS = ["take_uuid", "camera_key", "frames", "dimensions", "rotation", "files", "hashes", "calibration"]
PLAYER_UNREAD = (".toml", ".parquet", ".bin", ".npy", ".npz")  # SFF-892: the scope `player` reads none of them
PLAYER_LINKS = ("frames", "dimensions", "hashes", "calibration")
FULL_ONLY_WARNINGS = {"stale_processing_info", "calibration_mismatch", "realtime_run"}
FILE_MEMBERS = {"name", "kind", "state", "reason", "camera_key", "camera_label", "rows", "torn_bytes", "fit", "warnings"}
TAKE_MEMBERS = {
    "take_uuid", "recording_name", "state", "manifest", "warnings", "may_contain_private_data", "files",
    "folder_files", "links",
}  # fmt: skip
JOURNAL_MEMBERS = {"records", "rejected_records", "torn_bytes"}


def canonical(value) -> bytes:
    """The RFC 8785 form of a value with no float. A reader result holds no float (SFF-885)."""
    if isinstance(value, dict):
        keys = sorted(value, key=lambda key: key.encode("utf-16-be"))
        return b"{" + b",".join(canonical(key) + b":" + canonical(value[key]) for key in keys) + b"}"
    if isinstance(value, list):
        return b"[" + b",".join(canonical(item) for item in value) + b"]"
    assert not isinstance(value, float), "a reader result holds no float"
    return json.dumps(value, ensure_ascii=False).encode()


def _warnings_faults(where: str, codes: list, allowed) -> list[str]:
    faults = [f"{where}: the code {code} is not allowed" for code in codes if code not in allowed]
    if codes != sorted(set(codes)):
        faults.append(f"{where}: the warnings are not sorted, or a code is there two times")
    return faults


def _path_faults(where: str, path: str) -> list[str]:
    bad = "\\" in path or path.startswith("/") or ".." in path.split("/") or re.match(r"[A-Za-z]:", path)
    return [f"{where}: `{path}` is not a path relative to the take folder with `/`"] if bad else []


def result_faults(raw: bytes) -> list[str]:
    """The faults of one reader result against SFF-885, SFF-886, SFF-887 and SFF-890 (SFT-768)."""
    result = json.loads(raw)
    faults = [] if raw == canonical(result) else ["the bytes are not the canonical form of RFC 8785"]
    top = {"result_version", "folder_state", "folder_warnings", "takes", "other_files", "legacy"}
    if set(result) != top:
        return [*faults, f"the members of the result are {sorted(result)}"]
    if result["result_version"] != 2 or isinstance(result["result_version"], bool):
        faults.append("result_version is not 2")
    if result["folder_state"] not in {"ok", "unreadable", "legacy", "empty"}:
        faults.append(f"folder_state is {result['folder_state']}")
    faults += _warnings_faults("folder_warnings", result["folder_warnings"], FOLDER_WARNINGS)
    if [take["take_uuid"] for take in result["takes"]] != sorted(take["take_uuid"] for take in result["takes"]):
        faults.append("the takes are not in order of take_uuid")
    for take in result["takes"]:
        where = f"take {take.get('take_uuid')}"
        if set(take) != TAKE_MEMBERS:
            faults.append(f"{where}: the members are {sorted(take)}")
            continue
        if take["state"] not in {"complete", "incomplete"} or take["manifest"] not in {"present", "missing", "invalid"}:
            faults.append(f"{where}: state {take['state']}, manifest {take['manifest']}")
        if not isinstance(take["may_contain_private_data"], bool):
            faults.append(f"{where}: may_contain_private_data is not a boolean")
        faults += _warnings_faults(where, take["warnings"], TAKE_WARNINGS)
        kinds = [item.get("kind") for item in take["files"]]
        if kinds != sorted(kinds, key=["camera", "audio"].index):
            faults.append(f"{where}: an audio file is before a camera file")
        for item in take["files"]:
            at = f"{where}, file {item.get('name')}"
            if set(item) - {"records"} != FILE_MEMBERS:
                faults.append(f"{at}: the members are {sorted(item)}")
                continue
            faults += _path_faults(at, item["name"]) + _warnings_faults(at, item["warnings"], FILE_WARNINGS)
            if item["state"] not in FILE_STATES or item["reason"] not in REASONS | {None}:
                faults.append(f"{at}: state {item['state']}, reason {item['reason']}")
            if item["kind"] == "audio" and (item["camera_key"], item["camera_label"]) != (None, None):
                faults.append(f"{at}: an audio item has a camera_key or a camera_label")
            if item["camera_key"] is not None and not isinstance(item["camera_key"], str):
                faults.append(f"{at}: camera_key is not a text")
            refused = item["state"] in {"invalid", "unsupported_version"}
            numbers = [item["rows"], item["torn_bytes"], item["fit"]]
            if refused and numbers != [None, None, None]:
                faults.append(f"{at}: rows, torn_bytes and fit are not null")
            if not refused and (type(item["rows"]) is not int or type(item["torn_bytes"]) is not int):
                faults.append(f"{at}: rows or torn_bytes is not an integer")
            if not refused and not isinstance(item["fit"], bool):
                faults.append(f"{at}: fit is not a boolean")
            if refused and item.get("records") is not None:
                faults.append(f"{at}: a refused item has records that are not null")  # ADR-FB8P item 3, ADR-783H item 8
            for record in item.get("records") or []:
                if len(record) != 5 or any(value is not None and type(value) is not int for value in record):
                    faults.append(f"{at}: the record {record} does not have 5 integers or nulls")
                    break
        paths = [item.get("path", "") for item in take["folder_files"]]
        if paths != sorted(paths, key=str.encode):
            faults.append(f"{where}: folder_files is not in order of the bytes of the path")
        for item in take["folder_files"]:
            at = f"{where}, folder file {item.get('path')}"
            journal = JOURNAL_MEMBERS if item.get("role") == "realtime_journal" else set()
            if set(item) != {"path", "role", "state", "reason", "warnings"} | journal:
                faults.append(f"{at}: the members are {sorted(item)}")
                continue
            faults += _path_faults(at, item["path"]) + _warnings_faults(at, item["warnings"], FILE_WARNINGS)
            if item["state"] not in FOLDER_FILE_STATES or item["reason"] not in REASONS | {None}:
                faults.append(f"{at}: state {item['state']}, reason {item['reason']}")
            if any(item[member] is not None and type(item[member]) is not int for member in journal):
                faults.append(f"{at}: a count of the journal is not an integer or null")
        if [item.get("check") for item in take["links"]] != LINKS:
            faults.append(f"{where}: links does not hold each check one time in the order of SFF-872")
        for item in take["links"]:
            if set(item) != {"check", "state", "detail"} or item["detail"] is not None:
                faults.append(f"{where}: the link {item.get('check')} has other members, or a detail")
            elif item["state"] not in {"ok", "mismatch", "not_checked"}:
                faults.append(f"{where}: the link {item['check']} has the state {item['state']}")
    names = [item.get("name", "") for item in result["other_files"]]
    if names != sorted(names, key=str.encode):
        faults.append("other_files is not in order of the bytes of the path")
    for item in result["other_files"]:
        at = f"other file {item.get('name')}"
        if set(item) != {"name", "state", "reason"}:
            faults.append(f"{at}: the members are {sorted(item)}")
            continue
        faults += _path_faults(at, item["name"])
        if item["state"] not in FILE_STATES or item["reason"] not in REASONS | {None}:
            faults.append(f"{at}: state {item['state']}, reason {item['reason']}")
    legacy = result["legacy"]
    if legacy is not None:
        if set(legacy) != {"family", "release_range", "ambiguous", "eras", "warnings", "calibration"}:
            faults.append(f"legacy: the members are {sorted(legacy)}")
        else:
            faults += _warnings_faults("legacy", legacy["warnings"], LEGACY_WARNINGS)
            if legacy["family"] not in {"v1", "pre_v1", "unknown"} or result["takes"] != []:
                faults.append("legacy: the family is not known, or the result has a take")
    return faults


def scope_faults(full: dict, player: dict) -> list[str]:
    """The faults of a `player` result against the `full` result of the same folder (SFF-892, SFT-769)."""
    faults = []
    full, player = json.loads(json.dumps(full)), json.loads(json.dumps(player))  # the lines below change them
    if len(full["takes"]) != len(player["takes"]):
        return ["the two results do not have the same number of takes"]
    for take_full, take_player in zip(full["takes"], player["takes"], strict=True):
        where = f"take {take_player['take_uuid']}"
        if [item["path"] for item in take_full["folder_files"]] != [item["path"] for item in take_player["folder_files"]]:
            faults.append(f"{where}: the paths of folder_files differ")
            continue
        for item_full, item_player in zip(take_full["folder_files"], take_player["folder_files"], strict=True):
            unread = item_player["path"].endswith(PLAYER_UNREAD)
            if unread and item_full["state"] != "missing":
                want = {"state": "not_checked", "reason": None, "warnings": []}
                want |= {member: None for member in JOURNAL_MEMBERS if member in item_full}
                if {member: item_player.get(member, "absent") for member in want} != want:
                    faults.append(f"{where}: {item_player['path']} is not `not_checked` with null and empty members")
                item_full.update(want)
                item_player.update(want)
        states = {item["check"]: item["state"] for item in take_player["links"]}
        faults += [f"{where}: the link {check} is {states[check]}" for check in PLAYER_LINKS if states[check] != "not_checked"]
        if FULL_ONLY_WARNINGS & set(take_player["warnings"]):
            faults.append(f"{where}: the player result has a warning of the scope full")
        take_full["warnings"] = [code for code in take_full["warnings"] if code not in FULL_ONLY_WARNINGS]
        take_full["links"] = take_player["links"] = None  # the four other checks can have fewer parts
    if full["legacy"] is not None and full["legacy"]["family"] == "v1":
        want = full["legacy"] | {
            "release_range": ["v1.0.25", "v1.8.2"], "ambiguous": True, "eras": [], "warnings": LEGACY_WARNINGS,
        }  # fmt: skip
        if player["legacy"] != want:
            faults.append(f"legacy: the player result has {player['legacy']}")
        full["legacy"] = player["legacy"] = None
    if full != player:
        faults.append("a member that SFF-892 does not name differs between the two results")
    return faults


# ---------------------------------------------------------------- timing sidecars

GAP, ENCODE_SKIP = 1, 4  # SFF-756


def header(csv: Path) -> dict[str, str]:
    """The header keys of a timing sidecar."""
    pairs = {}
    for line in csv.read_text(encoding="utf-8").split("\n"):
        if not line.startswith("# "):
            break
        key, _, value = line[2:].partition("=")
        pairs[key] = value
    return pairs


def set_header(csv: Path, key: str, value: str) -> None:
    """Change one header value of a timing sidecar. The header has no CRC."""
    text = csv.read_bytes().decode()
    changed, count = re.subn(rf"(?m)^# {re.escape(key)}=.*$", f"# {key}={value}", text, count=1)
    assert count == 1, f"{csv.name} has no header key {key}"
    csv.write_bytes(changed.encode())


def row_flags(csv: Path) -> list[int]:
    """The `flags` value of each data row of a finished video sidecar."""
    lines = [line for line in csv.read_text(encoding="utf-8").split("\n") if line and not line.startswith("#")]
    column = lines[0].split(",").index("flags")
    return [int(line.split(",")[column]) for line in lines[1:]]


def file_warning_faults(folder: Path, result: dict) -> list[str]:
    """SFT-768: a finished camera file has the file warning `gap` or `encode_skip` only when a row has that flag."""
    faults = []
    for item in the_take(result)["files"]:
        if item["kind"] == "camera" and item["state"] == "finished":
            flags = row_flags((folder / item["name"]).with_suffix(".csv"))
            for code, bit in (("gap", GAP), ("encode_skip", ENCODE_SKIP)):
                if (code in item["warnings"]) != any(value & bit for value in flags):
                    faults.append(f"{item['name']}: the file warning {code} does not agree with the flags of the rows")
    return faults


def strict_ns(player_ns: list[int]) -> list[int]:
    """The strict player times of SFF-782."""
    strict: list[int] = []
    for p in player_ns:
        strict.append(max(p, strict[-1] + 1) if strict else p)
    return strict


def strict_by_label(folder: Path) -> dict[str, list[int]]:
    """The strict player times of each camera of a golden case, from the `records` of its committed result."""
    files = [item for take in committed(folder)["takes"] for item in take["files"] if item["kind"] == "camera"]
    return {item["camera_label"]: strict_ns([record[4] for record in item["records"]]) for item in files}


# ---------------------------------------------------------------- capture info JSON (section 13, SFT-735)

CONTROLS = {
    "exposure_us", "gain", "white_balance_k", "focus", "zoom", "pan_deg", "tilt_deg", "power_line_hz",
    "auto_exposure_priority", "brightness", "contrast", "saturation", "sharpness", "gamma", "backlight_compensation",
}  # fmt: skip
INFO_MEMBERS = ["skellyspecs", "format_version", "format_prerelease", "writer", "take_uuid"]
CONFIG_MEMBERS = ["camera_label", "user_name", "key_origin", "device", "requested", "controls", "exposure_step"]
DEVICE_MEMBERS = [
    "model", "os_name", "vendor_id", "product_id", "serial", "port_path", "os_device_id", "backend", "os_index",
]  # fmt: skip


def capture_info_faults(info: dict, camera_keys: list[str], microphone: str) -> list[str]:
    """The faults of a capture info JSON against the Pass text of SFT-735 (SFF-800, SFF-802)."""
    faults = []
    if list(info) != [*INFO_MEMBERS, "camera_configs", "audio"]:
        faults.append(f"the members are {list(info)}")
    if sorted(info.get("camera_configs", {})) != sorted(camera_keys):
        faults.append("camera_configs is not keyed by the camera_key of each camera")
    for key, config in info.get("camera_configs", {}).items():
        if list(config) != CONFIG_MEMBERS:
            faults.append(f"{key}: the members of the camera config are {list(config)}")
            continue
        if config["key_origin"] not in {"computed", "confirmed_by_user", "assigned", "provisional"}:
            faults.append(f"{key}: key_origin is {config['key_origin']}")
        if list(config["device"]) != DEVICE_MEMBERS:
            faults.append(f"{key}: the members of device are {list(config['device'])}")
        elif not isinstance(config["device"]["os_device_id"], (str, type(None))):
            faults.append(f"{key}: os_device_id is not a text or null")
        name = config["user_name"]
        if name is not None:
            good = isinstance(name, str) and 1 <= len(name.encode()) <= 128
            if not good or any(ord(c) < 32 or 127 <= ord(c) < 160 for c in name):
                faults.append(f"{key}: user_name is not a text of 1 to 128 bytes with no control character")
        if set(config["controls"]) - CONTROLS:
            faults.append(f"{key}: the control names {sorted(set(config['controls']) - CONTROLS)} are not in SFF-802")
    audio = info.get("audio")
    if not isinstance(audio, dict) or list(audio) != ["device_name", "host_api", "device_channels"]:
        faults.append("audio does not have the members device_name, host_api and device_channels")
    elif audio["device_name"] != microphone:
        faults.append("audio does not name the microphone")
    return faults


# ---------------------------------------------------------------- privacy list (section 22, SFT-766)


def privacy_fields(folder: Path) -> list[dict]:
    """The `fields` list that SFF-881 gives for the files of a take folder."""
    listed = manifest(folder)
    fields = [("recording_manifest.json", "/recording_name", "user_entered_name")]
    for index, camera in enumerate(listed["summary"]["cameras"]):
        fields += [
            ("recording_manifest.json", f"/summary/cameras/{index}/{member}", kind)
            for member, kind in (("user_name", "user_entered_name"), ("model", "device_name"))
            if camera[member] is not None
        ]
    timings = [camera["timing"] for camera in listed["cameras"]]
    timings += [listed["audio"]["timing"]] if listed["audio"] else []
    fields += [(path, "utc_offset_min", "time_zone") for path in timings if header(folder / path).get("utc_offset_min")]
    for item in listed["files"]:
        if item["role"] != "capture_info":
            continue
        info = load_json(folder / item["path"])
        device_kinds = {
            "model": "device_name", "os_name": "device_name", "serial": "serial_number", "port_path": "device_path",
            "os_device_id": "device_path",
        }  # fmt: skip
        for key, config in info["camera_configs"].items():
            if config["user_name"] is not None:
                fields.append((item["path"], f"/camera_configs/{key}/user_name", "user_entered_name"))
            fields += [
                (item["path"], f"/camera_configs/{key}/device/{member}", kind)
                for member, kind in device_kinds.items()
                if config["device"][member] is not None
            ]
        if info["audio"] is not None and info["audio"]["device_name"] is not None:
            fields.append((item["path"], "/audio/device_name", "device_name"))
    if listed["calibration"] is not None:
        toml = tomllib.loads((folder / listed["calibration"]["file"]).read_text(encoding="utf-8"))
        if "alignment_recording_id" in toml["metadata"]:
            fields.append((listed["calibration"]["file"], "metadata.alignment_recording_id", "user_entered_name"))
    return [{"file": file, "field": field, "kind": kind} for file, field, kind in sorted(fields)]


def privacy_faults(folder: Path) -> list[str]:
    privacy = manifest(folder)["privacy"]
    faults = [] if privacy["fields"] == privacy_fields(folder) else ["`fields` is not the sorted list of SFF-881"]
    return faults + ([] if privacy["media_shows_people"] is True else ["media_shows_people is not true"])


# ---------------------------------------------------------------- processing info JSON (section 14, SFT-737)

PROCESSED_MEMBERS = [
    "schema_version", "parquet_sha256", "recording_id", "parquet", "selected_run_id", "runs", "conventions",
    "export_inventories",
]  # fmt: skip
INFO_DATA_KINDS = {"LANDMARKS_3D", "KEYPOINTS_3D", "RAW_KEYPOINTS_3D", "OVERLAY_2D", "SEGMENT_ORIGINS", "ROTATIONS_WORLD"}


def channel_key(channel: dict) -> tuple:
    return (channel["sensor_group"], channel["source"], channel["reference_frame"], channel["kind"])


def processing_info_faults(folder: Path) -> list[str]:
    """The golden part of SFT-737 in stage 1a: the processing info JSON of a take alone. It reads no Parquet."""
    info = load_json(one(folder, "*_recording_info.json"))
    faults = []
    if list(info) != [*INFO_MEMBERS, "processed"] or info["skellyspecs"] != "processing_info":
        faults.append(f"the members are {list(info)}")
    processed = info["processed"]
    if list(processed) != PROCESSED_MEMBERS:
        faults.append(f"the members of processed are {list(processed)}")
    if str(processed["selected_run_id"]) not in processed["runs"]:
        faults.append("selected_run_id is not a key of runs")
    return faults


def processing_info_parquet_faults(folder: Path) -> list[str]:
    """The golden part of SFT-737 in stage 2: the processing info JSON of a take against its Parquet."""
    processed = load_json(one(folder, "*_recording_info.json"))["processed"]
    parquet = one(folder, "*_data.parquet")
    faults = []
    if processed["parquet_sha256"] != sha256(parquet):
        faults.append("parquet_sha256 is not the SHA-256 of the Parquet")
    runs = descriptor(parquet)["runs"]
    for run_id, run in processed["runs"].items():
        kinds = {channel_key(c) for c in runs[run_id]["channels"] if c["kind"] in INFO_DATA_KINDS}
        data = {(item["sensor_group"], item["source"], item["reference_frame"], item["channel"]) for item in run["data"]}
        if data != kinds:
            faults.append(f"run {run_id}: `channel` of a data item is not the `kind` of its descriptor channel")
    return faults


# ---------------------------------------------------------------- calibration TOML (section 15, SFT-738, SFT-739)

TOML_METADATA = {
    "format_version", "format_prerelease", "writer", "calibration_uuid", "reprojection_error_px", "initial_cost",
    "final_cost", "n_iterations", "solver_time_seconds", "n_observations_used", "n_observations_rejected", "aligned",
    "solver_method", "transformation_history", "board",
}  # fmt: skip
TOML_OPTIONAL = {"source_take_uuid"}  # "Absent when not known"
TOML_ALIGNMENT = {"alignment_method", "alignment_recording_id", "alignment_result"}
TOML_BOARD = {"squares_x", "squares_y", "square_length_mm", "marker_length_ratio", "aruco_dictionary_enum"}
TOML_CAMERA = {
    "name", "id", "camera_key", "camera_label", "index", "size", "matrix", "distortions", "rotation", "translation",
    "world_orientation", "world_position", "controls_at_calibration",
}  # fmt: skip


def rotation_matrix(rodrigues: list[float]):
    """The rotation matrix of a Rodrigues vector, as a numpy array."""
    np = pytest.importorskip("numpy")
    vector = np.array(rodrigues, dtype=float)
    angle = float(np.linalg.norm(vector))
    if angle == 0.0:
        return np.eye(3)
    x, y, z = vector / angle
    cross = np.array([[0, -z, y], [z, 0, -x], [-y, x, 0]])
    return np.eye(3) + math.sin(angle) * cross + (1 - math.cos(angle)) * cross @ cross


def rodrigues(matrix) -> list[float]:
    """The Rodrigues vector of a rotation matrix whose angle is less than 180 degrees."""
    np = pytest.importorskip("numpy")
    angle = math.acos(max(-1.0, min(1.0, (float(np.trace(matrix)) - 1) / 2)))
    if angle < 1e-12:
        return [0.0, 0.0, 0.0]
    axis = np.array([matrix[2][1] - matrix[1][2], matrix[0][2] - matrix[2][0], matrix[1][0] - matrix[0][1]])
    return (axis / (2 * math.sin(angle)) * angle).tolist()


def calibration_toml_faults(path: Path) -> list[str]:
    """The golden part of SFT-738: one calibration TOML against section 15."""
    np = pytest.importorskip("numpy")
    toml = tomllib.loads(path.read_text(encoding="utf-8"))  # tomllib reads TOML 1.0.0
    faults = []
    if next(iter(toml)) != "metadata":
        faults.append("[metadata] is not the first table")
    metadata = toml["metadata"]
    want = TOML_METADATA | (TOML_ALIGNMENT if metadata.get("aligned") is True else set())
    if set(metadata) - TOML_OPTIONAL != want:
        faults.append(f"the keys of [metadata] are {sorted(metadata)}")
    if set(metadata.get("board", {})) != TOML_BOARD:
        faults.append("the keys of the board are not those of section 15")
    cameras = {key: table for key, table in toml.items() if key != "metadata"}
    if [table.get("index") for table in cameras.values()] != sorted(table.get("index") for table in cameras.values()):
        faults.append("the camera tables are not in order of `index`")
    for key, table in cameras.items():
        if set(table) != TOML_CAMERA:
            faults.append(f"[{key}]: the keys are {sorted(table)}")
            continue
        if key != table["camera_label"]:
            faults.append(f"[{key}]: the key of the table is not the camera_label")
        if metadata.get("aligned") is False and table["index"] == 0 and table["rotation"] + table["translation"] != [0.0] * 6:
            faults.append(f"[{key}]: camera 0 does not have zero rotation and translation")
        if not np.allclose(np.array(table["world_orientation"]), rotation_matrix(table["rotation"]).T, rtol=0, atol=1e-9):
            faults.append(f"[{key}]: world_orientation is not the transpose of the rotation matrix")
    return faults


def toml_text(value: dict, name: str = "") -> str:
    """A TOML text of a parsed calibration TOML: the scalars of a table first, then its tables."""
    def scalar(item) -> str:
        if isinstance(item, bool):
            return "true" if item else "false"
        if isinstance(item, str):
            return json.dumps(item)
        if isinstance(item, list):
            return "[" + ", ".join(scalar(part) for part in item) + "]"
        if isinstance(item, dict):
            return "{" + ", ".join(f"{key} = {scalar(part)}" for key, part in item.items()) + "}"
        return repr(item)

    plain = {key: item for key, item in value.items() if not isinstance(item, dict)}
    text = (f"[{name}]\n" if name else "") + "".join(f"{key} = {scalar(item)}\n" for key, item in plain.items())
    tables = [toml_text(item, f"{name}.{key}" if name else key) for key, item in value.items() if isinstance(item, dict)]
    return "\n".join([text, *tables]) if text else "\n".join(tables)


def change_calibration(folder: Path, change) -> None:
    """Change the calibration TOML of a copy of a take with `change(toml, numpy)`.

    The manifest gets the new SHA-256, so that only the geometry differs from the committed case.
    """
    np = pytest.importorskip("numpy")
    listed = manifest(folder)
    path = folder / listed["calibration"]["file"]
    toml = tomllib.loads(path.read_text(encoding="utf-8"))
    change(toml, np)
    for key, table in toml.items():
        if key != "metadata":
            turned = rotation_matrix(table["rotation"]).T
            table["world_orientation"] = turned.tolist()
            table["world_position"] = (-turned @ np.array(table["translation"])).tolist()
    path.write_bytes(toml_text(toml).encode())
    listed["calibration"]["sha256"] = sha256(path)
    write_json(folder / "recording_manifest.json", listed)


def camera_tables(toml: dict) -> list[dict]:
    return sorted((table for key, table in toml.items() if key != "metadata"), key=lambda table: table["index"])


# ---------------------------------------------------------------- tracking Parquet (section 16)

DESCRIPTOR_KEY = b"freemocap.recording"
COLUMNS = [
    ("timestamp_s", "double", False), ("sensor_group", "string", False), ("frame_number", "int32", False),
    ("source", "string", False), ("reference_frame", "string", True), ("channel", "string", False),
    ("name", "string", False), ("component", "string", False), ("value", "float", True),
    ("value_f64", "double", True), ("units", "string", False), ("run_id", "int32", False),
]  # fmt: skip


def arrow():
    """pyarrow and pyarrow.parquet, or a skip when the group `conformance` is not installed."""
    return pytest.importorskip("pyarrow"), pytest.importorskip("pyarrow.parquet")


def descriptor(parquet: Path) -> dict:
    _, pq = arrow()
    return json.loads(pq.read_schema(parquet).metadata[DESCRIPTOR_KEY])


def rows_of(parquet: Path) -> list[dict]:
    _, pq = arrow()
    return pq.read_table(parquet).to_pylist()


def rewrite_parquet(folder: Path, change=None, int64: bool = False, rename: tuple[str, str] | None = None) -> Path:
    """Write the Parquet of a copy of a take again, with a changed descriptor or with int64 columns.

    `change(descriptor)` changes the descriptor in place, or returns a new one. `rename` is (old, new):
    a text to replace in the columns `source` and `reference_frame`. The processing info JSON gets the
    new `parquet_sha256`, so that only the Parquet differs from the committed case.
    """
    pa, pq = arrow()
    path = one(folder, "*_data.parquet")
    table = pq.read_table(path)
    if change is not None:
        changed = json.loads(table.schema.metadata[DESCRIPTOR_KEY])
        changed = change(changed) or changed
        text = json.dumps(changed, separators=(",", ":"), ensure_ascii=False).encode()
        table = table.replace_schema_metadata({**table.schema.metadata, DESCRIPTOR_KEY: text})
    if rename is not None:
        compute = pytest.importorskip("pyarrow.compute")
        for name in ("source", "reference_frame"):
            index = table.schema.get_field_index(name)
            table = table.set_column(index, table.schema.field(name), compute.replace_substring(table.column(name), *rename))
    if int64:
        for name in ("frame_number", "run_id"):
            index = table.schema.get_field_index(name)
            field = pa.field(name, pa.int64(), nullable=False)
            table = table.set_column(index, field, table.column(name).cast(pa.int64()))
    pq.write_table(
        table, path, compression="zstd", compression_level=3, use_dictionary=False,
        column_encoding={"value": "BYTE_STREAM_SPLIT", "value_f64": "BYTE_STREAM_SPLIT"},
    )  # fmt: skip
    info_path = one(folder, "*_recording_info.json")
    info = load_json(info_path)
    info["processed"]["parquet_sha256"] = sha256(path)
    write_json(info_path, info)
    return path


def schema_faults(parquet: Path) -> list[str]:
    """SFF-816, SFF-818 and SFF-823: the Arrow schema, the encodings and the row groups."""
    _, pq = arrow()
    file = pq.ParquetFile(parquet)
    schema = file.schema_arrow
    faults = []
    if [(field.name, str(field.type), field.nullable) for field in schema] != COLUMNS:
        faults.append("the Arrow schema is not the table of section 16")
    for group_index in range(file.metadata.num_row_groups):
        group = file.metadata.row_group(group_index)
        for column_index in range(group.num_columns):
            column = group.column(column_index)
            if column.compression != "ZSTD":
                faults.append(f"row group {group_index}, {column.path_in_schema}: the codec is {column.compression}")
            if column.path_in_schema in ("value", "value_f64"):
                if "BYTE_STREAM_SPLIT" not in column.encodings or column.has_dictionary_page:
                    faults.append(f"row group {group_index}, {column.path_in_schema}: {column.encodings}")
                if {"PLAIN_DICTIONARY", "RLE_DICTIONARY"} & set(column.encodings):
                    faults.append(f"row group {group_index}, {column.path_in_schema}: a dictionary encoding")
        rows = file.read_row_group(group_index, columns=["run_id", "sensor_group", "source", "reference_frame", "channel"])
        if len({tuple(row.values()) for row in rows.to_pylist()}) != 1:
            faults.append(f"row group {group_index} does not hold the rows of one channel")
    return faults


def run_channels(descriptor_: dict, run_id: int) -> dict[tuple, dict]:
    return {channel_key(channel): channel for channel in descriptor_["runs"][str(run_id)]["channels"]}


def row_channel(descriptor_: dict, row: dict) -> dict | None:
    key = (row["sensor_group"], row["source"], row["reference_frame"], row["channel"])
    return run_channels(descriptor_, row["run_id"]).get(key) if str(row["run_id"]) in descriptor_["runs"] else None


def row_value(channel: dict, row: dict):
    """The value of a row, from the column that the `dtype` of its channel names (SFF-820)."""
    return row["value_f64"] if channel["dtype"] == "float64" else row["value"]


def value_faults(parquet: Path) -> list[str]:
    """SFF-820 and SFF-821: each value is in the column of its `dtype`, and no value is NaN."""
    described = descriptor(parquet)
    faults = []
    for index, row in enumerate(rows_of(parquet)):
        channel = row_channel(described, row)
        if channel is None:
            faults.append(f"row {index}: no channel of the descriptor declares it")
            continue
        other = row["value"] if channel["dtype"] == "float64" else row["value_f64"]
        if other is not None:
            faults.append(f"row {index}: a value is in the column that the dtype does not name")
        value = row_value(channel, row)
        if value is not None and not math.isfinite(value):
            faults.append(f"row {index}: the value is NaN or infinite")
    return faults[:20]


def row_rule_faults(parquet: Path) -> list[str]:
    """The faults against the row rules 1 to 9 of parts/parquet-descriptor.md (SFF-822, SFF-831)."""
    described = descriptor(parquet)
    rows = rows_of(parquet)
    faults = []
    trajectories: dict[tuple, list[tuple]] = {}
    quaternions: list[tuple] = []
    points: dict[tuple, dict] = {}
    for index, row in enumerate(rows):
        channel = row_channel(described, row)
        declared = channel is not None and row["name"] in channel["names"]
        if not declared or channel["components"].get(row["component"]) != row["units"]:
            faults.append(f"rule 1, row {index}: the channel, name, component or units are not declared")
            continue
        value = row_value(channel, row)
        if row["frame_number"] < 0 or (value is not None and not math.isfinite(value)):
            faults.append(f"rule 2, row {index}")
        context = (row["run_id"], *channel_key(channel))
        key = (*context, row["name"], row["component"])
        trajectories.setdefault(key, []).append((row["frame_number"], row["timestamp_s"]))
        kind = row["channel"]
        if kind in ("ROTATIONS_LOCAL", "ROTATIONS_WORLD"):
            quaternions.append((*context, row["name"], row["frame_number"], row["component"], value))
        if kind == "TIMESTAMPS":
            good = (row["component"], row["units"], row["reference_frame"]) == ("timestamp_s", "s", None)
            if not good or value != row["timestamp_s"]:
                faults.append(f"rule 6, row {index}")
        if kind in ("OVERLAY_2D", "BOXES_2D"):
            points.setdefault((kind, *context, row["name"], row["frame_number"]), {})[row["component"]] = value
        if kind == "OVERLAY_2D" and row["source"].startswith("keypoint_model:") and row["name"].find(".") < 1:
            faults.append(f"rule 9, row {index}: the name {row['name']} has no tracker stage")
    for key, samples in trajectories.items():
        count = described["runs"][str(key[0])]["sensor_groups"][key[1]]["sample_count"]
        rising = all(a[0] < b[0] and a[1] < b[1] for a, b in zip(samples, samples[1:]))
        if len(samples) != count or not rising:
            faults.append(f"rule 3, trajectory {key}: {len(samples)} rows for sample_count {count}, rising {rising}")
    grids: dict[tuple, list] = {}
    for key, samples in trajectories.items():
        if grids.setdefault(key[:4], samples) != samples:  # (run_id, sensor_group, source, reference_frame)
            faults.append(f"rule 4, context {key[:4]}: the trajectories do not share one grid")
    for start in range(0, len(quaternions), 4):
        four = quaternions[start : start + 4]
        values = [item[-1] for item in four]
        together = len({item[:-2] for item in four}) == 1 and [item[-2] for item in four] == ["w", "x", "y", "z"]
        unit = all(v is None for v in values) or (
            None not in values and abs(math.sqrt(sum(v * v for v in values)) - 1) <= 1e-5
        )
        if not together or not unit:
            faults.append(f"rule 5: the quaternion rows at {four[0][:-2]}")
    for key, values in points.items():
        if key[0] == "OVERLAY_2D":
            visibility = values.get("visibility")
            absent = values.get("x") is None or values.get("y") is None
            good = visibility is None or 0 <= visibility <= 1
            if absent:  # SFF-831: not detected, or a frame that a realtime run skipped
                good = good and values.get("x") is None and values.get("y") is None and visibility in (0, None)
            if not good:
                faults.append(f"rule 7: the point {key[1:]}")
        elif not (all(v is None for v in values.values()) or values.get("detector_ran") in (0, 1)):
            faults.append(f"rule 8: the box {key[1:]}")
    return faults[:20]


def group_times(folder: Path, described: dict, run_id: int) -> tuple[dict, dict]:
    """The strict time of each camera frame, and the group time m of each frame of each sensor group (SFF-828)."""
    strict = strict_by_label(folder)
    members: dict[str, list[str]] = {}
    for channel in described["runs"][str(run_id)]["channels"]:
        if channel["kind"] == "TIMESTAMPS" and channel["source"].startswith("camera:"):
            members.setdefault(channel["sensor_group"], []).append(channel["source"].split(":", 1)[1])
    groups = {
        group: [(2 * sum(times) + len(times)) // (2 * len(times)) for times in zip(*(strict[label] for label in labels))]
        for group, labels in members.items()
    }
    return strict, groups


def time_faults(folder: Path, run_id: int) -> list[str]:
    """SFF-827 and SFF-828: the times of the rows of one run against the timing sidecars of a golden case."""
    parquet = one(folder, "*_data.parquet")
    described = descriptor(parquet)
    strict, groups = group_times(folder, described, run_id)
    faults = []
    for index, row in enumerate(rows_of(parquet)):
        if row["run_id"] != run_id:
            continue
        frame = row["frame_number"]
        if row["channel"] == "TIMESTAMPS" and row["source"].startswith("camera:"):
            times = strict[row["source"].split(":", 1)[1]]
        elif row["channel"] in ("OVERLAY_2D", "BOXES_2D"):
            times = strict[row["reference_frame"].split(":")[1]]  # `camera:<label>:image`
        else:
            times = groups[row["sensor_group"]]
        if not 0 <= frame < len(times):
            faults.append(f"row {index}: frame_number {frame} is not a position of a frame")
        elif row["timestamp_s"] != times[frame] / 10**9:  # the division of two integers gives the nearest float64
            faults.append(f"row {index}: timestamp_s is not the time of frame {frame}")
        elif row["channel"] == "TIMESTAMPS" and row["value_f64"] != row["timestamp_s"]:
            faults.append(f"row {index}: the value of the TIMESTAMPS row is not its time")
    return faults[:20]


def stored_size(camera_file: Path) -> tuple[int, int]:
    """The width and height of the stored JPEG frames of a camera file. PyAV decodes (decision G21H item 8)."""
    av = pytest.importorskip("av")
    with av.open(str(camera_file)) as container:
        stream = container.streams.video[0]
        return stream.width, stream.height


def spaces_faults(folder: Path) -> list[str]:
    """SFF-829 and SFF-830 (SFT-749): the image references and the 3D reference frame of a take."""
    parquet = one(folder, "*_data.parquet")
    described = descriptor(parquet)
    faults = []
    sizes = {}
    for run_id, run in described["runs"].items():
        cameras = {s["definition"]["camera_label"]: s["definition"] for s in run["sources"].values() if s["kind"] == "camera"}
        for label, definition in cameras.items():
            frame = run["reference_frames"].get(f"camera:{label}:image")
            size = stored_size(folder / MEDIA / definition["video_filename"])
            sizes[(run_id, f"camera:{label}:image")] = size
            if frame is None or (frame["width"], frame["height"]) != size:
                faults.append(f"run {run_id}: the image reference of {label} does not have the stored size {size}")
        for channel in run["channels"]:
            if channel["kind"] == "OVERLAY_2D" and [channel["components"].get(c) for c in ("x", "y")] != ["px", "px"]:
                faults.append(f"run {run_id}: a 2D channel is not in pixels")
        world = run["reference_frames"].get("calibrated_world")
        if len(cameras) >= 2 and (world is None or (world["basis"], world["units"]) != ("blender_x_right_y_forward_z_up", "mm")):
            faults.append(f"run {run_id}: the 3D reference frame is not calibrated_world with the Blender basis, in mm")
    # Each 2D value is a pixel of the stored JPEG, before `display_rotation` (SFF-829).
    for row in rows_of(parquet):
        size = sizes.get((str(row["run_id"]), row["reference_frame"]))
        if row["channel"] == "OVERLAY_2D" and size and row["component"] in ("x", "y") and row["value"] is not None:
            if not 0 <= row["value"] < size[row["component"] == "y"]:
                faults.append(f"run {row['run_id']}: a 2D {row['component']} of {row['reference_frame']} is outside the stored frame")
                break
    return faults


def sources_and_skeletons_faults(folder: Path) -> list[str]:
    """SFF-826 and SFF-832 (SFT-750): the camera sources and the models of each run."""
    described = descriptor(one(folder, "*_data.parquet"))
    members = {"camera_key", "camera_label", "video_filename", "timing_filename", "timing_method", "inferred_offset_s"}
    faults = []
    for run_id, run in described["runs"].items():
        for name, source in run["sources"].items():
            if source["kind"] != "camera":
                continue
            definition = source["definition"]
            if set(definition) != members or name != f"camera:{definition.get('camera_label')}":
                faults.append(f"run {run_id}, {name}: the definition has {sorted(definition)}")
                continue
            for file_name in (definition["video_filename"], definition["timing_filename"]):
                if "/" in file_name or "\\" in file_name or not (folder / MEDIA / file_name).is_file():
                    faults.append(f"run {run_id}, {name}: `{file_name}` is not a file name of the media folder")
        for model_id, model in run["models"].items():
            keypoints = set(model["tracker_keypoint_names"])
            pairs = model.get("tracker_connections")
            if pairs is not None and (pairs == [] or any(set(pair) - keypoints for pair in pairs)):
                faults.append(f"run {run_id}, model {model_id}: tracker_connections is empty or has an unknown name")
            want = [
                {
                    "name": segment["name"], "parent": model["rest_pose"]["parents"][segment["name"]],
                    "proximal": segment["frame"]["origin"], "distal": segment["frame"]["primary_point"],
                }
                for segment in model["skeleton"]["segments"]
            ]  # fmt: skip
            if model.get("segment_topology") != want:
                faults.append(f"run {run_id}, model {model_id}: segment_topology is not that of SFF-832")
    if list(folder.rglob("tracker_schema.json")):
        faults.append("a tracker_schema.json exists")
    return faults


def charuco_faults(folder: Path) -> list[str]:
    """SFF-836 (SFT-753): the Parquet of a calibration take."""
    parquet = one(folder, "*_data.parquet")
    board = tomllib.loads(one(folder, "*_camera_calibration.toml").read_text(encoding="utf-8"))["metadata"]["board"]
    source = f"charuco_detector:{board['squares_x']}x{board['squares_y']}"
    rows = rows_of(parquet)
    faults = [] if len(descriptor(parquet)["runs"]) == 1 else ["the Parquet does not have one run"]
    kinds = {row["channel"] for row in rows}
    if kinds != {"TIMESTAMPS", "OVERLAY_2D"}:
        faults.append(f"the channel kinds of the rows are {sorted(kinds)}")
    for row in rows:
        if row["channel"] == "OVERLAY_2D" and (row["source"] != source or not re.fullmatch(r"corner_(0|[1-9][0-9]*)", row["name"])):
            faults.append(f"a ChArUco row has the source {row['source']} and the name {row['name']}")
            break
    return faults


# ---------------------------------------------------------------- the descriptor (parts/parquet-descriptor.md)

TXT, INT, FLT, BOOL, OBJ = "text", "integer", "float", "boolean", "object"


def opt(spec):
    return ("null", spec)


def arr(spec, count: int | None = None):
    return ("array", spec, count)


def mp(spec):
    return ("map", spec)


def closed(members: dict, omit: tuple = (), defaults: tuple = ()):
    """`omit`: the members that a writer omits when empty or null. `defaults`: the members whose row gives a default."""
    return ("closed", members, frozenset(omit), frozenset(defaults))


def either(*specs):
    return ("either", specs)


_FRAME = closed({
    "origin": TXT, "primary_point": TXT, "primary_axis": arr(INT, 2), "secondary_point": opt(TXT),
    "secondary_axis": opt(arr(INT, 2)), "handedness": INT,
})  # fmt: skip
_MATERIAL = closed({"color": TXT, "opacity": FLT})
_CHANNEL = closed({
    "sensor_group": TXT, "source": TXT, "reference_frame": opt(TXT), "kind": TXT, "names": arr(TXT),
    "components": mp(TXT), "stage": TXT, "dtype": TXT,
}, defaults=("dtype",))  # fmt: skip
_CONTOURS = closed({
    **dict.fromkeys(("segment", "crown", "chin", "left_ear", "right_ear", "left_eye", "right_eye"), TXT),
    "vertical_exponent": FLT, "horizontal_exponent": FLT, "posterior_depth": FLT, "samples": INT, "nose": opt(TXT),
    "line_material": opt(_MATERIAL), "shell_material": opt(_MATERIAL), "side_material": opt(_MATERIAL),
}, defaults=(
    "vertical_exponent", "horizontal_exponent", "posterior_depth", "samples", "nose", "line_material", "shell_material",
    "side_material",
))  # fmt: skip
_PRESENTATION = closed({
    "contours": arr(_CONTOURS), "excluded_origin_edges": arr(arr(TXT, 2)), "excluded_bones": arr(TXT),
    "connection_materials": arr(closed({"group": TXT, "material": _MATERIAL})),
}, defaults=("contours", "excluded_origin_edges", "excluded_bones", "connection_materials"))  # fmt: skip
_SKELETON = closed({
    "name": TXT,
    "landmarks": arr(closed({"name": TXT, "definition": TXT, "position": arr(FLT, 3), "segment": TXT, "aliases": arr(TXT)})),
    "segments": arr(closed({
        "name": TXT, "landmarks": arr(TXT), "frame": _FRAME, "aliases": arr(TXT), "anatomical_segment": opt(TXT),
        "observation_frame": _FRAME,
    }, omit=("observation_frame",))),
    "joints": arr(closed({
        "name": TXT, "parent": TXT, "child": TXT, "connect_at": TXT, "joint_type": TXT,
        "convention": closed({"sequence": TXT, "angle_names": arr(TXT, 3), "zero_offsets": arr(FLT, 3)}, defaults=("zero_offsets",)),
    })),
    "chains": arr(closed({"name": TXT, "segments": arr(TXT), "joints": arr(TXT)})),
    "landmark_groups": arr(closed({"name": TXT, "landmark_names": arr(TXT), "tags": arr(TXT)})),
    "landmark_connections": arr(closed({"name": TXT, "pairs": arr(arr(TXT, 2)), "tags": arr(TXT)})),
    "derived_quantities": arr(TXT), "coordinate_system": TXT, "presentation": _PRESENTATION,
}, omit=("presentation",))  # fmt: skip
_GEOMETRY = closed({
    "feature_names": arr(TXT), "segment_name": TXT, "source_mesh_units": TXT, "mesh_sha256": opt(TXT),
    "reference_unit_mm": FLT, "object_to_segment_reference": arr(FLT, 16),
    "source_mesh_to_segment_reference": arr(FLT, 16), "segment_reference_to_source_mesh": arr(FLT, 16),
})  # fmt: skip
MODEL = closed({
    "model_id": TXT, "detector_type": TXT, "tracker_keypoint_names": arr(TXT), "tracker_connections": arr(arr(TXT, 2)),
    "segment_topology": arr(closed({"name": TXT, "parent": opt(TXT), "proximal": TXT, "distal": TXT})),
    "skeleton": _SKELETON,
    "rest_pose": closed({
        "name": TXT, "root_segment_name": TXT, "parents": mp(opt(TXT)), "connect_ats": mp(TXT),
        "orientations": mp(closed(dict.fromkeys("wxyz", FLT))),
    }),
    "mappings": arr(closed({
        "entries": mp(either(TXT, arr(TXT), OBJ)), "prefix": opt(TXT), "known_tracker_keypoints": opt(arr(TXT)),
        "passthrough": BOOL,
    })),
    "center_of_mass": closed({"definitions": mp(closed({
        "name": TXT, "proximal": TXT, "distal": TXT, "weights": arr(closed({"landmark": TXT, "weight": FLT})),
        "sided": BOOL,
    }, defaults=("sided",)))}),
    "segment_masses": mp(FLT), "scale_reference_name": TXT, "anchor_segment_name": opt(TXT),
    "object_geometry": opt(_GEOMETRY), "tracker_stage_path": opt(arr(TXT)),
}, omit=("tracker_connections", "object_geometry", "tracker_stage_path"), defaults=("anchor_segment_name",))  # fmt: skip
_PROVENANCE = closed({
    "attempt_id": TXT, "recorded_at": TXT, "effective_settings": OBJ, "default_settings": opt(OBJ),
    "input_signatures": mp(TXT), "software": OBJ, "output_sources": arr(TXT), "limitations": arr(TXT),
    "base_run_id": opt(INT), "base_descriptor_signature": opt(TXT), "origin": TXT, "coverage": opt(OBJ),
}, defaults=("limitations",))  # fmt: skip
_RUN = closed({
    "calibration_updates": mp(closed({
        "calibration_uuid_before": TXT, "calibration_uuid_after": TXT, "transformations": arr(OBJ),
        "recording_id": opt(TXT),
    })),
    "scale_fits": arr(closed({
        "sensor_group": TXT, "source": TXT, "reference_frame": TXT, "units": TXT, "fit": opt(OBJ), "inputs": OBJ,
    })),
    "camera_geometry": mp(arr(closed({
        "id": TXT, "camera_key": TXT, "index": INT, "image_size": arr(INT, 2),
        "intrinsics": closed(dict.fromkeys(("fx", "fy", "cx", "cy", "k1", "k2", "p1", "p2"), FLT), defaults=("k1", "k2", "p1", "p2")),
        "extrinsics": closed({"quaternion_wxyz": arr(FLT, 4), "translation": arr(FLT, 3)}),
        "world_position": arr(FLT, 3), "world_orientation": arr(arr(FLT, 3), 3),
    }, defaults=("world_position", "world_orientation")))),
    "sensor_groups": mp(closed({"clock_description": TXT, "sample_count": INT})),
    "sources": mp(closed({"kind": TXT, "definition": OBJ})),
    "reference_frames": mp(OBJ), "models": mp(MODEL), "processing": mp(OBJ), "channels": arr(_CHANNEL),
    "static_channels": arr(closed({"channel": _CHANNEL, "values": mp(mp(FLT))})),
    "checkpoints": arr(closed({"sensor_group": TXT, "stage": TXT, "signature": TXT})),
}, defaults=("calibration_updates", "scale_fits", "camera_geometry", "static_channels", "checkpoints"))  # fmt: skip
RECORDING = closed({
    "schema_version": INT, "format_version": TXT, "format_prerelease": INT, "writer": TXT, "take_uuid": TXT,
    "recording_id": TXT, "recording_info": OBJ, "runs": mp(_RUN),
})  # fmt: skip
_CAMERA_SOURCE = closed({
    "camera_key": TXT, "camera_label": TXT, "video_filename": TXT, "timing_filename": TXT, "timing_method": TXT,
    "inferred_offset_s": FLT,
})  # fmt: skip
_IMAGE_FRAME = closed({"camera_key": TXT, "calibration_camera": opt(TXT), "width": INT, "height": INT})
_PROVENANCE_SET = closed({"version": INT, "stages": mp(_PROVENANCE)})


def _number(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def structure_faults(value, spec, path: str = "$", reader: bool = False) -> list[str]:
    """The structure faults of a JSON value against a type of the part ("Structure rules and writer rules").

    With `reader`, a member whose row gives a default can be absent, and a member that a writer omits
    can be null (ADR-H2HQ item 2). Else the check is the one of a writer.
    """
    if isinstance(spec, str):
        good = {
            TXT: isinstance(value, str), INT: _number(value) and float(value).is_integer(), FLT: _number(value),
            BOOL: isinstance(value, bool), OBJ: isinstance(value, dict),
        }[spec]  # fmt: skip
        return [] if good else [f"{path}: not {spec}"]
    kind = spec[0]
    if kind == "null":
        return [] if value is None else structure_faults(value, spec[1], path, reader)
    if kind == "either":
        return [] if any(not structure_faults(value, part, path, reader) for part in spec[1]) else [f"{path}: no allowed type"]
    if kind == "array":
        if not isinstance(value, list) or (spec[2] is not None and len(value) != spec[2]):
            return [f"{path}: not an array" + (f" of {spec[2]} items" if spec[2] else "")]
        return [fault for index, item in enumerate(value) for fault in structure_faults(item, spec[1], f"{path}[{index}]", reader)]
    if not isinstance(value, dict):
        return [f"{path}: not an object"]
    if kind == "map":
        return [fault for key, item in value.items() for fault in structure_faults(item, spec[1], f"{path}.{key}", reader)]
    members, omit = spec[1], spec[2]
    may_lack = omit | spec[3] if reader else omit
    faults = [f"{path}: the member {name} is missing" for name in members if name not in value and name not in may_lack]
    faults += [f"{path}: the unknown member {name}" for name in value if name not in members]
    for name, part in members.items():
        # Of the omitted members, only an array (`tracker_connections`) is "omitted when empty", not "when null".
        if name in value and not (reader and name in omit and value[name] is None and part[0] != "array"):
            faults += structure_faults(value[name], part, f"{path}.{name}", reader)
    return faults


def descriptor_structure_faults(described: dict, reader: bool = False) -> list[str]:
    """The structure faults of a whole descriptor: the root, each run, and the objects that depend on a name."""
    faults = structure_faults(described, RECORDING, reader=reader)
    for run_id, run in described.get("runs", {}).items():
        if not isinstance(run, dict):
            continue
        at = f"$.runs.{run_id}"
        for name, source in run.get("sources", {}).items():
            if isinstance(source, dict) and source.get("kind") == "camera":
                faults += structure_faults(source.get("definition"), _CAMERA_SOURCE, f"{at}.sources.{name}.definition", reader)
        for name, frame in run.get("reference_frames", {}).items():
            if re.fullmatch(r"camera:[^:]+:image", name):
                faults += structure_faults(frame, _IMAGE_FRAME, f"{at}.reference_frames.{name}", reader)
        for group, processing in run.get("processing", {}).items():
            if isinstance(processing, dict) and "stage_provenance" in processing:
                where = f"{at}.processing.{group}.stage_provenance"
                faults += structure_faults(processing["stage_provenance"], _PROVENANCE_SET, where, reader)
    return faults


def _distinct(items) -> bool:
    items = [json.dumps(item) for item in items]
    return len(items) == len(set(items))


def _floats(value):
    if isinstance(value, dict):
        value = list(value.values())
    if isinstance(value, list):
        for item in value:
            yield from _floats(item)
    elif isinstance(value, float):
        yield value


def _mapping_keypoints(entry) -> list[str]:
    """The keypoint names of one mapping entry, in each of its four forms."""
    def ends(value) -> list[str]:
        return [value] if isinstance(value, str) else list(value)

    if isinstance(entry, str):
        return [entry]
    if isinstance(entry, list):
        return entry
    if entry.get("form") != "anatomical_offset":
        return list(entry)
    names = list(entry["origin"]) + ends(entry["reference_length"]["from"]) + ends(entry["reference_length"]["to"])
    return names + [name for axis in entry["frame"].values() for end in ("from", "to") for name in ends(axis[end])]


def model_rule_faults(model: dict) -> list[str]:
    """The faults of one `RecordedModel` against the writer rules of the part. The structure must be good.

    The rules of `SuperquadricContours` that need the compiled volume are not checked here
    (INTERFACE_NOTES_folder.md).
    """
    faults: list[str] = []

    def rule(good: bool, text: str) -> None:
        if not good:
            faults.append(text)

    skeleton, pose = model["skeleton"], model["rest_pose"]
    landmarks = {item["name"]: item for item in skeleton["landmarks"]}
    segments = {item["name"]: item for item in skeleton["segments"]}
    joints = {item["name"]: item for item in skeleton["joints"]}
    rule(all(math.isfinite(value) for value in _floats(model)), "a float is not finite")
    rule(bool(model["model_id"] and model["detector_type"] and model["scale_reference_name"]), "an empty text")
    keypoints = model["tracker_keypoint_names"]
    rule(bool(keypoints) and _distinct(keypoints), "tracker_keypoint_names is empty or has a name two times")
    if "tracker_connections" in model:
        pairs = model["tracker_connections"]
        rule(bool(pairs) and all(set(pair) <= set(keypoints) for pair in pairs), "tracker_connections")
    topology = [
        {"name": name, "parent": pose["parents"].get(name), "proximal": item["frame"]["origin"],
         "distal": item["frame"]["primary_point"]}
        for name, item in segments.items()
    ]  # fmt: skip
    rule(model["segment_topology"] == topology, "segment_topology is not that of SFF-832")
    rule(len(model["mappings"]) >= 1, "mappings is empty")
    rule(model["anchor_segment_name"] is None or model["anchor_segment_name"] in segments, "anchor_segment_name")
    # SkeletonSnapshot
    rule(bool(skeleton["name"] and skeleton["coordinate_system"]), "skeleton: an empty text")
    for member in ("landmarks", "segments", "joints", "chains", "landmark_groups", "landmark_connections"):
        rule(_distinct(item["name"] for item in skeleton[member]), f"skeleton.{member}: a name is there two times")
    rule(bool(landmarks) and bool(segments), "skeleton: no landmark or no segment")
    quantities = {"inertia", "extrapolated_center_of_mass", "center_of_pressure", "centroidal_moment_pivot", "roll_resolution"}
    derived = skeleton["derived_quantities"]
    rule(set(derived) <= quantities and derived == sorted(derived), "derived_quantities")
    owners = [name for item in segments.values() for name in item["landmarks"]]
    rule(sorted(owners) == sorted(landmarks), "each landmark is not in the landmarks of exactly one segment")
    segment_names = {alias for item in segments.values() for alias in [item["name"], *item["aliases"]]}
    rule(all(item["segment"] in segment_names for item in landmarks.values()), "a landmark names no segment")
    rule(_distinct(alias for item in landmarks.values() for alias in [item["name"], *item["aliases"]]), "two landmarks share a name or an alias")
    for item in [*landmarks.values(), *segments.values()]:
        aliases = item["aliases"]
        rule(_distinct(aliases) and "" not in aliases and item["name"] not in aliases, f"{item['name']}: aliases")
    rule(all(item["definition"] for item in landmarks.values()), "a landmark has an empty definition")
    for name, item in segments.items():
        rule(re.fullmatch(r"[a-z][a-z0-9]*(_[a-z0-9]+)*", name) is not None, f"segment {name}: the name")
        rule(item["frame"]["primary_point"] in item["landmarks"], f"segment {name}: primary_point is not its landmark")
        origin = item["frame"]["origin"]
        if origin in item["landmarks"] and origin in landmarks:
            rule(all(abs(v) <= 1e-9 for v in landmarks[origin]["position"]), f"segment {name}: the origin is not at 0")
        observed = item.get("observation_frame")
        if observed is not None:
            rule(None not in (observed["secondary_point"], observed["secondary_axis"]), f"segment {name}: observation_frame")
        for frame in filter(None, [item["frame"], observed]):
            points = [frame["origin"], frame["primary_point"], frame["secondary_point"]]
            rule(all(point is None or point in landmarks for point in points), f"segment {name}: a frame point is no landmark")
            rule(_distinct(point for point in points if point is not None), f"segment {name}: equal frame points")
            axes = [axis for axis in (frame["primary_axis"], frame["secondary_axis"]) if axis is not None]
            rule(all(axis[0] in (0, 1, 2) and axis[1] in (1, -1) for axis in axes), f"segment {name}: an axis")
            rule(len({axis[0] for axis in axes}) == len(axes), f"segment {name}: the two axes have one index")
            rule((frame["secondary_point"] is None) == (frame["secondary_axis"] is None), f"segment {name}: secondary")
            rule(frame["handedness"] in (1, -1), f"segment {name}: handedness")
    for name, item in joints.items():
        known = item["parent"] in segments and item["child"] in segments and item["child"] != item["parent"]
        rule(known, f"joint {name}: parent or child")
        rule(item["parent"] in segments and item["connect_at"] in segments[item["parent"]]["landmarks"], f"joint {name}: connect_at")
        rule(item["joint_type"] in {"ball", "hinge", "universal", "fixed"}, f"joint {name}: joint_type")
        sequence = item["convention"]["sequence"]
        good = re.fullmatch(r"[xyz]{3}", sequence) is not None and sequence[0] != sequence[1] != sequence[2]
        rule(good and _distinct(item["convention"]["angle_names"]), f"joint {name}: convention")
        rule(pose["parents"].get(item["child"]) == item["parent"], f"joint {name}: rest_pose.parents")
        rule(pose["connect_ats"].get(item["child"]) == item["connect_at"], f"joint {name}: rest_pose.connect_ats")
    rule(_distinct(name for item in joints.values() for name in item["convention"]["angle_names"]), "two joints share an angle name")
    if joints:
        children = [item["child"] for item in joints.values()]
        rule(_distinct(children) and len(set(segments) - set(children)) == 1, "the joints do not make one tree")
        parent_of = {item["child"]: item["parent"] for item in joints.values()}
        for start in parent_of:
            seen, at = set(), start
            while at in parent_of and at not in seen:
                seen.add(at)
                at = parent_of[at]
            rule(at not in seen, f"the joints make a cycle at {start}")
    if "inertia" in derived:
        rule(all(item["anatomical_segment"] is not None for item in segments.values()), "inertia with no anatomical_segment")
    for item in skeleton["chains"]:
        good = len(item["segments"]) >= 3 and len(item["joints"]) == len(item["segments"]) - 1
        rule(good and set(item["segments"]) <= set(segments) and set(item["joints"]) <= set(joints), f"chain {item['name']}")
    for item in skeleton["landmark_groups"]:
        names = item["landmark_names"]
        rule(bool(names) and _distinct(names) and set(names) <= set(landmarks), f"landmark group {item['name']}")
        rule(_distinct(item["tags"]) and "" not in item["tags"], f"landmark group {item['name']}: tags")
    for item in skeleton["landmark_connections"]:
        good = bool(item["pairs"]) and all(a != b and {a, b} <= set(landmarks) for a, b in item["pairs"])
        rule(good and _distinct(item["tags"]) and "" not in item["tags"], f"landmark connections {item['name']}")
    presentation = skeleton.get("presentation")
    if presentation is not None:
        rule(all(set(pair) <= set(segments) for pair in presentation["excluded_origin_edges"]), "excluded_origin_edges")
        rule(set(presentation["excluded_bones"]) <= set(segments), "excluded_bones")
        groups = [item["group"] for item in presentation["connection_materials"]]
        rule(_distinct(groups) and set(groups) <= {item["name"] for item in skeleton["landmark_connections"]}, "connection_materials")
        materials = [item["material"] for item in presentation["connection_materials"]]
        for contour in presentation["contours"]:
            at = f"contours of {contour['segment']}"
            materials += [contour[m] for m in ("line_material", "shell_material", "side_material") if contour[m]]
            points = ["crown", "chin", "left_ear", "right_ear", "left_eye", "right_eye"]
            own = segments.get(contour["segment"], {}).get("landmarks", [])
            named_points = [contour[point] for point in points] + ([contour["nose"]] if contour["nose"] else [])
            if contour["segment"] not in segments or not set(named_points) <= set(own) & set(landmarks):
                faults.append(f"{at}: the segment or a landmark")
                continue
            exponents = [contour[m] for m in ("vertical_exponent", "horizontal_exponent", "posterior_depth")]
            rule(all(0.2 <= value <= 2 for value in exponents) and 16 <= contour["samples"] <= 256, f"{at}: a range")
            x, y, z = ({point: landmarks[contour[point]]["position"][axis] for point in points} for axis in range(3))
            ears_z, eyes_z = (z["left_ear"] + z["right_ear"]) / 2, (z["left_eye"] + z["right_eye"]) / 2
            rule(z["crown"] > z["chin"], f"{at}: the crown is not above the chin")
            rule(z["chin"] < ears_z < z["crown"] and z["chin"] < eyes_z < z["crown"], f"{at}: the ears or the eyes")
            rule(x["left_ear"] != x["right_ear"], f"{at}: the ears have one x")
            rule(y["left_eye"] + y["right_eye"] > y["left_ear"] + y["right_ear"], f"{at}: the eyes are behind the ears")
        for material in materials:
            good = re.fullmatch(r"#[0-9a-fA-F]{6}", material["color"]) is not None and 0 <= material["opacity"] <= 1
            rule(good, f"the material {material}")
    # RestPoseSnapshot
    rule(pose["root_segment_name"] in segments, "rest_pose: the root is no segment")
    roots = [name for name, parent in pose["parents"].items() if parent is None]
    rule(set(pose["parents"]) == set(segments) and roots == [pose["root_segment_name"]], "rest_pose.parents")
    rule(all(parent is None or parent in segments for parent in pose["parents"].values()), "rest_pose.parents: a parent")
    rule(set(pose["connect_ats"]) == {item["child"] for item in joints.values()}, "rest_pose.connect_ats: the keys")
    rule(set(pose["orientations"]) == set(segments), "rest_pose.orientations: the keys")
    for name, q in pose["orientations"].items():
        rule(abs(math.sqrt(sum(q[c] ** 2 for c in "wxyz")) - 1) <= 1e-9, f"rest_pose.orientations.{name}: not unit")
    # TrackerMappingSnapshot
    for index, mapping in enumerate(model["mappings"]):
        at = f"mappings[{index}]"
        known = mapping["known_tracker_keypoints"]
        rule(set(mapping["entries"]) <= set(landmarks), f"{at}: a key of entries is no landmark")
        if mapping["passthrough"]:
            rule(mapping["entries"] == {} and bool(known), f"{at}: passthrough")
        if known is not None:
            rule(known == sorted(known), f"{at}: known_tracker_keypoints is not sorted")
            prefix = mapping["prefix"] or ""
            used = {prefix + name for entry in mapping["entries"].values() for name in _mapping_keypoints(entry)}
            rule(used <= set(known), f"{at}: a keypoint of entries is not in known_tracker_keypoints")
        for landmark, entry in mapping["entries"].items():
            if isinstance(entry, dict) and entry.get("form") == "anatomical_offset":
                good = set(entry) == {"form", "origin", "frame", "offset", "reference_length"} and len(entry["frame"]) == 2
                kinds = sorted(axis.get("kind") for axis in entry["frame"].values()) if good else []
                rule(good and kinds == ["approximate", "exact"] and bool(entry["origin"] and entry["offset"]), f"{at}.{landmark}")
            else:
                rule(bool(entry), f"{at}.{landmark}: an empty entry")
    # CenterOfMassDefinitions and segment_masses
    definitions = model["center_of_mass"]["definitions"]
    rule(bool(definitions) and all(key == item["name"] for key, item in definitions.items()), "center_of_mass: the keys")
    expanded = []
    for item in definitions.values():
        weights = [weight["weight"] for weight in item["weights"]]
        rule(bool(weights) and all(w > 0 for w in weights) and abs(sum(weights) - 1) <= 1e-6, f"center_of_mass {item['name']}: weights")
        for side in ("left_", "right_") if item["sided"] else ("",):
            expanded.append(side + item["name"])
            names = [item["proximal"], item["distal"], *(weight["landmark"] for weight in item["weights"])]
            rule({side + name for name in names} <= set(landmarks), f"center_of_mass {side}{item['name']}: a landmark")
    masses = model["segment_masses"]
    rule(sorted(masses) == sorted(expanded) and all(mass > 0 for mass in masses.values()), "segment_masses")
    geometry = model.get("object_geometry")
    rule(geometry is None or geometry["reference_unit_mm"] > 0, "object_geometry.reference_unit_mm")
    return faults


def descriptor_faults(folder: Path) -> list[str]:
    """SFF-817, SFF-824 and SFF-825 (SFT-746): the descriptor of the Parquet of a take validates against the part."""
    described = descriptor(one(folder, "*_data.parquet"))
    faults = descriptor_structure_faults(described)
    if faults:
        return faults
    if described["schema_version"] != 2 or "selected_run_id" in described:
        faults.append("schema_version is not 2, or the descriptor has selected_run_id")
    listed = manifest(folder)
    if (described["take_uuid"], described["recording_id"]) != (listed["take_uuid"], listed["recording_name"]):
        faults.append("take_uuid or recording_id is not that of the take")
    if described["format_version"] != "2.0" or not described["writer"]:
        faults.append("the format version or the writer")
    for run_id, run in described["runs"].items():
        at = f"run {run_id}"
        keys = [channel_key(c) for c in run["channels"]] + [channel_key(s["channel"]) for s in run["static_channels"]]
        if len(keys) != len(set(keys)):
            faults.append(f"{at}: two channels have one key")
        for channel in run["channels"]:
            known = channel["sensor_group"] in run["sensor_groups"] and channel["source"] in run["sources"]
            framed = channel["reference_frame"] is None or channel["reference_frame"] in run["reference_frames"]
            if not known or not framed or channel["dtype"] != ("float64" if channel["kind"] == "TIMESTAMPS" else channel["dtype"]):
                faults.append(f"{at}: the channel {channel_key(channel)}")
            if channel["dtype"] not in ("float32", "float64"):
                faults.append(f"{at}: the dtype of {channel_key(channel)}")
        for model_id, model in run["models"].items():
            if model["model_id"] != model_id:
                faults.append(f"{at}: models[{model_id}].model_id")
            faults += [f"{at}, model {model_id}: {fault}" for fault in model_rule_faults(model)]
    return faults


# ---------------------------------------------------------------- realtime journal (section 17)

MAGIC = b"SKRJ"
HEADER, DATA, EVENT, END = 1, 2, 3, 4
MISSING = bytes.fromhex("0000c07f")  # SFF-845: a missing value in the digest


def frame_record(kind: int, payload: bytes) -> bytes:
    """One framed record of the journal (the table of section 17)."""
    body = bytes([kind]) + payload
    return MAGIC + len(body).to_bytes(4, "little") + body + zlib.crc32(body).to_bytes(4, "little")


def scan_journal(data: bytes) -> dict:
    """The scan of SFF-843. `good` holds (offset, type, payload) of each good record."""
    found: list[tuple[str, int]] = []
    good = []
    at = 0
    while (o := data.find(MAGIC, at)) >= 0:
        length = int.from_bytes(data[o + 4 : o + 8], "little") if len(data) >= o + 8 else None
        in_range = length is not None and 1 <= length <= 2**26
        if length is None or (in_range and len(data) < o + 12 + length):
            found.append(("cut", o))
        elif not in_range or zlib.crc32(data[o + 8 : o + 8 + length]) != int.from_bytes(data[o + 8 + length : o + 12 + length], "little"):
            found.append(("rejected", o))
        else:
            found.append(("good", o))
            good.append((o, data[o + 8], data[o + 9 : o + 8 + length]))
            at = o + 12 + length
            continue
        at = o + 4
    last_good = max((index for index, (kind, _) in enumerate(found) if kind == "good"), default=-1)
    tail = next((index for index, (kind, _) in enumerate(found) if kind == "cut" and index > last_good), None)
    before_tail = found if tail is None else found[:tail]
    if tail is not None:
        torn = len(data) - found[tail][1]
    else:
        torn = next((size for size in (3, 2, 1) if data.endswith(MAGIC[:size])), 0)
    return {
        "good": good, "records": len(good), "rejected_records": sum(kind != "good" for kind, _ in before_tail),
        "torn_bytes": torn, "has_end": any(kind == END for _, kind, _ in good), "torn_tail": tail is not None,
    }  # fmt: skip


def journal_counts(scan: dict) -> dict:
    return {member: scan[member] for member in ("records", "rejected_records", "torn_bytes")}


def journal_header(scan: dict) -> dict:
    return json.loads(scan["good"][0][2])


def data_records(scan: dict) -> list[tuple]:
    """(channel_index, frame_number, processed_ns, n, k, the bytes of the values) of each good data record."""
    return [(*struct.unpack_from("<HiqII", payload), payload[22:]) for _, kind, payload in scan["good"] if kind == DATA]


def counted_records(scan: dict) -> dict[tuple[int, int], tuple]:
    """The data records that count in SFF-845: the last in file order for each channel and frame."""
    return {(record[0], record[1]): record for record in data_records(scan)}


def journal_faults(folder: Path) -> list[str]:
    """The golden part of SFT-756: the good records of the journal of a take."""
    scan = scan_journal(one(folder, "*_realtime_journal.bin").read_bytes())
    faults = []
    if not scan["good"] or scan["good"][0][1] != HEADER:
        return ["the first record is not the header"]
    channels = {channel["channel_index"]: channel for channel in journal_header(scan)["channels"]}
    if any(channel["dtype"] != "float32" for channel in channels.values()):
        faults.append("a channel does not declare the dtype float32")
    if any(channel["kind"] == "TIMESTAMPS" for channel in channels.values()):
        faults.append("a channel has the kind TIMESTAMPS")
    frames = min(len(times) for times in strict_by_label(folder).values())
    for index, frame, _, n, k, values in data_records(scan):
        if len(values) != 4 * n * k:
            faults.append(f"a data payload of channel {index} does not have 22 + 4 × n × k bytes")
        if index not in channels:
            faults.append(f"a data record names the channel {index}, which the header does not declare")
        if not 0 <= frame < frames:
            faults.append(f"frame_number {frame} is not a position of a multi-camera frame of the take")
        for (value,) in struct.iter_unpack("<f", values[: len(values) // 4 * 4]):
            if math.isinf(value):
                faults.append("a value is infinite: a missing value is NaN")
    for _, kind, payload in scan["good"]:
        if kind == END:
            end = json.loads(payload)
            if "data_records" not in end or end.get("clean_close") is not True:
                faults.append("the end record does not have data_records and clean_close")
    return faults[:20]


def _percentile(latencies: list[int], part: float):
    """The nearest-rank percentile of SFF-834, in milliseconds, or null with no latency."""
    return sorted(latencies)[math.ceil(part * len(latencies)) - 1] / 10**6 if latencies else None


def realtime_runs(described: dict) -> list[str]:
    """The `run_id` of each run with a stage provenance of the origin `realtime` (SFF-835)."""
    return [
        run_id
        for run_id, run in described["runs"].items()
        if any(
            stage.get("origin") == "realtime"
            for processing in run["processing"].values()
            for stage in processing.get("stage_provenance", {}).get("stages", {}).values()
        )
    ]


def fold_faults(folder: Path) -> list[str]:
    """The golden part of SFT-751: the realtime run of a take against its journal and its timing sidecars."""
    scan = scan_journal(one(folder, "*_realtime_journal.bin").read_bytes())
    channels = {channel["channel_index"]: channel for channel in journal_header(scan)["channels"]}
    parquet = one(folder, "*_data.parquet")
    described = descriptor(parquet)
    counted = counted_records(scan)
    events = [json.loads(payload) for _, kind, payload in scan["good"] if kind == EVENT]
    faults = []
    if any(set(event) != {"time_ns", "stage", "parameter", "value"} for event in events):
        faults.append("an event does not have time_ns, stage, parameter and value")
    if any(event.get("stage") not in {"timing"} | {c["stage"] for c in channels.values()} for event in events):
        faults.append("an event names a stage that is not timing and not the stage of a channel: the fold must fail")
    runs = realtime_runs(described)
    if not runs:
        return ["no run has the origin realtime"]
    # The latency uses m at the time of the fold. After a repair the files hold only the new times,
    # so the check does not compare `latency_ms` of a repaired take (ADR-1P4N).
    repaired = any(item["state"] == "repaired" for take in committed(folder)["takes"] for item in take["files"])
    for run_id in runs:
        run = described["runs"][run_id]
        _, groups = group_times(folder, described, int(run_id))  # the sidecar times of the committed result, not the rows
        if run["checkpoints"] != []:
            faults.append(f"run {run_id}: a realtime run has checkpoints")
        for group, processing in run["processing"].items():
            for stage, provenance in processing["stage_provenance"]["stages"].items():
                at = f"run {run_id}, {group}, {stage}"
                coverage = provenance["coverage"]
                if provenance["origin"] != "realtime" or not isinstance(coverage, dict):
                    faults.append(f"{at}: the origin is not realtime, or coverage is not an object")
                    continue
                # The stage `timing` counts the records of each channel of the group (Q94).
                mine = {i for i, c in channels.items() if c["sensor_group"] == group and stage in ("timing", c["stage"])}
                records = [record for (index, _), record in counted.items() if index in mine]
                in_take = run["sensor_groups"][group]["sample_count"]
                processed = len({record[1] for record in data_records(scan) if record[0] in mine})
                latencies = [record[2] - groups[group][record[1]] for record in records] if group in groups else []
                if stage == "timing":  # one latency for each frame: the lowest of its records (Q94)
                    lowest: dict[int, int] = {}
                    for record, latency in zip(records, latencies):
                        lowest[record[1]] = min(latency, lowest.get(record[1], latency))
                    latencies = list(lowest.values())
                want = {
                    "frames_in_take": in_take, "frames_processed": processed, "skips": {"no_record": in_take - processed},
                    "journal_crc_rejects": scan["rejected_records"], "clean_close": scan["has_end"],
                    "latency_ms": {"p50": _percentile(latencies, 0.5), "p99": _percentile(latencies, 0.99)},
                    "events": [event for event in events if event.get("stage") == stage],
                }  # fmt: skip
                if repaired:
                    del want["latency_ms"]
                faults += [f"{at}: coverage.{member} is {coverage.get(member)}, not {value}" for member, value in want.items() if coverage.get(member) != value]
        by_key = {channel_key(channel): index for index, channel in channels.items()}
        frames_of: dict[int, set[int]] = {}
        for index, frame in counted:
            frames_of.setdefault(index, set()).add(frame)
        for row in rows_of(parquet):
            key = (row["sensor_group"], row["source"], row["reference_frame"], row["channel"])
            skipped = row["frame_number"] not in frames_of.get(by_key.get(key, -1), set())
            if str(row["run_id"]) == run_id and row["channel"] == "OVERLAY_2D" and skipped and row["value"] is not None:
                faults.append(f"run {run_id}: a skipped frame has a value that is not null")
                break
        faults += [f"run {run_id}: {fault}" for fault in time_faults(folder, int(run_id))]
    return faults[:20]


def journal_digest(folder: Path) -> tuple[int, str]:
    """The count and the digest of SFF-845, from the journal."""
    counted = counted_records(scan_journal(one(folder, "*_realtime_journal.bin").read_bytes()))
    digest, count = hashlib.sha256(), 0
    for key in sorted(counted):
        for (value,) in struct.iter_unpack("<f", counted[key][5]):
            digest.update(MISSING if math.isnan(value) else struct.pack("<f", value))
            count += 1
    return count, digest.hexdigest()


def parquet_digest(folder: Path) -> tuple[int, str]:
    """The count and the digest of SFF-845, from the rows of the realtime run of the Parquet."""
    scan = scan_journal(one(folder, "*_realtime_journal.bin").read_bytes())
    channels = {channel["channel_index"]: channel for channel in journal_header(scan)["channels"]}
    parquet = one(folder, "*_data.parquet")
    (run_id,) = realtime_runs(descriptor(parquet))
    values = {
        (row["sensor_group"], row["source"], row["reference_frame"], row["channel"], row["frame_number"], row["name"], row["component"]): row["value"]
        for row in rows_of(parquet)
        if str(row["run_id"]) == run_id
    }  # fmt: skip
    digest, count = hashlib.sha256(), 0
    for index, frame in sorted(counted_records(scan)):
        channel = channels[index]
        for name in channel["names"]:
            for component in channel["components"]:
                value = values[(*channel_key(channel), frame, name, component)]
                digest.update(MISSING if value is None else struct.pack("<f", value))
                count += 1
    return count, digest.hexdigest()


# ---------------------------------------------------------------- other Parquet readers (SFT-747)


def values_sha256(rows) -> str:
    """The digest of the Parquet values that recording-files/golden/README.md defines. Each row is a sequence in column order.

    A null is 00. Another value is 01 and then: a float64 as 8 bytes and a float32 as 4 bytes (IEEE 754,
    little-endian), an integer as 8 bytes (two's complement, little-endian), a text as its UTF-8 length
    in 4 bytes (little-endian) and its UTF-8 bytes.
    """
    digest = hashlib.sha256()
    for row in rows:
        values = list(row)
        assert len(values) == len(COLUMNS)
        for value, (_, kind, _) in zip(values, COLUMNS):
            if value is None:
                digest.update(b"\x00")
                continue
            if kind == "string":
                data = value.encode()
                data = struct.pack("<I", len(data)) + data
            elif kind == "float":
                data = struct.pack("<f", value)
                assert struct.unpack("<f", data)[0] == value, "a float32 value reads back as the same value"
            else:
                data = struct.pack("<d" if kind == "double" else "<q", value)
            digest.update(b"\x01" + data)
    return digest.hexdigest()


def pyarrow_rows(parquet: Path) -> list[list]:
    """Each row of a Parquet as a list in column order. pyarrow reads."""
    return [list(row.values()) for row in rows_of(parquet)]


HYPARQUET = """
import {asyncBufferFromFile, parquetReadObjects} from 'hyparquet';
import {compressors} from 'hyparquet-compressors';
const file = await asyncBufferFromFile(process.argv[1]);
const rows = await parquetReadObjects({file, compressors});
const view = new DataView(new ArrayBuffer(8));
const floats = new Set(['timestamp_s', 'value', 'value_f64']);
const hex = (v) => { view.setFloat64(0, v, true); return [...new Uint8Array(view.buffer)].map((b) => b.toString(16).padStart(2, '0')).join(''); };
const out = rows.map((row) => Object.entries(row).map(([key, v]) => v === null || v === undefined ? null : floats.has(key) ? hex(v) : typeof v === 'bigint' ? Number(v) : v));
process.stdout.write(JSON.stringify(out));
"""


def js_adapter() -> Path | None:
    """The folder of the JavaScript adapter: `SKELLYSPECS_JS_ADAPTER` of conftest.py, or None."""
    folder = os.environ.get("SKELLYSPECS_JS_ADAPTER", "")
    return Path(folder) if folder else None


def node_package_version(name: str) -> str | None:
    """The installed version of a Node package of the JavaScript adapter, or None when it is not installed."""
    folder = js_adapter()
    package = folder / "node_modules" / name / "package.json" if folder else None
    return load_json(package)["version"] if package and package.is_file() else None


def hyparquet_rows(parquet: Path) -> list[list]:
    """The rows of a Parquet in column order, read by hyparquet through Node. The script was not run at gate 2.

    The script gives the 64 bits of each float, so the values reach Python with no change.
    """
    node = shutil.which("node")
    command = [node, "--input-type=module", "--eval", HYPARQUET, str(parquet)]
    done = subprocess.run(command, capture_output=True, check=True, cwd=js_adapter())  # noqa: S603
    floats = {name for name, kind, _ in COLUMNS if kind in ("float", "double")}
    return [
        [struct.unpack("<d", bytes.fromhex(v))[0] if name in floats and v is not None else v for v, (name, _, _) in zip(row, COLUMNS)]
        for row in json.loads(done.stdout)
    ]
