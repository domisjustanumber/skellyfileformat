"""Conformance tests SFT-705 to SFT-710: the take folder and the manifest (SPEC.md sections 4 and 5).

The Pass text of each test is in spec/conformance.md. A test gets the reader or the writer from a
fixture, so it fails with one line until the implementation exists (decision G21H).
"""

from __future__ import annotations

import json

import pytest

import checks_capture as c


def _trace(events: list):
    return lambda event, path: events.append((event, path))


@pytest.mark.parametrize("vector", ["plain", "labels_of_7", "labels_of_8", "camera_key_0", "file_of_another_take"])
def test_sft_705_names_and_layout(writer, tmp_path, vector):
    """SFT-705 (external: freemocap) Writer: names and layout. This is the part of the writer of the test adapter.

    Checks: SFF-715, SFF-716, SFF-719, SFF-720, SFF-722.
    """
    folder = tmp_path / "take"
    if vector == "plain":
        c.record_take(writer, folder, audio=c.microphone())
        c.check_names_and_layout(folder)
    elif vector in ("labels_of_7", "labels_of_8"):
        # Two cameras with remembered keys that have the same first 6, or the same first 7, characters.
        keys = {"labels_of_7": ["aabbcc1000000001", "aabbcc2000000002"], "labels_of_8": ["aabbcc1100000001", "aabbcc1200000002"]}[vector]
        cameras = [c.camera(index, camera_key=key, key_origin="confirmed_by_user") for index, key in enumerate(keys)]
        c.record_take(writer, folder, cameras)
        length = int(vector[-1])
        labels = [item["camera_label"] for item in c.load_json(folder / c.MANIFEST)["cameras"]]
        assert labels == [key[:length] for key in keys]
        c.check_names_and_layout(folder, label_length=length)
    elif vector == "camera_key_0":
        cameras = [c.camera(0), c.camera(1, camera_key="0", key_origin=None)]
        c.record_take(writer, folder, cameras, mode="conversion")
        item = c.load_json(folder / c.MANIFEST)["cameras"][1]
        assert (item["camera_key"], item["camera_label"]) == ("0", "cam1"), "the label is cam<N>, N is `group_position`"
        assert (folder / c.MEDIA / "synthetic_take.cam1.mkv").is_file()
        c.check_names_and_layout(folder, label_length=None)
    else:
        c.record_take(writer, folder, rec="take_a")
        before = c.snapshot(folder)
        with pytest.raises(ValueError):
            writer.TakeWriter(folder, "take_b", [c.camera(0)], None, writer=c.WRITER)
        assert c.snapshot(folder) == before, "the writer that refuses to start writes nothing"


def test_sft_705_golden_part(golden_or_skip):
    """SFT-705, the golden part: the names in G3. Checks: SFF-715, SFF-716, SFF-720, SFF-722."""
    c.check_names_and_layout(golden_or_skip("G03"))


@pytest.mark.external("freemocap")
def test_sft_705_external():
    """SFT-705, the external part: the names of the files that freemocap writes in a run. Checks: SFF-716."""


@pytest.mark.parametrize("scope", ["full", "player"])
def test_sft_706_renamed_take_folder(reader, golden_or_skip, scope):
    """SFT-706 Reader: a renamed take folder. Checks: SFF-717, SFF-718, SFF-824.

    "The reader opens no file by a glob pattern" is checked for the Python reader, through the audit
    events of Python for `glob` and for `pathlib.Path.glob`.
    """
    renamed, original = golden_or_skip("G08", "renamed"), golden_or_skip("G03")
    assert renamed.name != original.name
    with c.audit() as events:
        found = c.read_bytes(reader, renamed, scope=scope)
    assert found == c.read_bytes(reader, original, scope=scope), "equal to the result of G3, byte for byte"
    assert not [event for event in events if event[0] in c.GLOB_EVENTS], "the reader opens no file by a glob pattern"
    if scope == "full":
        (parquet,) = [item for item in c.only_take(json.loads(found))["folder_files"] if item["role"] == "tracking"]
        assert parquet["state"] == "present"


@pytest.mark.parametrize("base", ["G03", "G01"], ids=["g3", "g1"])
def test_sft_707_only_root_and_media_folder(reader, golden_or_skip, variant, base):
    """SFT-707 Reader: only the root and the media folder are scanned. Checks: SFF-721.

    The case `g1` is the same input on a copy of G1, for stage 1a (ADR-YT1F item 3).
    """
    folder = variant(base)
    video = c.media_files(folder, ".mkv")[0]
    (folder / "exports").mkdir()
    for path in (video, video.with_suffix(".csv")):
        (folder / "exports" / path.name).write_bytes(path.read_bytes())
    found = c.read_bytes(reader, folder)
    assert b'"exports/' not in found, "the copy is not in the result"
    assert found == c.read_bytes(reader, golden_or_skip(base))


def test_sft_708_manifest(writer, tmp_path):
    """SFT-708 Writer: the manifest. This is the part of the writer of the test adapter.

    Checks: SFF-723, SFF-724, SFF-725, SFF-726, SFF-727, SFF-728.
    """
    folder, events = tmp_path / "take", []
    take = writer.TakeWriter(folder, "synthetic_take", [c.camera(0), c.camera(1)], c.microphone(), writer=c.WRITER, trace=_trace(events))
    # The manifest exists before the first frame, and it is complete and valid at each moment of the take.
    manifest = c.check_recording_manifest(folder)
    keys = [item["camera_key"] for item in manifest["cameras"]]
    start = take.take_start_host_ns
    for position in range(8):
        for index in range(2):
            number = 1000 + position + (1 if index == 1 and position >= 5 else 0)  # the forced gap of camera 1
            take.write_frame(index, c.jpeg(position), start + 33_333_333 * (position + 1), source_frame_number=number)
            c.check_recording_manifest(folder)
    take.write_audio(c.click_pcm(4800, []), start + 114_000_000, adc_ns=start + 112_000_000)
    c.check_recording_manifest(folder)
    take.add_warning("control_mismatch", camera_key=keys[0], detail="exposure_us: set 4000, read back 4200")
    c.check_recording_manifest(folder)
    take.add_warning("awb_not_settled", camera_key=keys[1], detail="white balance did not settle in 2 s")
    c.check_recording_manifest(folder)
    take.close()

    manifest = c.check_manifest(folder)  # the members, each `sha256` and the summary values of SFF-728
    assert manifest["state"] == "finished" and manifest["writer"] == c.WRITER
    gap = [item for item in manifest["warnings"] if item["code"] == "camera_gap"]
    assert [(item["source"], item["camera_key"]) for item in gap] == [("skellycam", keys[1])], "`warnings` has `camera_gap`"
    for code, key, detail in (
        ("control_mismatch", keys[0], "exposure_us: set 4000, read back 4200"),
        ("awb_not_settled", keys[1], "white balance did not settle in 2 s"),
    ):
        assert {"code": code, "source": "skellycam", "camera_key": key, "detail": detail} in manifest["warnings"]
    assert manifest["summary"]["warnings"] == ["awb_not_settled", "camera_gap", "control_mismatch"]
    # skellycam holds `.processing.lock` while it reads, changes and writes the manifest.
    c.check_whole_writes_hold_lock(events, [c.MANIFEST, "synthetic_take_info.json"])
    assert [event for event in events if event == ("replace", c.MANIFEST)], "each write replaces the whole file (SFF-726)"


@pytest.mark.parametrize("target", ["G01/take", "G01/confirmed_key", "G03/take"])
def test_sft_708_check_on_golden(golden_or_skip, target):
    """SFT-708, the manifest check on a golden folder: the members, each `sha256` and the summary. Checks: SFF-723, SFF-728."""
    manifest = c.check_manifest(golden_or_skip(*target.split("/")))
    assert manifest["state"] == "finished" and "camera_gap" in manifest["summary"]["warnings"]


@pytest.mark.external("freemocap, skellycam")
def test_sft_708_external():
    """SFT-708, the external sentences. Checks: SFF-725, SFF-727, SFF-728.

    The detection of `control_mismatch` and `awb_not_settled` (skellycam). After freemocap, each file
    is listed, the warnings of skellycam remain and `writer` is the freemocap string. freemocap holds
    the lock and keeps the members of skellycam. `processing_runs` has its items.
    """


VECTORS_709 = ["rotation_and_fps", "gaps", "sha256"]


@pytest.mark.parametrize(
    ("base", "vector"),
    [pytest.param(base, vector, id=prefix + vector) for base, prefix in (("G03", ""), ("G01", "g1_")) for vector in VECTORS_709],
)
def test_sft_709_summary_is_not_used(reader, variant, expected, base, vector):
    """SFT-709 Reader: the summary is not used. Checks: SFF-729, SFF-730.

    The cases `g1_*` are the same inputs on a copy of G1, for stage 1a (ADR-YT1F item 3).
    """
    folder = variant(base)
    manifest = c.load_json(folder / c.MANIFEST)
    cameras = manifest["summary"]["cameras"]
    if vector == "rotation_and_fps":
        cameras[0].update(display_rotation=90, nominal_fps=25)
    elif vector == "gaps":
        cameras[1]["gaps"] += 5
    else:
        item = next(item for item in manifest["files"] if item["sha256"] is not None)
        item["sha256"] = "0" * 64
    c.write_json(folder / c.MANIFEST, manifest)
    result = c.read(reader, folder, records=True)
    want = json.loads(expected(base, "take", "full"))
    if vector == "sha256":
        assert result == want, "the wrong `sha256` changes nothing in the result"
        return
    take = c.only_take(result)
    assert "summary_stale" in take["warnings"]
    assert take["files"] == want["takes"][0]["files"], "the result uses the sidecar values"
    for item in c.cameras_of(take):
        header = c.read_sidecar(c.sidecar_path(folder, item["name"])).header
        details = reader.camera_details(folder, item["name"])
        assert details["display_rotation"] == int(header["display_rotation"])
        assert list(details["nominal_rate"]) == [int(part) for part in header["nominal_rate"].split("/")]


@pytest.mark.parametrize("vector", ["no_manifest", "other_take_manifest", "audio_only", "other_info_and_exports", "renamed_pair"])
def test_sft_710_missing_or_wrong_manifest(reader, golden_or_skip, variant, expected, vector):
    """SFT-710 Reader: a missing or wrong manifest. Checks: SFF-731, SFF-867, SFF-868.

    "The reader does not list that subfolder" is checked for the Python reader, through the audit
    events of Python for `os.listdir` and `os.scandir`.
    """
    if vector == "audio_only":
        folder = variant("G01")
        (folder / c.MANIFEST).unlink()
        for path in c.media_files(folder, ".mkv"):
            path.unlink()
            path.with_suffix(".csv").unlink()
        (sidecar,) = c.media_files(folder, ".csv")
        before = c.snapshot(folder)
        take = c.only_take(c.read(reader, folder))
        assert take["recording_name"] == sidecar.name.removesuffix(".audio.csv")
        assert c.snapshot(folder) == before, "the reader writes no file"
        return

    folder = variant("G07", "other_take_manifest" if vector == "other_take_manifest" else "no_manifest")
    videos = [c.read_sidecar(path) for path in c.media_files(folder, ".csv") if not path.name.endswith(".audio.csv")]
    videos.sort(key=lambda sidecar: int(sidecar.header["group_position"]))
    rec = videos[0].path.name.split(".")[0]
    if vector == "other_info_and_exports":
        (folder / "other_info.json").write_bytes(b"{}")
        (folder / "exports").mkdir()
        (folder / "exports" / f"{rec}_export.csv").write_bytes(b"x")
    elif vector == "renamed_pair":
        for suffix in (".csv", ".mkv"):
            path = videos[1].path.with_suffix(suffix)
            path.rename(path.with_name(path.name.replace(rec, "another_rec", 1)))
    before = c.snapshot(folder)
    with c.audit() as events:
        result = c.read(reader, folder, records=True)
    take = c.only_take(result)
    assert c.snapshot(folder) == before, "the reader writes no file"
    assert "manifest_missing" in take["warnings"]
    assert take["recording_name"] == rec, "`recording_name` is the <rec> of the camera sidecar names"
    paths = [item["path"] for item in take["folder_files"]]
    states = {item["check"]: item["state"] for item in take["links"]}
    g3 = json.loads(expected("G03", "take", "full"))["takes"][0]
    g3_states = {item["check"]: item["state"] for item in g3["links"]}

    if vector == "no_manifest":
        assert take["manifest"] == "missing"
        assert take["files"] == g3["files"], "the same device pairs as G3"
        names = [f"{rec}_info.json", f"{rec}_recording_info.json", f"{rec}_camera_calibration.toml", f"{rec}_data.parquet"]
        assert paths == sorted(names), "the root files of G3 that have an exact name of SFF-731"
        assert (states["calibration"], states["camera_key"]) == ("not_checked", "not_checked")
        assert (states["hashes"], states["files"]) == ("ok", "ok"), "only their Parquet parts, and they are `ok`"
        assert states["rotation"] == "ok", "`rotation` has only its capture info part"
        # The checks that compare no manifest value (SFF-872): `frames` and `dimensions`.
        assert (states["frames"], states["dimensions"]) == (g3_states["frames"], g3_states["dimensions"])
    elif vector == "other_take_manifest":
        assert take["manifest"] == "invalid"
        rebuilt = c.only_take(c.read(reader, golden_or_skip("G07", "no_manifest")))
        assert take["links"] == rebuilt["links"], "the reader rebuilds the links in the same way"
        assert c.MANIFEST not in paths, "the manifest is not in `folder_files`"
        assert {"name": c.MANIFEST, "state": "invalid", "reason": "take_fact_mismatch"} in result["other_files"]
        assert "orphan_file" in result["folder_warnings"]
    elif vector == "other_info_and_exports":
        assert "other_info.json" not in paths
        assert '"exports/' not in json.dumps(result), "the file in `exports/` is not in the result"
        listed = [path for event, path in events if event in ("os.listdir", "os.scandir")]
        assert not [path for path in listed if path.rstrip("/\\").endswith("exports")], "the reader does not list that subfolder"
    else:
        assert "take_fact_mismatch" in take["warnings"]
