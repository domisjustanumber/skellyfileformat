"""Golden folder G13 (spec/SPEC.md Appendix A): a realtime take after the fold, in the case `take`.

The take is a small finished take with two cameras and no audio. It also holds the realtime journal
of freemocap and the Parquet run that the fold of that journal made. The journal has good records, a
record with a wrong CRC, a hole of 4 KiB of zeros and a torn tail. The take is in the state after the
fold and before the verified delete of the journal (SFF-845). golden/G10_G13_G14_CHOICES.md gives each
value that the spec does not give. G10 `higher_minor_journal` and G14 use the code of this module.
"""

from __future__ import annotations

import json
import struct
import zlib
from pathlib import Path

from goldgen import capture_cases, common, g03
from goldgen import folder_common as fc

TAKE = {
    "rec": "g13_synthetic_take",
    "take_uuid": "00000000000040008000000000000013",
    "take_start_host_ns": 1_000_000_000_000,
    "take_start_utc_ns": 946_684_800_000_000_000,  # 2000-01-01T00:00:00Z
    "utc_offset_min": 0,
    "clock": "windows_qpc",
    "clock_hz": 10_000_000,
}
FRAMES = 12
LATTICES = [(33_483_200, 33_333_400_000), (33_133_500, 33_333_250_000)]  # the lattices of G1
TRACKER = "keypoint_model:synthetic_pair"
NAMES = [f"{g03.TRACKER_STAGE}.{name}" for name in g03.PAIR["tracker_keypoint_names"]]
PIXEL, TIMESTAMP = {"x": "px", "y": "px", "visibility": "1"}, {"timestamp_s": "s"}

MAGIC, HEADER, DATA, EVENT = b"SKRJ", 1, 2, 3  # SPEC.md section 17
UNKNOWN_TYPE = 200  # G10 `higher_minor_journal`
QNAN = b"\x00\x00\xc0\x7f"  # SFF-841, SFF-845: a missing value
SKIPPED = {(1, 4), (0, 9), (1, 9)}  # (channel_index, frame) with no data record: the pipeline skipped it
REJECTED = (0, 6)  # the data record with a wrong CRC
HOLE_AFTER, HOLE_BYTES = 8, 4096  # the zero hole follows the records of this frame
TORN, TORN_BYTES = (1, FRAMES - 1), 20  # the last record, cut after 20 bytes
UNDETECTED = (0, 2, 1)  # (channel_index, frame, name index): x and y missing, visibility 0 (SFF-831)
EVENT_VALUE = {"time_ns": 150_000_000, "stage": "observations", "parameter": "min_visibility", "value": 0.5}
RECORDED_AT = {"timing": "2000-01-01T00:01:00Z", "observations": "2000-01-01T00:01:01Z"}


def cameras(frames: int = FRAMES) -> list[dict]:
    """Two cameras with the lattices of G1 and no gap. Camera 0 has a serial and driver times."""
    return [
        capture_cases.camera(index, [first + p for p in range(frames)], [(0, frames - 1, *LATTICES[index])], sample_ns=index == 0)
        for index, first in enumerate((1000, 500))
    ]


# ---------------------------------------------------------------- a run of TIMESTAMPS and OVERLAY_2D (also G14)


def overlay_run(files: list[dict], cameras: list[dict], tracker: str, definition: dict, names: list[str], value,
                models: dict, origin: str, calibration_camera: bool) -> tuple[dict, list[tuple], list[int]]:  # fmt: skip
    """Run 0 with the `TIMESTAMPS` channels (SFF-828) and one `OVERLAY_2D` channel for each camera.

    `value(c)` gives the value function of `folder_common.write_parquet` for camera c. The run has no
    3D: the take has no calibration (G13), or the run makes it (G14). The function returns the run,
    the items for `write_parquet` and the group time of each frame in ns. The caller sets `coverage`.
    """
    labels = [item["camera_label"] for item in files]
    group = fc.sensor_group_name([item["camera_key"] for item in files])
    strict = [fc.strict_ns([record[4] for record in item["records"]]) for item in files]
    group_ns = fc.group_ns(strict)
    camera_times = [[fc.seconds(s) for s in times] for times in strict]
    group_times = [fc.seconds(m) for m in group_ns]

    def channel(source, reference_frame, kind, channel_names, components, stage, dtype="float32") -> dict:
        return {
            "sensor_group": group, "source": source, "reference_frame": reference_frame, "kind": kind,
            "names": channel_names, "components": components, "stage": stage, "dtype": dtype,
        }  # fmt: skip

    items = [
        (channel(f"camera:{label}", None, "TIMESTAMPS", ["capture"], TIMESTAMP, "timing", "float64"), times, None)
        for label, times in zip(labels, camera_times)
    ]
    items.append(
        (channel(f"timing:{group}", None, "TIMESTAMPS", ["synchronized"], TIMESTAMP, "timing", "float64"), group_times, None)
    )
    items += [
        (channel(tracker, f"camera:{label}:image", "OVERLAY_2D", names, PIXEL, "observations"), camera_times[c], value(c))
        for c, label in enumerate(labels)
    ]
    # A `TIMESTAMPS` value is the `timestamp_s` of its row (row rule 6).
    rows = [(0, ch, times, v or (lambda frame, n, k, times=times: times[frame])) for ch, times, v in items]
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
    sources[tracker] = {"kind": "tracker", "definition": definition}
    reference_frames = {
        f"camera:{label}:image": {
            "camera_key": item["camera_key"], "calibration_camera": label if calibration_camera else None,
            "width": camera["width"], "height": camera["height"],
        }
        for label, item, camera in zip(labels, files, cameras)
    }  # fmt: skip
    stages = {
        stage: {
            "attempt_id": "goldgen-synthetic-attempt",
            "recorded_at": recorded_at,
            "effective_settings": {},
            "default_settings": None,
            "input_signatures": {"synthetic_input": "0" * 64},
            "software": {"python": "3.13.13", "packages": {}, "core_sha256": "0" * 64},
            "output_sources": list(dict.fromkeys(ch["source"] for ch in channels if ch["stage"] == stage)),
            "limitations": [],
            "base_run_id": None,
            "base_descriptor_signature": None,
            "origin": origin,
            "coverage": None,  # SFF-834: null for a posthoc run; the caller sets it for a realtime run
        }
        for stage, recorded_at in RECORDED_AT.items()
    }
    run = {
        "calibration_updates": {},
        "scale_fits": [],
        "camera_geometry": {},  # the run stores no geometry, so SFF-837 compares nothing
        "sensor_groups": {
            group: {
                "clock_description": "recording-relative seconds; timing method declared per source",
                "sample_count": len(group_times),
            }
        },
        "sources": sources,
        "reference_frames": reference_frames,
        "models": models,
        "processing": {group: {"stage_provenance": {"version": 1, "stages": stages}}},
        "channels": channels,
        "static_channels": [],
        "checkpoints": [],  # SFF-834: a realtime run has no checkpoints
    }
    return run, rows, group_ns


def descriptor(take: dict, run: dict) -> dict:
    return {
        "schema_version": 2, "format_version": common.FORMAT_VERSION, "format_prerelease": common.FORMAT_PRERELEASE,
        "writer": common.WRITER, "take_uuid": take["take_uuid"], "recording_id": take["rec"], "recording_info": {},
        "runs": {"0": run},
    }  # fmt: skip


# ---------------------------------------------------------------- the journal (section 17)


def record(kind: int, payload: bytes) -> bytes:
    """One framed record (SFF-840): magic, length, type, payload and the CRC-32 of type and payload."""
    body = bytes([kind]) + payload
    return MAGIC + struct.pack("<I", len(body)) + body + struct.pack("<I", zlib.crc32(body))


def json_payload(value: dict) -> bytes:
    return json.dumps(value, separators=(",", ":"), ensure_ascii=False).encode()


def values(c: int, frame: int) -> list[float | None]:
    """The n × k values of a data record, in name order, then component order. Each float32 is exact."""
    out = []
    for n in range(len(NAMES)):
        if (c, frame, n) == UNDETECTED:
            out += [None, None, 0.0]
        else:
            out += [(7 * frame + 11 * n + 5 * c) % 256 / 4, (3 * frame + 13 * n + 7 * c) % 192 / 4, (8 - n % 4) / 8]
    return out


def f32(value: float | None) -> bytes:
    return QNAN if value is None else struct.pack("<f", value)


def journal(channels: list[dict], group_ns: list[int], format_version: str, unknown_record: bool) -> dict:
    """The bytes of the journal and the facts of its scan (SFF-843) and of its check (SFF-845)."""
    header = {
        "skellyfileformat": "realtime_journal", "format_version": format_version,
        "format_prerelease": common.FORMAT_PRERELEASE, "writer": common.WRITER, "take_uuid": TAKE["take_uuid"],
        "origin": "realtime", "channels": [{"channel_index": i} | ch for i, ch in enumerate(channels)],
    }  # fmt: skip
    data, good, rejected, latencies, folded = b"", [], [], [], {}

    def add(chunk: bytes, is_good: bool = True) -> None:
        nonlocal data
        (good if is_good else rejected).append(len(data))
        data += chunk

    add(record(HEADER, json_payload(header)))
    add(record(EVENT, json_payload(EVENT_VALUE)))
    if unknown_record:  # SFF-709: a reader ignores the record type, and the record counts in `records`
        add(record(UNKNOWN_TYPE, b"x_future"))
    hole = torn = None
    for frame in range(len(group_ns)):
        for c in range(len(channels)):
            if (c, frame) in SKIPPED:
                continue
            processed_ns = group_ns[frame] + 20_000_000 + 1_300_000 * frame + 250_000 * c
            items = values(c, frame)
            chunk = record(DATA, struct.pack("<HiqII", c, frame, processed_ns, len(NAMES), len(PIXEL)) + b"".join(map(f32, items)))
            assert len(chunk) == 12 + 1 + 22 + 4 * len(items)  # SFF-840
            if (c, frame) == REJECTED:
                add(chunk[:-4] + struct.pack("<I", struct.unpack("<I", chunk[-4:])[0] ^ 1), is_good=False)
            elif (c, frame) == TORN:
                torn = len(data)
                data += chunk[:TORN_BYTES]
            else:
                add(chunk)
                folded[c, frame] = items
                latencies.append(processed_ns - group_ns[frame])  # SFF-834
        if frame == HOLE_AFTER:
            hole = len(data)
            data += bytes(HOLE_BYTES)
    assert data.count(MAGIC) == len(good) + len(rejected) + 1, "no `magic` inside a record"
    # SFF-845: each channel in order of `channel_index`, each frame in order, the values of the record.
    digest = b"".join(f32(v) for key in sorted(folded) for v in folded[key])
    return {
        "bytes": data, "folded": folded, "latencies": sorted(latencies),
        "counts": {"records": len(good), "rejected_records": len(rejected), "torn_bytes": len(data) - torn},
        "truth": {
            "good_offsets": good, "rejected_offsets": rejected, "hole": [hole, HOLE_BYTES], "torn_tail": torn,
            "check_count": len(digest) // 4, "check_digest": common.sha256_hex(digest),
        },
    }  # fmt: skip


def coverage(channels: list[dict], stage: str, frames: int, scan: dict) -> dict:
    """The `coverage` of SFF-834 for the one sensor group and one stage."""
    indexes = {i for i, ch in enumerate(channels) if ch["stage"] == stage}
    processed = len({frame for c, frame in scan["folded"] if c in indexes})
    latencies = scan["latencies"] if indexes else []
    k = len(latencies)
    return {
        "frames_in_take": frames,
        "frames_processed": processed,
        "skips": {"no_record": frames - processed},
        "journal_crc_rejects": scan["counts"]["rejected_records"],
        "clean_close": False,  # the journal has no end record
        "latency_ms": {  # nearest rank, counted from 1; null when k is 0
            "p50": latencies[(k + 1) // 2 - 1] / 10**6 if k else None,
            "p99": latencies[(99 * k + 99) // 100 - 1] / 10**6 if k else None,
        },
        "events": [EVENT_VALUE] if EVENT_VALUE["stage"] == stage else [],
    }


# ---------------------------------------------------------------- the case


def write_case(folder: Path, journal_version: str | None = None, unknown_record: bool = False) -> dict:
    """Write the take of G13 into `folder`. Return the facts for `expected_result` and the truth."""
    rec = TAKE["rec"]
    take_cameras = cameras()
    files, facts = capture_cases.finished_take(TAKE, take_cameras, None)
    capture_cases.write_files(folder, files)
    camera_files = facts["files"]

    folded: dict = {}  # filled by `journal` below, before `write_parquet` calls the value functions

    def value(c: int):
        def get(frame: int, n: int, k: int) -> float | None:
            items = folded.get((c, frame))
            return None if items is None else items[n * len(PIXEL) + k]  # a skipped frame: all null (SFF-834)

        return get

    models = {"pair": g03.recorded_model(g03.PAIR, [])}
    run, rows, group_ns = overlay_run(camera_files, take_cameras, TRACKER, {}, NAMES, value, models, "realtime", False)
    overlay = [ch for ch in run["channels"] if ch["kind"] == "OVERLAY_2D"]
    scan = journal(overlay, group_ns, journal_version or common.FORMAT_VERSION, unknown_record)
    folded |= scan["folded"]
    (group,) = run["processing"].values()
    for stage, provenance in group["stage_provenance"]["stages"].items():
        provenance["coverage"] = coverage(overlay, stage, FRAMES, scan)

    journal_path, parquet_path, info_path = f"{rec}_realtime_journal.bin", f"{rec}_data.parquet", f"{rec}_recording_info.json"
    (folder / journal_path).write_bytes(scan["bytes"])
    d = descriptor(TAKE, run)
    fc.write_parquet(folder / parquet_path, d, rows)
    info = fc.processing_info(d, (folder / parquet_path).read_bytes(), 0)
    (folder / info_path).write_bytes(info)

    manifest_path = folder / capture_cases.MANIFEST
    manifest = json.loads(manifest_path.read_bytes())
    manifest["files"] += [
        {"path": journal_path, "role": "realtime_journal", "owner": "freemocap", "sha256": None},  # SFF-723
        {"path": parquet_path, "role": "tracking", "owner": "freemocap", "sha256": None},
        {"path": info_path, "role": "processing_info", "owner": "freemocap", "sha256": common.sha256_hex(info)},
    ]
    manifest["files"].sort(key=lambda item: item["path"].encode())
    # SFF-728: one run with the origin `realtime`, and its latest `recorded_at`.
    manifest["summary"]["processing_runs"] = [{"run_id": 0, "origin": "realtime", "recorded_at": max(RECORDED_AT.values())}]
    manifest_path.write_bytes(common.file_json(manifest))

    facts["folder_files"] = [(item["path"], item["role"]) for item in manifest["files"]]
    return facts | {"journal": journal_path, "journal_counts": scan["counts"], "truth": {"journal": {"name": journal_path} | scan["truth"]}}


def expected_result(facts: dict, scope: str) -> dict:
    """The reader result of the take of `write_case` (SFF-885). G10_G13_G14_CHOICES.md gives each requirement."""
    result = fc.expected_result(facts, scope)
    (take,) = result["takes"]
    for item in take["folder_files"]:
        if item["path"] == facts["journal"]:
            if scope == "full":  # SFF-843, SFF-886: a rejected record and a torn tail give `damaged`
                item |= {"state": "damaged", "reason": "crc_mismatch"} | facts["journal_counts"]
            else:  # SFF-892
                item |= dict.fromkeys(facts["journal_counts"])
    for link in take["links"]:
        if link["check"] == "calibration":  # SFF-872: the take has no TOML and no manifest calibration
            link["state"] = "not_checked"
    take["warnings"] = ["realtime_run"] if scope == "full" else []  # SFF-835, SFF-892
    return result


def write_results(out: Path, case: str, facts: dict) -> None:
    for scope in ("full", "player"):
        (out / f"{case}.{scope}.json").write_bytes(common.canonical_json(expected_result(facts, scope)))
    (out / f"{case}.truth.json").write_bytes(common.canonical_json(facts["truth"]))


def build(out: Path) -> None:
    """Write the case `take` of G13 into `out`, with its two expected results and its truth file."""
    write_results(out, "take", write_case(out / "take"))
