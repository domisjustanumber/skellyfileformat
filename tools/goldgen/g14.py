"""Golden folder G14 (spec/SPEC.md Appendix A): a calibration and its copies.

The cases are `calibration_take` and `mocap_take`. The folder `library/` is not a case. The
calibration take holds the calibration TOML that it made, the processing info JSON and a Parquet with
one run: the `TIMESTAMPS` rows and the ChArUco `OVERLAY_2D` rows (SFF-836). The motion-capture take
holds a byte-identical copy of the TOML (SFF-811). `library/` holds the library copy and
`last_successful_camera_calibration.toml` (SFF-812). The two takes record the same two cameras. Each
take is small and has no audio. golden/G10_G13_G14_CHOICES.md gives each value that the spec does not
give.
"""

from __future__ import annotations

import json
from pathlib import Path

from goldgen import capture_cases, common, g03, g13
from goldgen import folder_common as fc

CALIBRATION = g13.TAKE | {"rec": "g14_calibration_take", "take_uuid": "00000000000040008000000000001401"}
MOCAP = g13.TAKE | {"rec": "g14_mocap_take", "take_uuid": "00000000000040008000000000001402"}
CALIBRATION_UUID = "00000000000040008000000000001403"
FRAMES = 10
TRACKER = f"charuco_detector:{g03.BOARD['squares_x']}x{g03.BOARD['squares_y']}"  # SFF-836
# The OpenCV corner IDs of the inner corners of the board: (squares_x − 1) × (squares_y − 1).
CORNERS = [f"corner_{i}" for i in range((g03.BOARD["squares_x"] - 1) * (g03.BOARD["squares_y"] - 1))]
NOT_SEEN = (1, range(3, 5))  # camera 1 does not see the board on frames 3 and 4


def corner(c: int):
    """The value function of `folder_common.write_parquet` for camera c. Each value is a number of quarters."""

    def value(frame: int, n: int, k: int) -> float | None:
        if c == NOT_SEEN[0] and frame in NOT_SEEN[1]:
            return (None, None, 0.0)[k]  # SFF-831: a corner that the detector did not find
        x, y = (32 + 48 * (n % 4) + 4 * frame + 9 * c) % 256 / 4, (40 + 64 * (n // 4) + 3 * frame + 5 * c) % 192 / 4
        return (x, y, 1.0)[k]

    return value


def toml(files: list[dict], cameras: list[dict]) -> bytes:
    metadata = {
        "format_version": common.FORMAT_VERSION,
        "format_prerelease": common.FORMAT_PRERELEASE,
        "writer": common.WRITER,
        "calibration_uuid": CALIBRATION_UUID,
        "source_take_uuid": CALIBRATION["take_uuid"],  # the take that made it
        "reprojection_error_px": 0.25,
        "initial_cost": 1.5,
        "final_cost": 0.25,
        "n_iterations": 4,
        "solver_time_seconds": 0.5,
        "n_observations_used": 144,
        "n_observations_rejected": 0,
        "aligned": False,
        "solver_method": "anipose",
        "transformation_history": [],
    }
    return fc.calibration_toml(metadata, g03.BOARD, g03.toml_cameras(cameras, files))


def build(out: Path) -> None:
    take_cameras = g13.cameras(FRAMES)
    toml_facts = {"calibration_uuid": CALIBRATION_UUID, "source_take_uuid": CALIBRATION["take_uuid"]}

    # The calibration take: freemocap adds the TOML, the Parquet and the processing info JSON.
    folder = out / "calibration_take"
    files, facts = capture_cases.finished_take(CALIBRATION, take_cameras, None)
    capture_cases.write_files(folder, files)
    data = toml(facts["files"], take_cameras)
    run, rows, _ = g13.overlay_run(facts["files"], take_cameras, TRACKER, g03.BOARD, CORNERS, corner, {}, "posthoc", True)
    d = g13.descriptor(CALIBRATION, run)
    facts = fc.add_processing(folder, facts, data, toml_facts, d, lambda path: fc.write_parquet(path, d, rows))
    manifest_path = folder / capture_cases.MANIFEST
    manifest = json.loads(manifest_path.read_bytes())
    manifest["purpose"] = "calibration"
    manifest_path.write_bytes(common.file_json(manifest))
    write_results(out, "calibration_take", facts)

    # The motion-capture take: freemocap copies the TOML into it and updates the manifest (SFF-811).
    folder = out / "mocap_take"
    files, facts = capture_cases.finished_take(MOCAP, take_cameras, None)
    capture_cases.write_files(folder, files)
    toml_path = f"{MOCAP['rec']}_camera_calibration.toml"
    (folder / toml_path).write_bytes(data)
    manifest_path = folder / capture_cases.MANIFEST
    manifest = json.loads(manifest_path.read_bytes())
    for camera in manifest["cameras"]:
        camera["calibration_camera"] = camera["camera_label"]  # the key of its TOML table (SFF-806)
    manifest["calibration"] = {"calibration_uuid": CALIBRATION_UUID, "file": toml_path, "sha256": common.sha256_hex(data)}
    manifest["summary"]["calibration"] = toml_facts  # SFF-728
    manifest_path.write_bytes(common.file_json(manifest))
    write_results(out, "mocap_take", facts | {"folder_files": [(toml_path, "calibration"),(facts["info_path"], "capture_info")]})

    # The library of SFF-812: the library copy, and `last_successful_camera_calibration.toml`.
    (out / "library").mkdir()
    for name in (f"{CALIBRATION['rec']}_camera_calibration.toml", "last_successful_camera_calibration.toml"):
        (out / "library" / name).write_bytes(data)


def write_results(out: Path, case: str, facts: dict) -> None:
    has_parquet = any(role == "tracking" for _, role in facts["folder_files"])
    for scope in ("full", "player"):
        result = fc.expected_result(facts, scope)
        for link in result["takes"][0]["links"]:
            if link["check"] == "dimensions" and not has_parquet:
                link["state"] = "not_checked"  # SFF-872: the part needs the Parquet
        (out / f"{case}.{scope}.json").write_bytes(common.canonical_json(result))
