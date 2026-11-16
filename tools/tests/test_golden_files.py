"""Checks of the committed golden files that need only the standard library.

They test the sums, the form of each expected reader result (SPEC.md section 23) and the text files
of G1. They do not import the generator, so a fault of the generator does not hide here.
"""

from __future__ import annotations

import hashlib
import json
import zlib
from pathlib import Path

import pytest

GOLDEN = Path(__file__).resolve().parents[2] / "golden"
FOLDERS = sorted(p for p in GOLDEN.glob("G[0-9][0-9]") if p.is_dir())
RESULTS = sorted(p for folder in FOLDERS for p in folder.glob("*.json") if p.name.split(".")[-2] in ("full", "player"))
G01_CASES = [GOLDEN / "G01" / "take", GOLDEN / "G01" / "confirmed_key"]


def relative(path: Path) -> str:
    return path.relative_to(GOLDEN).as_posix()


def test_golden_folders_exist():
    assert FOLDERS and RESULTS


# ---------------------------------------------------------------- SHA256SUMS


@pytest.mark.parametrize("folder", FOLDERS, ids=relative)
def test_sums_match_and_list_each_file(folder):
    lines = (folder / "SHA256SUMS").read_bytes().decode().split("\n")
    assert lines.pop() == "", "the last line ends with LF"
    listed = dict(reversed(line.split("  ", 1)) for line in lines)
    present = {p.relative_to(folder).as_posix() for p in folder.rglob("*") if p.is_file()} - {"SHA256SUMS"}
    assert set(listed) == present
    assert list(listed) == sorted(listed, key=str.encode)
    for name, digest in listed.items():
        assert hashlib.sha256((folder / name).read_bytes()).hexdigest() == digest, name


# ---------------------------------------------------------------- the form of a reader result

FILE_STATES = {"unsupported_version", "invalid", "damaged", "unfinished", "repaired", "finished", "not_in_format"}
FOLDER_FILE_STATES = {
    "present", "missing", "invalid", "not_checked", "unsupported_version", "unfinished", "damaged",
}  # fmt: skip
REASONS = {
    None, "bad_metadata", "missing_metadata", "bad_rate", "bad_rotation", "bad_label", "bad_time", "crc_mismatch",
    "take_fact_mismatch", "missing_media", "bad_schema", "code_in_file",
}  # fmt: skip
TAKE_WARNINGS = {
    "incomplete_take", "duplicate_label", "take_fact_mismatch", "extra_files", "manifest_missing",
    "camera_key_zero", "stale_processing_info", "summary_stale", "calibration_mismatch", "realtime_run",
}  # fmt: skip
FILE_WARNINGS = {"missing_fit", "encode_skip", "prerelease"}
FOLDER_WARNINGS = {"multiple_takes", "stray_tmp", "orphan_file"}
LEGACY_WARNINGS = {
    "legacy_fake_confidence", "legacy_marker_order", "legacy_nonrigid_alignment", "legacy_calibration_unverified",
}  # fmt: skip
LINK_CHECKS = ["take_uuid", "camera_key", "frames", "dimensions", "rotation", "files", "hashes", "calibration"]
JOURNAL_MEMBERS = {"records", "rejected_records", "torn_bytes"}


def no_float(text: str):
    raise AssertionError(f"a float in a reader result: {text}")


def load(path: Path) -> dict:
    return json.loads(path.read_bytes(), parse_float=no_float)


def warnings_ok(codes: list, allowed: set) -> bool:
    return set(codes) <= allowed and codes == sorted(set(codes))


@pytest.mark.parametrize("path", RESULTS, ids=relative)
def test_result_is_canonical_json(path):
    """RFC 8785 for a value with no float and with ASCII keys: sorted members, no white space (SFF-885)."""
    data = path.read_bytes()
    again = json.dumps(load(path), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    assert data == again


@pytest.mark.parametrize("path", RESULTS, ids=relative)
def test_result_members_codes_and_orders(path):
    result = load(path)
    assert set(result) == {"result_version", "folder_state", "folder_warnings", "takes", "other_files", "legacy"}
    assert result["result_version"] == 2
    assert result["folder_state"] in {"ok", "unreadable", "legacy", "empty"}
    assert warnings_ok(result["folder_warnings"], FOLDER_WARNINGS)
    assert [t["take_uuid"] for t in result["takes"]] == sorted(t["take_uuid"] for t in result["takes"])

    for take in result["takes"]:
        assert set(take) == {
            "take_uuid", "recording_name", "state", "manifest", "warnings", "may_contain_private_data", "files",
            "folder_files", "links",
        }  # fmt: skip
        assert take["state"] in {"complete", "incomplete"}
        assert take["manifest"] in {"present", "missing", "invalid"}
        assert warnings_ok(take["warnings"], TAKE_WARNINGS)
        assert isinstance(take["may_contain_private_data"], bool)

        kinds = [item["kind"] for item in take["files"]]
        assert kinds == sorted(kinds, key=["camera", "audio"].index), "the audio file is last (SFF-890)"
        for item in take["files"]:
            assert set(item) == {
                "name", "kind", "state", "reason", "camera_key", "camera_label", "rows", "torn_bytes", "fit",
                "warnings", "records",
            }, "the committed results hold `records`"  # fmt: skip
            assert item["state"] in FILE_STATES - {"not_in_format"} and item["reason"] in REASONS
            assert (item["reason"] is not None) == (item["state"] == "invalid")
            assert warnings_ok(item["warnings"], FILE_WARNINGS)
            assert "\\" not in item["name"] and not item["name"].startswith("/")
            if item["state"] in {"invalid", "unsupported_version"}:
                assert item["rows"] is item["torn_bytes"] is item["fit"] is None
            else:
                assert isinstance(item["rows"], int) and isinstance(item["torn_bytes"], int)
                assert isinstance(item["fit"], bool)
            if item["kind"] == "audio":
                assert item["camera_key"] is item["camera_label"] is None
            for record in item["records"] or []:
                assert len(record) == 5 and all(v is None or type(v) is int for v in record)

        paths = [item["path"] for item in take["folder_files"]]
        assert paths == sorted(paths, key=str.encode) and "recording_manifest.json" not in paths
        for item in take["folder_files"]:
            assert set(item) - JOURNAL_MEMBERS == {"path", "role", "state", "reason", "warnings"}
            assert item["state"] in FOLDER_FILE_STATES and item["reason"] in REASONS
            assert warnings_ok(item["warnings"], FILE_WARNINGS)

        assert [link["check"] for link in take["links"]] == LINK_CHECKS
        for link in take["links"]:
            assert set(link) == {"check", "state", "detail"}
            assert link["state"] in {"ok", "mismatch", "not_checked"} and link["detail"] is None

    names = [item["name"] for item in result["other_files"]]
    assert names == sorted(names, key=str.encode)
    for item in result["other_files"]:
        assert set(item) == {"name", "state", "reason"}
        assert item["state"] in FILE_STATES and item["reason"] in REASONS

    legacy = result["legacy"]
    assert (legacy is not None) == (result["folder_state"] == "legacy")
    if legacy is not None:
        assert set(legacy) == {"family", "release_range", "ambiguous", "eras", "warnings", "calibration"}
        assert legacy["family"] in {"v1", "pre_v1", "unknown"} and result["takes"] == []
        assert warnings_ok(legacy["warnings"], LEGACY_WARNINGS)


@pytest.mark.parametrize("path", [p for p in RESULTS if ".player." in p.name], ids=relative)
def test_player_result_against_full_result(path):
    """The part of SFF-892 that needs no knowledge of the folder."""
    player, full = load(path), load(path.with_name(path.name.replace(".player.", ".full.")))
    assert len(player["takes"]) == len(full["takes"])
    for player_take, full_take in zip(player["takes"], full["takes"]):
        assert player_take["files"] == full_take["files"]
        states = {link["check"]: link["state"] for link in player_take["links"]}
        assert {states[c] for c in ("frames", "dimensions", "hashes", "calibration")} == {"not_checked"}
        assert not set(player_take["warnings"]) & {"stale_processing_info", "calibration_mismatch", "realtime_run"}


# ---------------------------------------------------------------- G1: the text files against the results


def read_sidecar(path: Path) -> tuple[dict, list[list[str]], list[str]]:
    """The header, the data rows and the footer lines of a finished sidecar. It checks each row CRC."""
    data = path.read_bytes()
    assert not data.startswith(b"\xef\xbb\xbf") and b"\r" not in data and data.endswith(b"\n")  # SFF-700
    lines = data.decode("utf-8").split("\n")[:-1]
    header = dict(line[2:].split("=", 1) for line in lines if line.startswith("# ") and "=" in line.split(" ")[1])
    column_line = next(i for i, line in enumerate(lines) if not line.startswith("#"))
    rows, footer = [], []
    for line in lines[column_line + 1 :]:
        if line.startswith("#") or footer:
            footer.append(line)
            continue
        body, crc = line.rsplit(",", 1)
        assert f"{zlib.crc32(body.encode()):08x}" == crc, line  # SFF-744
        rows.append(body.split(","))
    assert len({len(r) for r in rows}) == 1 and len(rows[0]) + 1 == len(lines[column_line].split(","))
    return header, rows, footer


def footer_values(footer: list[str], word: str) -> dict:
    (line,) = [line for line in footer if line.split(" ")[1] == word]
    return dict(pair.split("=", 1) for pair in line.split(" ")[2:])


def number(text: str) -> int | None:
    return int(text) if text else None


@pytest.mark.parametrize("case", G01_CASES, ids=relative)
def test_g01_results_agree_with_the_sidecars(case):
    full = load(case.with_name(case.name + ".full.json"))
    player = load(case.with_name(case.name + ".player.json"))
    for link_full, link_player in zip(full["takes"][0]["links"], player["takes"][0]["links"]):
        if link_full["check"] == "frames":  # the row-count part: SFF-872 for `full`, SFF-892 for `player`
            assert (link_full["state"], link_player["state"]) == ("ok", "not_checked")
            link_player["state"] = "ok"
    assert full == player, "the two scopes differ only in the check `frames`"

    (take,) = full["takes"]
    manifest = json.loads((case / "recording_manifest.json").read_bytes())
    assert (take["take_uuid"], take["recording_name"]) == (manifest["take_uuid"], manifest["recording_name"])
    assert [item["name"] for item in take["files"]] == [c["video"] for c in manifest["cameras"]] + [
        manifest["audio"]["audio"]
    ]
    take_keys = set()
    for position, item in enumerate(take["files"]):
        header, rows, footer = read_sidecar(case / Path(item["name"]).with_suffix(".csv"))
        take_keys.add(tuple(list(header.items())[4:12]))  # `take_uuid` to `audio_count` (SFF-749)
        end = footer_values(footer, "end")
        assert footer[-1].startswith("# end ") and item["rows"] == len(rows) == int(end["rows"])
        assert [int(r[0]) for r in rows] == list(range(len(rows)))
        assert header["format_prerelease"] == "1" and item["warnings"] == ["prerelease"]
        segment = footer_values(footer, "fit_segment")
        t0_ns = int(segment["t0_ns"])
        if item["kind"] == "camera":
            assert int(header["group_position"]) == position  # SFF-890
            assert (header["camera_key"], header["camera_label"]) == (item["camera_key"], item["camera_label"])
            assert (segment["pos_first"], int(segment["pos_last"])) == ("0", len(rows) - 1)
            sources = [int(r[1]) for r in rows]
            flags = [int(p > 0 and sources[p] != sources[p - 1] + 1) for p in range(len(rows))]  # SFF-756
            assert [int(r[4]) for r in rows] == flags and int(end["gaps"]) == sum(flags)
            assert sum(flags) == (1 if position == 1 else 0), "only camera 1 of G1 has a gap"
            records = [
                [p, sources[p], int(r[2]), number(r[3]),
                 t0_ns + (sources[p] - sources[0]) * int(segment["period_ps"]) // 1000]  # SFF-777
                for p, r in enumerate(rows)
            ]  # fmt: skip
        else:
            assert (segment["row_first"], int(segment["row_last"]), segment["n0"]) == ("0", len(rows) - 1, "0")
            firsts = [int(r[1]) for r in rows]
            assert firsts == [sum(int(r[2]) for r in rows[:b]) for b in range(len(rows))]  # SFF-767
            assert int(end["samples"]) == sum(int(r[2]) for r in rows)
            records = [
                [b, firsts[b], int(r[2]), int(r[3]), t0_ns + firsts[b] * int(segment["period_fs"]) // 10**6]
                for b, r in enumerate(rows)
            ]  # SFF-779
        assert item["records"] == records
        player_times = [record[4] for record in records]
        assert player_times == sorted(player_times)  # SFF-782
    assert len(take_keys) == 1


@pytest.mark.parametrize("case", G01_CASES, ids=relative)
def test_g01_camera_keys_manifest_and_capture_info(case):
    manifest = json.loads((case / "recording_manifest.json").read_bytes())
    (info_item,) = manifest["files"]
    info_bytes = (case / info_item["path"]).read_bytes()
    assert hashlib.sha256(info_bytes).hexdigest() == info_item["sha256"]  # SFF-723
    info = json.loads(info_bytes)
    origins = []
    for camera in manifest["cameras"]:
        key = camera["camera_key"]
        config = info["camera_configs"][key]
        device = config["device"]
        form = f"serial:{device['serial']}" if device["serial"] is not None else f"port:{device['port_path']}"
        identity = f"{device['vendor_id']}:{device['product_id']}:{form}"
        computed = hashlib.sha256(identity.encode()).digest()[:8].hex()  # SFF-752
        origins.append(config["key_origin"])
        assert (key == computed) == (config["key_origin"] == "computed")
        assert len(key) == 16 and int(key, 16) != 0
        assert camera["camera_label"] == config["camera_label"] == key[:6]  # SFF-720
        stem = f"synchronized_videos/{manifest['recording_name']}.{key[:6]}"
        assert (camera["video"], camera["timing"]) == (stem + ".mkv", stem + ".csv")
    assert origins == (["computed", "confirmed_by_user"] if case.name == "confirmed_key" else ["computed"] * 2)

    fields = [(f["file"].encode(), f["field"].encode()) for f in manifest["privacy"]["fields"]]
    assert fields == sorted(fields)  # SFF-881
    for item in manifest["privacy"]["fields"]:
        assert (case / item["file"]).is_file()
        if item["field"].startswith("/"):
            value = json.loads((case / item["file"]).read_bytes())
            for part in item["field"][1:].split("/"):
                value = value[int(part)] if isinstance(value, list) else value[part]
            assert value is not None
