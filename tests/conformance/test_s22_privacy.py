"""SFT-766 and SFT-767: privacy and safety (SPEC.md section 22)."""

from __future__ import annotations

import io
import pickle
import zipfile
from pathlib import Path

import checks_capture as capture
import checks_folder as checks
import pytest


def test_sft_766_golden_part(golden_or_skip):
    """SFT-766 Writer: the privacy list of the manifest of G3. Checks: SFF-881, SFF-882.

    A check on the golden folder: `fields` has exactly the fields of the table of SFF-881 that exist
    and are not null, sorted, and `media_shows_people` is true.
    """
    folder = golden_or_skip("G03")
    info = checks.load_json(checks.capture_info(folder))
    devices = [config["device"] for config in info["camera_configs"].values()]
    assert any(config["user_name"] for config in info["camera_configs"].values()), "G3 has a user camera name"
    assert any(device["serial"] for device in devices) and any(device["os_device_id"] for device in devices)
    assert checks.privacy_faults(folder) == []


def test_sft_766_writer_part(writer, tmp_path):
    """SFT-766 Writer: the privacy list of the manifest that the writer of the test adapter writes (a camera with a name, a serial and a port)."""
    capture.record_take(writer, tmp_path / "take", audio=capture.microphone())
    assert checks.privacy_faults(tmp_path / "take") == []


@pytest.mark.parametrize("case", ["g3", "g7_no_manifest", "g1_audio_only"])
def test_sft_766_may_contain_private_data(reader, variant, golden_or_skip, case):
    """SFT-766 Reader: `may_contain_private_data`. Checks: SFF-883."""
    if case == "g3":
        folder = golden_or_skip("G03")
    elif case == "g7_no_manifest":
        folder = golden_or_skip("G07", "no_manifest")
    else:  # G1 with its camera pairs deleted
        folder = variant("G01")
        for camera in checks.manifest(folder)["cameras"]:
            (folder / camera["video"]).unlink()
            (folder / camera["timing"]).unlink()
    assert checks.the_take(checks.read(reader, folder))["may_contain_private_data"] is True


def _npy(descr: str, body: bytes = b"") -> bytes:
    """An NPY file of version 1.0 with this `descr`."""
    text = f"{{'descr': '{descr}', 'fortran_order': False, 'shape': (1,), }}"
    text += " " * (-(10 + len(text) + 1) % 64) + "\n"
    return b"\x93NUMPY\x01\x00" + len(text).to_bytes(2, "little") + text.encode("latin-1") + body


def _npz(members: dict[str, bytes]) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, data in members.items():
            archive.writestr(name, data)
    return buffer.getvalue()


class _Canary:
    """A value whose pickle creates the canary file when a program loads it. The test never loads it."""

    def __init__(self, path: Path):
        self.path = path

    def __reduce__(self):
        return (open, (str(self.path), "w"))


def _code_files(canary: Path) -> dict[str, tuple[bytes, str]]:
    """Each file that SFT-767 adds to a copy of G16: its path, its bytes and the reason of its item."""
    bomb = pickle.dumps(_Canary(canary), protocol=2)
    return {
        "exports/object_member.npz": (_npz({"a.values.npy": _npy("|O", bomb), "recording_info.json": b"{}"}), "code_in_file"),
        "exports/not_a_zip.npz": (b"this file is not a ZIP file\n", "bad_schema"),
        "exports/member_with_no_header.npz": (_npz({"a.values.npy": b"no NPY header"}), "bad_schema"),
        "exports/npy/no_header.npy": (b"no NPY header", "bad_schema"),
    }  # fmt: skip


@pytest.mark.parametrize("scope", ["full", "player"])
def test_sft_767_no_code_in_files(reader, variant, tmp_path, scope):
    """SFT-767 Reader: no code in files. Checks: SFF-884.

    The NPY and NPZ checks are tests of the scope `full` only. For the scope `player`, each of these
    items is `not_checked`. The pickle of G16 is harmless, so the test adds a pickle and an NPZ member
    whose load creates a canary file.
    """
    folder = variant("G16")
    canary = tmp_path / "canary.txt"
    files = _code_files(canary)
    (folder / "canary.pkl").write_bytes(pickle.dumps(_Canary(canary), protocol=2))
    listed = checks.manifest(folder)
    for path, (data, _) in files.items():
        (folder / path).parent.mkdir(parents=True, exist_ok=True)
        (folder / path).write_bytes(data)
        listed["files"].append({"path": path, "role": "export", "owner": "freemocap", "sha256": None})
    listed["files"].sort(key=lambda item: item["path"].encode())
    checks.write_json(folder / "recording_manifest.json", listed)
    result = checks.read(reader, folder, scope=scope)
    take = checks.the_take(result)
    pickles = [item for item in result["other_files"] if item["name"].endswith(".pkl")]
    assert len(pickles) == 2 and all((item["state"], item["reason"]) == ("invalid", "code_in_file") for item in pickles)
    arrays = [item for item in take["folder_files"] if item["path"].endswith((".npy", ".npz"))]
    assert len(arrays) == len(files) + 1, "the NPY of G16 and the four files of the test"
    for item in arrays:
        reason = files[item["path"]][1] if item["path"] in files else "code_in_file"  # the NPY of G16 has an object `descr`
        want = ("invalid", reason) if scope == "full" else ("not_checked", None)
        assert (item["state"], item["reason"]) == want, item["path"]
    assert not canary.exists(), "no code from the files runs"
