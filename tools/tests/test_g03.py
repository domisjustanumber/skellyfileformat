"""Cross-checks of the committed files of golden folder G3, and tests of `goldgen.folder_common`.

The cross-checks read the files with `json`, `tomllib`, pyarrow and Pillow. They compute each value
again from the text of the spec. They do not use the code path that wrote the files. A test that needs
pyarrow or Pillow skips when the package is absent.
"""

from __future__ import annotations

import hashlib
import io
import json
import math
import re
import tomllib
from pathlib import Path

import pytest
from goldgen import folder_common

from test_golden_files import GOLDEN, footer_values, load, read_sidecar

G03 = GOLDEN / "G03"
CASE = G03 / "take"
MEDIA = "synchronized_videos"
PART = GOLDEN.parent / "parts" / "parquet-descriptor.md"
pytestmark = pytest.mark.skipif(not CASE.is_dir(), reason="recording-files/golden/G03 does not exist")

# The table of SPEC.md section 16: the column, the Arrow type and the nullability.
SCHEMA = [
    ("timestamp_s", "double", False), ("sensor_group", "string", False), ("frame_number", "int32", False),
    ("source", "string", False), ("reference_frame", "string", True), ("channel", "string", False),
    ("name", "string", False), ("component", "string", False), ("value", "float", True),
    ("value_f64", "double", True), ("units", "string", False), ("run_id", "int32", False),
]  # fmt: skip
MODEL_MEMBERS = {
    "model_id", "detector_type", "tracker_keypoint_names", "segment_topology", "skeleton", "rest_pose", "mappings",
    "center_of_mass", "segment_masses", "scale_reference_name", "anchor_segment_name",
}  # fmt: skip
SKELETON_MEMBERS = {
    "name", "landmarks", "segments", "joints", "chains", "landmark_groups", "landmark_connections",
    "derived_quantities", "coordinate_system",
}  # fmt: skip
PROVENANCE_MEMBERS = {
    "attempt_id", "recorded_at", "effective_settings", "default_settings", "input_signatures", "software",
    "output_sources", "limitations", "base_run_id", "base_descriptor_signature", "origin", "coverage",
}  # fmt: skip
STAGES = ["timing", "observations", "triangulation", "filtering", "scale_fit", "reconstruction", "biomechanics", "reprojection"]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest() -> dict:
    return json.loads((CASE / "recording_manifest.json").read_bytes())


def rec() -> str:
    return manifest()["recording_name"]


def parquet_path() -> Path:
    return CASE / f"{rec()}_data.parquet"


def toml() -> dict:
    return tomllib.loads((CASE / manifest()["calibration"]["file"]).read_bytes().decode())


def processing_info() -> dict:
    return json.loads((CASE / f"{rec()}_recording_info.json").read_bytes())


def descriptor() -> dict:
    pq = pytest.importorskip("pyarrow.parquet")
    return json.loads(pq.read_schema(parquet_path()).metadata[b"freemocap.recording"])


def rows() -> list[dict]:
    pq = pytest.importorskip("pyarrow.parquet")
    return pq.read_table(parquet_path()).to_pylist()


def strict_times_ns(camera: dict) -> list[int]:
    """The strict player times of a camera from its sidecar (SFF-777, SFF-781, SFF-782)."""
    _, sidecar_rows, footer = read_sidecar(CASE / camera["timing"])
    fit = footer_values(footer, "fit_segment")
    sources = [int(row[1]) for row in sidecar_rows]
    strict: list[int] = []
    for source in sources:
        p = int(fit["t0_ns"]) + (source - sources[0]) * int(fit["period_ps"]) // 1000
        strict.append(p if not strict else max(p, strict[-1] + 1))
    return strict


# ---------------------------------------------------------------- folder_common, standard library only


def test_strict_and_group_times():
    assert folder_common.strict_ns([5, 5, 5, 9, 8]) == [5, 6, 7, 9, 10]  # SFF-782
    assert folder_common.group_ns([[1, 1, -3], [2, 1, 0]]) == [2, 1, -1]  # SFF-828: 1.5 -> 2 and -1.5 -> -1
    assert folder_common.seconds(33_483_200) == 0.0334832
    assert folder_common.sensor_group_name(["b", "a"]) == "camera_group:" + hashlib.sha256(b"a|b").hexdigest()[:6]


def test_values_sha256_encoding():
    """The digest of recording-files/golden/README.md for one row, from bytes written by hand."""
    row = dict.fromkeys(name for name, _, _ in SCHEMA) | {
        "timestamp_s": 0.5, "sensor_group": "g", "frame_number": 1, "value": 0.25, "run_id": -1,
    }  # fmt: skip
    data = bytes.fromhex(
        "01" "000000000000e03f"  # timestamp_s
        "01" "01000000" "67"  # sensor_group
        "01" "0100000000000000"  # frame_number
        "00" "00" "00" "00" "00"  # source, reference_frame, channel, name, component
        "01" "0000803e"  # value
        "00" "00"  # value_f64, units
        "01" "ffffffffffffffff"  # run_id
    )
    assert folder_common.values_sha256([row]) == hashlib.sha256(data).hexdigest()


def test_calibration_toml_text():
    camera = {"camera_label": "cam0", "index": 0, "size": [2, 1], "controls_at_calibration": {"gain": 3}}
    text = folder_common.calibration_toml({"writer": "w", "aligned": False, "cost": 0.5}, {"squares_x": 5}, [camera])
    assert tomllib.loads(text.decode()) == {
        "metadata": {"writer": "w", "aligned": False, "cost": 0.5, "board": {"squares_x": 5}},
        "cam0": {"camera_label": "cam0", "index": 0, "size": [2, 1], "controls_at_calibration": {"gain": 3}},
    }
    assert text.startswith(b'[metadata]\nwriter = "w"\naligned = false\ncost = 0.5\n\n[metadata.board]\n')


def test_expected_result_scopes():
    facts = {
        "take_uuid": "u", "recording_name": "r", "files": [], "info_path": "r_info.json",
        "folder_files": [("r_info.json", "capture_info"), ("r_data.parquet", "tracking"), ("r_camera_calibration.toml", "calibration")],
    }  # fmt: skip
    full, player = (folder_common.expected_result(facts, scope)["takes"][0] for scope in ("full", "player"))
    assert [item["path"] for item in full["folder_files"]] == ["r_camera_calibration.toml", "r_data.parquet", "r_info.json"]
    assert [item["state"] for item in player["folder_files"]] == ["not_checked", "not_checked", "present"]
    assert [item["warnings"] for item in player["folder_files"]] == [[], [], ["prerelease"]]
    assert {link["state"] for link in full["links"]} == {"ok"}
    assert [link["check"] for link in player["links"] if link["state"] == "not_checked"] == [
        "frames", "dimensions", "hashes", "calibration",
    ]  # fmt: skip


# ---------------------------------------------------------------- the take against G1, and the manifest


def test_take_is_the_take_of_g01_with_more_folder_files():
    def sums(folder: Path) -> dict:
        lines = (folder / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
        return {name: digest for digest, name in (line.split("  ", 1) for line in lines) if name.startswith("take/")}

    g01, g03 = sums(GOLDEN / "G01"), sums(G03)
    new = {f"take/{rec()}{suffix}" for suffix in ("_camera_calibration.toml", "_data.parquet", "_recording_info.json")}
    assert set(g03) - set(g01) == new and set(g01) <= set(g03)
    rotated = f"take/{manifest()['cameras'][1]['timing']}"
    assert {name for name in g01 if g01[name] != g03[name]} == {"take/recording_manifest.json", rotated}
    # Camera 1 has `display_rotation` 90 (SFT-749). A header line has no CRC, so no other line changes.
    old, now = ((folder / rotated).read_bytes().split(b"\n") for folder in (GOLDEN / "G01", G03))
    assert [(a, b) for a, b in zip(old, now, strict=True) if a != b] == [(b"# display_rotation=0", b"# display_rotation=90")]
    truth = load(G03 / "take.truth.json")
    assert truth | {"parquet": None} == load(GOLDEN / "G01" / "take.truth.json") | {"parquet": None}
    assert load(G03 / "take.full.json")["takes"][0]["files"] == load(GOLDEN / "G01" / "take.full.json")["takes"][0]["files"]
    assert not (CASE / "exports").exists() and not (CASE / "tracker_schema.json").exists()  # Appendix A, SFF-832


def test_manifest_lists_the_folder_files():
    m, g01 = manifest(), json.loads((GOLDEN / "G01" / "take" / "recording_manifest.json").read_bytes())
    name = m["recording_name"]
    assert list(m) == list(g01)  # SFF-723: the members and their order
    assert [(f["path"], f["role"], f["owner"]) for f in m["files"]] == [
        (f"{name}_data.parquet", "tracking", "freemocap"),
        (f"{name}_info.json", "capture_info", "skellycam"),
        (f"{name}_recording_info.json", "processing_info", "freemocap"),
    ]  # in order of `path`; no item has the role `export`
    for item in m["files"]:
        assert item["sha256"] == (None if item["role"] == "tracking" else sha256(CASE / item["path"]))  # SFF-723
    calibration = m["calibration"]
    assert list(calibration) == ["calibration_uuid", "file", "sha256"]
    assert calibration["file"] == f"{name}_camera_calibration.toml" and calibration["sha256"] == sha256(CASE / calibration["file"])
    tables = toml()
    assert calibration["calibration_uuid"] == tables["metadata"]["calibration_uuid"]
    for camera in m["cameras"]:
        assert tables[camera["calibration_camera"]]["camera_key"] == camera["camera_key"]
    # SFF-728: the summary. Each other member of the manifest is the member of G1.
    assert m["summary"]["calibration"] == {
        "calibration_uuid": tables["metadata"]["calibration_uuid"],
        "source_take_uuid": tables["metadata"]["source_take_uuid"],
    }
    changed = {"cameras", "calibration", "files", "summary"}
    assert {key for key in m if m[key] != g01[key]} == changed  # so SFF-881 adds no privacy field
    assert {key for key in m["summary"] if m["summary"][key] != g01["summary"][key]} == {"calibration", "processing_runs", "cameras"}
    # The summary of camera 1 differs only in `display_rotation` (SFF-728).
    assert [c["display_rotation"] for c in m["summary"]["cameras"]] == [0, 90]
    assert [c | {"display_rotation": 0} for c in m["summary"]["cameras"]] == g01["summary"]["cameras"]


def test_manifest_summary_runs_agree_with_the_descriptor():
    runs = descriptor()["runs"]
    expected = []
    for run_id in sorted(runs, key=int):
        stages = [s for g in runs[run_id]["processing"].values() for s in g["stage_provenance"]["stages"].values()]
        assert len({s["recorded_at"] for s in stages}) > 1, "the take tests `the latest`"
        latest = max(stages, key=lambda s: s["recorded_at"].replace("Z", "+00:00"))
        expected.append({"run_id": int(run_id), "origin": "posthoc", "recorded_at": latest["recorded_at"]})
        assert {s["origin"] for s in stages} == {"posthoc"}
    assert manifest()["summary"]["processing_runs"] == expected


# ---------------------------------------------------------------- calibration TOML (section 15)


def rodrigues(vector: list[float]) -> list[list[float]]:
    angle = math.sqrt(sum(v * v for v in vector))
    x, y, z = (v / angle for v in vector) if angle else (0.0, 0.0, 0.0)
    c, s = math.cos(angle), math.sin(angle)
    k = 1 - c
    return [
        [c + x * x * k, x * y * k - z * s, x * z * k + y * s],
        [y * x * k + z * s, c + y * y * k, y * z * k - x * s],
        [z * x * k - y * s, z * y * k + x * s, c + z * z * k],
    ]


def test_calibration_toml():
    data = (CASE / manifest()["calibration"]["file"]).read_bytes()
    assert not data.startswith(b"\xef\xbb\xbf") and b"\r" not in data and data.endswith(b"\n")  # SFF-700
    tables = tomllib.loads(data.decode())
    metadata = tables["metadata"]
    assert list(metadata) == [
        "format_version", "format_prerelease", "writer", "calibration_uuid", "source_take_uuid",
        "reprojection_error_px", "initial_cost", "final_cost", "n_iterations", "solver_time_seconds",
        "n_observations_used", "n_observations_rejected", "aligned", "solver_method", "transformation_history", "board",
    ]  # SFF-807: `aligned` is false, so no alignment key  # fmt: skip
    assert (metadata["format_version"], metadata["format_prerelease"]) == ("2.0", 1)
    assert metadata["aligned"] is False and metadata["solver_method"] == "anipose" and metadata["transformation_history"] == []
    assert re.fullmatch(r"[0-9a-f]{32}", metadata["calibration_uuid"]) and metadata["calibration_uuid"][12] == "4"
    assert list(metadata["board"]) == ["squares_x", "squares_y", "square_length_mm", "marker_length_ratio", "aruco_dictionary_enum"]
    assert metadata["board"]["squares_x"] >= 2 and metadata["board"]["squares_y"] >= 2

    cameras = manifest()["cameras"]
    assert list(tables) == ["metadata", *(camera["camera_label"] for camera in cameras)]  # SFF-806
    info = json.loads((CASE / f"{rec()}_info.json").read_bytes())
    for camera in cameras:
        table = tables[camera["camera_label"]]
        assert list(table) == [
            "name", "id", "camera_key", "camera_label", "index", "size", "matrix", "distortions", "rotation",
            "translation", "world_orientation", "world_position", "controls_at_calibration",
        ]  # fmt: skip
        assert table["name"] == table["id"] == table["camera_label"] == camera["camera_label"]
        assert (table["camera_key"], table["index"]) == (camera["camera_key"], camera["group_position"])
        fx, fy, cx, cy = table["matrix"][0][0], table["matrix"][1][1], table["matrix"][0][2], table["matrix"][1][2]
        assert table["matrix"] == [[fx, 0.0, cx], [0.0, fy, cy], [0.0, 0.0, 1.0]]
        assert len(table["distortions"]) == 5 and table["distortions"][4] == 0.0
        r, t = rodrigues(table["rotation"]), table["translation"]
        transposed = [list(column) for column in zip(*r)]
        assert table["world_orientation"] == transposed  # SFF-808
        assert table["world_position"] == [0.0 - sum(row[i] * t[i] for i in range(3)) for row in transposed]
        if table["index"] == 0:
            assert table["rotation"] == table["translation"] == [0.0, 0.0, 0.0]  # SFF-809
        controls = info["camera_configs"][camera["camera_key"]]["controls"]
        assert table["controls_at_calibration"] == {k: v["value"] for k, v in controls.items() if v["value"] is not None}
    pytest.importorskip("PIL")
    for camera in cameras:
        assert tuple(tables[camera["camera_label"]]["size"]) == stored_size(camera)


def stored_size(camera: dict) -> tuple[int, int]:
    """The size of the first stored JPEG of a camera file, through `byte_offset` and `byte_size` of its sidecar."""
    from PIL import Image

    _, sidecar_rows, _ = read_sidecar(CASE / camera["timing"])
    at, size = int(sidecar_rows[0][5]), int(sidecar_rows[0][6])
    return Image.open(io.BytesIO((CASE / camera["video"]).read_bytes()[at : at + size])).size


# ---------------------------------------------------------------- processing info JSON (section 14)


def test_processing_info():
    info, m = processing_info(), manifest()
    assert list(info) == ["skellyfileformat", "format_version", "format_prerelease", "writer", "take_uuid", "processed"]
    assert (info["skellyfileformat"], info["format_version"], info["format_prerelease"]) == ("processing_info", "2.0", 1)
    assert info["take_uuid"] == m["take_uuid"]
    processed = info["processed"]
    assert list(processed) == [
        "schema_version", "parquet_sha256", "recording_id", "parquet", "selected_run_id", "runs", "conventions",
        "export_inventories",
    ]  # fmt: skip
    assert processed["schema_version"] == 1 and processed["export_inventories"] == []
    assert processed["parquet_sha256"] == sha256(parquet_path())
    assert (processed["recording_id"], processed["parquet"]) == (rec(), parquet_path().name)
    assert str(processed["selected_run_id"]) in processed["runs"]
    assert processed["conventions"] == {
        "quaternion_order": "wxyz", "segment_pose": "saved origin and world orientation", "units": "per component",
        "coordinates": "per reference frame", "array_order": "frames, names, components",
    }  # fmt: skip
    kinds = {"LANDMARKS_3D", "KEYPOINTS_3D", "RAW_KEYPOINTS_3D", "OVERLAY_2D", "SEGMENT_ORIGINS", "ROTATIONS_WORLD"}
    runs = descriptor()["runs"]
    assert list(processed["runs"]) == list(runs)
    for run_id, run in processed["runs"].items():
        assert list(run) == ["sensor_groups", "cameras", "reference_frames", "data"]
        assert run["sensor_groups"] == runs[run_id]["sensor_groups"]
        assert run["cameras"] == [camera["camera_label"] for camera in m["cameras"]]
        assert run["reference_frames"] == runs[run_id]["reference_frames"]
        assert run["data"] == [
            {
                "channel": c["kind"], "source": c["source"], "sensor_group": c["sensor_group"],
                "reference_frame": c["reference_frame"], "names": c["names"], "components": c["components"],
            }
            for c in runs[run_id]["channels"]
            if c["kind"] in kinds
        ]  # fmt: skip
        assert {item["channel"] for item in run["data"]} == {"OVERLAY_2D", "RAW_KEYPOINTS_3D", "KEYPOINTS_3D"}


# ---------------------------------------------------------------- tracking Parquet (section 16)


def test_parquet_schema_encodings_and_row_groups():
    pq = pytest.importorskip("pyarrow.parquet")
    file = pq.ParquetFile(parquet_path())
    schema = file.schema_arrow
    assert [(f.name, str(f.type), f.nullable) for f in schema] == SCHEMA  # SFF-816
    assert list(schema.metadata) == [b"freemocap.recording"]  # SFF-817
    assert file.metadata.created_by == "parquet-cpp-arrow version 26.0.0"
    channels = descriptor()["runs"]["0"]["channels"]
    assert file.metadata.num_row_groups == len(channels)
    for index, channel in enumerate(channels):
        group = file.metadata.row_group(index)
        for column in (group.column(i) for i in range(group.num_columns)):
            assert column.compression == "ZSTD"  # SFF-818. The file does not show the level
            dictionary = {"PLAIN_DICTIONARY", "RLE_DICTIONARY"} & set(column.encodings)
            if column.path_in_schema in ("value", "value_f64"):
                assert "BYTE_STREAM_SPLIT" in column.encodings and not dictionary and not column.has_dictionary_page
            assert column.statistics.null_count == 0 or column.path_in_schema in ("reference_frame", "value", "value_f64")
        table = file.read_row_group(index).to_pylist()
        keys = {(r["run_id"], r["sensor_group"], r["source"], r["reference_frame"], r["channel"]) for r in table}
        assert keys == {(0, channel["sensor_group"], channel["source"], channel["reference_frame"], channel["kind"])}  # SFF-823
        frames = [r["frame_number"] for r in table]
        per_frame = len(channel["names"]) * len(channel["components"])
        assert frames == sorted(frames) and len(frames) == per_frame * len(set(frames))  # whole frames


def test_descriptor_members():
    d, m = descriptor(), manifest()
    assert list(d) == [
        "schema_version", "format_version", "format_prerelease", "writer", "take_uuid", "recording_id",
        "recording_info", "runs",
    ]  # no `selected_run_id`  # fmt: skip
    assert (d["schema_version"], d["format_version"], d["format_prerelease"]) == (2, "2.0", 1)  # SFF-817, SFF-825
    assert (d["take_uuid"], d["recording_id"], d["recording_info"]) == (m["take_uuid"], rec(), {})  # SFF-824
    assert d["writer"] == m["writer"] and list(d["runs"]) == ["0"]
    run = d["runs"]["0"]
    assert list(run) == [
        "calibration_updates", "scale_fits", "camera_geometry", "sensor_groups", "sources", "reference_frames",
        "models", "processing", "channels", "static_channels", "checkpoints",
    ]  # fmt: skip
    keys = sorted(camera["camera_key"] for camera in m["cameras"])
    (group,) = run["sensor_groups"]
    assert group == "camera_group:" + hashlib.sha256("|".join(keys).encode()).hexdigest()[:6]
    assert run["sensor_groups"][group] == {
        "clock_description": "recording-relative seconds; timing method declared per source",
        "sample_count": 90,
    }
    assert set(run["camera_geometry"]) | set(run["processing"]) <= set(run["sensor_groups"])

    # SFF-826: the camera sources.
    for camera in m["cameras"]:
        label = camera["camera_label"]
        assert run["sources"][f"camera:{label}"] == {
            "kind": "camera",
            "definition": {
                "camera_key": camera["camera_key"], "camera_label": label, "video_filename": Path(camera["video"]).name,
                "timing_filename": Path(camera["timing"]).name, "timing_method": "recorded", "inferred_offset_s": 0.0,
            },
        }  # fmt: skip
        assert run["reference_frames"][f"camera:{label}:image"] == {
            "camera_key": camera["camera_key"], "calibration_camera": camera["calibration_camera"], "width": 64,
            "height": 48,
        }  # fmt: skip
    assert run["sources"][f"timing:{group}"] == {"kind": "timing", "definition": {"method": "mean_camera_times"}}
    assert {s["kind"] for s in run["sources"].values()} == {"camera", "timing", "tracker"}
    assert all(isinstance(s["definition"], dict) and set(s) == {"kind", "definition"} for s in run["sources"].values())
    world = run["reference_frames"]["calibrated_world"]  # SFF-830
    assert world == {
        "name": "calibrated_world", "basis": "blender_x_right_y_forward_z_up", "units": "mm", "alignment": None,
        "additional_transform": None,
    }  # fmt: skip

    # The channels and the reference rules of `RunDescriptor`.
    channel_keys = [(c["sensor_group"], c["source"], c["reference_frame"], c["kind"]) for c in run["channels"]]
    assert len(set(channel_keys)) == len(channel_keys)
    for channel in run["channels"]:
        assert list(channel) == ["sensor_group", "source", "reference_frame", "kind", "names", "components", "stage", "dtype"]
        assert channel["sensor_group"] == group and channel["source"] in run["sources"]
        assert channel["reference_frame"] is None or channel["reference_frame"] in run["reference_frames"]
        assert channel["names"] and len(set(channel["names"])) == len(channel["names"]) and channel["components"]
        assert channel["dtype"] == ("float64" if channel["kind"] == "TIMESTAMPS" else "float32")  # SFF-820
        kind, prefix = channel["kind"], channel["source"].split(":")[0]
        if kind == "TIMESTAMPS":
            name = {"camera": "capture", "timing": "synchronized"}[prefix]
            expected = (None, [name], {"timestamp_s": "s"}, "timing")
        elif kind == "OVERLAY_2D":
            assert prefix == "keypoint_model" and re.fullmatch(r"camera:[0-9a-f]+:image", channel["reference_frame"])
            assert all(re.fullmatch(r"[^.]+\..+", name) for name in channel["names"])  # row rule 9
            expected = (channel["reference_frame"], channel["names"], {"x": "px", "y": "px", "visibility": "1"}, "observations")
        else:
            stage = {"RAW_KEYPOINTS_3D": "triangulation", "KEYPOINTS_3D": "filtering"}[kind]
            expected = ("calibrated_world", channel["names"], {"x": "mm", "y": "mm", "z": "mm"}, stage)
        assert (channel["reference_frame"], channel["names"], channel["components"], channel["stage"]) == expected
        assert list(channel["components"]) == list(expected[2])
    assert {c["kind"] for c in run["channels"]} == {"TIMESTAMPS", "OVERLAY_2D", "RAW_KEYPOINTS_3D", "KEYPOINTS_3D"}
    assert (run["calibration_updates"], run["scale_fits"], run["static_channels"], run["checkpoints"]) == ({}, [], [], [])

    provenance = run["processing"][group]["stage_provenance"]
    assert provenance["version"] == 1 and list(provenance["stages"]) == [s for s in STAGES if s in provenance["stages"]]
    for stage, item in provenance["stages"].items():
        assert set(item) == PROVENANCE_MEMBERS and (item["origin"], item["coverage"]) == ("posthoc", None)  # SFF-834
        assert item["output_sources"] and set(item["output_sources"]) <= set(run["sources"])
        assert any(c["stage"] == stage for c in run["channels"])
        assert re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", item["recorded_at"])


def test_descriptor_models():
    """SFF-832, and the structure of the two models (parts/parquet-descriptor.md)."""
    models = descriptor()["runs"]["0"]["models"]
    trackers = descriptor()["runs"]["0"]["channels"]
    example = json.loads(re.search(r"```json\n(.*?)```", PART.read_text(encoding="utf-8"), re.DOTALL).group(1))
    stick = dict(models["stick"])
    connections, topology = stick.pop("tracker_connections"), stick.pop("segment_topology")
    assert stick == example and list(stick) == list(example)
    assert connections and "tracker_connections" not in models["pair"]  # a model with no pair omits the member
    assert list(models["stick"])[:5] == [
        "model_id", "detector_type", "tracker_keypoint_names", "tracker_connections", "segment_topology",
    ]  # fmt: skip
    for model_id, model in models.items():
        assert model["model_id"] == model_id and set(model) - {"tracker_connections"} == MODEL_MEMBERS
        assert set(model["skeleton"]) == SKELETON_MEMBERS and model["skeleton"]["landmarks"] and model["skeleton"]["segments"]
        names = model["tracker_keypoint_names"]
        assert all(len(pair) == 2 and set(pair) <= set(names) for pair in model.get("tracker_connections", []))
        assert model["segment_topology"] == [
            {
                "name": s["name"], "parent": model["rest_pose"]["parents"][s["name"]],
                "proximal": s["frame"]["origin"], "distal": s["frame"]["primary_point"],
            }
            for s in model["skeleton"]["segments"]
        ]  # fmt: skip
        landmarks = {item["name"] for item in model["skeleton"]["landmarks"]}
        segments = [s["name"] for s in model["skeleton"]["segments"]]
        assert all({t["proximal"], t["distal"]} <= landmarks for t in model["segment_topology"])
        # Writer rules that are cheap to check.
        assert set(model["rest_pose"]["parents"]) == set(model["rest_pose"]["orientations"]) == set(segments)
        assert [s for s, p in model["rest_pose"]["parents"].items() if p is None] == [model["rest_pose"]["root_segment_name"]]
        assert set(model["rest_pose"]["connect_ats"]) == {j["child"] for j in model["skeleton"]["joints"]}
        assert set(model["segment_masses"]) == set(model["center_of_mass"]["definitions"])  # no definition is sided
        for definition in model["center_of_mass"]["definitions"].values():
            assert abs(sum(w["weight"] for w in definition["weights"]) - 1) <= 1e-6
        for q in model["rest_pose"]["orientations"].values():
            assert abs(math.sqrt(sum(q[k] ** 2 for k in "wxyz")) - 1) <= 1e-9
        for s in model["skeleton"]["segments"]:
            assert set(s) - {"observation_frame"} == {"name", "landmarks", "frame", "aliases", "anatomical_segment"}
            assert set(s["frame"]) == {"origin", "primary_point", "primary_axis", "secondary_point", "secondary_axis", "handedness"}
            assert s["frame"]["handedness"] in (1, -1) and s["frame"]["primary_point"] in s["landmarks"]
        (mapping,) = model["mappings"]
        assert set(mapping) == {"entries", "prefix", "known_tracker_keypoints", "passthrough"}
        assert mapping["known_tracker_keypoints"] == sorted(names) and mapping["passthrough"] == (mapping["entries"] == {})
        # Each tracker of G3 gives the keypoints of one model.
        points = [c["names"] for c in trackers if c["kind"] == "KEYPOINTS_3D" and c["source"].endswith(f"_{model_id}")]
        assert points == [names]


def test_camera_geometry_agrees_with_the_toml():
    """SFF-837: so the take has no warning `calibration_mismatch`."""
    run, tables = descriptor()["runs"]["0"], toml()
    (geometry,) = run["camera_geometry"].values()
    assert [camera["index"] for camera in geometry] == [0, 1]
    for camera in geometry:
        assert list(camera) == [
            "id", "camera_key", "index", "image_size", "intrinsics", "extrinsics", "world_position", "world_orientation",
        ]  # fmt: skip
        table = tables[camera["id"]]
        assert (camera["camera_key"], camera["index"], camera["image_size"]) == (table["camera_key"], table["index"], table["size"])
        k, d = table["matrix"], table["distortions"]
        assert camera["intrinsics"] == {
            "fx": k[0][0], "fy": k[1][1], "cx": k[0][2], "cy": k[1][2], "k1": d[0], "k2": d[1], "p1": d[2], "p2": d[3],
        }  # fmt: skip
        assert table["rotation"] == [0.0, 0.0, 0.0], "the quaternion check below is for the identity"
        assert camera["extrinsics"] == {"quaternion_wxyz": [1.0, 0.0, 0.0, 0.0], "translation": table["translation"]}
        assert camera["world_position"] == table["world_position"]
        assert camera["world_orientation"] == table["world_orientation"]


def test_row_rules():
    run, table = descriptor()["runs"]["0"], rows()
    declared = {(c["sensor_group"], c["source"], c["reference_frame"], c["kind"]): c for c in run["channels"]}
    trajectories: dict[tuple, list] = {}
    for row in table:
        channel = declared[(row["sensor_group"], row["source"], row["reference_frame"], row["channel"])]  # rule 1
        assert row["run_id"] == 0 and row["name"] in channel["names"]
        assert row["units"] == channel["components"][row["component"]]
        used, other = ("value_f64", "value") if channel["dtype"] == "float64" else ("value", "value_f64")
        assert row[other] is None  # SFF-820
        assert row[used] is None or math.isfinite(row[used])  # rule 2, SFF-821
        assert row["frame_number"] >= 0 and math.isfinite(row["timestamp_s"])
        if row["channel"] == "TIMESTAMPS":  # rule 6
            assert (row["component"], row["units"], row["reference_frame"]) == ("timestamp_s", "s", None)
            assert row["value_f64"] == row["timestamp_s"]
        key = (row["sensor_group"], row["source"], row["reference_frame"], row["channel"], row["name"], row["component"])
        trajectories.setdefault(key, []).append((row["frame_number"], row["timestamp_s"], row[used]))
    assert len(trajectories) == sum(len(c["names"]) * len(c["components"]) for c in run["channels"])

    grids: dict[tuple, list] = {}
    for key, samples in trajectories.items():
        assert len(samples) == run["sensor_groups"][key[0]]["sample_count"]  # rule 3
        assert all(a[0] < b[0] and a[1] < b[1] for a, b in zip(samples, samples[1:]))
        grid = [sample[:2] for sample in samples]
        assert grids.setdefault(key[:3], grid) == grid  # rule 4

    # Rule 7 and SFF-831. The take has a point that the tracker did not detect.
    undetected = 0
    for (*context, kind, name, component), samples in trajectories.items():
        if kind != "OVERLAY_2D" or component != "visibility":
            continue
        xs, ys = (trajectories[(*context, kind, name, c)] for c in ("x", "y"))
        for (_, _, visibility), (_, _, x), (_, _, y) in zip(samples, xs, ys):
            assert 0 <= visibility <= 1 and (x is None) == (y is None) == (visibility == 0)
            undetected += x is None
            assert x is None or (0 <= x < 64 and 0 <= y < 48)  # SFF-829
    assert undetected > 0
    # SFT-749: the rotated camera has 2D values in stored-JPEG pixels. The upright picture is 48 wide.
    rotated = manifest()["cameras"][1]["camera_label"]
    assert read_sidecar(CASE / manifest()["cameras"][1]["timing"])[0]["display_rotation"] == "90"
    xs = [s[2] for key, samples in trajectories.items() if key[2] == f"camera:{rotated}:image" and key[5] == "x" for s in samples]
    assert max(x for x in xs if x is not None) >= 48
    raw = [s[2] for key, samples in trajectories.items() if key[3] == "RAW_KEYPOINTS_3D" for s in samples]
    assert None in raw and any(v is not None for v in raw), "a missing 3D sample is a row with a null value"


def test_truth_digest_of_the_parquet_values():
    """SFT-747: the digest of recording-files/golden/README.md, from the values that pyarrow reads, equals the truth file."""
    truth = load(G03 / "take.truth.json")["parquet"]
    table = rows()
    assert truth["name"] == parquet_path().name and truth["rows"] == len(table)
    assert folder_common.values_sha256(table) == truth["values_sha256"]
    # The digest sees a change of one bit.
    changed = [dict(row) for row in table]
    changed[0]["timestamp_s"] = math.nextafter(changed[0]["timestamp_s"], 1.0)
    assert folder_common.values_sha256(changed) != truth["values_sha256"]


def test_times_are_the_strict_player_times():
    """SFF-827, SFF-828: each time comes from the sidecars, with integer arithmetic."""
    cameras = manifest()["cameras"]
    strict = {camera["camera_label"]: strict_times_ns(camera) for camera in cameras}
    n = len(cameras)
    group_ns = [(2 * sum(times) + n) // (2 * n) for times in zip(*strict.values(), strict=True)]
    for row in rows():
        frame = row["frame_number"]
        if row["channel"] == "OVERLAY_2D" or row["name"] == "capture":
            label = (row["reference_frame"] or row["source"]).split(":")[1]
            assert row["timestamp_s"] == strict[label][frame] / 10**9
        else:
            assert row["timestamp_s"] == group_ns[frame] / 10**9
        assert 0 <= frame < 90


# ---------------------------------------------------------------- the expected results (section 23)


def test_results_agree_with_the_files():
    full, player = (load(G03 / f"take.{scope}.json") for scope in ("full", "player"))
    m, name = manifest(), rec()
    (take,) = full["takes"]
    assert (full["folder_state"], full["folder_warnings"], full["other_files"], full["legacy"]) == ("ok", [], [], None)
    assert (take["state"], take["manifest"], take["warnings"], take["may_contain_private_data"]) == ("complete", "present", [], True)

    # SFF-885: one item for each `files` item of the manifest and one for `calibration.file`.
    roles = {item["path"]: item["role"] for item in m["files"]} | {m["calibration"]["file"]: "calibration"}
    root_files = {p.name for p in CASE.iterdir() if p.is_file()} - {"recording_manifest.json"}
    assert set(roles) == root_files
    assert take["folder_files"] == [
        {"path": path, "role": roles[path], "state": "present", "reason": None, "warnings": ["prerelease"]}
        for path in sorted(roles, key=str.encode)
    ]
    assert [link["state"] for link in take["links"]] == ["ok"] * 8

    # SFF-892: the differences of the scope `player`.
    (player_take,) = player["takes"]
    for item, player_item in zip(take["folder_files"], player_take["folder_files"], strict=True):
        if not item["path"].endswith(".json"):
            item |= {"state": "not_checked", "warnings": []}
        assert item == player_item
    for link, player_link in zip(take["links"], player_take["links"], strict=True):
        skipped = link["check"] in ("frames", "dimensions", "hashes", "calibration")
        assert player_link == link | {"state": "not_checked" if skipped else "ok"}
    for key in set(take) - {"folder_files", "links"}:
        assert take[key] == player_take[key]
    assert {k: v for k, v in full.items() if k != "takes"} == {k: v for k, v in player.items() if k != "takes"}
    assert name == take["recording_name"]


def test_each_link_check_is_ok_in_the_files():
    """The parts of SFF-872, computed from the files. Each part passes, so each check of the scope `full` is `ok`."""
    pytest.importorskip("PIL")
    m, name, d, tables, table = manifest(), rec(), descriptor(), toml(), rows()
    capture = json.loads((CASE / f"{name}_info.json").read_bytes())
    pairs = [(c["video"], c["timing"]) for c in m["cameras"]] + [(m["audio"]["audio"], m["audio"]["timing"])]
    headers = [read_sidecar(CASE / timing)[0] for _, timing in pairs]
    run = d["runs"]["0"]
    sources = {k: s["definition"] for k, s in run["sources"].items() if s["kind"] == "camera"}

    # take_uuid
    assert {m["take_uuid"], capture["take_uuid"], processing_info()["take_uuid"], d["take_uuid"]} | {
        header["take_uuid"] for header in headers
    } == {m["take_uuid"]}
    # camera_key
    for camera in m["cameras"]:
        key = camera["camera_key"]
        assert [header.get("camera_key") for header in headers].count(key) == 1 and key in capture["camera_configs"]
        assert [t.get("camera_key") for k, t in tables.items() if k != "metadata"].count(key) == 1
        assert [definition["camera_key"] for definition in sources.values()].count(key) == 1
    # frames
    row_counts = [len(read_sidecar(CASE / camera["timing"])[1]) for camera in m["cameras"]]
    assert len(set(row_counts)) == 1 and max(row["frame_number"] for row in table) <= row_counts[0] - 1
    # dimensions
    for camera in m["cameras"]:
        frame = run["reference_frames"][f"camera:{camera['camera_label']}:image"]
        assert (frame["width"], frame["height"]) == stored_size(camera)
    # rotation
    assert all("rotation" not in config for config in capture["camera_configs"].values())
    for camera, summary, header in zip(m["cameras"], m["summary"]["cameras"], headers):
        assert str(summary["display_rotation"]) == header["display_rotation"]
    # files
    paths = [p for pair in pairs for p in pair] + [item["path"] for item in m["files"]] + [m["calibration"]["file"]]
    names = [definition[k] for definition in sources.values() for k in ("video_filename", "timing_filename")]
    assert all((CASE / path).is_file() for path in paths) and all((CASE / MEDIA / n).is_file() for n in names)
    assert all("/" not in n for n in names)  # SFF-826
    # hashes
    assert m["calibration"]["sha256"] == sha256(CASE / m["calibration"]["file"])
    assert processing_info()["processed"]["parquet_sha256"] == sha256(parquet_path())
    # calibration
    assert m["calibration"]["calibration_uuid"] == tables["metadata"]["calibration_uuid"]
