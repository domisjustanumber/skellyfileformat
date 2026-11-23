"""Cross-checks of the committed files of golden folders G10, G13 and G14 (recording-files/golden/G10_G13_G14_CHOICES.md).

The checks read the files with `json`, `struct`, `zlib`, `tomllib` and pyarrow. They compute each value
again from the text of the spec. They do not use the code path that wrote the files. A test that
needs pyarrow skips when the package is absent.
"""

from __future__ import annotations

import hashlib
import json
import math
import struct
import tomllib
import zlib
from pathlib import Path

import pytest

from test_golden_files import GOLDEN, load, read_sidecar

G10, G13, G14 = GOLDEN / "G10", GOLDEN / "G13", GOLDEN / "G14"
pytestmark = pytest.mark.skipif(not all(p.is_dir() for p in (G10, G13, G14)), reason="a golden folder does not exist")
MAGIC, QNAN = b"SKRJ", b"\x00\x00\xc0\x7f"


def manifest(case: Path) -> dict:
    return json.loads((case / "recording_manifest.json").read_bytes())


def take(path: Path) -> dict:
    (result,) = load(path)["takes"]
    return result


def descriptor(path: Path) -> dict:
    pq = pytest.importorskip("pyarrow.parquet")
    return json.loads(pq.read_schema(path).metadata[b"freemocap.recording"])


def rows(path: Path) -> list[dict]:
    pq = pytest.importorskip("pyarrow.parquet")
    return pq.read_table(path).to_pylist()


# ---------------------------------------------------------------- the journal scan of SFF-843


def scan(data: bytes) -> dict:
    """The scan of SFF-843, written again from the text of the spec."""
    at, good, rejected, cut = 0, [], [], []
    while (o := data.find(MAGIC, at)) >= 0:
        length = struct.unpack("<I", data[o + 4 : o + 8])[0] if o + 8 <= len(data) else None
        in_range = length is not None and 1 <= length <= 2**26
        if length is None or (in_range and o + 12 + length > len(data)):
            cut.append(o)
            at = o + 4
            continue
        body = data[o + 8 : o + 8 + length]
        if in_range and struct.unpack("<I", data[o + 8 + length : o + 12 + length])[0] == zlib.crc32(body):
            good.append((o, body[0], body[1:]))
            at = o + 12 + length
        else:
            rejected.append(o)
            at = o + 4
    last_good = good[-1][0] if good else -1
    torn = next((o for o in cut if o > last_good), None)
    rejected += [o for o in cut if o < last_good]  # a cut record with a good record after it
    return {
        "good": good, "rejected": sorted(o for o in rejected if torn is None or o < torn), "torn": torn,
        "torn_bytes": len(data) - torn if torn is not None else 0,
    }  # fmt: skip


def test_scan_of_the_test():
    record = MAGIC + struct.pack("<I", 2) + b"\x02x" + struct.pack("<I", zlib.crc32(b"\x02x"))
    assert scan(record + bytes(8) + record[:-1])["torn_bytes"] == len(record) - 1
    result = scan(MAGIC + struct.pack("<I", 1000) + record)  # a cut record before a good record is rejected
    assert (len(result["good"]), result["rejected"], result["torn"]) == (1, [0], None)


# ---------------------------------------------------------------- G13 and G10 `higher_minor_journal`

JOURNAL_CASES = [(G13, "take", "2.0"), (G10, "higher_minor_journal", "2.1")]


@pytest.mark.parametrize(("folder", "case", "version"), JOURNAL_CASES, ids=lambda v: getattr(v, "name", v))
def test_journal_bytes(folder, case, version):
    truth = json.loads((folder / f"{case}.truth.json").read_bytes())["journal"]
    m = manifest(folder / case)
    data = (folder / case / truth["name"]).read_bytes()
    found = scan(data)

    # The header record (SFF-839), with the version of the case.
    offset, kind, payload = found["good"][0]
    assert offset == 0 and kind == 1
    header = json.loads(payload)
    assert list(header) == ["skellyspecs", "format_version", "format_prerelease", "writer", "take_uuid", "origin", "channels"]
    assert (header["skellyspecs"], header["format_version"], header["format_prerelease"]) == ("realtime_journal", version, 1)
    assert (header["take_uuid"], header["origin"]) == (m["take_uuid"], "realtime")
    for index, channel in enumerate(header["channels"]):
        assert channel["channel_index"] == index and channel["dtype"] == "float32" and channel["kind"] != "TIMESTAMPS"  # SFF-841

    # The good records, the record with a wrong CRC, the hole and the torn tail.
    assert [o for o, _, _ in found["good"]] == truth["good_offsets"]
    (bad,) = truth["rejected_offsets"]
    assert found["rejected"] == [bad]
    length = struct.unpack("<I", data[bad + 4 : bad + 8])[0]
    assert data[bad : bad + 4] == MAGIC and 1 <= length <= 2**26
    assert struct.unpack("<I", data[bad + 8 + length : bad + 12 + length])[0] != zlib.crc32(data[bad + 8 : bad + 8 + length])
    hole, size = truth["hole"]
    assert size == 4096 and data[hole : hole + size] == bytes(size) and data[hole + size : hole + size + 4] == MAGIC
    assert found["torn"] == truth["torn_tail"] and data[found["torn"] :].startswith(MAGIC)
    assert not any(kind == 4 for _, kind, _ in found["good"]), "no end record"
    kinds = [kind for _, kind, _ in found["good"]]
    assert kinds.count(200) == (version == "2.1")  # SFF-709: the unknown type counts in `records`

    for _, kind, payload in found["good"]:
        if kind == 2:  # SFF-840: 22 + 4 × n × k bytes
            _, frame, _, n, k = struct.unpack("<HiqII", payload[:22])
            assert len(payload) == 22 + 4 * n * k and 0 <= frame < 12

    # The result of the scope `full` (SFF-843, SFF-886), and the scope `player` (SFF-892).
    item = next(i for i in take(folder / f"{case}.full.json")["folder_files"] if i["path"] == truth["name"])
    assert item == {
        "path": truth["name"], "role": "realtime_journal", "state": "damaged", "reason": "crc_mismatch",
        "warnings": ["prerelease"], "records": len(found["good"]), "rejected_records": 1,
        "torn_bytes": found["torn_bytes"],
    }  # fmt: skip
    item = next(i for i in take(folder / f"{case}.player.json")["folder_files"] if i["path"] == truth["name"])
    assert (item["state"], item["records"], item["rejected_records"], item["torn_bytes"]) == ("not_checked", None, None, None)


def folded(data: bytes) -> dict:
    """SFF-845: the values of the last good data record of each (channel, frame), and its `processed_ns`."""
    values = {}
    for _, kind, payload in scan(data)["good"]:
        if kind == 2:
            channel, frame, processed_ns, n, k = struct.unpack("<HiqII", payload[:22])
            values[channel, frame] = (processed_ns, [payload[22 + 4 * i : 26 + 4 * i] for i in range(n * k)])
    return values


@pytest.mark.parametrize(("folder", "case", "version"), JOURNAL_CASES, ids=lambda v: getattr(v, "name", v))
def test_fold_check_and_parquet_run(folder, case, version):
    truth = json.loads((folder / f"{case}.truth.json").read_bytes())["journal"]
    m = manifest(folder / case)
    data = (folder / case / truth["name"]).read_bytes()
    values = folded(data)
    digest = b"".join(v for key in sorted(values) for v in values[key][1])
    assert (len(digest) // 4, hashlib.sha256(digest).hexdigest()) == (truth["check_count"], truth["check_digest"])

    parquet = folder / case / f"{m['recording_name']}_data.parquet"
    d = descriptor(parquet)
    assert list(d["runs"]) == ["0"]
    run = d["runs"]["0"]
    header = json.loads(scan(data)["good"][0][2])
    channels = [{k: v for k, v in c.items() if k != "channel_index"} for c in header["channels"]]
    assert [c for c in run["channels"] if c["kind"] != "TIMESTAMPS"] == channels
    assert run["checkpoints"] == [] and m["summary"]["processing_runs"][0]["origin"] == "realtime"

    # SFF-834: the coverage of each stage, from the journal. m is the group time at the fold
    # (ADR-1P4N). No camera file is repaired, so the rows still hold it.
    assert all(f["state"] != "repaired" for f in take(folder / f"{case}.full.json")["files"])
    (group,) = run["sensor_groups"]
    frames = run["sensor_groups"][group]["sample_count"]
    times = {}
    for row in rows(parquet):
        if row["channel"] == "TIMESTAMPS" and row["name"] == "synchronized":
            times[row["frame_number"]] = round(row["value_f64"] * 10**9)
    for stage, provenance in run["processing"][group]["stage_provenance"]["stages"].items():
        # The stage `timing`: the records of each channel of the group, and the lowest latency of each frame.
        indexes = {i for i, c in enumerate(channels) if stage in ("timing", c["stage"])}
        keys = [key for key in values if key[0] in indexes]
        processed = len({frame for _, frame in keys})
        latency = {key: values[key][0] - times[key[1]] for key in keys}
        if stage == "timing":
            latencies = sorted(min(ns for (_, f), ns in latency.items() if f == frame) for frame in {f for _, f in keys})
        else:
            latencies = sorted(latency.values())
        k = len(latencies)
        assert provenance["origin"] == "realtime"
        assert provenance["coverage"] == {
            "frames_in_take": frames, "frames_processed": processed, "skips": {"no_record": frames - processed},
            "journal_crc_rejects": 1, "clean_close": False,
            "latency_ms": {
                "p50": latencies[math.ceil(0.5 * k) - 1] / 10**6 if k else None,
                "p99": latencies[math.ceil(0.99 * k) - 1] / 10**6 if k else None,
            },
            "events": [json.loads(p) for _, kind, p in scan(data)["good"] if kind == 3 and json.loads(p)["stage"] == stage],
        }  # fmt: skip
    stages = run["processing"][group]["stage_provenance"]["stages"]
    assert stages["observations"]["coverage"]["skips"]["no_record"] > 0
    # The hand values (G10_G13_G14_CHOICES.md items 12 and 44). The late record of frame 10 makes the
    # lowest latency of each frame differ from the latency of each record.
    assert stages["timing"]["coverage"]["frames_processed"] == 11
    assert (stages["timing"]["coverage"]["latency_ms"], stages["observations"]["coverage"]["latency_ms"]) == (
        {"p50": 26.5, "p99": 34.3}, {"p50": 26.5, "p99": 83.0},
    )  # fmt: skip

    # The rows of the fold: the journal values, null for NaN, and all null for a skipped frame (row rule 7).
    for row in rows(parquet):
        if row["channel"] != "OVERLAY_2D":
            continue
        channel = next(i for i, c in enumerate(channels) if c["reference_frame"] == row["reference_frame"])
        n, k = channels[channel]["names"].index(row["name"]), list(channels[channel]["components"]).index(row["component"])
        record = values.get((channel, row["frame_number"]))
        raw = record[1][n * len(channels[channel]["components"]) + k] if record else QNAN
        assert row["value"] == (None if raw == QNAN else struct.unpack("<f", raw)[0])


def test_g13_take_and_manifest():
    case = G13 / "take"
    m = manifest(case)
    rec = m["recording_name"]
    assert m["audio"] is None and m["calibration"] is None and len(m["cameras"]) == 2
    assert [(f["path"], f["role"], f["sha256"] is None) for f in m["files"]] == [
        (f"{rec}_data.parquet", "tracking", True), (f"{rec}_info.json", "capture_info", False),
        (f"{rec}_realtime_journal.bin", "realtime_journal", True), (f"{rec}_recording_info.json", "processing_info", False),
    ]  # SFF-723  # fmt: skip
    for camera in m["cameras"]:
        header, sidecar_rows, footer = read_sidecar(case / camera["timing"])
        assert header["audio_count"] == "0" and len(sidecar_rows) == 12 and footer[-1].startswith("# end ")
    full, player = take(G13 / "take.full.json"), take(G13 / "take.player.json")
    assert (full["warnings"], player["warnings"]) == (["realtime_run"], [])  # SFF-835, SFF-892
    assert {link["check"]: link["state"] for link in full["links"]}["calibration"] == "not_checked"
    # G10 `higher_minor_journal` is G13 with another journal: the same Parquet and a result with one more record.
    other = G10 / "higher_minor_journal"
    assert (other / f"{rec}_data.parquet").read_bytes() == (case / f"{rec}_data.parquet").read_bytes()
    for scope in ("full", "player"):
        a, b = load(G13 / f"take.{scope}.json"), load(G10 / f"higher_minor_journal.{scope}.json")
        for item in b["takes"][0]["folder_files"]:
            if item["path"].endswith(".bin") and scope == "full":
                item["records"] -= 1
        assert a == b


# ---------------------------------------------------------------- G14


def test_g14_toml_copies_and_library():
    cal, mocap = manifest(G14 / "calibration_take"), manifest(G14 / "mocap_take")
    assert (cal["purpose"], mocap["purpose"]) == ("calibration", "motion_capture")
    data = (G14 / "calibration_take" / cal["calibration"]["file"]).read_bytes()
    library = sorted(p.name for p in (G14 / "library").iterdir())
    assert library == sorted([f"{cal['recording_name']}_camera_calibration.toml", "last_successful_camera_calibration.toml"])
    assert all((G14 / "library" / name).read_bytes() == data for name in library)  # SFF-812, SFT-739
    assert (G14 / "mocap_take" / mocap["calibration"]["file"]).read_bytes() == data  # SFF-811
    metadata = tomllib.loads(data.decode())["metadata"]
    assert metadata["source_take_uuid"] == cal["take_uuid"] != mocap["take_uuid"]
    for m in (cal, mocap):
        assert m["calibration"] == {
            "calibration_uuid": metadata["calibration_uuid"], "file": f"{m['recording_name']}_camera_calibration.toml",
            "sha256": hashlib.sha256(data).hexdigest(),
        }  # fmt: skip
        assert m["summary"]["calibration"] == {"calibration_uuid": metadata["calibration_uuid"], "source_take_uuid": cal["take_uuid"]}
    assert [c["camera_key"] for c in cal["cameras"]] == [c["camera_key"] for c in mocap["cameras"]]
    assert not list(G14.glob("library.*.json")), "library/ is not a case"
    links = {link["check"]: link["state"] for link in take(G14 / "mocap_take.full.json")["links"]}
    assert links == dict.fromkeys(links, "ok") | {"dimensions": "not_checked"}  # SFF-872: no Parquet


def test_g14_charuco_run():
    """SFF-836: the Parquet of the calibration take has one run, with `TIMESTAMPS` rows and ChArUco rows."""
    case = G14 / "calibration_take"
    m = manifest(case)
    parquet = case / f"{m['recording_name']}_data.parquet"
    run = descriptor(parquet)["runs"]["0"]
    board = tomllib.loads((case / m["calibration"]["file"]).read_bytes().decode())["metadata"]["board"]
    source = f"charuco_detector:{board['squares_x']}x{board['squares_y']}"
    assert run["sources"][source] == {"kind": "tracker", "definition": board}
    corners = [f"corner_{i}" for i in range((board["squares_x"] - 1) * (board["squares_y"] - 1))]
    assert {(c["kind"], c["source"]) for c in run["channels"]} == {("TIMESTAMPS", f"camera:{c['camera_label']}") for c in m["cameras"]} | {
        ("TIMESTAMPS", f"timing:{next(iter(run['sensor_groups']))}"), ("OVERLAY_2D", source),
    }  # fmt: skip
    for channel in run["channels"]:
        if channel["kind"] == "OVERLAY_2D":
            assert channel["names"] == corners and channel["stage"] == "observations"
    undetected = [r for r in rows(parquet) if r["channel"] == "OVERLAY_2D" and r["component"] == "visibility" and r["value"] == 0]
    assert undetected, "a corner that the detector did not find (SFF-831)"


# ---------------------------------------------------------------- G10


def sidecars(case: Path) -> list[Path]:
    return sorted((case / "synchronized_videos").glob("*.csv"))


def test_g10_higher_minor():
    case, g03 = G10 / "higher_minor", GOLDEN / "G03" / "take"
    assert load(G10 / "higher_minor.full.json") == load(GOLDEN / "G03" / "take.full.json")  # SFF-709
    assert load(G10 / "higher_minor.player.json") == load(GOLDEN / "G03" / "take.player.json")
    flagged = 0
    for path in sidecars(case):
        header, sidecar_rows, _ = read_sidecar(path)
        assert header["format_version"] == "2.1" and list(header)[-1] == "x_future"
        column = next(line for line in path.read_text(encoding="utf-8").split("\n") if not line.startswith("#"))
        assert column.endswith(",x_future,crc32")
        old = read_sidecar(g03 / "synchronized_videos" / path.name)[1]
        flagged += sum(1 for r in sidecar_rows if r[4] == "128")
        assert [r[:4] + r[5:-1] for r in sidecar_rows] == [r[:4] + r[5:] for r in old]
    assert flagged == 1
    m = manifest(case)
    for path in ["recording_manifest.json"] + [item["path"] for item in m["files"] if item["path"].endswith(".json")]:
        data = json.loads((case / path).read_bytes())
        assert data["format_version"] == "2.1" and list(data)[-1] == "x_future"
        if path != "recording_manifest.json":
            assert next(i for i in m["files"] if i["path"] == path)["sha256"] == hashlib.sha256((case / path).read_bytes()).hexdigest()
    toml = tomllib.loads((case / m["calibration"]["file"]).read_bytes().decode())
    assert toml["metadata"]["format_version"] == "2.1" and "x_future" in toml["metadata"]
    assert sum("x_future" in table for key, table in toml.items() if key != "metadata") == 1
    assert descriptor(case / f"{m['recording_name']}_data.parquet")["format_version"] == "2.1"


def g01_differences(case: Path) -> set[str]:
    def sums(folder: Path, prefix: str) -> dict:
        lines = (folder / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
        return {n[len(prefix) :]: d for d, n in (line.split("  ", 1) for line in lines) if n.startswith(prefix)}

    g01, other = sums(GOLDEN / "G01", "take/"), sums(G10, f"{case.name}/")
    assert set(g01) == set(other)
    return {name for name in g01 if g01[name] != other[name]}


def test_g10_unknown_major():
    case = G10 / "unknown_major_sidecar"
    (changed,) = g01_differences(case)
    assert read_sidecar(case / changed)[0]["format_version"] == "3.0"
    item = next(f for f in take(G10 / "unknown_major_sidecar.full.json")["files"] if Path(f["name"]).with_suffix(".csv").as_posix() == changed)
    assert (item["state"], item["reason"], item["rows"], item["records"]) == ("unsupported_version", None, None, None)  # SFF-708

    case = G10 / "unknown_major_folder_file"
    m = manifest(case)
    assert g01_differences(case) == {"recording_manifest.json", f"{m['recording_name']}_info.json"}
    assert json.loads((case / m["files"][0]["path"]).read_bytes())["format_version"] == "3.0"
    for scope in ("full", "player"):
        (item,) = take(G10 / f"unknown_major_folder_file.{scope}.json")["folder_files"]
        assert (item["state"], item["reason"]) == ("unsupported_version", None)  # SFF-886


def test_g10_prerelease_0():
    case = G10 / "prerelease_0"
    m = manifest(case)
    assert m["format_prerelease"] == 0
    assert json.loads((case / m["files"][0]["path"]).read_bytes())["format_prerelease"] == 0
    assert all(read_sidecar(p)[0]["format_prerelease"] == "0" for p in sidecars(case))
    for scope in ("full", "player"):
        text = (G10 / f"prerelease_0.{scope}.json").read_text(encoding="utf-8")
        assert "prerelease" not in text  # SFF-891
        expected = (GOLDEN / "G01" / f"take.{scope}.json").read_text(encoding="utf-8")
        assert text == expected.replace(',"prerelease"', "").replace('"prerelease"', "")
