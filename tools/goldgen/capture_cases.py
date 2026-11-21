"""Shared code of the golden folders G2, G4, G5, G6, G11 and G12 (spec/SPEC.md Appendix A).

`common.write_take` writes only a finished take with mono audio and one fit segment for each file.
This module makes each device pair in memory, with the bytes of its media file before and after the
muxer closes it. So a folder module can also write the files of a crash, of a repair or of a fit
vector. For the input of G1, `finished_take` gives the bytes of `common.write_take`: a test checks it.

Each expected reader result comes from the input of the generator and from the rules of SPEC.md
section 23, not from a read of the files. golden/CAPTURE_VECTORS_CHOICES.md gives the requirement of
each value.
"""

from __future__ import annotations

import datetime
import io
import struct
from fractions import Fraction
from pathlib import Path

from goldgen import common
from goldgen.g01 import _device

GAP, ENCODE_SKIP, REPEAT, MISSING = 1, 4, 8, 16  # SFF-756
VIDEO_COLUMNS = ["frame", "source_frame_number", "arrival_ns", "sample_ns", "flags", "byte_offset", "byte_size"]
AUDIO_COLUMNS = ["block", "first_sample", "n_samples", "host_ns", "adc_ns", "flags"]
MANIFEST = "recording_manifest.json"

# ---------------------------------------------------------------- media, through a sink in memory


def mux_mkv(jpegs: list[bytes], rate: Fraction, width: int, height: int) -> tuple[bytes, bytes]:
    """The bytes of a camera file before and after the muxer closes it. `common.build_mkv` gives the second."""
    import av

    sink = io.BytesIO()
    # flush_packets makes the muxer give each complete Cluster to the sink at once. It changes no byte.
    options = {"fflags": "+bitexact", "flush_packets": "1"}
    container = av.open(sink, "w", format="matroska", options=options)
    stream = container.add_stream("mjpeg", rate=rate)
    stream.width, stream.height, stream.pix_fmt = width, height, "yuvj420p"
    stream.time_base = Fraction(1, 1000)
    for position, jpeg in enumerate(jpegs):
        packet = av.Packet(jpeg)
        packet.stream = stream
        packet.time_base = Fraction(1, 1000)
        packet.pts = packet.dts = common.container_ms(position, rate)
        packet.is_keyframe = True
        container.mux(packet)
    before = sink.getvalue()
    container.close()
    return before, sink.getvalue()


def mux_opus(pcm: bytes, channels: int) -> tuple[bytes, bytes]:
    """The bytes of an audio file (section 9) before and after the muxer closes it. `pcm` is interleaved s16."""
    import av

    sink = io.BytesIO()
    options = {
        "movflags": "empty_moov+default_base_moof", "frag_duration": "1000000", "fflags": "+bitexact",
        "flush_packets": "1",
    }  # fmt: skip
    container = av.open(sink, "w", format="mp4", options=options)
    layout = {1: "mono", 2: "stereo"}[channels]
    stream = container.add_stream("libopus", rate=48000, layout=layout)
    stream.codec_context.options = {
        "b": str(128000 * channels), "application": "audio", "vbr": "on", "compression_level": "10",
        "frame_duration": "20",
    }  # fmt: skip  SFF-762
    stream.time_base = Fraction(1, 48000)
    width = 2 * channels
    for first in range(0, len(pcm) // width, 960):
        block = pcm[width * first : width * (first + 960)]
        frame = av.AudioFrame(format="s16", layout=layout, samples=len(block) // width)
        frame.planes[0].update(block)
        frame.sample_rate, frame.pts, frame.time_base = 48000, first, Fraction(1, 48000)
        container.mux(stream.encode(frame))
    before = sink.getvalue()
    container.mux(stream.encode(None))
    container.close()
    return before, sink.getvalue()


def complete_blocks(data: bytes) -> list[tuple[int, int]]:
    """The payload (offset, size) of each SimpleBlock that is whole, by a walk (SFF-740). The file can be cut."""

    def children(start: int, end: int):
        try:
            yield from common.ebml_children(data, start, min(end, len(data)))
        except IndexError:  # the cut is in the header of an element
            return

    blocks = []
    for top_id, top_at, top_size in children(0, len(data)):
        if top_id != common.SEGMENT:
            continue
        for element_id, at, size in children(top_at, top_at + top_size):
            if element_id != common.CLUSTER:
                continue
            for block_id, block_at, block_size in children(at, at + size):
                if block_id == common.SIMPLE_BLOCK and block_at + block_size <= len(data):
                    # The block header has 4 bytes: a track number below 128 is 1 byte (SFF-732, SFF-739).
                    blocks.append((block_at + 4, block_size - 4))
    return blocks


def complete_fragments(data: bytes) -> list[tuple[int, int]]:
    """The (start, end) of each fragment whose `moof` and `mdat` are whole (SFF-792). The file can be cut."""
    at, moof, fragments = 0, None, []
    while at + 8 <= len(data):
        size, kind = struct.unpack(">I4s", data[at : at + 8])
        if at + size > len(data):
            break
        if kind == b"moof":
            moof = at
        elif kind == b"mdat" and moof is not None:
            fragments.append((moof, at + size))
            moof = None
        at += size
    return fragments


def _boxes(data: bytes, start: int, end: int):
    """(kind, payload start, end) of each box from `start` to `end`."""
    while start + 8 <= end:
        size, kind = struct.unpack(">I4s", data[start : start + 8])
        yield kind, start + 8, start + size
        start += size


def _box(data: bytes, start: int, end: int, *path: bytes) -> tuple[int, int]:
    for kind in path:
        start, end = next((at, stop) for k, at, stop in _boxes(data, start, end) if k == kind)
    return start, end


def held_samples(data: bytes) -> int:
    """The samples that an audio file holds: the samples of its complete fragments, minus the pre-skip (SFF-785)."""
    stsd, stsd_end = _box(data, 0, len(data), b"moov", b"trak", b"mdia", b"minf", b"stbl", b"stsd")
    entry = stsd + 8  # after the version, the flags and the entry count of `stsd`
    # The `Opus` sample entry has a box header of 8 bytes and 28 bytes of audio sample entry fields.
    dops, _ = _box(data, entry + 36, stsd_end, b"dOps")
    pre_skip = struct.unpack(">H", data[dops + 2 : dops + 4])[0]
    samples = 0
    for moof, end in complete_fragments(data):
        traf = _box(data, moof + 8, end, b"traf")
        tfhd, _ = _box(data, *traf, b"tfhd")
        trun, _ = _box(data, *traf, b"trun")
        flags = int.from_bytes(data[tfhd + 1 : tfhd + 4], "big")
        assert flags & 0x08 and not int.from_bytes(data[trun + 1 : trun + 4], "big") & 0x100, "one default duration"
        duration_at = tfhd + 8 + 8 * (flags & 0x01) + 4 * bool(flags & 0x02)
        samples += int.from_bytes(data[trun + 4 : trun + 8], "big") * int.from_bytes(data[duration_at : duration_at + 4], "big")
    return samples - pre_skip


def whole_blocks(rows: list[list], held: int) -> int:
    """The number of first rows whose every sample is in the samples that the file holds (SFF-792).

    `file_sample_offset` is 0, so sample n of a row is decoded sample n: the sample after the pre-skip
    and n more (SFF-766). A block that is only partly in the complete fragments is not usable.
    """
    return next((count for count, row in enumerate(rows) if row[1] + row[2] > held), len(rows))


# ---------------------------------------------------------------- fit (section 11)


def video_fitted(rows: list[list], segments: list[tuple]) -> list[int]:
    """SFF-777 for each position of the segments (pos_first, pos_last, t0_ns, period_ps). A row is [p, source, ...]."""
    times = []
    for first, last, t0_ns, period_ps in segments:
        for p in range(first, last + 1):
            both = rows[p][1] is not None and rows[first][1] is not None
            times.append(common.video_fitted_ns(t0_ns, period_ps, rows[p][1] - rows[first][1] if both else p - first))
    return times


def reader_audio_fit(rows: list[list]) -> tuple | None:
    """The one segment (row_first, row_last, n0, t0_ns, period_fs) that a reader computes from the rows (SFF-784)."""
    if len(rows) < 2:
        return None
    a, b = rows[0], rows[-1]
    t_a, t_b = (row[4] if row[4] is not None else row[3] for row in (a, b))
    period_fs = (t_b - t_a) * 10**6 // (b[1] - a[1])
    return (a[0], b[0], a[1], t_a, period_fs) if period_fs > 0 else None


def fit_lines(kind: str, segments: list[tuple]) -> list[str]:
    """The `# fit` line and the segment lines of a footer (SFF-775). No segment gives no line."""
    if kind == "camera":
        form = "# fit_segment pos_first={} pos_last={} t0_ns={} period_ps={}"
    else:
        form = "# fit_segment row_first={} row_last={} n0={} t0_ns={} period_fs={}"
    return [common.fit_line()] * bool(segments) + [form.format(*segment) for segment in segments]


def end_line(kind: str, rows: list[list]) -> str:
    """The `# end` line for these rows (SFF-758, SFF-769). The generator writes no `filled` and no `silence` row."""
    if kind == "camera":
        gaps, missing, skips = (sum(1 for row in rows if row[4] & bit) for bit in (GAP, MISSING, ENCODE_SKIP))
        return f"# end rows={len(rows)} gaps={gaps} filled=0 missing={missing} encode_skips={skips}"
    return f"# end rows={len(rows)} samples={sum(row[2] for row in rows)} gaps=0 silence_samples=0"


# ---------------------------------------------------------------- synthetic cameras and device pairs


def camera(index: int, sources: list[int], lattice: list[tuple], *, rate=(30, 1), sample_ns=False, **members) -> dict:
    """A synthetic camera, in the form of `goldgen.g01`. Its frames are on the lines of `lattice`.

    `lattice` holds (pos_first, pos_last, t0_ns, period_ps). It is also the fit, when `members` gives
    no `segments`. A camera with an even index has a serial and a user name, as camera 0 of G1.
    """
    letter = "ABCD"[index]
    serial = f"FAKE-SERIAL-{letter}" if index % 2 == 0 else None
    device = _device(index, serial, None if serial else f"FAKE-OS-DEVICE-{index}")
    identity = f"serial:{serial}" if serial else f"port:{device['port_path']}"
    fitted = video_fitted([[p, source] for p, source in enumerate(sources)], lattice)
    assert rate[1] == 1
    return {
        "camera_key": common.camera_key(f"ffff:{device['product_id']}:{identity}"),
        "user_name": f"Fake camera {letter}" if serial else None,
        "key_origin": "computed",
        "device": device,
        "requested": {
            "width": 64, "height": 48, "framerate": rate[0], "capture_format": "MJPG", "exposure_mode": "manual",
        },
        "controls": (
            {"exposure_us": {"value": 4000, "auto": False}, "gain": {"value": 32, "auto": False}}
            if serial
            else {"exposure_us": {"value": None, "auto": None}}
        ),
        "exposure_step": None,
        "rate": rate, "width": 64, "height": 48, "display_rotation": 0, "shade": 40 * index, "flash_positions": [],
        "segments": lattice,
        "rows": [
            # The frame arrives 4 ms to 5 ms after its fitted time, as in G1.
            (source, t + 4_000_000 + p * 104_729 % 1_000_003, t + p * 7_919 % 100_001 - 50_000 if sample_ns else None)
            for p, (source, t) in enumerate(zip(sources, fitted))
        ],
    } | members  # fmt: skip


def _video_pair(take: dict, group_size: int, audio_count: int, position: int, camera: dict, label: str) -> dict:
    stem = f"{common.MEDIA_FOLDER}/{take['rec']}.{label}"
    rate = Fraction(*camera["rate"])
    count = len(camera["rows"])
    jpegs = camera.get("jpegs") or [
        common.jpeg_frame(camera["width"], camera["height"], p, camera["shade"], p in camera["flash_positions"])
        for p in range(count)
    ]
    before, after = mux_mkv(jpegs, rate, camera["width"], camera["height"])
    payloads = complete_blocks(after)
    assert [size for _, size in payloads] == [len(j) for j in jpegs]
    assert payloads[: len(complete_blocks(before))] == complete_blocks(before), "SFF-757: the close moves no block"

    rows = []
    for p, (source, arrival_ns, sample_ns) in enumerate(camera["rows"]):
        earlier = camera["rows"][p - 1][0] if p else None
        known = source is not None and earlier is not None
        flags = camera.get("flags", {}).get(p, 0)
        flags |= GAP * int(known and source not in (earlier, earlier + 1)) | REPEAT * int(known and source == earlier)
        rows.append([p, source, arrival_ns, sample_ns, flags, *payloads[p]])
    header = common.take_header("video_timing", take, group_size, audio_count) | {
        "group_position": position,
        "camera_key": camera["camera_key"],
        "camera_label": label,
        "nominal_rate": f"{rate.numerator}/{rate.denominator}",
        "display_rotation": camera["display_rotation"],
    }
    return {
        "kind": "camera", "name": stem + ".mkv", "timing": stem + ".csv", "camera_key": camera["camera_key"],
        "camera_label": label, "head": common.sidecar(header, VIDEO_COLUMNS, [], []), "rows": rows,
        "lines": [common.csv_row(row).encode() for row in rows],
        "segments": camera.get("segments", [(0, count - 1, camera.get("t0_ns"), camera.get("period_ps"))]),
        "before": before, "after": after,
    }  # fmt: skip


def _audio_pair(take: dict, group_size: int, audio: dict) -> dict:
    stem = f"{common.MEDIA_FOLDER}/{take['rec']}.audio"
    channels = audio.get("channels", 1)
    rows = [[b, first, n, host_ns, adc_ns, 0] for b, (first, n, host_ns, adc_ns) in enumerate(audio["rows"])]
    pcm = audio.get("pcm") or common.click_pcm(sum(row[2] for row in rows), audio["click_samples"])
    assert len(pcm) == 2 * channels * sum(row[2] for row in rows)
    before, after = mux_opus(pcm, channels)
    header = common.take_header("audio_timing", take, group_size, 1) | {
        "sample_rate": 48000,
        "channels": channels,
        "codec": "opus",
        "file_sample_offset": 0,
        "audio_latency_ns": None,
    }
    return {
        "kind": "audio", "name": stem + ".m4a", "timing": stem + ".csv", "camera_key": None, "camera_label": None,
        "head": common.sidecar(header, AUDIO_COLUMNS, [], []), "rows": rows,
        "lines": [common.csv_row(row).encode() for row in rows], "channels": channels,
        "segments": [(0, len(rows) - 1, 0, audio["t0_ns"], audio["period_fs"])],
        "before": before, "after": after,
    }  # fmt: skip


def device_pairs(take: dict, cameras: list[dict], audio: dict | None) -> list[dict]:
    """The device pairs of a take: each camera in order of `group_position`, then the audio."""
    labels = [camera["camera_key"][:6] for camera in cameras]
    assert len(set(labels)) == len(labels), "SFF-720: this generator has no label longer than 6 characters"
    pairs = [
        _video_pair(take, len(cameras), int(audio is not None), position, camera, label)
        for position, (camera, label) in enumerate(zip(cameras, labels))
    ]
    return pairs + ([_audio_pair(take, len(cameras), audio)] if audio else [])


def finished_sidecar(pair: dict) -> bytes:
    footer = [*fit_lines(pair["kind"], pair["segments"]), end_line(pair["kind"], pair["rows"])]
    return pair["head"] + b"".join(pair["lines"]) + "".join(line + "\n" for line in footer).encode()


# ---------------------------------------------------------------- the reader result (section 23)


def item(
    pair: dict, state: str, n_rows: int, segments: list[tuple] | None, *, complete: int | None = None,
    torn_bytes: int = 0, reason: str | None = None,
) -> dict:  # fmt: skip
    """The `files` item of a pair that a reader does not refuse (SFF-885).

    `n_rows` is the number of rows that SFF-746 lets the reader use. `segments` holds the fit lines
    that the reader uses, or nothing when it uses none (SFF-747). `complete` is the number of complete
    blocks of a camera file that its muxer did not close (SFF-740), or the number of blocks of an
    unfinished audio file whose every sample is in a complete fragment (SFF-792).
    """
    rows = pair["rows"][:n_rows]
    if pair["kind"] == "camera":
        # SFF-781: the fitted time, or the arrival time for each frame of the file. A row with no
        # `arrival_ns` has no player time.
        times = video_fitted(rows, segments) if segments else [row[2] for row in rows]
        records = [[*row[:4], times[p] if row[2] is not None else None] for p, row in enumerate(rows)]
    else:
        fit = segments or [s for s in [reader_audio_fit(rows)] if s]  # SFF-784
        records = [
            [*row[:4], common.audio_fitted_ns(t0_ns, period_fs, n0, row[1])]
            for first, last, n0, t0_ns, period_fs in fit
            for row in rows[first : last + 1]
        ] or [[*row[:4], None] for row in rows]
    records = records[: n_rows if complete is None else min(n_rows, complete)]  # SFF-740, SFF-792
    warnings = {"prerelease"}  # SFF-891
    if pair["kind"] == "camera":  # SFF-887: a usable row with the flag
        warnings |= {name for name, bit in (("gap", GAP), ("encode_skip", ENCODE_SKIP)) if any(r[4] & bit for r in rows)}
    if not segments:
        warnings.add("missing_fit")  # SFF-781, SFF-784
    return {
        "name": pair["name"], "kind": pair["kind"], "state": state, "reason": reason,
        "camera_key": pair["camera_key"], "camera_label": pair["camera_label"], "rows": n_rows,
        "torn_bytes": torn_bytes, "fit": bool(segments), "warnings": sorted(warnings), "records": records,
    }  # fmt: skip


def expected_result(facts: dict, scope: str, folder_warnings: tuple = ()) -> dict:
    """`common.expected_result`, for a take whose files can have each state.

    In each take of this module, the files exist, the manifest is the manifest of the take and the take
    keys agree. So only the row-count part of `frames` and the folder warnings differ from G1.
    """
    result = common.expected_result(facts, scope)
    result["folder_warnings"] = sorted(folder_warnings)
    finished = [f["rows"] for f in facts["files"] if f["kind"] == "camera" and f["state"] == "finished"]
    assert len(set(finished)) <= 1, "SFF-754"
    if len(finished) < 2:  # SFF-872: the reader does not evaluate the part, and the take has no Parquet
        frames = result["takes"][0]["links"][common.LINK_CHECKS.index("frames")]
        frames["state"] = "not_checked"
    return result


# ---------------------------------------------------------------- folder files and output


def folder_files(
    take: dict, cameras: list[dict], pairs: list[dict], audio: dict | None, kept: list[int] | None,
    warnings: tuple = (),
) -> dict:  # fmt: skip
    """The capture info JSON (section 13) and the manifest (section 5), as {path: bytes}.

    `kept` is None for the manifest of the take start, with `state` `recording` (SFF-724, SFF-728).
    Else it gives, for each pair, the number of rows of its finished or repaired sidecar. `warnings`
    holds more manifest warnings, after the warnings `camera_gap` (SFF-727).
    """
    rec = take["rec"]
    info_path = f"{rec}_info.json"
    config_members = ("user_name", "key_origin", "device", "requested", "controls", "exposure_step")
    info = common.file_json(
        {
            "skellyfileformat": "capture_info",
            "format_version": common.FORMAT_VERSION,
            "format_prerelease": common.FORMAT_PRERELEASE,
            "writer": common.WRITER,
            "take_uuid": take["take_uuid"],
            "camera_configs": {
                pair["camera_key"]: {"camera_label": pair["camera_label"]} | {m: camera[m] for m in config_members}
                for camera, pair in zip(cameras, pairs)
            },
            "audio": audio["config"] if audio else None,
        }
    )
    device_kinds = {
        "model": "device_name", "os_name": "device_name", "serial": "serial_number",
        "port_path": "device_path", "os_device_id": "device_path",
    }  # fmt: skip
    privacy = [(MANIFEST, "/recording_name", "user_entered_name")]
    privacy += [(pair["timing"], "utc_offset_min", "time_zone") for pair in pairs]
    if audio:
        privacy.append((info_path, "/audio/device_name", "device_name"))
    summary_cameras, gap_warnings, last_arrival_ns = [], [], []
    for position, (camera, pair) in enumerate(zip(cameras, pairs)):
        rows = pair["rows"][: kept[position]] if kept else []
        rate = Fraction(*camera["rate"])
        exposure = camera["controls"].get("exposure_us")
        summary_cameras.append(
            {
                "camera_label": pair["camera_label"],
                "user_name": camera["user_name"],
                "model": camera["device"]["model"],
                "stored_px": f"{camera['width']}x{camera['height']}" if kept else None,
                "display_rotation": camera["display_rotation"],
                "nominal_fps": common.thousandths((2000 * rate.numerator + rate.denominator) // (2 * rate.denominator)),
                "gaps": sum(1 for row in rows if row[4] & GAP) if kept else None,
                "filled": 0 if kept else None,
                "missing": sum(1 for row in rows if row[4] & MISSING) if kept else None,
                "exposure_us": exposure["value"] if exposure else None,
            }
        )
        if kept:  # SFF-728: the last row that holds an `arrival_ns`
            last_arrival_ns += [next(row[2] for row in reversed(rows) if row[2] is not None)]
            if summary_cameras[-1]["gaps"]:
                gap_warnings.append(
                    {"code": "camera_gap", "source": "skellycam", "camera_key": pair["camera_key"], "detail": None}
                )
        base = f"/camera_configs/{pair['camera_key']}"
        privacy.append((MANIFEST, f"/summary/cameras/{position}/model", "device_name"))
        if camera["user_name"] is not None:
            privacy.append((MANIFEST, f"/summary/cameras/{position}/user_name", "user_entered_name"))
            privacy.append((info_path, f"{base}/user_name", "user_entered_name"))
        privacy += [
            (info_path, f"{base}/device/{member}", kind)
            for member, kind in device_kinds.items()
            if camera["device"][member] is not None
        ]
    audio_pair = pairs[-1] if audio else None
    samples = sum(row[2] for row in audio_pair["rows"][: kept[-1]]) if audio and kept else None
    utc_s = take["take_start_utc_ns"] // 10**9
    manifest = {
        "skellyfileformat": "recording_manifest",
        "format_version": common.FORMAT_VERSION,
        "format_prerelease": common.FORMAT_PRERELEASE,
        "writer": common.WRITER,
        "take_uuid": take["take_uuid"],
        "recording_name": rec,
        "purpose": "motion_capture",
        "state": "finished" if kept else "recording",
        "cameras": [
            {
                "camera_key": pair["camera_key"], "camera_label": pair["camera_label"], "group_position": position,
                "video": pair["name"], "timing": pair["timing"], "calibration_camera": None,
            }
            for position, pair in enumerate(pairs[: len(cameras)])
        ],  # fmt: skip
        "audio": {"audio": audio_pair["name"], "timing": audio_pair["timing"]} if audio else None,
        "calibration": None,
        "files": [
            {"path": info_path, "role": "capture_info", "owner": "skellycam", "sha256": common.sha256_hex(info)}
        ],
        "warnings": gap_warnings + list(warnings),
        "privacy": {
            "fields": [
                {"file": file, "field": field, "kind": kind}
                for file, field, kind in sorted(privacy, key=lambda entry: (entry[0].encode(), entry[1].encode()))
            ],
            "media_shows_people": True,
        },
        "summary": {
            "take_start_utc": datetime.datetime.fromtimestamp(utc_s, datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "duration_s": common.thousandths((max(last_arrival_ns) + 500_000) // 10**6) if kept else None,
            "cameras": summary_cameras,
            "audio": {
                "file": audio_pair["name"],
                "sample_rate": 48000,
                "channels": audio_pair["channels"],
                "duration_s": common.thousandths((2000 * samples + 48000) // (2 * 48000)) if kept else None,
            }
            if audio
            else None,
            "calibration": None,
            "processing_runs": [],
            "warnings": sorted({warning["code"] for warning in gap_warnings + list(warnings)}),
        },
    }
    return {info_path: info, MANIFEST: common.file_json(manifest)}


def take_facts(take: dict, items: list[dict]) -> dict:
    return {
        "take_uuid": take["take_uuid"], "recording_name": take["rec"], "files": items,
        "info_path": f"{take['rec']}_info.json",
    }  # fmt: skip


def finished_take(take: dict, cameras: list[dict], audio: dict | None) -> tuple[dict, dict]:
    """A finished capture-only take: its files as {path: bytes}, and the facts for `expected_result`."""
    pairs = device_pairs(take, cameras, audio)
    files = folder_files(take, cameras, pairs, audio, [len(pair["rows"]) for pair in pairs])
    for pair in pairs:
        files |= {pair["name"]: pair["after"], pair["timing"]: finished_sidecar(pair)}
    items = [item(pair, "finished", len(pair["rows"]), pair["segments"]) for pair in pairs]
    return files, take_facts(take, items)


def write_files(folder: Path, files: dict) -> None:
    for path, data in files.items():
        (folder / path).parent.mkdir(parents=True, exist_ok=True)
        (folder / path).write_bytes(data)


def write_results(out: Path, case: str, facts: dict, folder_warnings: tuple = (), truth: dict | None = None) -> None:
    """Write the two expected results of a case and, when given, its truth file (golden/README.md)."""
    for scope in ("full", "player"):
        result = expected_result(facts, scope, folder_warnings)
        (out / f"{case}.{scope}.json").write_bytes(common.canonical_json(result))
    if truth is not None:
        (out / f"{case}.truth.json").write_bytes(common.canonical_json(truth))
