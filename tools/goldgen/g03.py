"""Golden folder G3 (spec/SPEC.md Appendix A): a processed take, in the case `take`.

The take is the take of G1 with a calibration TOML, a tracking Parquet and the processing info JSON.
Each value of this file is synthetic. The 2D and 3D values come from small formulas: they are not a
triangulation with the calibration of the take.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from goldgen import common, g01
from goldgen import folder_common as fc

PART = Path(__file__).resolve().parents[2] / "spec" / "parts" / "parquet-descriptor.md"
CALIBRATION_UUID = "00000000000040008000000000000301"
SOURCE_TAKE_UUID = "00000000000040008000000000000302"  # a calibration take that is not in a golden folder
BOARD = {
    "squares_x": 5, "squares_y": 3, "square_length_mm": 54.0, "marker_length_ratio": 0.8, "aruco_dictionary_enum": 2,
}  # fmt: skip
INTRINSICS = {"fx": 60.0, "fy": 60.0, "cx": 32.0, "cy": 24.0, "k1": 0.01, "k2": -0.02, "p1": 0.0, "p2": 0.0}
IDENTITY = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
# t of each camera, in mm. R is the identity for each camera, so each value of the TOML is exact.
TRANSLATIONS = [[0.0, 0.0, 0.0], [-500.0, 0.0, 0.0]]
TRACKER_STAGE = "body"
STAGES = ("timing", "observations", "triangulation", "filtering")  # the stages of G3, in the order of the part
# The tracker did not detect this point of the model `stick` in camera 1 on these frames (SFF-831).
UNDETECTED_NAME, UNDETECTED_CAMERA, UNDETECTED_FRAMES = 4, 1, range(10, 13)

PAIR = {
    "model_id": "pair",
    "detector_type": "synthetic",
    "tracker_keypoint_names": ["p", "q"],
    "skeleton": {
        "name": "pair",
        "landmarks": [
            {"name": "p", "definition": "Bar origin", "position": [0.0, 0.0, 0.0], "segment": "bar", "aliases": []},
            {"name": "q", "definition": "Bar end", "position": [0.0, 0.0, 1.0], "segment": "bar", "aliases": []},
        ],
        "segments": [
            {
                "name": "bar", "landmarks": ["p", "q"],
                "frame": {
                    "origin": "p", "primary_point": "q", "primary_axis": [2, 1], "secondary_point": None,
                    "secondary_axis": None, "handedness": 1,
                },
                "aliases": [], "anatomical_segment": None,
            }
        ],
        "joints": [],
        "chains": [],
        "landmark_groups": [],
        "landmark_connections": [],
        "derived_quantities": [],
        "coordinate_system": "blender",
    },
    "rest_pose": {
        "name": "pair_rest",
        "root_segment_name": "bar",
        "parents": {"bar": None},
        "connect_ats": {},
        "orientations": {"bar": {"w": 1.0, "x": 0.0, "y": 0.0, "z": 0.0}},
    },
    "mappings": [{"entries": {}, "prefix": None, "known_tracker_keypoints": ["p", "q"], "passthrough": True}],
    "center_of_mass": {
        "definitions": {
            "bar": {
                "name": "bar", "proximal": "p", "distal": "q",
                "weights": [{"landmark": "p", "weight": 0.5}, {"landmark": "q", "weight": 0.5}], "sided": False,
            }
        }
    },
    "segment_masses": {"bar": 1.0},
    "scale_reference_name": "bar_length",
    "anchor_segment_name": None,
}  # fmt: skip


def stick_example() -> dict:
    """The informative example of a `RecordedModel` of the part."""
    text = PART.read_text(encoding="utf-8")
    return json.loads(re.search(r"### Example of a `RecordedModel`.*?```json\n(.*?)```", text, re.DOTALL).group(1))


def recorded_model(model: dict, connections: list[list[str]]) -> dict:
    """Add `tracker_connections` (omitted when empty) and `segment_topology` at their places (SFF-832)."""
    topology = [
        {
            "name": segment["name"],
            "parent": model["rest_pose"]["parents"][segment["name"]],
            "proximal": segment["frame"]["origin"],
            "distal": segment["frame"]["primary_point"],
        }
        for segment in model["skeleton"]["segments"]
    ]
    head = {key: model[key] for key in ("model_id", "detector_type", "tracker_keypoint_names")}
    return head | ({"tracker_connections": connections} if connections else {}) | {"segment_topology": topology} | model


def models() -> dict:
    return {
        "stick": recorded_model(stick_example(), [["kp_a", "kp_b"], ["kp_b", "kp_d"], ["kp_d", "kp_e"]]),
        "pair": recorded_model(PAIR, []),
    }


def toml_cameras(cameras: list[dict], files: list[dict]) -> list[dict]:
    return [
        {
            "name": item["camera_label"],
            "id": item["camera_label"],
            "camera_key": item["camera_key"],
            "camera_label": item["camera_label"],
            "index": index,
            "size": [camera["width"], camera["height"]],
            "matrix": [[INTRINSICS["fx"], 0.0, INTRINSICS["cx"]], [0.0, INTRINSICS["fy"], INTRINSICS["cy"]], [0.0, 0.0, 1.0]],
            "distortions": [INTRINSICS["k1"], INTRINSICS["k2"], INTRINSICS["p1"], INTRINSICS["p2"], 0.0],
            "rotation": [0.0, 0.0, 0.0],
            "translation": t,
            "world_orientation": IDENTITY,
            "world_position": [0.0 - v for v in t],  # −Rᵀt, with no −0.0
            # A control with no value has no key: TOML has no null.
            "controls_at_calibration": {k: v["value"] for k, v in camera["controls"].items() if v["value"] is not None},
        }
        for index, (camera, item, t) in enumerate(zip(cameras, files, TRANSLATIONS, strict=True))
    ]  # fmt: skip


def run_and_rows(cameras: list[dict], files: list[dict]) -> tuple[dict, list[tuple]]:
    """Run 0 of the descriptor, and the item of `folder_common.write_parquet` for each of its channels."""
    labels = [item["camera_label"] for item in files]
    group = fc.sensor_group_name([item["camera_key"] for item in files])
    strict = [fc.strict_ns([record[4] for record in item["records"]]) for item in files]
    camera_times = [[fc.seconds(s) for s in times] for times in strict]
    group_times = [fc.seconds(m) for m in fc.group_ns(strict)]
    trackers = {f"keypoint_model:synthetic_{name}": model["tracker_keypoint_names"] for name, model in models().items()}

    def channel(source, reference_frame, kind, names, components, stage, dtype="float32") -> dict:
        return {
            "sensor_group": group, "source": source, "reference_frame": reference_frame, "kind": kind,
            "names": names, "components": components, "stage": stage, "dtype": dtype,
        }  # fmt: skip

    def undetected(t: int, frame: int, n: int) -> bool:
        return t == 0 and n == UNDETECTED_NAME and frame in UNDETECTED_FRAMES

    def overlay(t: int, c: int):
        def value(frame: int, n: int, k: int) -> float | None:
            if undetected(t, frame, n) and c == UNDETECTED_CAMERA:
                return (None, None, 0.0)[k]  # SFF-831
            # Each value is a number of quarters or eighths, so its float32 is exact.
            x, y = (7 * frame + 11 * n + 5 * c + 3 * t) % 256 / 4, (3 * frame + 13 * n + 7 * c + 5 * t) % 192 / 4
            return (x, y, (8 - n % 4) / 8)[k]

        return value

    def points(t: int, filtered: bool):
        def value(frame: int, n: int, k: int) -> float | None:
            if undetected(t, frame, n) and not filtered:
                return None  # one view is not enough for a 3D point, and the filter fills the gap
            base = (100 * n + frame, 200 + 100 * n - frame, 1000 + 2 * frame + n)[k] + 5000 * t
            return base + 0.5 * filtered

        return value

    timestamp, pixel = {"timestamp_s": "s"}, {"x": "px", "y": "px", "visibility": "1"}
    millimetre = {"x": "mm", "y": "mm", "z": "mm"}
    rows = [
        (channel(f"camera:{label}", None, "TIMESTAMPS", ["capture"], timestamp, "timing", "float64"), times, None)
        for label, times in zip(labels, camera_times)
    ]
    rows.append(
        (channel(f"timing:{group}", None, "TIMESTAMPS", ["synchronized"], timestamp, "timing", "float64"), group_times, None)
    )
    rows += [
        (
            channel(source, f"camera:{label}:image", "OVERLAY_2D", [f"{TRACKER_STAGE}.{name}" for name in names], pixel, "observations"),
            camera_times[c],
            overlay(t, c),
        )
        for t, (source, names) in enumerate(trackers.items())
        for c, label in enumerate(labels)
    ]  # fmt: skip
    for kind, stage, filtered in (("RAW_KEYPOINTS_3D", "triangulation", False), ("KEYPOINTS_3D", "filtering", True)):
        rows += [
            (channel(source, "calibrated_world", kind, names, millimetre, stage), group_times, points(t, filtered))
            for t, (source, names) in enumerate(trackers.items())
        ]
    # A `TIMESTAMPS` value is the `timestamp_s` of its row (row rule 6).
    rows = [(0, ch, times, value or (lambda frame, n, k, times=times: times[frame])) for ch, times, value in rows]
    channels = [ch for _, ch, _, _ in rows]

    sources = {
        f"camera:{label}": {
            "kind": "camera",
            "definition": {
                "camera_key": item["camera_key"], "camera_label": label, "video_filename": Path(item["name"]).name,
                "timing_filename": Path(item["name"]).with_suffix(".csv").name, "timing_method": "recorded",
                "inferred_offset_s": 0.0,
            },
        }
        for label, item in zip(labels, files)
    }  # fmt: skip
    sources[f"timing:{group}"] = {"kind": "timing", "definition": {"method": "mean_camera_times"}}
    sources |= {source: {"kind": "tracker", "definition": {}} for source in trackers}
    reference_frames = {
        f"camera:{label}:image": {
            "camera_key": item["camera_key"], "calibration_camera": label, "width": camera["width"],
            "height": camera["height"],
        }
        for label, item, camera in zip(labels, files, cameras)
    }  # fmt: skip
    reference_frames["calibrated_world"] = {
        "name": "calibrated_world", "basis": "blender_x_right_y_forward_z_up", "units": "mm", "alignment": None,
        "additional_transform": None,
    }  # fmt: skip
    provenance = {
        stage: {
            "attempt_id": "g03-synthetic-attempt",
            "recorded_at": f"2000-01-01T00:01:0{second}Z",
            "effective_settings": {},
            "default_settings": None,
            "input_signatures": {"synthetic_input": "0" * 64},
            "software": {"python": "3.13.13", "packages": {}, "core_sha256": "0" * 64},
            "output_sources": list(dict.fromkeys(ch["source"] for ch in channels if ch["stage"] == stage)),
            "limitations": [],
            "base_run_id": None,
            "base_descriptor_signature": None,
            "origin": "posthoc",
            "coverage": None,  # SFF-834
        }
        for second, stage in enumerate(STAGES)
    }
    run = {
        "calibration_updates": {},
        "scale_fits": [],
        "camera_geometry": {
            group: [
                {
                    "id": table["name"], "camera_key": table["camera_key"], "index": table["index"],
                    "image_size": table["size"], "intrinsics": INTRINSICS,
                    "extrinsics": {"quaternion_wxyz": [1.0, 0.0, 0.0, 0.0], "translation": table["translation"]},
                    "world_position": table["world_position"], "world_orientation": table["world_orientation"],
                }
                for table in toml_cameras(cameras, files)
            ]
        },
        "sensor_groups": {
            group: {
                "clock_description": "recording-relative seconds; timing method declared per source",
                "sample_count": len(group_times),
            }
        },
        "sources": sources,
        "reference_frames": reference_frames,
        "models": models(),
        "processing": {group: {"stage_provenance": {"version": 1, "stages": provenance}}},
        "channels": channels,
        "static_channels": [],
        "checkpoints": [],
    }  # fmt: skip
    return run, rows


def write_case(folder: Path) -> tuple[dict, list[dict], dict]:
    """Write the take of G3 into `folder`. Return its facts, its cameras and its audio."""
    cameras, audio = g01.cameras(), g01.audio()
    facts = common.write_take(folder, g01.TAKE, cameras, audio)
    files = facts["files"][: len(cameras)]
    toml = fc.calibration_toml(
        {
            "format_version": common.FORMAT_VERSION,
            "format_prerelease": common.FORMAT_PRERELEASE,
            "writer": common.WRITER,
            "calibration_uuid": CALIBRATION_UUID,
            "source_take_uuid": SOURCE_TAKE_UUID,
            "reprojection_error_px": 0.25,
            "initial_cost": 1.5,
            "final_cost": 0.25,
            "n_iterations": 4,
            "solver_time_seconds": 0.5,
            "n_observations_used": 180,
            "n_observations_rejected": 0,
            "aligned": False,
            "solver_method": "anipose",
            "transformation_history": [],
        },
        BOARD,
        toml_cameras(cameras, files),
    )
    run, rows = run_and_rows(cameras, files)
    descriptor = {
        "schema_version": 2,
        "format_version": common.FORMAT_VERSION,
        "format_prerelease": common.FORMAT_PRERELEASE,
        "writer": common.WRITER,
        "take_uuid": facts["take_uuid"],
        "recording_id": facts["recording_name"],
        "recording_info": {},
        "runs": {"0": run},
    }
    toml_facts = {"calibration_uuid": CALIBRATION_UUID, "source_take_uuid": SOURCE_TAKE_UUID}
    facts = fc.add_processing(folder, facts, toml, toml_facts, descriptor, lambda path: fc.write_parquet(path, descriptor, rows))
    return facts, cameras, audio


def build(out: Path) -> None:
    """Write the case `take` of G3 into `out`, with its two expected results and its truth file."""
    facts, cameras, audio = write_case(out / "take")
    for scope in ("full", "player"):
        (out / f"take.{scope}.json").write_bytes(common.canonical_json(fc.expected_result(facts, scope)))
    truth = {  # the same facts as for G1
        "audio": {"name": facts["files"][-1]["name"], "click_samples": audio["click_samples"]},
        "cameras": [
            {"name": item["name"], "flash_positions": camera["flash_positions"]}
            for item, camera in zip(facts["files"], cameras)
        ],
    }
    (out / "take.truth.json").write_bytes(common.canonical_json(truth))
