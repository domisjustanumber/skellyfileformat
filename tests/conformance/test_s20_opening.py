"""SFT-761 to SFT-763: opening a folder (SPEC.md section 20)."""

from __future__ import annotations

import shutil
import tomllib
from pathlib import Path

import checks_folder as checks
import pytest

MEDIA = checks.MEDIA
OTHER_UUID = "0000000000004000800000000000ffff"
OTHER_KEY, OTHER_LABEL = "abcdef0123456789", "abcdef"


def _pair(folder: Path, position: int) -> tuple[Path, Path]:
    """The camera file and the timing sidecar of the camera at one `group_position`."""
    camera = checks.manifest(folder)["cameras"][position]
    return folder / camera["video"], folder / camera["timing"]


def _third_sidecar(folder: Path, name: str, with_media: bool) -> Path:
    """A copy of the sidecar of camera 1 for a third camera of the same take, with or without its camera file."""
    mkv, csv = _pair(folder, 1)
    sidecar = folder / MEDIA / f"{name}.csv"
    shutil.copy(csv, sidecar)
    for key, value in (("camera_key", OTHER_KEY), ("camera_label", OTHER_LABEL), ("group_position", "2")):
        checks.set_header(sidecar, key, value)
    if with_media:
        shutil.copy(mkv, sidecar.with_suffix(".mkv"))
    return sidecar


@pytest.mark.parametrize("case", ["sidecar_of_the_take", "sidecar_of_another_take"])
def test_sft_761_device_pairs_and_orphan_files(reader, variant, case):
    """SFT-761 Reader: device pairs and orphan files. Checks: SFF-864, SFF-865."""
    folder = variant("G03")
    rec = checks.manifest(folder)["recording_name"]
    if case == "sidecar_of_the_take":
        shutil.copy(_pair(folder, 0)[0], folder / MEDIA / "extra.mkv")  # an extra `.mkv` with no sidecar
        _third_sidecar(folder, f"{rec}.{OTHER_LABEL}", with_media=False)
        result = checks.read(reader, folder)
        take = checks.the_take(result)
        assert checks.named(result["other_files"], f"{MEDIA}/extra.mkv")["state"] == "not_in_format"
        item = checks.named(take["files"], f"{MEDIA}/{rec}.{OTHER_LABEL}.mkv")  # the path of the missing media file
        assert (item["state"], item["reason"]) == ("invalid", "missing_media")
        assert "extra_files" not in take["warnings"]
    else:
        sidecar = _third_sidecar(folder, f"other.{OTHER_LABEL}", with_media=False)
        checks.set_header(sidecar, "take_uuid", OTHER_UUID)
        result = checks.read(reader, folder)
        item = checks.named(result["other_files"], f"{MEDIA}/{sidecar.name}")  # the path of the sidecar
        assert (item["state"], item["reason"]) == ("invalid", "missing_media")
    assert result["folder_warnings"].count("orphan_file") == 1


@pytest.mark.parametrize("case", ["g9", "two_takes", "camera_missing", "third_camera_pair", "one_label", "clock_disagrees", "group_size_disagrees"])
def test_sft_762_takes_and_counts(reader, variant, golden_or_skip, case):
    """SFT-762 Reader: takes and counts. Checks: SFF-866, SFF-869, SFF-870, SFF-871."""
    if case == "g9":  # each take is reported
        for name in checks.G09_CHECKS:
            folder = golden_or_skip("G09", name)
            uuids = {checks.header(sidecar)["take_uuid"] for sidecar in (folder / MEDIA).glob("*.csv")}
            assert {take["take_uuid"] for take in checks.read(reader, folder)["takes"]} == uuids, name
        return
    folder = variant("G03")
    rec = checks.manifest(folder)["recording_name"]
    if case == "two_takes":
        for media in sorted((folder / MEDIA).glob(f"{rec}.*")):
            copy = media.with_name("second_take" + media.name.removeprefix(rec))
            shutil.copy(media, copy)
            if copy.suffix == ".csv":
                checks.set_header(copy, "take_uuid", OTHER_UUID)
        result = checks.read(reader, folder)
        assert sorted(take["take_uuid"] for take in result["takes"]) == sorted([checks.manifest(folder)["take_uuid"], OTHER_UUID])
        assert "multiple_takes" in result["folder_warnings"]
        return
    if case == "camera_missing":
        for path in _pair(folder, 1):
            path.unlink()
    elif case == "third_camera_pair":
        _third_sidecar(folder, f"{rec}.{OTHER_LABEL}", with_media=True)
    elif case == "one_label":
        checks.set_header(_pair(folder, 1)[1], "camera_label", checks.manifest(folder)["cameras"][0]["camera_label"])
    elif case == "group_size_disagrees":
        # Camera 1 says 3 and camera 0 says 2. The two files are the full take only with the value of group_position 0.
        assert checks.header(_pair(folder, 0)[1])["group_size"] == "2"
        checks.set_header(_pair(folder, 1)[1], "group_size", "3")
    else:
        assert checks.header(_pair(folder, 0)[1])["clock"] != "linux_monotonic"
        checks.set_header(_pair(folder, 1)[1], "clock", "linux_monotonic")
    take = checks.the_take(checks.read(reader, folder))
    if case == "camera_missing":
        assert take["state"] == "incomplete" and "incomplete_take" in take["warnings"]
    else:
        code = {"third_camera_pair": "extra_files", "one_label": "duplicate_label", "clock_disagrees": "take_fact_mismatch", "group_size_disagrees": "take_fact_mismatch"}[case]
        assert code in take["warnings"]
    if case == "group_size_disagrees":
        assert take["state"] == "complete" and "incomplete_take" not in take["warnings"], "the values of `group_position` 0 are used"
    if case == "one_label":
        assert len([item for item in take["files"] if item["kind"] == "camera"]) == 2, "the reader keeps both files"


def _key_zero(folder: Path) -> str:
    """Change camera 1 of a copy of G3 to a camera with `camera_key` 0. Return its label `cam<N>`.

    Each file that names the camera changes: its pair, the manifest, the two info JSONs, the TOML and
    the Parquet. In the capture info JSON, the key of the camera config is `0:<camera_label>`.
    """
    listed = checks.manifest(folder)
    camera = listed["cameras"][1]
    key, label, new = camera["camera_key"], camera["camera_label"], f"cam{camera['group_position']}"

    def text(value: str) -> str:
        return value.replace(f"/camera_configs/{key}/", f"/camera_configs/0:{new}/").replace(key, "0").replace(label, new)

    def renamed(value):
        if isinstance(value, dict):
            return {text(name): renamed(item) for name, item in value.items()}
        if isinstance(value, list):
            return [renamed(item) for item in value]
        return text(value) if isinstance(value, str) else value

    for path in _pair(folder, 1):
        if path.suffix == ".csv":
            checks.set_header(path, "camera_key", "0")
            checks.set_header(path, "camera_label", new)
        path.rename(path.with_name(text(path.name)))
    info_path = checks.capture_info(folder)
    info = renamed(checks.load_json(info_path))
    info["camera_configs"] = {(f"0:{new}" if name == "0" else name): config for name, config in info["camera_configs"].items()}
    info["camera_configs"][f"0:{new}"]["key_origin"] = None
    checks.write_json(info_path, info)
    processing_path = checks.one(folder, "*_recording_info.json")
    checks.write_json(processing_path, renamed(checks.load_json(processing_path)))
    checks.rewrite_parquet(folder, renamed, rename=(label, new))
    toml_path = folder / listed["calibration"]["file"]
    toml_path.write_bytes(checks.toml_text(renamed(tomllib.loads(toml_path.read_text(encoding="utf-8")))).encode())
    listed = renamed(listed)
    listed["calibration"]["sha256"] = checks.sha256(toml_path)
    listed["privacy"]["fields"].sort(key=lambda item: (item["file"], item["field"]))
    checks.write_json(folder / "recording_manifest.json", listed)
    return new


def test_sft_763_link_checks_g3(reader, golden_or_skip):
    """SFT-763 Reader: link checks, G3. Checks: SFF-872."""
    take = checks.the_take(checks.read(reader, golden_or_skip("G03")))
    assert take["links"] == [{"check": check, "detail": None, "state": "ok"} for check in checks.LINKS]


@pytest.mark.parametrize("case", checks.G09_CHECKS)
def test_sft_763_link_checks_g9(reader, golden_or_skip, case):
    """SFT-763 Reader: link checks, each vector of G9. Checks: SFF-824, SFF-872, SFF-874."""
    take = checks.the_take(checks.read(reader, golden_or_skip("G09", case)))
    assert [(item["check"], item["detail"]) for item in take["links"]] == [(check, None) for check in checks.LINKS]
    if case == "recording_id":
        item = checks.folder_file(take, "_data.parquet")
        assert (item["state"], item["reason"]) == ("invalid", "take_fact_mismatch")
        assert checks.link(take, "dimensions") == "not_checked", "a part whose file is `invalid` is not evaluated"
    else:
        assert checks.link(take, checks.G09_CHECKS[case]) == "mismatch"
    assert ("stale_processing_info" in take["warnings"]) == (case == "stale_parquet_sha256")


@pytest.mark.parametrize("name", ["G05", "G06"])
def test_sft_763_link_checks_unfinished_files(reader, golden_or_skip, name):
    """SFT-763 Reader: the row-count part of `frames` is not evaluated for G5 and G6. Checks: SFF-872."""
    cases = {"G05": ["audio_clean_kill", "audio_torn_fragment"], "G06": ["repaired", "interrupted_repair"]}[name]
    for case in cases:
        take = checks.the_take(checks.read(reader, golden_or_skip(name, case)))
        assert checks.link(take, "frames") == "not_checked", case


def test_sft_763_link_checks_key_zero(reader, variant):
    """SFT-763 Reader: G3 with one `camera_key` 0. Checks: SFF-720, SFF-873."""
    folder = variant("G03")
    label = _key_zero(folder)
    take = checks.the_take(checks.read(reader, folder))
    camera = take["files"][1]
    assert (camera["camera_key"], camera["camera_label"]) == ("0", label)
    assert "camera_key_zero" in take["warnings"]
    assert checks.link(take, "camera_key") == "ok", "the camera is linked by its label"
