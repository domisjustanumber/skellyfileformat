"""SFT-768 and SFT-769: the reader result and its scopes (SPEC.md section 23).

Each case folder under `golden/` at collection time is an input: the tests find them, and a golden
folder that is built later is a new input with no change of this file.
"""

from __future__ import annotations

import hashlib
import json
import shutil

import checks_folder as checks
import pytest

KINDS = ["full", "player", "js"]  # the Python reader with each scope, and the JavaScript reader
CASES = [pytest.param(name, case, id=f"{name}-{case}") for name, case in checks.golden_cases()]


def _scope(kind: str) -> str:
    return "player" if kind == "js" else kind


@pytest.mark.parametrize("kind", KINDS)
@pytest.mark.parametrize(("name", "case"), CASES)
def test_sft_768_reader_result_of_each_golden_case(reader, js_reader, golden_or_skip, expected, name, case, kind):
    """SFT-768 Reader: the reader result, Python and JS, for every case of every golden folder.

    Checks: SFF-756, SFF-853, SFF-885, SFF-886, SFF-887, SFF-888, SFF-889, SFF-890 (and SFF-892).
    """
    folder = golden_or_skip(name, case)
    raw = checks.read_bytes(kind, reader, js_reader, folder)
    assert raw == expected(name, case, _scope(kind)), "byte for byte"
    assert checks.result_faults(raw) == []
    if name in ("G01", "G12"):  # the file warnings `gap` and `encode_skip`
        assert checks.file_warning_faults(folder, json.loads(raw)) == []


@pytest.mark.parametrize(("name", "case"), CASES)
def test_sft_768_committed_results(golden_or_skip, expected, name, case):
    """SFT-768, on the committed results: the form of SFF-885 to SFF-890. It needs no implementation."""
    folder = golden_or_skip(name, case)
    for scope in ("full", "player"):
        raw = expected(name, case, scope)
        assert checks.result_faults(raw) == [], scope
        if name in ("G01", "G12"):
            assert checks.file_warning_faults(folder, json.loads(raw)) == [], scope
    if (name, case) == ("G12", "take"):
        warnings = [item["warnings"] for item in checks.the_take(checks.committed(folder))["files"] if item["kind"] == "camera"]
        assert "gap" in warnings[0] and any("encode_skip" in codes for codes in warnings)


@pytest.mark.parametrize("kind", KINDS)
@pytest.mark.parametrize("made", ["empty", "one_timing_sidecar", "only_capture_info", "empty_annotated_video"])
def test_sft_768_folders_that_the_test_makes(reader, js_reader, variant, golden_or_skip, expected, tmp_path, made, kind):
    """SFT-768 Reader: the folders that the test makes. Checks: SFF-853, SFF-888, SFF-889."""
    folder = tmp_path / "made"
    if made == "empty":
        folder.mkdir()
    elif made == "one_timing_sidecar":
        source = golden_or_skip("G01")
        sidecar = source / checks.manifest(source)["cameras"][0]["timing"]
        (folder / checks.MEDIA).mkdir(parents=True)
        shutil.copy(sidecar, folder / checks.MEDIA / sidecar.name)
    elif made == "only_capture_info":
        info = checks.capture_info(golden_or_skip("G03"))
        folder.mkdir()
        shutil.copy(info, folder / info.name)
    else:
        folder = variant("G03")
        listed = checks.manifest(folder)
        path = f"annotated_videos/{listed['recording_name']}.{listed['cameras'][0]['camera_label']}.annotated.mp4"
        (folder / path).parent.mkdir()
        (folder / path).write_bytes(b"")
        item = {"path": path, "role": "annotated_video", "owner": "freemocap", "sha256": hashlib.sha256(b"").hexdigest()}
        listed["files"] = sorted([*listed["files"], item], key=lambda entry: entry["path"].encode())
        checks.write_json(folder / "recording_manifest.json", listed)
    raw = checks.read_bytes(kind, reader, js_reader, folder)
    assert checks.result_faults(raw) == []
    result = json.loads(raw)
    if made == "empty":
        assert result["folder_state"] == "empty"
    elif made == "one_timing_sidecar":
        want = [{"name": f"{checks.MEDIA}/{sidecar.name}", "reason": "missing_media", "state": "invalid"}]
        assert (result["folder_state"], result["other_files"], result["folder_warnings"]) == ("unreadable", want, ["orphan_file"])
    elif made == "only_capture_info":
        want = [{"name": info.name, "reason": "take_fact_mismatch", "state": "invalid"}]
        assert (result["folder_state"], result["other_files"], result["folder_warnings"]) == ("unreadable", want, ["orphan_file"])
    else:
        take = checks.the_take(result)
        video = checks.folder_file(take, ".annotated.mp4")
        assert video["state"] == "present"
        take["folder_files"].remove(video)
        assert checks.canonical(result) == expected("G03", "take", _scope(kind)), "the other members do not change"


SCOPE_PLAYER = pytest.mark.parametrize(
    ("name", "cases"),
    [("G03", ["take"]), ("G09", list(checks.G09_CHECKS)), ("G13", ["take"]), ("G16", ["take"]), ("G15", ["v1a"])],
    ids=["G03", "G09", "G13", "G16", "G15-v1a"],
)


@SCOPE_PLAYER
def test_sft_769_scope_player(reader, js_reader, golden_or_skip, expected, name, cases):
    """SFT-769 Reader: the scope `player`, Python and JS. Checks: SFF-892."""
    for case in cases:
        folder = golden_or_skip(name, case)
        player = checks.read_bytes("player", reader, js_reader, folder)
        assert player == expected(name, case, "player"), case
        assert checks.read_bytes("js", reader, js_reader, folder) == player, case
        without_records = checks.read_bytes("player", reader, js_reader, folder, records=False)
        assert checks.read_bytes("js", reader, js_reader, folder, records=False) == without_records, case
        assert without_records == checks.canonical(json.loads(without_records)), "the canonical JSON, and no other byte"


@SCOPE_PLAYER
def test_sft_769_scope_player_against_full(reader, js_reader, golden_or_skip, name, cases):
    """SFT-769 Reader: the `player` result against the `full` result of the Python reader. Checks: SFF-892."""
    for case in cases:
        folder = golden_or_skip(name, case)
        player = checks.read_bytes("player", reader, js_reader, folder)
        full = checks.read_bytes("full", reader, js_reader, folder)
        assert checks.scope_faults(json.loads(full), json.loads(player)) == [], case


@pytest.mark.parametrize("kind", KINDS)
@pytest.mark.parametrize(
    ("source", "pattern"),
    [("G03", "*_camera_calibration.toml"), ("G03", "*_data.parquet"), ("G13", "*_realtime_journal.bin")],
    ids=["toml", "parquet", "journal"],
)
def test_sft_769_folder_file_alone(reader, js_reader, golden_or_skip, tmp_path, source, pattern, kind):
    """SFT-769 Reader: a folder with only one TOML, Parquet or journal of this format. Checks: SFF-892.

    The folder is `unreadable` in the two scopes (ADR-XR63 item 10). For the scope `player`, the reader
    reads only the mark of the file, and the item is `not_in_format` with no `orphan_file` (ADR-W5AK
    item 8).
    """
    alone = checks.one(golden_or_skip(source), pattern)
    shutil.copy(alone, tmp_path / alone.name)
    result = json.loads(checks.read_bytes(kind, reader, js_reader, tmp_path))
    assert result["folder_state"] == "unreadable"
    if _scope(kind) == "player":
        item = checks.named(result["other_files"], alone.name)
        assert item["state"] == "not_in_format" and "orphan_file" not in result["folder_warnings"]


@pytest.mark.parametrize(("name", "case"), CASES)
def test_sft_769_committed_results(golden_or_skip, name, case):
    """SFT-769, on the committed results: the `player` result against the `full` result. It needs no implementation."""
    folder = golden_or_skip(name, case)
    assert checks.scope_faults(checks.committed(folder, "full"), checks.committed(folder, "player")) == []
