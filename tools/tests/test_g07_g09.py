"""Structure checks of the committed golden folders G7, G8 and G9: each is a copy of G3 (SPEC.md Appendix A).

The checks compare each case with G3 through the sums, read the vector of each case of G9 from its
files, and compare each expected result with the result of G3. They do not import the generator. A
test that needs pyarrow skips when the package is absent.
"""

from __future__ import annotations

import hashlib
import json
import tomllib
from pathlib import Path

import pytest

from test_golden_files import GOLDEN, load, read_sidecar

MANIFEST = "recording_manifest.json"
REC = "g01_synthetic_take"
INFO, PROCESSING, TOML, PARQUET = (f"{REC}{s}" for s in ("_info.json", "_recording_info.json", "_camera_calibration.toml", "_data.parquet"))
G09_CASES = [
    "take_uuid", "camera_key", "frame_range", "row_counts", "dimensions", "rotation_in_configs", "unresolved_file",
    "stale_parquet_sha256", "calibration_hash", "calibration_uuid", "recording_id",
]  # Appendix A, "Layout and cases"  # fmt: skip
# The files of each case whose bytes differ from G3, and the check that shows the vector (SFF-872).
PARQUET_CHANGE = {PARQUET, PROCESSING, MANIFEST}
CASES = {
    ("G07", "no_manifest"): (set(), None),
    ("G07", "other_take_manifest"): ({MANIFEST}, None),
    ("G08", "renamed"): (set(), None),
    ("G09", "take_uuid"): ({PROCESSING, MANIFEST}, "take_uuid"),
    ("G09", "camera_key"): ({INFO, MANIFEST}, "camera_key"),
    ("G09", "frame_range"): (PARQUET_CHANGE, "frames"),
    ("G09", "row_counts"): (PARQUET_CHANGE | {f"synchronized_videos/{REC}.e40ba1.{s}" for s in ("mkv", "csv")}, "frames"),
    ("G09", "dimensions"): (PARQUET_CHANGE, "dimensions"),
    ("G09", "rotation_in_configs"): ({INFO, MANIFEST}, "rotation"),
    ("G09", "unresolved_file"): (PARQUET_CHANGE, "files"),
    ("G09", "stale_parquet_sha256"): ({PROCESSING, MANIFEST}, "hashes"),
    ("G09", "calibration_hash"): ({MANIFEST}, "hashes"),
    ("G09", "calibration_uuid"): ({MANIFEST}, "calibration"),
    ("G09", "recording_id"): (PARQUET_CHANGE, None),
}
IN_PLAYER = {"take_uuid", "camera_key", "rotation"}  # the vector is in a JSON file (SFF-892)
NOT_IN_PLAYER = ("frames", "dimensions", "hashes", "calibration")
pytestmark = pytest.mark.skipif(
    not all((GOLDEN / f).is_dir() for f in ("G03", "G07", "G08", "G09")), reason="a golden folder does not exist"
)


def sums(folder: str, case: str) -> dict:
    lines = (GOLDEN / folder / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    pairs = (line.split("  ", 1) for line in lines)
    return {name.removeprefix(f"{case}/"): digest for digest, name in pairs if name.startswith(f"{case}/")}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def result(folder: str, case: str, scope: str) -> dict:
    return load(GOLDEN / folder / f"{case}.{scope}.json")


def states(take: dict) -> dict:
    return {link["check"]: link["state"] for link in take["links"]}


def test_the_cases_of_appendix_a():
    found = {(f, p.name) for f in ("G07", "G08", "G09") for p in (GOLDEN / f).iterdir() if p.is_dir()}
    assert found == set(CASES) and [c for f, c in CASES if f == "G09"] == G09_CASES


@pytest.mark.parametrize(("folder", "case"), CASES, ids="/".join)
def test_case_is_g03_with_one_change(folder, case):
    changed, _ = CASES[(folder, case)]
    g3, copy = sums("G03", "take"), sums(folder, case)
    assert set(copy) == set(g3) - ({MANIFEST} if case == "no_manifest" else set())
    assert {name for name in copy if copy[name] != g3[name]} == changed
    # Each `sha256` of the manifest is the hash of its file, except the vector `calibration_hash` (SFF-723).
    root = GOLDEN / folder / case
    if (root / MANIFEST).is_file():
        manifest = json.loads((root / MANIFEST).read_bytes())
        for item in manifest["files"]:
            assert item["sha256"] == (None if item["role"] == "tracking" else sha256(root / item["path"]))
        assert (manifest["calibration"]["sha256"] == sha256(root / TOML)) == (case != "calibration_hash")


def test_g07_manifests():
    g3 = json.loads((GOLDEN / "G03" / "take" / MANIFEST).read_bytes())
    assert not (GOLDEN / "G07" / "no_manifest" / MANIFEST).exists()
    other = json.loads((GOLDEN / "G07" / "other_take_manifest" / MANIFEST).read_bytes())
    assert other["take_uuid"] != g3["take_uuid"] and other | {"take_uuid": g3["take_uuid"]} == g3
    assert list(other) == list(g3)


@pytest.mark.parametrize("scope", ["full", "player"])
@pytest.mark.parametrize("case", ["no_manifest", "other_take_manifest"])
def test_g07_results(case, scope):
    """SFT-710: the rebuild, against the result of G3 (SFF-731, SFF-867, SFF-872, SFF-883)."""
    found, g3 = result("G07", case, scope), result("G03", "take", scope)
    (take,), (g3_take,) = found["takes"], g3["takes"]
    assert take["manifest"] == ("missing" if case == "no_manifest" else "invalid")
    assert take["warnings"] == ["manifest_missing"] and take["may_contain_private_data"] is True
    for member in ("take_uuid", "recording_name", "state", "files", "folder_files"):
        assert take[member] == g3_take[member], member
    no_part = {"camera_key", "calibration"} | ({"files"} if scope == "player" else set())
    assert states(take) == states(g3_take) | dict.fromkeys(no_part, "not_checked")
    if case == "no_manifest":
        assert {k: v for k, v in found.items() if k != "takes"} == {k: v for k, v in g3.items() if k != "takes"}
    else:
        assert found["other_files"] == [{"name": MANIFEST, "state": "invalid", "reason": "take_fact_mismatch"}]
        assert found["folder_warnings"] == ["orphan_file"]
        assert result("G07", "no_manifest", scope)["takes"][0]["links"] == take["links"]


def test_g08_results_are_the_bytes_of_g03():
    """SFT-706: the reader result of the renamed folder is the result of G3, byte for byte."""
    for suffix in ("full.json", "player.json", "truth.json"):
        assert (GOLDEN / "G08" / f"renamed.{suffix}").read_bytes() == (GOLDEN / "G03" / f"take.{suffix}").read_bytes()


@pytest.mark.parametrize("scope", ["full", "player"])
@pytest.mark.parametrize("case", G09_CASES)
def test_g09_results(case, scope):
    """SFT-763: each vector gives `mismatch` in its check, and in no other (SFF-824, SFF-872, SFF-874, SFF-892)."""
    _, check = CASES[("G09", case)]
    (take,), (g3_take,) = result("G09", case, scope)["takes"], result("G03", "take", scope)["takes"]
    expected = states(g3_take)
    if check and (scope == "full" or check in IN_PLAYER):
        expected[check] = "mismatch"
    if case == "recording_id" and scope == "full":
        expected["dimensions"] = "not_checked"  # a part whose file is `invalid` is not evaluated
    assert states(take) == expected
    assert take["warnings"] == (["stale_processing_info"] if case == "stale_parquet_sha256" and scope == "full" else [])
    folder_files = [dict(item) for item in g3_take["folder_files"]]
    if case == "recording_id" and scope == "full":
        (parquet,) = [item for item in folder_files if item["path"] == PARQUET]
        parquet |= {"state": "invalid", "reason": "take_fact_mismatch"}
    assert take["folder_files"] == folder_files
    if case != "row_counts":
        assert take["files"] == g3_take["files"]
    if scope == "player" and check not in IN_PLAYER:
        assert result("G09", case, scope) == result("G03", "take", scope) | {"takes": [take]}


def test_g09_vectors_in_the_json_toml_and_csv_files():
    def case(name: str, path: str):
        data = (GOLDEN / "G09" / name / path).read_bytes()
        return tomllib.loads(data.decode()) if path.endswith(".toml") else json.loads(data)

    g3_take_uuid = case("take_uuid", MANIFEST)["take_uuid"]
    assert case("take_uuid", PROCESSING)["take_uuid"] != g3_take_uuid == case("take_uuid", INFO)["take_uuid"]
    manifest = case("camera_key", MANIFEST)
    configs = case("camera_key", INFO)["camera_configs"]
    assert [c["camera_key"] in configs for c in manifest["cameras"]] == [True, False]
    keys = {f["field"].split("/")[2] for f in manifest["privacy"]["fields"] if f["field"].startswith("/camera_configs/")}
    assert keys == set(configs)  # SFF-881: `<key>` is a key of `camera_configs`
    assert ["rotation" in c for c in case("rotation_in_configs", INFO)["camera_configs"].values()] == [False, True]
    stale = case("stale_parquet_sha256", PROCESSING)["processed"]["parquet_sha256"]
    assert stale != sha256(GOLDEN / "G09" / "stale_parquet_sha256" / PARQUET)
    toml_uuid = case("calibration_uuid", TOML)["metadata"]["calibration_uuid"]
    assert case("calibration_uuid", MANIFEST)["calibration"]["calibration_uuid"] != toml_uuid
    assert case("calibration_uuid", MANIFEST)["summary"]["calibration"]["calibration_uuid"] == toml_uuid  # SFF-728
    rows = [len(read_sidecar(GOLDEN / "G09" / "row_counts" / c["timing"])[1]) for c in case("row_counts", MANIFEST)["cameras"]]
    assert rows == [89, 90]  # both sidecars are finished: they end with `# end` (read_sidecar)
    files = result("G09", "row_counts", "full")["takes"][0]["files"]
    assert [f["rows"] for f in files] == [89, 90, 30] and [len(f["records"]) for f in files] == [89, 90, 30]


def test_g09_vectors_in_the_parquet():
    pq = pytest.importorskip("pyarrow.parquet")

    def parquet(name: str) -> tuple[dict, dict, list[dict]]:
        path = GOLDEN / "G09" / name / PARQUET
        descriptor = json.loads(pq.read_schema(path).metadata[b"freemocap.recording"])
        info = json.loads((path.parent / PROCESSING).read_bytes())["processed"]
        assert info["parquet_sha256"] == sha256(path) and info["recording_id"] == REC  # only the vector differs
        return descriptor, descriptor["runs"]["0"], pq.read_table(path, columns=["frame_number"]).to_pylist()

    def frames(rows: list[dict]) -> int:
        return max(row["frame_number"] for row in rows) + 1

    _, run, rows = parquet("frame_range")
    assert frames(rows) == 91 and next(iter(run["sensor_groups"].values()))["sample_count"] == 91
    _, run, rows = parquet("row_counts")
    assert frames(rows) == 89  # SFF-754: the smallest row count
    _, run, _ = parquet("dimensions")
    assert [(f["width"], f["height"]) for k, f in run["reference_frames"].items() if k.endswith(":image")] == [(64, 48), (128, 96)]
    _, run, _ = parquet("unresolved_file")
    media = GOLDEN / "G09" / "unresolved_file" / "synchronized_videos"
    names = [s["definition"]["video_filename"] for s in run["sources"].values() if s["kind"] == "camera"]
    assert [(media / name).is_file() for name in names] == [True, False]
    descriptor, _, _ = parquet("recording_id")
    assert descriptor["recording_id"] != REC
