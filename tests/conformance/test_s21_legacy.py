"""SFT-764 and SFT-765: legacy folders (SPEC.md section 21)."""

from __future__ import annotations

import json

import checks_folder as checks
import pytest

# The cases of G15 whose matched rows are in one chain, with the range of the last matched row (SFF-878).
ONE_CHAIN = {
    "v1a": ["v1.0.25", "v1.0.34"], "v1b_v1d": ["v1.1.0", "v1.3.0"], "v1b_v1c": ["v1.1.0", "v1.1.1"],
    "v1e_v1h": ["v1.3.1", "v1.7.4"], "v1f_v1h": ["v1.5.0", "v1.7.4"], "v1g_v1h": ["v1.6.0", "v1.7.4"],
    "v1h": ["v1.7.0", "v1.7.4"], "v1h_prime": ["v1.7.4", "v1.7.4"], "v1i": ["v1.8.0", "v1.8.2"],
}  # fmt: skip
TOML_SIGNAL = ["v1g_v1h", "v1h", "v1h_prime"]
NO_RANGE = {"v0_0_x": "pre_v1", "v0_1_0": "pre_v1", "mp4_only": "unknown"}
G15 = [*ONE_CHAIN, "two_chains", "no_signal", *NO_RANGE]


@pytest.mark.parametrize("case", G15)
def test_sft_764_legacy_recognition(reader, golden_or_skip, case):
    """SFT-764 Reader: legacy recognition. Checks: SFF-875, SFF-876, SFF-877, SFF-878, SFF-879."""
    folder = golden_or_skip("G15", case)
    raw = checks.read_bytes("full", reader, None, folder)
    result = json.loads(raw)
    legacy = result["legacy"]
    assert result["folder_state"] == "legacy" and result["takes"] == []
    assert legacy == checks.committed(folder)["legacy"], "the family, the range, `ambiguous`, `eras` and the warnings"
    if case in ONE_CHAIN:
        assert (legacy["family"], legacy["release_range"], legacy["ambiguous"]) == ("v1", ONE_CHAIN[case], False)
    if case in ("two_chains", "no_signal"):
        assert legacy["family"] == "v1" and legacy["ambiguous"] is True
    if case == "v1i":
        assert legacy["eras"] == ["V1i"]
    if case in TOML_SIGNAL:
        assert legacy["calibration"]["state"] == "present"
    if case in NO_RANGE:
        want = {"family": NO_RANGE[case], "release_range": None, "ambiguous": False, "eras": [], "warnings": [], "calibration": None}
        assert legacy == want
    assert b"unsupported" not in raw, "the result holds no note text"
    listed = [path for path in [*folder.iterdir(), *(folder / checks.MEDIA).glob("*")] if path.is_file()]
    names = [path.relative_to(folder).as_posix() for path in listed if not path.name.startswith(".") and not path.name.endswith(".tmp")]
    assert [item["name"] for item in result["other_files"]] == sorted(names, key=str.encode)


@pytest.mark.parametrize("case", ["exact_name", "one_toml", "two_tomls", "no_toml"])
def test_sft_765_calibration_lookup_in_v1_folders(reader, variant, case):
    """SFT-765 Reader: calibration lookup in v1 folders. Checks: SFF-880.

    The test makes the four folders from the case `v1a` of G15: it adds the TOML files.
    """
    folder = variant("G15", "v1a", folder_name="old_session")
    for toml in folder.glob("*.toml"):
        toml.unlink()
    names = {
        "exact_name": ["old_session_camera_calibration.toml"], "one_toml": ["my_calibration_2.toml"],
        "two_tomls": ["a_calibration.toml", "b_calibration.toml"], "no_toml": [],
    }[case]  # fmt: skip
    for name in names:
        (folder / name).write_bytes(b"[cam_0]\nrotation = [0.0, 0.0, 0.0]\n")
    result = checks.read(reader, folder)
    state = {"exact_name": "present", "one_toml": "present", "two_tomls": "ambiguous", "no_toml": "missing"}[case]
    assert result["legacy"]["calibration"] == {"path": names[0] if state == "present" else None, "state": state}
