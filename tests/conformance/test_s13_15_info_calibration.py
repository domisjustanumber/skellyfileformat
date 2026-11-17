"""SFT-735 to SFT-740: capture info, processing info and calibration (SPEC.md sections 13 to 15)."""

from __future__ import annotations

import tomllib

import checks_folder as checks
import pytest


def test_sft_735_capture_info_json(writer, tmp_path):
    """SFT-735 Writer: the capture info JSON. Checks: SFF-800, SFF-801, SFF-802.

    "skellycam" is `TakeWriter` with synthetic input (decision QH61 item 46). The input and the calls
    of `TakeWriter` are those of `checks_capture.record_take` (INTERFACE_NOTES_capture.md).
    """
    capture = pytest.importorskip("checks_capture")
    cameras, microphone = [capture.camera(0), capture.camera(1)], capture.microphone()
    folder, rec = tmp_path / "take", "synthetic_take"
    events: list[tuple[str, str]] = []
    trace = lambda event, path: events.append((event, path))  # noqa: E731
    take = writer.TakeWriter(folder, rec, cameras, microphone, writer=capture.WRITER, trace=trace)
    info_path = folder / f"{rec}_info.json"
    at_start = checks.load_json(info_path)  # the file exists at the take start, and it is complete
    start = take.take_start_host_ns
    for position in range(3):
        for index in range(2):
            take.write_frame(index, capture.jpeg(position), start + 33_333_333 * (position + 1), source_frame_number=position)
    take.close()
    at_end = checks.load_json(info_path)
    keys = [camera["camera_key"] for camera in checks.manifest(folder)["cameras"]]
    for info in (at_start, at_end):
        assert checks.capture_info_faults(info, keys, microphone["device_name"]) == []
    assert at_end["camera_configs"][keys[0]]["user_name"] == cameras[0]["user_name"]  # one camera has a user name
    held, writes = False, []
    for event, path in events:  # the events of INTERFACE_NOTES_capture.md: `lock`, `unlock` and `replace`
        if path == capture.LOCK and event in ("lock", "unlock"):
            held = event == "lock"
        elif (event, path) == ("replace", info_path.name):
            writes.append(held)
    assert writes == [True, True], "skellycam holds `.processing.lock` for each of the two writes"


@pytest.mark.parametrize("base", ["G03", "G01"], ids=["g3", "g1"])
def test_sft_736_camera_configs_by_key(reader, variant, expected, base):
    """SFT-736 Reader: camera configs by key. Checks: SFF-803.

    The case `g1` is the same input on a copy of G1, for stage 1a (ADR-YT1F item 3).
    """
    folder = variant(base)
    info_path = checks.capture_info(folder)
    info = checks.load_json(info_path)
    configs = dict(reversed(info["camera_configs"].items()))  # another order
    labels = [config["camera_label"] for config in configs.values()]
    for config, label in zip(configs.values(), reversed(labels), strict=True):  # the labels swapped
        config["camera_label"] = label
    checks.write_json(info_path, info | {"camera_configs": configs})
    result = checks.read(reader, folder, records=True)
    assert checks.link(checks.the_take(result), "camera_key") == "ok"
    # The result holds no value of a camera config, so the links by key give the committed result.
    assert checks.canonical(result) == expected(base, "take", "full")


def test_sft_736_confirmed_key(reader, golden_or_skip):
    """SFT-736 Reader: the case `confirmed_key` of G1. Checks: SFF-803.

    The reader does not compute the key from the `device` values, so the case reads with no error.
    """
    folder = golden_or_skip("G01", "confirmed_key")
    take = checks.the_take(checks.read(reader, folder))
    assert checks.folder_file(take, checks.capture_info(folder).name)["state"] == "present"
    assert checks.link(take, "camera_key") == "ok"


@pytest.mark.parametrize(
    ("base", "key_origin"),
    [
        pytest.param(base, key_origin, id=prefix + name)
        for base, prefix in (("G03", ""), ("G01", "g1_"))
        for key_origin, name in (("remembered", "remembered"), (None, "null_with_a_key"))
    ],
)
def test_sft_736_bad_key_origin(reader, variant, base, key_origin):
    """SFT-736 Reader: a `key_origin` outside the three values, and null with a `camera_key` that is not 0.

    Checks: SFF-803. G3 with one camera config changed at test time (ADR-XR63 item 9; ADR-W5AK
    item 7). The cases `g1_*` are the same inputs on a copy of G1, for stage 1a (ADR-YT1F item 3).
    """
    folder = variant(base)
    info_path = checks.capture_info(folder)
    info = checks.load_json(info_path)
    key, config = next(iter(info["camera_configs"].items()))
    assert key != "0"
    config["key_origin"] = key_origin
    checks.write_json(info_path, info)
    item = checks.folder_file(checks.the_take(checks.read(reader, folder)), info_path.name)
    assert (item["state"], item["reason"]) == ("invalid", "bad_schema")


@pytest.mark.external("freemocap")
def test_sft_737_processing_info_json():
    """SFT-737 (external: freemocap) Writer: the processing info JSON. Checks: SFF-804, SFF-805."""
    checks.not_run_here()


def test_sft_737_golden_part(golden_or_skip):
    """SFT-737, golden part: the processing info JSON of G3 alone. Checks: SFF-804, SFF-805.

    G3 holds no export, so the sentence about the file after an export has no golden part. This part
    reads no Parquet, so it is in stage 1a (ADR-YT1F item 4).
    """
    assert checks.processing_info_faults(golden_or_skip("G03")) == []


def test_sft_737_golden_part_against_the_parquet(golden_or_skip):
    """SFT-737, golden part: the processing info JSON of G3 against its Parquet. Checks: SFF-804, SFF-805.

    This part reads the Parquet, so it is in stage 2 (ADR-YT1F item 4).
    """
    assert checks.processing_info_parquet_faults(golden_or_skip("G03")) == []


@pytest.mark.external("freemocap")
def test_sft_738_calibration_toml():
    """SFT-738 (external: freemocap) Writer: the calibration TOML. Checks: SFF-806, SFF-807, SFF-808, SFF-809."""
    checks.not_run_here()


def test_sft_738_golden_part(golden_or_skip):
    """SFT-738, golden part: each calibration TOML of G14. Checks: SFF-806, SFF-807, SFF-808, SFF-809.

    The sentence about a triangulated point needs a run of freemocap.
    """
    tomls = sorted(golden_or_skip("G14", "calibration_take").parent.rglob("*.toml"))
    assert tomls, "G14 holds a calibration TOML"
    for toml in tomls:
        assert checks.calibration_toml_faults(toml) == [], toml.name


@pytest.mark.external("freemocap")
def test_sft_739_calibration_identity_copies_library():
    """SFT-739 (external: freemocap) Writer: calibration identity, copies and the library. Checks: SFF-810 to SFF-813."""
    checks.not_run_here()


def test_sft_739_golden_part(golden_or_skip):
    """SFT-739, golden part: G14. Checks: SFF-811, SFF-812.

    The alignment and the kills need a run of freemocap.
    """
    calibration_take, mocap_take = golden_or_skip("G14", "calibration_take"), golden_or_skip("G14", "mocap_take")
    library = calibration_take.parent / "library"
    listed = checks.manifest(mocap_take)["calibration"]
    source = calibration_take / checks.manifest(calibration_take)["calibration"]["file"]
    copies = [library / source.name, library / "last_successful_camera_calibration.toml", mocap_take / listed["file"]]
    for copy in copies:
        assert copy.read_bytes() == source.read_bytes(), f"{copy.name} is a byte-identical copy"
    toml = tomllib.loads(source.read_text(encoding="utf-8"))
    assert listed["calibration_uuid"] == toml["metadata"]["calibration_uuid"]
    assert listed["sha256"] == checks.sha256(source)


@pytest.mark.parametrize("case", ["second_toml", "calibration_hash", "calibration_uuid", "by_key_and_index", "no_manifest"])
def test_sft_740_finding_and_linking_the_calibration(reader, variant, golden_or_skip, case):
    """SFT-740 Reader: finding and linking the calibration. Checks: SFF-814, SFF-815, SFF-889."""
    if case == "second_toml":  # a take with a second TOML in its root
        folder = variant("G14", "mocap_take")
        first = folder / checks.manifest(folder)["calibration"]["file"]
        toml = tomllib.loads(first.read_text(encoding="utf-8"))
        toml["metadata"]["calibration_uuid"] = "0" * 12 + "4" + "0" * 3 + "8" + "f" * 15  # another UUID version 4
        (folder / "second_camera_calibration.toml").write_bytes(checks.toml_text(toml).encode())
        result = checks.read(reader, folder)
        take = checks.the_take(result)
        want = checks.the_take(checks.committed(golden_or_skip("G14", "mocap_take")))
        assert take["links"] == want["links"] and take["folder_files"] == want["folder_files"]
        # Its name has the `<rec>` of no take (ADR-158N item 13).
        item = checks.named(result["other_files"], "second_camera_calibration.toml")
        assert (item["state"], item["reason"]) == ("invalid", "take_fact_mismatch")
        assert result["folder_warnings"].count("orphan_file") == 1
    elif case in ("calibration_hash", "calibration_uuid"):  # G9
        take = checks.the_take(checks.read(reader, golden_or_skip("G09", case)))
        assert checks.link(take, "hashes" if case == "calibration_hash" else "calibration") == "mismatch"
    elif case == "by_key_and_index":  # G14, with the camera tables in the other order in the file
        folder = variant("G14", "mocap_take")
        checks.change_calibration(folder, lambda toml, np: [toml.update({k: toml.pop(k)}) for k in reversed(list(toml)[1:])])
        take = checks.the_take(checks.read(reader, folder))
        assert checks.link(take, "camera_key") == "ok" and checks.link(take, "calibration") == "ok"
        assert "calibration_mismatch" not in take["warnings"]
    else:  # G7, the copy with no manifest
        folder = golden_or_skip("G07", "no_manifest")
        take = checks.the_take(checks.read(reader, folder))
        item = checks.folder_file(take, "_camera_calibration.toml")
        rec = checks.one(folder, "*_camera_calibration.toml").name.removesuffix("_camera_calibration.toml")
        assert item["path"] == f"{rec}_camera_calibration.toml" and item["state"] == "present"
        assert take["recording_name"] == rec
