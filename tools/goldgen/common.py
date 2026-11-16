"""Shared code of the golden generator (decision G21H item 9).

The generator writes the golden folders of spec/SPEC.md Appendix A from synthetic input. This module
holds the parts that more than one golden folder uses. It is not the reader and not the writer of the
package: it writes each file directly from the text of the spec, and it derives each expected reader
result from its own input, not from a read of the files.

The media builders need the dependency group ``golden``. Each other function needs only the standard
library.
"""

from __future__ import annotations

import datetime
import hashlib
import json
import zlib
from fractions import Fraction
from pathlib import Path

FORMAT_VERSION = "2.0"
FORMAT_PRERELEASE = 1  # SFF-710
WRITER = "skellyfileformat-goldgen 1.0.0"
FITTER = "goldgen-truth"
FITTER_VERSION = "1.0.0"
MEDIA_FOLDER = "synchronized_videos"
LINK_CHECKS = (  # the order of the table of SFF-872
    "take_uuid", "camera_key", "frames", "dimensions", "rotation", "files", "hashes", "calibration",
)  # fmt: skip

# ---------------------------------------------------------------- JSON and sums


def canonical_json(value: object) -> bytes:
    """The RFC 8785 form of a value that holds no float, no integer of 2^53 or more and only ASCII keys.

    Under these limits, sorted compact ``json.dumps`` gives the bytes of RFC 8785: the two differ only
    in the number form of a float and in the sort order of keys outside the Basic Multilingual Plane.
    """

    def check(v: object) -> None:
        if isinstance(v, dict):
            for key, item in v.items():
                assert isinstance(key, str) and key.isascii(), key
                check(item)
        elif isinstance(v, list):
            for item in v:
                check(item)
        elif isinstance(v, int) and not isinstance(v, bool):
            assert abs(v) < 2**53, v
        else:
            assert v is None or isinstance(v, (str, bool)), repr(v)

    check(value)
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def file_json(value: dict) -> bytes:
    """A JSON file of the take folder (SFF-700, SFF-702): the members stay in the order given."""
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()


def thousandths(n: int) -> int | float:
    """n / 1000 as the JSON number of SFF-728: an integer when it has no fraction."""
    return n // 1000 if n % 1000 == 0 else n / 1000


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sums_text(folder: Path) -> str:
    """The text of ``SHA256SUMS``: one line for each file below ``folder``, in order of the path bytes."""
    paths = sorted(
        (p.relative_to(folder).as_posix().encode(), p)
        for p in folder.rglob("*")
        if p.is_file() and p.name != "SHA256SUMS"
    )
    return "".join(f"{sha256_hex(p.read_bytes())}  {rel.decode()}\n" for rel, p in paths)


# ---------------------------------------------------------------- timing sidecars (sections 7, 8, 10, 11)


def csv_row(fields: list) -> str:
    """One data row with its CRC and its LF (SFF-744). None is an empty field."""
    body = ",".join("" if f is None else str(f) for f in fields)
    return f"{body},{zlib.crc32(body.encode()):08x}\n"


def sidecar(header: dict, columns: list[str], rows: list[list], footer: list[str]) -> bytes:
    lines = [f"# {key}={'' if value is None else value}\n" for key, value in header.items()]
    lines.append(",".join([*columns, "crc32"]) + "\n")
    lines += [csv_row(row) for row in rows]
    lines += [line + "\n" for line in footer]
    return "".join(lines).encode()


def fit_line() -> str:
    return f"# fit fitter={FITTER} fitter_version={FITTER_VERSION} fitter_params={{}}"


def video_fitted_ns(t0_ns: int, period_ps: int, d: int) -> int:
    return t0_ns + d * period_ps // 1000  # SFF-777


def audio_fitted_ns(t0_ns: int, period_fs: int, n0: int, n: int) -> int:
    return t0_ns + (n - n0) * period_fs // 10**6  # SFF-779


def take_header(kind: str, take: dict, group_size: int, audio_count: int) -> dict:
    """The header keys from ``skellyfileformat`` to ``audio_count`` (sections 8 and 10)."""
    return {
        "skellyfileformat": kind,
        "format_version": FORMAT_VERSION,
        "format_prerelease": FORMAT_PRERELEASE,
        "writer": WRITER,
        "take_uuid": take["take_uuid"],
        "take_start_host_ns": take["take_start_host_ns"],
        "take_start_utc_ns": take["take_start_utc_ns"],
        "utc_offset_min": take["utc_offset_min"],
        "clock": take["clock"],
        "clock_hz": take["clock_hz"],
        "group_size": group_size,
        "audio_count": audio_count,
    }


# ---------------------------------------------------------------- camera identity (SFF-752, SFF-720)


def camera_key(identity: str) -> str:
    return hashlib.sha256(identity.encode()).digest()[:8].hex()


# ---------------------------------------------------------------- media (sections 6 and 9)
# The imports of PyAV and Pillow are inside the functions, so that the default test run, which has
# no golden dependency, can import this module.


def jpeg_frame(width: int, height: int, position: int, shade: int, flash: bool) -> bytes:
    """A synthetic frame: a dark field with a square that moves with the position, or a white flash."""
    import io

    from PIL import Image, ImageDraw

    image = Image.new("RGB", (width, height), (255, 255, 255) if flash else (shade, 40, 80 - shade))
    if not flash:
        x = position % (width - 8)
        ImageDraw.Draw(image).rectangle((x, 20, x + 7, 27), fill=(200, 200, 60))
    buffer = io.BytesIO()
    image.save(buffer, "JPEG", quality=90)
    return buffer.getvalue()


def container_ms(position: int, rate: Fraction) -> int:
    """The container timestamp of SFF-736: position / rate in ms, rounded half up."""
    return (2 * position * rate.denominator * 1000 + rate.numerator) // (2 * rate.numerator)


def build_mkv(path: Path, jpegs: list[bytes], rate: Fraction, width: int, height: int) -> None:
    """Mux ready JPEG images into a camera file (section 6). No frame is encoded again."""
    import av

    # Without bitexact, FFmpeg writes a random SegmentUID and TrackUID.
    with av.open(str(path), "w", format="matroska", options={"fflags": "+bitexact"}) as container:
        stream = container.add_stream("mjpeg", rate=rate)
        stream.width, stream.height, stream.pix_fmt = width, height, "yuvj420p"
        stream.time_base = Fraction(1, 1000)
        for position, jpeg in enumerate(jpegs):
            packet = av.Packet(jpeg)
            packet.stream = stream
            packet.time_base = Fraction(1, 1000)
            packet.pts = packet.dts = container_ms(position, rate)
            packet.is_keyframe = True
            container.mux(packet)


def _vint(data: bytes, at: int, keep_marker: bool) -> tuple[int, int]:
    length = 9 - data[at].bit_length()
    value = int.from_bytes(data[at : at + length], "big")
    return (value if keep_marker else value & ((1 << (7 * length)) - 1)), at + length


def ebml_children(data: bytes, start: int, end: int):
    """Yield (element ID, payload offset, payload size) for each element from start to end."""
    at = start
    while at < end:
        element_id, at = _vint(data, at, keep_marker=True)
        size, at = _vint(data, at, keep_marker=False)
        yield element_id, at, size
        at += size


SEGMENT, CLUSTER, SIMPLE_BLOCK = 0x18538067, 0x1F43B675, 0xA3


def mkv_payloads(data: bytes) -> list[tuple[int, int]]:
    """The (byte offset, byte size) of the payload of each SimpleBlock of a finished MKV, in file order."""
    payloads = []
    for top_id, top_at, top_size in ebml_children(data, 0, len(data)):
        if top_id != SEGMENT:
            continue
        for element_id, at, size in ebml_children(data, top_at, top_at + top_size):
            if element_id != CLUSTER:
                continue
            for block_id, block_at, block_size in ebml_children(data, at, at + size):
                if block_id == SIMPLE_BLOCK:
                    # The block header: the track number, 2 bytes of timestamp, 1 byte of flags (SFF-739).
                    header = _vint(data, block_at, keep_marker=False)[1] - block_at + 3
                    payloads.append((block_at + header, block_size - header))
    return payloads


def click_pcm(n_samples: int, click_samples: list[int]) -> bytes:
    """Mono s16 silence with a click of 48 samples (1 ms at 48 kHz) at each given sample index."""
    import array

    pcm = array.array("h", bytes(2 * n_samples))
    for first in click_samples:
        for i in range(48):
            pcm[first + i] = (24000 if i % 12 < 6 else -24000) * (48 - i) // 48
    return pcm.tobytes()


def build_opus_mp4(path: Path, pcm: bytes) -> None:
    """Encode mono s16 PCM at 48 kHz to the audio file of section 9, with the settings of SFF-762."""
    import av

    options = {"movflags": "empty_moov+default_base_moof", "frag_duration": "1000000", "fflags": "+bitexact"}
    with av.open(str(path), "w", format="mp4", options=options) as container:
        stream = container.add_stream("libopus", rate=48000, layout="mono")
        stream.codec_context.options = {
            "b": "128000", "application": "audio", "vbr": "on", "compression_level": "10", "frame_duration": "20",
        }  # fmt: skip
        stream.time_base = Fraction(1, 48000)
        for first in range(0, len(pcm) // 2, 960):
            block = pcm[2 * first : 2 * (first + 960)]
            frame = av.AudioFrame(format="s16", layout="mono", samples=len(block) // 2)
            frame.planes[0].update(block)
            frame.sample_rate, frame.pts, frame.time_base = 48000, first, Fraction(1, 48000)
            container.mux(stream.encode(frame))
        container.mux(stream.encode(None))


# ---------------------------------------------------------------- a finished capture-only take


def write_take(folder: Path, take: dict, cameras: list[dict], audio: dict) -> dict:
    """Write the files of a finished capture-only take. Return the facts for the expected result.

    ``take`` holds ``rec`` and the take keys. Each camera holds its config members (section 13), its
    ``camera_key``, its ``rate`` (num, den), ``width``, ``height``, ``display_rotation``, ``shade``,
    the fit (``t0_ns``, ``period_ps``), ``flash_positions`` and its ``rows``:
    (source_frame_number, arrival_ns, sample_ns). ``audio`` holds ``config`` (section 13), the fit
    (``t0_ns``, ``period_fs``), ``click_samples`` and its ``rows``: (first_sample, n_samples, host_ns,
    adc_ns).
    """
    rec = take["rec"]
    media = folder / MEDIA_FOLDER
    media.mkdir(parents=True)
    keys = [camera["camera_key"] for camera in cameras]
    labels = [key[:6] for key in keys]
    assert len(set(labels)) == len(labels), "SFF-720: this generator has no label longer than 6 characters"

    files, manifest_cameras, summary_cameras, privacy = [], [], [], []
    for position, (camera, key, label) in enumerate(zip(cameras, keys, labels)):
        video, timing = f"{MEDIA_FOLDER}/{rec}.{label}.mkv", f"{MEDIA_FOLDER}/{rec}.{label}.csv"
        rate = Fraction(*camera["rate"])
        jpegs = [
            jpeg_frame(camera["width"], camera["height"], p, camera["shade"], p in camera["flash_positions"])
            for p in range(len(camera["rows"]))
        ]
        build_mkv(folder / video, jpegs, rate, camera["width"], camera["height"])
        payloads = mkv_payloads((folder / video).read_bytes())
        assert [size for _, size in payloads] == [len(j) for j in jpegs]

        first_source = camera["rows"][0][0]
        rows, records, gaps = [], [], 0
        for p, (source, arrival_ns, sample_ns) in enumerate(camera["rows"]):
            before = camera["rows"][p - 1][0] if p else source - 1
            assert source != before, "SFF-756: this generator writes no flag `repeat`"
            gap = int(source != before + 1)  # SFF-756, bit 0
            gaps += gap
            rows.append([p, source, arrival_ns, sample_ns, gap, *payloads[p]])
            player_ns = video_fitted_ns(camera["t0_ns"], camera["period_ps"], source - first_source)
            records.append([p, source, arrival_ns, sample_ns, player_ns])
        header = take_header("video_timing", take, len(cameras), 1) | {
            "group_position": position,
            "camera_key": key,
            "camera_label": label,
            "nominal_rate": f"{rate.numerator}/{rate.denominator}",
            "display_rotation": camera["display_rotation"],
        }
        footer = [
            fit_line(),
            f"# fit_segment pos_first=0 pos_last={len(rows) - 1} t0_ns={camera['t0_ns']} "
            f"period_ps={camera['period_ps']}",
            f"# end rows={len(rows)} gaps={gaps} filled=0 encode_skips=0",
        ]
        columns = ["frame", "source_frame_number", "arrival_ns", "sample_ns", "flags", "byte_offset", "byte_size"]
        (folder / timing).write_bytes(sidecar(header, columns, rows, footer))

        files.append(
            {
                "name": video, "kind": "camera", "state": "finished", "reason": None, "camera_key": key,
                "camera_label": label, "rows": len(rows), "torn_bytes": 0, "fit": True,
                "warnings": ["prerelease"], "records": records,
            }
        )  # fmt: skip
        manifest_cameras.append(
            {
                "camera_key": key, "camera_label": label, "group_position": position, "video": video,
                "timing": timing, "calibration_camera": None,
            }
        )  # fmt: skip
        exposure = camera["controls"].get("exposure_us")
        summary_cameras.append(
            {
                "camera_label": label,
                "user_name": camera["user_name"],
                "model": camera["device"]["model"],
                "stored_px": f"{camera['width']}x{camera['height']}",
                "display_rotation": camera["display_rotation"],
                "nominal_fps": thousandths((2000 * rate.numerator + rate.denominator) // (2 * rate.denominator)),
                "gaps": gaps,
                "filled": 0,
                "exposure_us": exposure["value"] if exposure else None,
            }
        )
        privacy.append((timing, "utc_offset_min", "time_zone"))
        privacy.append(("recording_manifest.json", f"/summary/cameras/{position}/model", "device_name"))
        if camera["user_name"] is not None:
            privacy.append(
                ("recording_manifest.json", f"/summary/cameras/{position}/user_name", "user_entered_name")
            )

    # The audio pair.
    audio_path, audio_timing = f"{MEDIA_FOLDER}/{rec}.audio.m4a", f"{MEDIA_FOLDER}/{rec}.audio.csv"
    samples = sum(n for _, n, _, _ in audio["rows"])
    build_opus_mp4(folder / audio_path, click_pcm(samples, audio["click_samples"]))
    rows = [[b, first, n, host_ns, adc_ns, 0] for b, (first, n, host_ns, adc_ns) in enumerate(audio["rows"])]
    header = take_header("audio_timing", take, len(cameras), 1) | {
        "sample_rate": 48000,
        "channels": 1,
        "codec": "opus",
        "file_sample_offset": 0,
        "audio_latency_ns": None,
    }
    footer = [
        fit_line(),
        f"# fit_segment row_first=0 row_last={len(rows) - 1} n0=0 t0_ns={audio['t0_ns']} "
        f"period_fs={audio['period_fs']}",
        f"# end rows={len(rows)} samples={samples} gaps=0 silence_samples=0",
    ]
    columns = ["block", "first_sample", "n_samples", "host_ns", "adc_ns", "flags"]
    (folder / audio_timing).write_bytes(sidecar(header, columns, rows, footer))
    files.append(
        {
            "name": audio_path, "kind": "audio", "state": "finished", "reason": None, "camera_key": None,
            "camera_label": None, "rows": len(rows), "torn_bytes": 0, "fit": True, "warnings": ["prerelease"],
            "records": [
                [b, first, n, host_ns, audio_fitted_ns(audio["t0_ns"], audio["period_fs"], 0, first)]
                for b, (first, n, host_ns, _) in enumerate(audio["rows"])
            ],
        }
    )  # fmt: skip
    privacy.append((audio_timing, "utc_offset_min", "time_zone"))

    # The capture info JSON (section 13).
    config_members = ("user_name", "key_origin", "device", "requested", "controls", "exposure_step")
    info_path = f"{rec}_info.json"
    info = file_json(
        {
            "skellyfileformat": "capture_info",
            "format_version": FORMAT_VERSION,
            "format_prerelease": FORMAT_PRERELEASE,
            "writer": WRITER,
            "take_uuid": take["take_uuid"],
            "camera_configs": {
                key: {"camera_label": label} | {m: camera[m] for m in config_members}
                for camera, key, label in zip(cameras, keys, labels)
            },
            "audio": audio["config"],
        }
    )
    (folder / info_path).write_bytes(info)
    device_kinds = {
        "model": "device_name", "os_name": "device_name", "serial": "serial_number",
        "port_path": "device_path", "os_device_id": "device_path",
    }  # fmt: skip
    for camera, key in zip(cameras, keys):
        base = f"/camera_configs/{key}"
        if camera["user_name"] is not None:
            privacy.append((info_path, f"{base}/user_name", "user_entered_name"))
        privacy += [
            (info_path, f"{base}/device/{member}", kind)
            for member, kind in device_kinds.items()
            if camera["device"][member] is not None
        ]
    privacy.append((info_path, "/audio/device_name", "device_name"))
    privacy.append(("recording_manifest.json", "/recording_name", "user_entered_name"))

    # The manifest (section 5).
    gap_warnings = [
        {"code": "camera_gap", "source": "skellycam", "camera_key": key, "detail": None}
        for key, summary in zip(keys, summary_cameras)
        if summary["gaps"]
    ]
    last_arrival_ns = max(camera["rows"][-1][1] for camera in cameras)
    utc_s = take["take_start_utc_ns"] // 10**9
    manifest = {
        "skellyfileformat": "recording_manifest",
        "format_version": FORMAT_VERSION,
        "format_prerelease": FORMAT_PRERELEASE,
        "writer": WRITER,
        "take_uuid": take["take_uuid"],
        "recording_name": rec,
        "purpose": "motion_capture",
        "state": "finished",
        "cameras": manifest_cameras,
        "audio": {"audio": audio_path, "timing": audio_timing},
        "calibration": None,
        "files": [{"path": info_path, "role": "capture_info", "owner": "skellycam", "sha256": sha256_hex(info)}],
        "warnings": gap_warnings,
        "privacy": {
            "fields": [
                {"file": file, "field": field, "kind": kind}
                for file, field, kind in sorted(privacy, key=lambda item: (item[0].encode(), item[1].encode()))
            ],
            "media_shows_people": True,
        },
        "summary": {
            "take_start_utc": datetime.datetime.fromtimestamp(utc_s, datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "duration_s": thousandths((last_arrival_ns + 500_000) // 10**6),
            "cameras": summary_cameras,
            "audio": {
                "file": audio_path,
                "sample_rate": 48000,
                "channels": 1,
                "duration_s": thousandths((2000 * samples + 48000) // (2 * 48000)),
            },
            "calibration": None,
            "processing_runs": [],
            "warnings": sorted({warning["code"] for warning in gap_warnings}),
        },
    }
    (folder / "recording_manifest.json").write_bytes(file_json(manifest))
    return {"take_uuid": take["take_uuid"], "recording_name": rec, "files": files, "info_path": info_path}


def expected_result(facts: dict, scope: str) -> dict:
    """The reader result (SFF-885) of a folder that holds one finished capture-only take of ``write_take``.

    golden/README.md gives the requirement of each member.
    """
    # The take has no TOML, no Parquet and no journal. So only the row-count part of `frames` differs
    # between the scopes (SFF-872, SFF-892).
    link_states = {
        "take_uuid": "ok",
        "camera_key": "ok",
        "frames": "ok" if scope == "full" else "not_checked",
        "dimensions": "not_checked",
        "rotation": "ok",
        "files": "ok",
        "hashes": "not_checked",
        "calibration": "not_checked",
    }
    return {
        "result_version": 2,
        "folder_state": "ok",
        "folder_warnings": [],
        "takes": [
            {
                "take_uuid": facts["take_uuid"],
                "recording_name": facts["recording_name"],
                "state": "complete",
                "manifest": "present",
                "warnings": [],
                "may_contain_private_data": True,
                "files": facts["files"],
                "folder_files": [
                    {
                        "path": facts["info_path"], "role": "capture_info", "state": "present",
                        "reason": None, "warnings": ["prerelease"],
                    }
                ],  # fmt: skip
                "links": [{"check": check, "state": link_states[check], "detail": None} for check in LINK_CHECKS],
            }
        ],
        "other_files": [],
        "legacy": None,
    }
