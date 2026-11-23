"""Shared code of the golden generator for the folder files that freemocap writes (decision G21H item 4).

It writes the calibration TOML (section 15), the tracking Parquet with its descriptor (section 16) and
the processing info JSON (section 14), adds them to the manifest of a take of `common.write_take`,
and gives the expected reader result of that take. It is not the writer of an implementation: each file
comes directly from the text of the spec.

Only `write_parquet` needs the dependency group ``golden`` (pyarrow).
"""

from __future__ import annotations

import hashlib
import json
import struct
from pathlib import Path

from goldgen import common

DESCRIPTOR_KEY = "freemocap.recording"  # SFF-817
# The table of section 16 (SFF-816): the name, the Arrow type, and true when the column can hold a null.
COLUMNS = (
    ("timestamp_s", "float64", False), ("sensor_group", "string", False), ("frame_number", "int32", False),
    ("source", "string", False), ("reference_frame", "string", True), ("channel", "string", False),
    ("name", "string", False), ("component", "string", False), ("value", "float32", True),
    ("value_f64", "float64", True), ("units", "string", False), ("run_id", "int32", False),
)  # fmt: skip
INFO_DATA_KINDS = (
    "LANDMARKS_3D", "KEYPOINTS_3D", "RAW_KEYPOINTS_3D", "OVERLAY_2D", "SEGMENT_ORIGINS", "ROTATIONS_WORLD",
)  # fmt: skip
CONVENTIONS = {
    "quaternion_order": "wxyz",
    "segment_pose": "saved origin and world orientation",
    "units": "per component",
    "coordinates": "per reference frame",
    "array_order": "frames, names, components",
}
PLAYER_SUFFIXES = (".json",)  # SFF-892: of the folder files, the scope `player` reads only the JSON files

# ---------------------------------------------------------------- times (SFF-782, SFF-828)


def strict_ns(player_ns: list[int]) -> list[int]:
    """The strict player times of SFF-782."""
    strict: list[int] = []
    for p in player_ns:
        strict.append(max(p, strict[-1] + 1) if strict else p)
    return strict


def group_ns(strict_by_camera: list[list[int]]) -> list[int]:
    """The group time of each frame (SFF-828): the mean of the cameras, rounded half up."""
    n = len(strict_by_camera)
    return [(2 * sum(times) + n) // (2 * n) for times in zip(*strict_by_camera, strict=True)]


def seconds(ns: int) -> float:
    return ns / 10**9  # the true division of two Python integers gives the nearest float64 (SFF-828)


def sensor_group_name(camera_keys: list[str]) -> str:
    """The name of a camera sensor group (parts/parquet-descriptor.md, `SensorGroup`)."""
    return "camera_group:" + hashlib.sha256("|".join(sorted(camera_keys)).encode()).hexdigest()[:6]


# ---------------------------------------------------------------- calibration TOML (section 15)


def _toml_value(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        assert value.isascii() and value.isprintable(), value
        return json.dumps(value)
    if isinstance(value, list):
        return "[" + ", ".join(_toml_value(item) for item in value) + "]"
    assert isinstance(value, (int, float)), repr(value)
    return repr(value)


def _toml_table(name: str, values: dict) -> str:
    return f"[{name}]\n" + "".join(f"{key} = {_toml_value(value)}\n" for key, value in values.items())


def calibration_toml(metadata: dict, board: dict, cameras: list[dict]) -> bytes:
    """The TOML of section 15. Each camera holds the keys of its table and, last, `controls_at_calibration`."""
    tables = [_toml_table("metadata", metadata), _toml_table("metadata.board", board)]
    for camera in sorted(cameras, key=lambda c: c["index"]):  # SFF-806
        label = camera["camera_label"]
        assert label.isalnum() and label.isascii(), "the label must be a bare TOML key"
        tables.append(_toml_table(label, {k: v for k, v in camera.items() if k != "controls_at_calibration"}))
        tables.append(_toml_table(f"{label}.controls_at_calibration", camera["controls_at_calibration"]))
    return "\n".join(tables).encode()


# ---------------------------------------------------------------- tracking Parquet (section 16)


def descriptor_json(descriptor: dict) -> bytes:
    return json.dumps(descriptor, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()


def write_parquet(path: Path, descriptor: dict, channels: list[tuple]) -> None:
    """Write the Parquet of section 16, with one row group for each item of `channels` (SFF-823).

    Each item is (run_id, channel, times, value). `channel` is a `Channel` of the descriptor. `times`
    has the `timestamp_s` of each frame. `value(frame, name index, component index)` gives a float or
    None. The rows of a channel are in order of the frame, then the name, then the component.
    """
    import pyarrow as pa
    import pyarrow.parquet as pq

    types = {"float64": pa.float64(), "float32": pa.float32(), "int32": pa.int32(), "string": pa.string()}
    schema = pa.schema(
        [pa.field(name, types[kind], nullable=null) for name, kind, null in COLUMNS],
        metadata={DESCRIPTOR_KEY: descriptor_json(descriptor)},
    )
    writer = pq.ParquetWriter(
        path, schema, compression="zstd", compression_level=3,  # SFF-818
        use_byte_stream_split=["value", "value_f64"],
        use_dictionary=[name for name, kind, _ in COLUMNS if kind == "string"],
    )  # fmt: skip
    with writer:
        for rows in parquet_rows(descriptor, channels):
            writer.write_table(pa.Table.from_pylist(rows, schema=schema))


def parquet_rows(descriptor: dict, channels: list[tuple]):
    """The rows that `write_parquet` writes: one list of row dicts for each item of `channels`."""
    for run_id, channel, times, value in channels:
        sample_count = descriptor["runs"][str(run_id)]["sensor_groups"][channel["sensor_group"]]["sample_count"]
        assert len(times) == sample_count  # row rule 3
        column = "value_f64" if channel["dtype"] == "float64" else "value"  # SFF-820
        yield [
            {
                "timestamp_s": time, "sensor_group": channel["sensor_group"], "frame_number": frame,
                "source": channel["source"], "reference_frame": channel["reference_frame"],
                "channel": channel["kind"], "name": name, "component": component,
                "value": None, "value_f64": None, "units": units, "run_id": run_id,
            } | {column: value(frame, n, c)}
            for frame, time in enumerate(times)
            for n, name in enumerate(channel["names"])
            for c, (component, units) in enumerate(channel["components"].items())
        ]  # fmt: skip


def values_sha256(rows) -> str:
    """The digest of the values of the rows, in file order, as recording-files/golden/README.md defines it."""
    digest = hashlib.sha256()
    for row in rows:
        for name, kind, _ in COLUMNS:
            value = row[name]
            if value is None:
                digest.update(b"\x00")
                continue
            if kind == "string":
                data = value.encode()
                data = struct.pack("<I", len(data)) + data
            elif kind == "float32":
                data = struct.pack("<f", value)
                assert struct.unpack("<f", data)[0] == value, "the value is exact in float32"
            else:
                data = struct.pack("<d" if kind == "float64" else "<q", value)
            digest.update(b"\x01" + data)
    return digest.hexdigest()


# ---------------------------------------------------------------- processing info JSON (section 14)


def processing_info(descriptor: dict, parquet: bytes, selected_run_id: int) -> bytes:
    """The processing info JSON of the Parquet with this descriptor. The take has no export."""
    rec = descriptor["recording_id"]
    runs = {
        run_id: {
            "sensor_groups": run["sensor_groups"],
            "cameras": [s["definition"]["camera_label"] for s in run["sources"].values() if s["kind"] == "camera"],
            "reference_frames": run["reference_frames"],
            "data": [
                {
                    "channel": channel["kind"], "source": channel["source"],
                    "sensor_group": channel["sensor_group"], "reference_frame": channel["reference_frame"],
                    "names": channel["names"], "components": channel["components"],
                }
                for channel in run["channels"]
                if channel["kind"] in INFO_DATA_KINDS
            ],
        }
        for run_id, run in descriptor["runs"].items()
    }  # fmt: skip
    assert str(selected_run_id) in runs
    return common.file_json(
        {
            "skellyfileformat": "processing_info",
            "format_version": common.FORMAT_VERSION,
            "format_prerelease": common.FORMAT_PRERELEASE,
            "writer": common.WRITER,
            "take_uuid": descriptor["take_uuid"],
            "processed": {
                "schema_version": 1,
                "parquet_sha256": common.sha256_hex(parquet),
                "recording_id": rec,
                "parquet": f"{rec}_data.parquet",
                "selected_run_id": selected_run_id,
                "runs": runs,
                "conventions": CONVENTIONS,
                "export_inventories": [],
            },
        }
    )


# ---------------------------------------------------------------- the files in the take


def add_processing(folder: Path, facts: dict, toml: bytes, toml_facts: dict, descriptor: dict, write_rows) -> dict:
    """Add the TOML, the Parquet and the processing info JSON to a take of `common.write_take`.

    `toml_facts` holds `calibration_uuid` and `source_take_uuid` of the TOML. `write_rows(path)` writes
    the Parquet. The function updates the manifest as freemocap does (SFF-725, SFF-838) and returns
    the facts with the member `folder_files`, for `expected_result`.
    """
    rec = facts["recording_name"]
    toml_path, parquet_path, info_path = (
        f"{rec}_camera_calibration.toml", f"{rec}_data.parquet", f"{rec}_recording_info.json",
    )  # fmt: skip
    (folder / toml_path).write_bytes(toml)
    write_rows(folder / parquet_path)
    info = processing_info(descriptor, (folder / parquet_path).read_bytes(), 0)
    (folder / info_path).write_bytes(info)

    manifest = json.loads((folder / "recording_manifest.json").read_bytes())
    for camera in manifest["cameras"]:
        camera["calibration_camera"] = camera["camera_label"]  # the key of its TOML table (SFF-806)
    manifest["calibration"] = {
        "calibration_uuid": toml_facts["calibration_uuid"], "file": toml_path, "sha256": common.sha256_hex(toml),
    }  # fmt: skip
    manifest["files"] += [
        {"path": parquet_path, "role": "tracking", "owner": "freemocap", "sha256": None},  # SFF-723
        {"path": info_path, "role": "processing_info", "owner": "freemocap", "sha256": common.sha256_hex(info)},
    ]
    manifest["files"].sort(key=lambda item: item["path"].encode())
    manifest["summary"]["calibration"] = toml_facts
    manifest["summary"]["processing_runs"] = []  # SFF-728
    for run_id, run in sorted(descriptor["runs"].items(), key=lambda item: int(item[0])):
        stages = [s for g in run["processing"].values() for s in g["stage_provenance"]["stages"].values()]
        manifest["summary"]["processing_runs"].append(
            {
                "run_id": int(run_id),
                "origin": "realtime" if any(s["origin"] == "realtime" for s in stages) else "posthoc",
                # Each text has one form, so the order of the texts is the order of the times.
                "recorded_at": max(s["recorded_at"] for s in stages),
            }
        )
    (folder / "recording_manifest.json").write_bytes(common.file_json(manifest))
    # The TOML that `calibration.file` names has the role `calibration` (SFF-885).
    folder_files = [(toml_path, "calibration"), *((item["path"], item["role"]) for item in manifest["files"])]
    return facts | {"folder_files": folder_files}


def expected_result(facts: dict, scope: str) -> dict:
    """The reader result (SFF-885) of a take of `add_processing` whose files agree with each other.

    recording-files/golden/G03_CHOICES.md gives the requirement of each member that `common.expected_result` does not give.
    """
    result = common.expected_result(facts, scope)
    (take,) = result["takes"]
    take["folder_files"] = [
        {"path": path, "role": role, "state": "present", "reason": None, "warnings": ["prerelease"]}
        if scope == "full" or path.endswith(PLAYER_SUFFIXES)
        else {"path": path, "role": role, "state": "not_checked", "reason": None, "warnings": []}  # SFF-892
        for path, role in sorted(facts["folder_files"], key=lambda item: item[0].encode())  # SFF-890
    ]
    not_in_player = ("frames", "dimensions", "hashes", "calibration")  # SFF-892
    for link in take["links"]:
        # Each check has a part that the scope evaluates, and no part fails (SFF-872).
        link["state"] = "not_checked" if scope == "player" and link["check"] in not_in_player else "ok"
    return result
