"""Checks of the committed golden folders G15 (legacy folders) and G16 (files that could run code).

The G15 checks read the stub files and apply the tables of SPEC.md section 21 with logic that is
written here by hand. They do not import the generator. The G16 checks never load a pickle: they
only read the opcodes.
"""

from __future__ import annotations

import ast
import json
import pickletools
import re
import tomllib
from pathlib import Path

import pytest

GOLDEN = Path(__file__).resolve().parents[2] / "recording-files" / "golden"
G15, G16 = GOLDEN / "G15", GOLDEN / "G16" / "take"

# case: (family, release_range, ambiguous, eras), from SPEC.md "Layout and cases" and SFF-876 to SFF-878.
EXPECTED = {
    "v1a": ("v1", ["v1.0.25", "v1.0.34"], False, ["V1a"]),
    "v1b_v1d": ("v1", ["v1.1.0", "v1.3.0"], False, ["V1b-V1d"]),
    "v1b_v1c": ("v1", ["v1.1.0", "v1.1.1"], False, ["V1b-V1d", "V1b-V1c"]),
    "v1e_v1h": ("v1", ["v1.3.1", "v1.7.4"], False, ["V1e-V1h'"]),
    "v1f_v1h": ("v1", ["v1.5.0", "v1.7.4"], False, ["V1e-V1h'", "V1f-V1h'"]),
    "v1g_v1h": ("v1", ["v1.6.0", "v1.7.4"], False, ["V1e-V1h'", "V1f-V1h'", "V1g-V1h'"]),
    "v1h": ("v1", ["v1.7.0", "v1.7.4"], False, ["V1e-V1h'", "V1f-V1h'", "V1g-V1h'", "V1h-V1h'"]),
    "v1h_prime": ("v1", ["v1.7.4", "v1.7.4"], False, ["V1e-V1h'", "V1f-V1h'", "V1g-V1h'", "V1h-V1h'", "V1h'"]),
    "v1i": ("v1", ["v1.8.0", "v1.8.2"], False, ["V1i"]),
    "two_chains": ("v1", ["v1.1.0", "v1.7.4"], True, ["V1b-V1d", "V1e-V1h'"]),
    "no_signal": ("v1", ["v1.0.25", "v1.8.2"], True, []),
    "v0_0_x": ("pre_v1", None, False, []),
    "v0_1_0": ("pre_v1", None, False, []),
    "mp4_only": ("unknown", None, False, []),
}
FOUR_WARNINGS = [
    "legacy_calibration_unverified", "legacy_fake_confidence", "legacy_marker_order", "legacy_nonrigid_alignment",
]  # fmt: skip

pytestmark = pytest.mark.skipif(not (G15.is_dir() and G16.is_dir()), reason="G15 or G16 is not built")


def load(path: Path) -> dict:
    return json.loads(path.read_bytes())


# ---------------------------------------------------------------- G15: the tables of section 21


def has_key(value: object, key: str) -> bool:
    """True when a JSON object at any depth has the member `key`."""
    if isinstance(value, dict):
        return key in value or any(has_key(v, key) for v in value.values())
    return isinstance(value, list) and any(has_key(v, key) for v in value)


def header(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").split("\n")[0].split(",")


def family(folder: Path) -> str:
    media = folder / "synchronized_videos"
    v0_0_x = ((folder / "SyncedVideos").is_dir() or (folder / "RawVideos").is_dir()) and (
        any(folder.glob("*_config.yaml")) or (folder / "sessionSettings.txt").is_file()
    )
    v0_1_0 = any(
        re.fullmatch(r"Camera_\d{3}\.mp4", p.name) and (media / "timestamps" / f"{p.stem}_binary.npy").is_file()
        for p in media.glob("*.mp4")
    )
    if v0_0_x or v0_1_0:  # SFF-876
        return "pre_v1"
    if any(media.glob("*_synchronized.mp4")) or any(media.glob("timestamps/*_synchronized_binary.npy")):  # SFF-877
        return "v1"
    return "unknown"


def calibration(folder: Path) -> dict:
    """SFF-880: the exact name, else the one TOML with `calibration` in its name."""
    exact = f"{folder.name}_camera_calibration.toml"
    others = [p.name for p in folder.glob("*.toml") if "calibration" in p.name]
    if (folder / exact).is_file() or len(others) == 1:
        return {"path": exact if (folder / exact).is_file() else others[0], "state": "present"}
    return {"path": None, "state": "ambiguous" if others else "missing"}


def matched_rows(folder: Path, toml_path: str | None) -> list[tuple[str, str, str, int]]:
    """The matched rows of the table of SFF-878: (Era cell, first release, last release, chain)."""
    out = folder / "output_data"
    raw = out / "raw_data"
    file = out / "recording_parameters.json"
    parameters = load(file) if file.is_file() else {}
    toml = tomllib.loads((folder / toml_path).read_text(encoding="utf-8")) if toml_path else {}
    by_frame = list(folder.glob("*_by_frame.csv"))

    def has(*keys: str) -> bool:
        return all(has_key(parameters, key) for key in keys)

    a = has_key(parameters.get("mediapipe_parameters_model"), "skip_2d_image_tracking") and any(
        raw.glob("mediapipeBodyWorld_*")
    )
    b_d = has("mediapipe_parameters_model", "run_3d_triangulation", "run_reprojection_error_filtering") and any(
        raw.glob("mediapipe3dData_numCams_*")
    )
    b_c = b_d and (out / "mediapipe_skeleton_segment_lengths.json").is_file()
    e = (
        has("tracking_parameters_model", "run_reprojection_error_filtering")
        and ((out / "mediapipe_skeleton_3d.npy").is_file() or any(raw.glob("mediapipe_2dData_*")))
        and any(header(p)[0] == "body_nose_x" for p in out.glob("*body*.csv"))
    )
    f = e and bool(by_frame)
    rotation = toml.get("cam_0", {}).get("rotation", [])
    g = f and len(rotation) == 3 and all(abs(value) <= 1e-6 for value in rotation)
    metadata = toml.get("metadata", {})
    h = g and (
        any("world_position" in table for table in toml.values())
        or "groundplane_calibration" in metadata
        or "name=" in str(metadata.get("charuco_board_object", ""))
    )
    h_prime = h and any("reprojection_error" in header(p) for p in by_frame)
    i = has("use_triangulate_outlier_rejection")
    table = [
        (a, "V1a", "v1.0.25", "v1.0.34", 0),
        (b_d, "V1b-V1d", "v1.1.0", "v1.3.0", 1),
        (b_c, "V1b-V1c", "v1.1.0", "v1.1.1", 1),
        (e, "V1e-V1h'", "v1.3.1", "v1.7.4", 2),
        (f, "V1f-V1h'", "v1.5.0", "v1.7.4", 2),
        (g, "V1g-V1h'", "v1.6.0", "v1.7.4", 2),
        (h, "V1h-V1h'", "v1.7.0", "v1.7.4", 2),
        (h_prime, "V1h'", "v1.7.4", "v1.7.4", 2),
        (i, "V1i", "v1.8.0", "v1.8.2", 3),
    ]
    return [row[1:] for row in table if row[0]]


def number(release: str) -> list[int]:
    return [int(part) for part in release[1:].split(".")]


def v1_legacy(rows: list[tuple[str, str, str, int]], found: dict) -> dict:
    """The range rule of SFF-878 and the warnings of SFF-879."""
    one_chain = len({row[3] for row in rows}) == 1
    if one_chain:
        first, last = rows[-1][1:3]
    else:
        first = min([row[1] for row in rows] or ["v1.0.25"], key=number)
        last = max([row[2] for row in rows] or ["v1.8.2"], key=number)
    ranges = {
        "legacy_fake_confidence": ("v1.0.25", "v1.0.34"),
        "legacy_marker_order": ("v1.1.0", "v1.1.0"),
        "legacy_nonrigid_alignment": ("v1.0.25", "v1.5.4"),
        "legacy_calibration_unverified": ("v1.0.25", "v1.8.2"),
    }
    return {
        "family": "v1",
        "release_range": [first, last],
        "ambiguous": not one_chain,
        "eras": [row[0] for row in rows],
        "warnings": sorted(
            code for code, (low, high) in ranges.items() if number(low) <= number(last) and number(first) <= number(high)
        ),
        "calibration": found,
    }


def test_g15_has_each_case_of_the_spec():
    assert {p.name for p in G15.iterdir() if p.is_dir()} == set(EXPECTED)
    assert {p.name for p in G15.iterdir() if p.is_file()} == {"SHA256SUMS"} | {
        f"{case}.{scope}.json" for case in EXPECTED for scope in ("full", "player")
    }


@pytest.mark.parametrize("case", EXPECTED)
def test_g15_result_follows_from_the_stub_files(case):
    folder = G15 / case
    full, player = load(G15 / f"{case}.full.json"), load(G15 / f"{case}.player.json")
    kind, release_range, ambiguous, eras = EXPECTED[case]
    assert family(folder) == kind
    if kind == "v1":
        found = calibration(folder)
        rows = matched_rows(folder, found["path"])
        legacy = v1_legacy(rows, found)
        player_legacy = legacy | {
            "release_range": ["v1.0.25", "v1.8.2"], "ambiguous": True, "eras": [], "warnings": FOUR_WARNINGS,
        }  # SFF-892  # fmt: skip
        assert player_legacy == v1_legacy([], found)
    else:
        legacy = player_legacy = {
            "family": kind, "release_range": None, "ambiguous": False, "eras": [], "warnings": [], "calibration": None,
        }  # fmt: skip
    assert (legacy["release_range"], legacy["ambiguous"], legacy["eras"]) == (release_range, ambiguous, eras)

    # SFF-885: the files of the root and of the media folder, not of their subfolders.
    listed = [p.name for p in folder.iterdir() if p.is_file()]
    listed += [f"synchronized_videos/{p.name}" for p in (folder / "synchronized_videos").glob("*") if p.is_file()]
    other_files = [{"name": n, "state": "not_in_format", "reason": None} for n in sorted(listed, key=str.encode)]
    for result, expected_legacy in ((full, legacy), (player, player_legacy)):
        assert result == {
            "result_version": 2, "folder_state": "legacy", "folder_warnings": [], "takes": [],
            "other_files": other_files, "legacy": expected_legacy,
        }  # fmt: skip


def test_g15_stubs_hold_no_data_and_no_file_of_this_format():
    for path in G15.rglob("*"):
        if path.is_file() and path.parent != G15:
            data = path.read_bytes()
            assert len(data) < 300, path
            assert b"skellyspecs" not in data and b"calibration_uuid" not in data, path  # SFF-875
            assert not path.name.lower().endswith((".pkl", ".pickle")), path


# ---------------------------------------------------------------- G16: the files are harmless

CODE_OPCODES = {
    "GLOBAL", "STACK_GLOBAL", "REDUCE", "INST", "OBJ", "NEWOBJ", "NEWOBJ_EX", "BUILD", "EXT1", "EXT2", "EXT4",
    "PERSID", "BINPERSID",
}  # fmt: skip


def opcodes(data: bytes) -> set[str]:
    """The opcode names of one pickle stream. `genops` reads the stream. It does not run it."""
    names = [op.name for op, _, _ in pickletools.genops(data)]
    assert names[-1] == "STOP"
    return set(names)


def npy_parts(data: bytes) -> tuple[dict, bytes]:
    """The header dictionary and the body of an NPY file of version 1.0."""
    assert data[:8] == b"\x93NUMPY\x01\x00"
    end = 10 + int.from_bytes(data[8:10], "little")
    assert end % 64 == 0 and data[end - 1 : end] == b"\n"
    return ast.literal_eval(data[10:end].decode("latin-1")), data[end:]


def pickles_and_npys(folder: Path) -> tuple[list[Path], list[Path]]:
    files = [p for p in folder.rglob("*") if p.is_file()]
    return (
        [p for p in files if p.name.lower().endswith((".pkl", ".pickle"))],
        [p for p in files if p.suffix.lower() == ".npy"],
    )


def test_g16_pickle_runs_no_code():
    (pickle_path,), (npy_path,) = pickles_and_npys(G16)
    assert pickle_path.parent == G16 and pickle_path.suffix == ".pkl"  # Appendix A: in the take folder
    assert not opcodes(pickle_path.read_bytes()) & CODE_OPCODES
    _, body = npy_parts(npy_path.read_bytes())
    assert not opcodes(body) & CODE_OPCODES


def test_g16_npy_header_declares_an_object_type():
    (npy_path,) = pickles_and_npys(G16)[1]
    header_dict, _ = npy_parts(npy_path.read_bytes())
    assert header_dict == {"descr": "|O", "fortran_order": False, "shape": (0,)}


def test_g16_numpy_sees_an_object_array_and_refuses_it():
    numpy = pytest.importorskip("numpy")
    (npy_path,) = pickles_and_npys(G16)[1]
    with npy_path.open("rb") as file:
        assert numpy.lib.format.read_magic(file) == (1, 0)
        assert numpy.lib.format.read_array_header_1_0(file)[2].hasobject
    with pytest.raises(ValueError, match="allow_pickle=False"):
        numpy.load(npy_path, allow_pickle=False)


def test_g16_results_name_the_two_files():
    (pickle_path,), (npy_path,) = pickles_and_npys(G16)
    pickle_name, npy_name = pickle_path.name, npy_path.relative_to(G16).as_posix()
    manifest = load(G16 / "recording_manifest.json")
    paths = [item["path"] for item in manifest["files"]]
    assert paths == sorted(paths, key=str.encode) and pickle_name not in paths
    (npy_manifest_item,) = [item for item in manifest["files"] if item["path"] == npy_name]
    assert npy_manifest_item == {"path": npy_name, "role": "export", "owner": "freemocap", "sha256": None}  # SFF-723

    full, player = load(G16.with_name("take.full.json")), load(G16.with_name("take.player.json"))
    for result, npy_state in ((full, ("invalid", "code_in_file")), (player, ("not_checked", None))):
        # SFF-884: the pickle is found by its name, so the scope does not change its item.
        assert result["other_files"] == [{"name": pickle_name, "state": "invalid", "reason": "code_in_file"}]
        assert (result["folder_state"], result["folder_warnings"], result["legacy"]) == ("ok", [], None)
        (take,) = result["takes"]
        assert (take["state"], take["manifest"], take["warnings"]) == ("complete", "present", [])
        assert [item["path"] for item in take["folder_files"]] == paths
        (npy_item,) = [item for item in take["folder_files"] if item["path"] == npy_name]
        assert npy_item == {
            "path": npy_name, "role": "export", "state": npy_state[0], "reason": npy_state[1], "warnings": [],
        }  # SFF-884, SFF-892  # fmt: skip
        assert {link["check"]: link["state"] for link in take["links"]}["files"] == "ok"

    # SFF-892: the scopes differ only in the item of the NPY and in the check `frames`.
    (full_take,), (player_take,) = full["takes"], player["takes"]
    assert [a["check"] for a, b in zip(full_take["links"], player_take["links"]) if a != b] == ["frames"]
    for take in (full_take, player_take):
        take["links"] = take["folder_files"] = None
    assert full == player
