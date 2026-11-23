"""SFT-746 to SFT-755 and SFT-770: the tracking Parquet (SPEC.md section 16, parts/parquet-descriptor.md).

freemocap writes the Parquet (decision G21H item 4). The writer tests of this file are checks on the
golden folders. They need no implementation.
"""

from __future__ import annotations

import json
import shutil

import checks_folder as checks
import pytest

PINNED = {"pyarrow": "26.0.0", "polars": "2.0.0", "duckdb": "2.0.0", "hyparquet": "1.25.6", "hyparquet-compressors": "1.1.2"}


@pytest.mark.parametrize("name", ["G03", "G13"])
def test_sft_746_schema_descriptor_and_encoding(golden_or_skip, name):
    """SFT-746 Writer: schema, descriptor and encoding. Checks: SFF-816, SFF-817, SFF-818, SFF-820, SFF-821, SFF-823, SFF-825, SFF-824.

    The file does not hold the ZSTD level, so no assertion checks "level 3" (INTERFACE_NOTES_folder.md).
    """
    folder = golden_or_skip(name)
    parquet = checks.one(folder, "*_data.parquet")
    assert checks.schema_faults(parquet) == []
    assert checks.descriptor_faults(folder) == []
    assert checks.value_faults(parquet) == []


@pytest.mark.parametrize("other", ["pyarrow", "polars", "duckdb", "hyparquet"])
def test_sft_747_other_parquet_readers(golden_or_skip, truth, other):
    """SFT-747 Reader: other Parquet readers, on the Parquet of G3. Checks: SFF-819.

    The truth file of G3 holds the SHA-256 of the values that the generator gave to the Parquet writer
    (recording-files/golden/README.md). Each reader must give values with that digest. A reader that is not installed
    is skipped.
    """
    facts = truth("G03", "take")["parquet"]
    parquet = golden_or_skip("G03") / facts["name"]
    if other == "pyarrow":
        pa, _ = checks.arrow()
        assert pa.__version__ == PINNED["pyarrow"]
        rows = checks.pyarrow_rows(parquet)
    elif other == "hyparquet":
        versions = {name: checks.node_package_version(name) for name in ("hyparquet", "hyparquet-compressors")}
        if shutil.which("node") is None or None in versions.values():
            pytest.skip("hyparquet and hyparquet-compressors are not installed in node_modules of the JavaScript adapter, or node is absent")
        assert versions == {name: PINNED[name] for name in versions}
        rows = checks.hyparquet_rows(parquet)
    else:
        module = pytest.importorskip(other, reason=f"{other} is not in the dependency group `conformance`")
        assert module.__version__ == PINNED[other]
        if other == "polars":
            rows = module.read_parquet(parquet).rows()
        else:
            rows = module.connect().execute("select * from read_parquet(?)", [str(parquet)]).fetchall()
    assert len(rows) == facts["rows"] > 0
    assert checks.values_sha256(rows) == facts["values_sha256"], "the reader gives each value bit-exactly"


def test_sft_747_int64_copy(reader, variant, golden_or_skip):
    """SFT-747 Reader: a copy of the Parquet of G3 with `frame_number` and `run_id` as int64. Checks: SFF-819."""
    folder = variant("G03")
    checks.rewrite_parquet(folder, int64=True)
    item = checks.folder_file(checks.the_take(checks.read(reader, folder)), "_data.parquet")
    assert item["state"] == "present" and item["reason"] != "bad_schema"
    assert reader.run_details(folder) == reader.run_details(golden_or_skip("G03"))


def test_sft_748_row_rules(golden_or_skip):
    """SFT-748 Writer: the row rules, on the Parquet of G3. Checks: SFF-822, SFF-827, SFF-828, SFF-831."""
    folder = golden_or_skip("G03")
    parquet = checks.one(folder, "*_data.parquet")
    assert checks.row_rule_faults(parquet) == []
    for run_id in checks.descriptor(parquet)["runs"]:
        assert checks.time_faults(folder, int(run_id)) == []


def test_sft_748_equal_fitted_times(golden_or_skip):
    """SFT-748 Writer: the committed Parquet of G12 (recording-files/golden/README.md). Checks: SFF-828.

    The Parquet holds the capture times of the camera of G12 with two equal fitted times. The two
    frames have times that differ by 1 ns.
    """
    folder = golden_or_skip("G12")
    take = checks.the_take(checks.committed(folder))
    rows = checks.rows_of(folder.with_name("equal_fitted_times.parquet"))
    (camera,) = [item for item in take["files"] if f"camera:{item['camera_label']}" == rows[0]["source"]]
    player = [record[4] for record in camera["records"]]
    strict = checks.strict_ns(player)
    equal = [k for k in range(1, len(player)) if player[k] == player[k - 1]]
    assert equal, "the camera has two rows with equal fitted times"
    assert [row["frame_number"] for row in rows] == list(range(len(player)))
    for k, row in enumerate(rows):
        assert (row["channel"], row["name"], row["component"]) == ("TIMESTAMPS", "capture", "timestamp_s")
        assert row["timestamp_s"] == row["value_f64"] == strict[k] / 10**9  # SFF-828
    for k in equal:
        assert strict[k] - strict[k - 1] == 1 and rows[k - 1]["timestamp_s"] != rows[k]["timestamp_s"]


def test_sft_749_2d_and_3d_spaces(golden_or_skip):
    """SFT-749 Writer: 2D and 3D spaces, on G3. Checks: SFF-829, SFF-830.

    Camera 1 of G3 has `display_rotation` 90. The take with one camera (`camera_plane`) is external: freemocap.
    """
    folder = golden_or_skip("G03")
    rotations = [checks.header(folder / camera["timing"])["display_rotation"] for camera in checks.manifest(folder)["cameras"]]
    assert "90" in rotations, "G3 has a rotated camera"
    assert checks.spaces_faults(folder) == []


def test_sft_750_camera_sources_and_skeletons(golden_or_skip):
    """SFT-750 Writer: camera sources and skeletons, on the Parquet of G3. Checks: SFF-826, SFF-832."""
    assert checks.sources_and_skeletons_faults(golden_or_skip("G03")) == []


@pytest.mark.external("freemocap")
def test_sft_751_runs_and_realtime_runs():
    """SFT-751 (external: freemocap) Writer: runs and realtime runs. Checks: SFF-833, SFF-834, SFF-844."""
    checks.not_run_here()


def test_sft_751_golden_part(golden_or_skip):
    """SFT-751, golden part: the realtime run of G13 against its journal and its sidecars. Checks: SFF-834, SFF-844.

    The posthoc run, the repair and the manifest with `state` `recording` need a run of freemocap.
    """
    assert checks.fold_faults(golden_or_skip("G13")) == []


def test_sft_752_realtime_warning(reader, golden_or_skip):
    """SFT-752 Reader: the realtime warning. Checks: SFF-835."""
    raw = checks.read_bytes("full", reader, None, golden_or_skip("G13"))
    take = checks.the_take(json.loads(raw))
    assert take["warnings"].count("realtime_run") == 1
    assert set(take) == checks.TAKE_MEMBERS and b"Realtime run" not in raw and b"frames processed" not in raw


def test_sft_753_charuco_observations(golden_or_skip):
    """SFT-753 Writer: ChArUco observations, on the calibration take of G14. Checks: SFF-836."""
    assert checks.charuco_faults(golden_or_skip("G14", "calibration_take")) == []


def _move_camera_0(toml, np):
    camera = checks.camera_tables(toml)[0]
    camera["translation"] = [camera["translation"][0] + 10.0, *camera["translation"][1:]]


def _rigid_change(toml, np):
    turn = checks.rotation_matrix([0.1, -0.2, 0.3])  # the new world: x' = turn · x + shift
    shift = np.array([100.0, -50.0, 25.0])
    for camera in checks.camera_tables(toml):
        rotation = checks.rotation_matrix(camera["rotation"]) @ turn.T
        camera["translation"] = (np.array(camera["translation"]) - rotation @ shift).tolist()
        camera["rotation"] = checks.rodrigues(rotation)


def _change_fx(toml, np):
    checks.camera_tables(toml)[0]["matrix"][0][0] += 1e-3


@pytest.mark.parametrize(
    ("change", "mismatch"),
    [(_move_camera_0, True), (_rigid_change, False), (_change_fx, True)],
    ids=["camera_0_moved_10_mm", "rigid_change_of_the_world", "fx_differs_by_1e-3"],
)
def test_sft_754_geometry_against_the_toml(reader, variant, change, mismatch):
    """SFT-754 Reader: geometry against the TOML. Checks: SFF-837."""
    folder = variant("G03")
    checks.change_calibration(folder, change)
    take = checks.the_take(checks.read(reader, folder))
    assert ("calibration_mismatch" in take["warnings"]) == mismatch
    if mismatch:
        assert all(run["geometry"] == "stored" for run in reader.run_details(folder))


@pytest.mark.external("freemocap")
def test_sft_755_parquet_publication():
    """SFT-755 (external: freemocap) Writer: Parquet publication. Checks: SFF-838. No golden part."""
    checks.not_run_here()


def _missing_member(model):
    del model["detector_type"]


def _wrong_type(model):
    model["scale_reference_name"] = 5


def _unknown_member(model):
    model["skeleton"]["x_unknown"] = 1


def _writer_rule(model):
    model["skeleton"]["joints"][0]["child"] = "no_such_segment"  # the example of the Input line


def _number_forms(model):
    frame = model["skeleton"]["segments"][0]["frame"]
    frame["handedness"] = float(frame["handedness"])  # `1.0` for an integer member
    model["skeleton"]["landmarks"][0]["position"][0] = 0  # `0` for a value of a `position`


def _default_and_null(model):
    # ADR-H2HQ item 2: a reader accepts these two, a writer does not write them.
    del model["anchor_segment_name"]  # its row gives a default
    model["skeleton"]["segments"][0]["observation_frame"] = None  # its row says "omitted when null"


@pytest.mark.parametrize(
    ("change", "state", "reason"),
    [
        (_missing_member, "invalid", "bad_schema"), (_wrong_type, "invalid", "bad_schema"),
        (_unknown_member, "invalid", "bad_schema"), (_writer_rule, "present", None), (_number_forms, "present", None),
        (_default_and_null, "present", None),
    ],
    ids=[
        "missing_member", "wrong_json_type", "unknown_member", "writer_rule_only", "integer_1.0_and_position_0",
        "default_absent_and_omitted_null",
    ],
)  # fmt: skip
def test_sft_770_structure_of_a_model(reader, variant, golden_or_skip, change, state, reason):
    """SFT-770 Reader: the structure of a model in the descriptor. Checks: SFF-893. A test of the scope `full` only."""
    folder = variant("G03")
    before = checks.descriptor(checks.one(folder, "*_data.parquet"))

    def change_model(described):
        models = [model for run in described["runs"].values() for model in run["models"].values()]
        change(next(model for model in models if model["skeleton"]["joints"]))

    parquet = checks.rewrite_parquet(folder, change_model)
    after = checks.descriptor(parquet)
    assert after != before or change is _number_forms, "the copy has a changed descriptor"
    faults = checks.descriptor_structure_faults(after, reader=True)
    assert bool(faults) == (state == "invalid"), "the copy has the structure fault that the test wants, and no other"
    item = checks.folder_file(checks.the_take(checks.read(reader, folder)), "_data.parquet")
    assert (item["state"], item["reason"]) == (state, reason)
    if state == "present":  # "as for G3"
        assert item == checks.folder_file(checks.the_take(checks.committed(golden_or_skip("G03"))), "_data.parquet")
