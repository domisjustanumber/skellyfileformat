"""Golden folder G15 (recording-files/SPEC.md Appendix A): legacy folders, one case for each name of "Layout and cases".

Each case is a set of stub files: the smallest files that carry the signals of its row of SFF-878, or
of its family (SFF-876, SFF-877). No file holds media or data. The input of each case names the rows
that it must match, and the expected result follows from the tables of SFF-878 and SFF-879.
recording-files/golden/G15_CHOICES.md gives each value that the spec does not give.
"""

from __future__ import annotations

from pathlib import Path

from goldgen import common

# SFF-878: the Era cell (with `-`, SFF-885), the first release, the last release and the chain.
ROWS = [
    ("V1a", "v1.0.25", "v1.0.34", 0),
    ("V1b-V1d", "v1.1.0", "v1.3.0", 1),
    ("V1b-V1c", "v1.1.0", "v1.1.1", 1),
    ("V1e-V1h'", "v1.3.1", "v1.7.4", 2),
    ("V1f-V1h'", "v1.5.0", "v1.7.4", 2),
    ("V1g-V1h'", "v1.6.0", "v1.7.4", 2),
    ("V1h-V1h'", "v1.7.0", "v1.7.4", 2),
    ("V1h'", "v1.7.4", "v1.7.4", 2),
    ("V1i", "v1.8.0", "v1.8.2", 3),
]
WARNINGS = [  # SFF-879
    ("legacy_fake_confidence", "v1.0.25", "v1.0.34"),
    ("legacy_marker_order", "v1.1.0", "v1.1.0"),
    ("legacy_nonrigid_alignment", "v1.0.25", "v1.5.4"),
    ("legacy_calibration_unverified", "v1.0.25", "v1.8.2"),
]
ALL_V1 = ("v1.0.25", "v1.8.2")  # SFF-878: the range when no row matches

# `{case}` is the name of the case folder: v1 builds these two names from the folder name (SFF-880).
TOML = "{case}_camera_calibration.toml"
BY_FRAME = "{case}_by_frame.csv"
MP4 = "synchronized_videos/Camera_000_synchronized.mp4"
PARAMETERS = "output_data/recording_parameters.json"
RAW = "output_data/raw_data/"
ANIPOSE = "anipose_triangulate_3d_parameters_model"  # the v1 home of the triangulation keys
TIDY = b"frame,timestamp,timestamp_by_camera,model,keypoint,x,y,z"
CAM_0 = b"[cam_0]\nrotation = [ 0.0, 5e-7, -5e-7,]\n"  # each magnitude is below the limit 1e-6 of SFF-878


def parameters(*models: str, **triangulation: bool) -> bytes:
    return common.file_json({model: {} for model in models} | {ANIPOSE: triangulation})


V1B = {
    MP4: b"",
    PARAMETERS: parameters("mediapipe_parameters_model", run_3d_triangulation=True, run_reprojection_error_filtering=False),
    RAW + "mediapipe3dData_numCams_numFrames_numTrackedPoints_reprojectionError.npy": b"",
}  # fmt: skip
V1E = {
    MP4: b"",
    PARAMETERS: parameters("tracking_parameters_model", run_reprojection_error_filtering=False),
    "output_data/mediapipe_body_3d_xyz.csv": b"body_nose_x,body_nose_y,body_nose_z\n",
}
SKELETON = {"output_data/mediapipe_skeleton_3d.npy": b""}
V1F = V1E | SKELETON | {BY_FRAME: TIDY + b"\n"}
V1G = V1F | {TOML: CAM_0}

# case: (family, the indexes of the rows of ROWS that the stubs match, the stub files)
CASES = {
    "v1a": ("v1", [0], {
        MP4: b"",
        PARAMETERS: common.file_json({"mediapipe_parameters_model": {"skip_2d_image_tracking": False}}),
        RAW + "mediapipeBodyWorld_numCams_numFrames_numTrackedPoints_XYZ.npy": b"",
    }),
    "v1b_v1d": ("v1", [1], V1B),
    "v1b_v1c": ("v1", [1, 2], V1B | {"output_data/mediapipe_skeleton_segment_lengths.json": b"{}\n"}),
    # The row V1e-V1h' takes one of two file names. This case has the second, each later case the first.
    "v1e_v1h": ("v1", [3], V1E | {RAW + "mediapipe_2dData_numCams_numFrames_numTrackedPoints_pixelXY.npy": b""}),
    "v1f_v1h": ("v1", [3, 4], V1F),
    "v1g_v1h": ("v1", [3, 4, 5], V1G),
    "v1h": ("v1", [3, 4, 5, 6], V1G | {TOML: CAM_0 + b"world_position = [ 0.0, 0.0, 0.0,]\n"}),
    "v1h_prime": ("v1", [3, 4, 5, 6, 7], V1G | {
        TOML: CAM_0 + b"\n[metadata]\ngroundplane_calibration = false\n",
        BY_FRAME: TIDY + b",reprojection_error\n",
    }),
    "v1i": ("v1", [8], {
        MP4: b"",
        PARAMETERS: parameters("tracking_parameters_model", use_triangulate_outlier_rejection=False),
    }),
    "two_chains": ("v1", [1, 3], V1B | V1E | SKELETON | {
        PARAMETERS: parameters(
            "mediapipe_parameters_model", "tracking_parameters_model",
            run_3d_triangulation=True, run_reprojection_error_filtering=False,
        ),
    }),
    "no_signal": ("v1", [], {MP4: b""}),
    "v0_0_x": ("pre_v1", [], {"SyncedVideos/{case}_synced_Cam1.mp4": b"", "{case}_config.yaml": b""}),
    "v0_1_0": ("pre_v1", [], {
        "synchronized_videos/Camera_000.mp4": b"",
        "synchronized_videos/timestamps/Camera_000_binary.npy": b"",
    }),
    "mp4_only": ("unknown", [], {"clip_a.mp4": b"", "clip_b.mp4": b""}),
}  # fmt: skip


def release(name: str) -> tuple[int, ...]:
    return tuple(int(part) for part in name[1:].split("."))


def legacy(family: str, matched: list[int], names: list[str], case: str, scope: str) -> dict:
    if family != "v1":  # SFF-876, SFF-877, SFF-880
        return {
            "family": family, "release_range": None, "ambiguous": False, "eras": [], "warnings": [],
            "calibration": None,
        }  # fmt: skip
    rows = [ROWS[i] for i in matched] if scope == "full" else []  # SFF-892: `player` reads no era signal
    one_chain = len({chain for *_, chain in rows}) == 1
    if one_chain:
        first, last = rows[-1][1:3]
    else:
        first = min((row[1] for row in rows), key=release, default=ALL_V1[0])
        last = max((row[2] for row in rows), key=release, default=ALL_V1[1])
    toml = TOML.format(case=case)
    return {
        "family": "v1",
        "release_range": [first, last],
        "ambiguous": not one_chain,
        "eras": [row[0] for row in rows],
        "warnings": sorted(code for code, low, high in WARNINGS if release(low) <= release(last) and release(first) <= release(high)),
        "calibration": {"path": toml, "state": "present"} if toml in names else {"path": None, "state": "missing"},
    }  # fmt: skip


def build(out: Path) -> None:
    """Write each case of G15 into `out`, with its two expected results."""
    for case, (family, matched, files) in CASES.items():
        names = sorted((name.format(case=case) for name in files), key=str.encode)
        for name, data in files.items():
            path = out / case / name.format(case=case)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        # SFF-885: `other_files` of a legacy folder lists the root and `synchronized_videos/`, not a subfolder.
        listed = [n for n in names if "/" not in n or (n.startswith("synchronized_videos/") and n.count("/") == 1)]
        for scope in ("full", "player"):
            result = {
                "result_version": 2,
                "folder_state": "legacy",
                "folder_warnings": [],
                "takes": [],
                "other_files": [{"name": name, "state": "not_in_format", "reason": None} for name in listed],
                "legacy": legacy(family, matched, names, case, scope),
            }
            (out / f"{case}.{scope}.json").write_bytes(common.canonical_json(result))
