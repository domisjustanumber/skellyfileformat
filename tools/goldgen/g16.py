"""Golden folder G16 (recording-files/SPEC.md Appendix A): a take with a pickle and with an NPY object array (SFF-884).

The take is the take of G1 with another `<rec>` and `take_uuid`. The two added files are harmless:
each pickle stream holds a plain value, so a load runs no code. A reader finds the pickle by its
name suffix and the object array by the NPY header. recording-files/golden/G16_CHOICES.md gives each value that the
spec does not give.
"""

from __future__ import annotations

import json
import pickle
from pathlib import Path

from goldgen import common, g01

TAKE = g01.TAKE | {"rec": "g16_synthetic_take", "take_uuid": "00000000000040008000000000000016"}
PICKLE = "harmless_plain_dict.pkl"
NPY = f"exports/npy/{TAKE['rec']}.frames.npy"
# A fixed protocol gives fixed bytes. Protocol 2 writes a plain value with no frame and no class.
PICKLE_BYTES = pickle.dumps({"harmless": True}, protocol=2)


def npy_object_array() -> bytes:
    """An NPY file of version 1.0 with an object `descr`, written by hand: NumPy is not needed.

    NumPy stores an object array as one pickle after the header. Here that pickle is an empty list.
    """
    header = "{'descr': '|O', 'fortran_order': False, 'shape': (0,), }"
    header += " " * (-(10 + len(header) + 1) % 64) + "\n"  # the magic, the version and the length are 10 bytes
    return b"\x93NUMPY\x01\x00" + len(header).to_bytes(2, "little") + header.encode("latin-1") + pickle.dumps([], 2)


def build(out: Path) -> None:
    """Write the case `take` of G16 into `out`, with its two expected results."""
    case = out / "take"
    facts = common.write_take(case, TAKE, g01.cameras(), g01.audio())
    (case / PICKLE).write_bytes(PICKLE_BYTES)
    (case / NPY).parent.mkdir(parents=True)
    (case / NPY).write_bytes(npy_object_array())

    # `write_take` takes no other file, so the manifest gets the item of the NPY here (SFF-723).
    manifest_path = case / "recording_manifest.json"
    manifest = json.loads(manifest_path.read_bytes())
    manifest["files"].append({"path": NPY, "role": "export", "owner": "freemocap", "sha256": None})
    manifest["files"].sort(key=lambda item: item["path"].encode())
    manifest_path.write_bytes(common.file_json(manifest))

    for scope in ("full", "player"):
        result = common.expected_result(facts, scope)
        npy_item = (
            {"path": NPY, "role": "export", "state": "invalid", "reason": "code_in_file", "warnings": []}  # SFF-884
            if scope == "full"
            else {"path": NPY, "role": "export", "state": "not_checked", "reason": None, "warnings": []}  # SFF-892
        )
        (take,) = result["takes"]
        take["folder_files"] = sorted([*take["folder_files"], npy_item], key=lambda item: item["path"].encode())
        result["other_files"] = [{"name": PICKLE, "state": "invalid", "reason": "code_in_file"}]  # SFF-884
        (out / f"{case.name}.{scope}.json").write_bytes(common.canonical_json(result))
