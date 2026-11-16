"""Shared helpers of the conformance tests SFT-700 to SFT-734 (decision G21H).

Each `check_*` function takes a folder or a file and asserts. It imports no implementation, so the same
check runs on the output of the writer and on a golden folder. The parsers here are independent of the
package: stdlib only. The decoders use PyAV and Pillow through `pytest.importorskip`.

The interfaces that these helpers and the tests expect from the package are in
INTERFACE_NOTES_capture.md.
"""

from __future__ import annotations

import array
import contextlib
import hashlib
import io
import json
import re
import struct
import sys
import tomllib
import zlib
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path

import pytest

MEDIA = "synchronized_videos"
LOCK = ".processing.lock"
MANIFEST = "recording_manifest.json"
WRITER = "skellycam 2.0.0"

# ---------------------------------------------------------------- the reader result


def read(reader, folder: Path, records: bool = False, scope: str = "full") -> dict:
    """The reader result of a folder, as the parsed canonical JSON."""
    return json.loads(read_bytes(reader, folder, records, scope))


def read_bytes(reader, folder: Path, records: bool = True, scope: str = "full") -> bytes:
    return reader.canonical_json(reader.read_folder(folder, records=records, scope=scope))


def only_take(result: dict) -> dict:
    assert len(result["takes"]) == 1, "the folder has one take"
    return result["takes"][0]


def cameras_of(take: dict) -> list[dict]:
    return [item for item in take["files"] if item["kind"] == "camera"]


def audio_of(take: dict) -> dict:
    (item,) = [item for item in take["files"] if item["kind"] == "audio"]
    return item


def sidecar_path(folder: Path, name: str) -> Path:
    """The timing sidecar of a media file. `name` is the `name` of a `files` item."""
    return (folder / name).with_suffix(".csv")


def snapshot(folder: Path) -> dict:
    """The SHA-256 and the modification time of each file, by path (SFT-734)."""
    return {
        path.relative_to(folder).as_posix(): (hashlib.sha256(path.read_bytes()).hexdigest(), path.stat().st_mtime_ns)
        for path in sorted(folder.rglob("*"))
        if path.is_file()
    }


# ---------------------------------------------------------------- timing sidecars (sections 7, 8, 10)

TAKE_KEYS = [
    "take_uuid", "take_start_host_ns", "take_start_utc_ns", "utc_offset_min", "clock", "clock_hz", "group_size",
    "audio_count",
]  # fmt: skip
COMMON_KEYS = ["skellyfileformat", "format_version", "format_prerelease", "writer", *TAKE_KEYS]
VIDEO_KEYS = [*COMMON_KEYS, "group_position", "camera_key", "camera_label", "nominal_rate", "display_rotation"]
AUDIO_KEYS = [*COMMON_KEYS, "sample_rate", "channels", "codec", "file_sample_offset", "audio_latency_ns"]
VIDEO_COLUMNS = ["frame", "source_frame_number", "arrival_ns", "sample_ns", "flags", "byte_offset", "byte_size", "crc32"]
AUDIO_COLUMNS = ["block", "first_sample", "n_samples", "host_ns", "adc_ns", "flags", "crc32"]
INTEGER_KEYS = [
    "format_prerelease", "take_start_host_ns", "take_start_utc_ns", "utc_offset_min", "group_size", "audio_count",
    "group_position", "display_rotation", "sample_rate", "channels", "file_sample_offset",
]  # fmt: skip
INTEGER_OR_EMPTY_KEYS = ["clock_hz", "audio_latency_ns"]
FOOTER_KEYS = {
    "fit": ["fitter", "fitter_version", "fitter_params"],
    "repair": ["cut_bytes", "media_cut_bytes", "repair_writer"],
    ("video", "fit_segment"): ["pos_first", "pos_last", "t0_ns", "period_ps"],
    ("audio", "fit_segment"): ["row_first", "row_last", "n0", "t0_ns", "period_fs"],
    ("video", "end"): ["rows", "gaps", "filled", "encode_skips"],
    ("audio", "end"): ["rows", "samples", "gaps", "silence_samples"],
}
INTEGER = re.compile(r"0|-?[1-9][0-9]*")  # SFF-701
HEX8 = re.compile(r"[0-9a-f]{8}")
HEX16 = re.compile(r"[0-9a-f]{16}")
UUID4 = re.compile(r"[0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15}")  # SFF-703
GAP, FILLED, ENCODE_SKIP, REPEAT = 1, 2, 4, 8  # SFF-756
OVERFLOW, SILENCE = 1, 2  # SFF-768


def crc_text(text: str) -> str:
    return f"{zlib.crc32(text.encode()):08x}"


def row_line(fields: list) -> str:
    """A data row with its CRC and its LF (SFF-744). None gives an empty field."""
    text = ",".join("" if value is None else str(value) for value in fields)
    return f"{text},{crc_text(text)}\n"


@dataclass
class Sidecar:
    """A timing sidecar, read strictly (SFF-746), with no use of the package."""

    path: Path
    data: bytes
    header: dict = field(default_factory=dict)
    columns: list = field(default_factory=list)
    rows: list = field(default_factory=list)  # the usable rows, each a dict of texts
    row_lines: list = field(default_factory=list)  # each complete data line, also after a wrong CRC
    footer: list = field(default_factory=list)  # the complete footer lines
    torn: int = 0  # the bytes of a last line with no LF
    bad_crc: bool = False
    rows_end: int = 0  # the byte offset after the last usable row

    @property
    def kind(self) -> str:
        return {"video_timing": "video", "audio_timing": "audio"}[self.header["skellyfileformat"]]

    @property
    def finished(self) -> bool:
        return self.torn == 0 and bool(self.footer) and self.footer[-1].startswith("# end")

    def lines(self, word: str) -> list[dict]:
        """The values of each complete footer line with this word."""
        return [footer_values(line, self.kind)[1] for line in self.footer if line.split(" ")[1] == word]

    @property
    def repaired(self) -> bool:
        return self.finished and any(line.startswith("# repair ") for line in self.footer)

    def integers(self, column: str) -> list:
        return [int(row[column]) if row[column] else None for row in self.rows]


def footer_values(line: str, kind: str) -> tuple[str, dict]:
    """The word and the values of a footer line. The keys must be in the order of the spec (SFF-745)."""
    assert line.startswith("# "), line
    word, _, rest = line[2:].partition(" ")
    keys = FOOTER_KEYS.get(word) or FOOTER_KEYS[(kind, word)]
    parts = rest.split(" ", len(keys) - 1)
    assert len(parts) == len(keys), f"the line has each key, with single spaces: {line}"
    values = {}
    for key, part in zip(keys, parts):
        assert part.startswith(key + "="), f"the keys are in the order {keys}: {line}"
        values[key] = part[len(key) + 1 :]
    return word, values


def read_sidecar(path: Path) -> Sidecar:
    data = path.read_bytes()
    out = Sidecar(path, data)
    *complete, last = data.split(b"\n")
    out.torn = len(last)
    at, state = 0, "header"
    for raw in complete:
        line = raw.decode("utf-8")
        end = at + len(raw) + 1
        if state == "header" and line.startswith("# "):
            key, _, value = line[2:].partition("=")
            out.header[key] = value
        elif state == "header":
            out.columns, state, out.rows_end = line.split(","), "rows", end
        elif state == "rows" and not line.startswith("#"):
            out.row_lines.append(line)
            body, _, crc = line.rpartition(",")
            fields = line.split(",")
            if not out.bad_crc and len(fields) == len(out.columns) and crc == crc_text(body):
                out.rows.append(dict(zip(out.columns, fields)))
                out.rows_end = end
            else:
                out.bad_crc = True  # the read stops at this row
        else:
            state = "footer"
            out.footer.append(line)
        at = end
    return out


def set_header(path: Path, key: str, value) -> None:
    """Change one header value of a sidecar. A header line has no CRC."""
    data = path.read_bytes()
    changed, count = re.subn(rb"(?m)^# " + key.encode() + rb"=.*$", f"# {key}={value}".encode(), data, count=1)
    assert count == 1, key
    path.write_bytes(changed)


def set_row(path: Path, index: int, column: str, value) -> None:
    """Change one field of one data row of a sidecar, and write the correct CRC of the new row."""
    sidecar = read_sidecar(path)
    row = dict(sidecar.rows[index], **{column: value})
    old = sidecar.row_lines[index] + "\n"
    new = row_line([row[name] for name in sidecar.columns[:-1]])
    assert sidecar.data.count(old.encode()) == 1
    path.write_bytes(sidecar.data.replace(old.encode(), new.encode()))


def video_fitted_ns(sidecar: Sidecar) -> list[int]:
    """The fitted time of each usable row of a video sidecar, from its fit lines (SFF-777)."""
    numbers = sidecar.integers("source_frame_number")
    times = {}
    for segment in sidecar.lines("fit_segment"):
        first, last, t0, period = (int(segment[key]) for key in FOOTER_KEYS[("video", "fit_segment")])
        for p in range(first, min(last, len(numbers) - 1) + 1):
            both = numbers[p] is not None and numbers[first] is not None
            d = numbers[p] - numbers[first] if both else p - first
            times[p] = t0 + d * period // 1000
    return [times[p] for p in range(len(numbers))]


def audio_fit_of_lines(sidecar: Sidecar) -> list[dict]:
    return [{key: int(value) for key, value in segment.items()} for segment in sidecar.lines("fit_segment")]


def audio_fit_of_reader(sidecar: Sidecar) -> list[dict]:
    """The one segment that a reader computes from the usable rows, or no segment (SFF-784)."""
    if len(sidecar.rows) < 2:
        return []
    a, b = sidecar.rows[0], sidecar.rows[-1]
    time_a, time_b = (int(row["adc_ns"] or row["host_ns"]) for row in (a, b))
    n_a, n_b = int(a["first_sample"]), int(b["first_sample"])
    period_fs = (time_b - time_a) * 10**6 // (n_b - n_a)
    if period_fs <= 0:
        return []
    return [{"row_first": int(a["block"]), "row_last": int(b["block"]), "n0": n_a, "t0_ns": time_a, "period_fs": period_fs}]


def audio_fitted_ns(segments: list[dict], row: int, sample: int) -> int | None:
    """The fitted time of a sample of a row (SFF-779). A fit of the reader has one segment for each row."""
    if not segments:
        return None
    inside = [s for s in segments if s["row_first"] <= row <= s["row_last"]]
    segment = inside[0] if inside else segments[0]
    return segment["t0_ns"] + (sample - segment["n0"]) * segment["period_fs"] // 10**6


# ---------------------------------------------------------------- Matroska (section 6)

EBML, SEGMENT, CLUSTER, SIMPLE_BLOCK, BLOCK_GROUP = 0x1A45DFA3, 0x18538067, 0x1F43B675, 0xA3, 0xA0
INFO, TRACKS, TRACK_ENTRY, VIDEO, PROJECTION = 0x1549A966, 0x1654AE6B, 0xAE, 0xE0, 0x7670
DOC_TYPE, DOC_TYPE_VERSION, TIMESTAMP_SCALE, CLUSTER_TIMESTAMP = 0x4282, 0x4287, 0x2AD7B1, 0xE7
TRACK_NUMBER, TRACK_TYPE, CODEC_ID, DEFAULT_DURATION = 0xD7, 0x83, 0x86, 0x23E383
MASTERS = {EBML, SEGMENT, CLUSTER, INFO, TRACKS, TRACK_ENTRY, VIDEO, PROJECTION}
# The elements that end a Cluster of unknown size: the children of the Segment.
SEGMENT_CHILDREN = {0x114D9B74, INFO, TRACKS, CLUSTER, 0x1C53BB6B, 0x1254C367, 0x1941A469, 0x1043A770}


def ebml_elements(data: bytes, at: int = 0, end: int | None = None, parent: int = 0, open_size: bool = False):
    """Yield (ID, payload offset, payload size, parent ID) for each complete element, in file order.

    The walk goes into each master element, also one of unknown size and one that the file end cuts.
    It stops at the first element that is not complete (SFF-740). It returns the offset of its stop.
    """
    end = len(data) if end is None else min(end, len(data))
    while at < end:
        id_length = 9 - data[at].bit_length()
        size_at = at + id_length
        if id_length > 4 or size_at >= end or data[size_at] == 0:
            return at
        element_id = int.from_bytes(data[at:size_at], "big")
        if open_size and parent == CLUSTER and element_id in SEGMENT_CHILDREN:
            return at
        size_length = 9 - data[size_at].bit_length()
        body = size_at + size_length
        if body > end:
            return at
        ones = (1 << (7 * size_length)) - 1
        size = int.from_bytes(data[size_at:body], "big") & ones
        unknown = size == ones
        if element_id in MASTERS:
            yield element_id, body, None if unknown else size, parent
            stop = end if unknown else body + size
            reached = yield from ebml_elements(data, body, stop, element_id, unknown)
            if not unknown and stop > end:
                return reached  # the file end cuts this master element
            at = reached if unknown else stop
            continue
        if unknown or body + size > end:
            return at
        yield element_id, body, size, parent
        at = body + size
    return at


@dataclass
class Block:
    track: int
    track_bytes: int  # the length of the track number in the block header (SFF-739)
    timestamp: int  # the Cluster timestamp plus the block timestamp, in TimestampScale units
    flags: int
    offset: int  # of the payload, from the start of the file
    size: int  # of the payload
    end: int


@dataclass
class Mkv:
    doc_type: str = ""
    doc_type_version_at: int = 0  # the offset of the payload of DocTypeVersion
    timestamp_scale: int | None = None
    tracks: list = field(default_factory=list)  # each: number, type, codec, default_duration
    blocks: list = field(default_factory=list)  # the complete SimpleBlocks, in file order
    ids: set = field(default_factory=set)

    @property
    def blocks_end(self) -> int:
        """The offset after the last complete block."""
        return self.blocks[-1].end


def parse_mkv(data: bytes) -> Mkv:
    assert data[:4] == b"\x1a\x45\xdf\xa3", "a camera file starts with the EBML magic (SFF-864)"
    out, cluster_time = Mkv(), 0
    for element_id, at, size, parent in ebml_elements(data):
        out.ids.add(element_id)
        if size is None or element_id in MASTERS:
            if element_id == TRACK_ENTRY:
                out.tracks.append({})
            continue
        payload = data[at : at + size]
        number = int.from_bytes(payload, "big")
        if element_id == DOC_TYPE:
            out.doc_type = payload.decode()
        elif element_id == DOC_TYPE_VERSION:
            out.doc_type_version_at = at
        elif element_id == TIMESTAMP_SCALE:
            out.timestamp_scale = number
        elif parent == TRACK_ENTRY and element_id in (TRACK_NUMBER, TRACK_TYPE, DEFAULT_DURATION):
            out.tracks[-1][{TRACK_NUMBER: "number", TRACK_TYPE: "type", DEFAULT_DURATION: "default_duration"}[element_id]] = number
        elif parent == TRACK_ENTRY and element_id == CODEC_ID:
            out.tracks[-1]["codec"] = payload.decode()
        elif element_id == CLUSTER_TIMESTAMP:
            cluster_time = number
        elif element_id == SIMPLE_BLOCK:
            track_bytes = 9 - payload[0].bit_length()
            track = int.from_bytes(payload[:track_bytes], "big") & ((1 << (7 * track_bytes)) - 1)
            relative = int.from_bytes(payload[track_bytes : track_bytes + 2], "big", signed=True)
            header = track_bytes + 3
            out.blocks.append(
                Block(track, track_bytes, cluster_time + relative, payload[track_bytes + 2], at + header, size - header, at + size)
            )
    return out


def ebml_number(value: int, length: int | None = None) -> bytes:
    """An EBML variable-size integer, with the smallest length or with a given length."""
    length = length or next(n for n in range(1, 9) if value < (1 << (7 * n)) - 1)
    return ((1 << (7 * length)) | value).to_bytes(length, "big")


def ebml_element(element_id: int, payload: bytes | int | str) -> bytes:
    if isinstance(payload, int):
        payload = payload.to_bytes(max(1, (payload.bit_length() + 7) // 8), "big")
    elif isinstance(payload, str):
        payload = payload.encode()
    return element_id.to_bytes((element_id.bit_length() + 7) // 8, "big") + ebml_number(len(payload)) + payload


def container_ms(position: int, num: int, den: int) -> int:
    """The container timestamp of SFF-736: position / rate in ms, rounded half up."""
    return (2 * position * den * 1000 + num) // (2 * num)


def build_mkv(jpegs: list[bytes], width: int, height: int, track_bytes: list[int], num: int = 30, den: int = 1) -> bytes:
    """A small camera file, written with no muxer (SFT-713, decision G21H item 7).

    It has one `V_MJPEG` track with the number 1 and one Cluster for each 5 frames. `track_bytes` gives,
    for each frame, the length of the track number in its block header: 1 (`81`) or 2 (`40 01`).
    """
    header = ebml_element(
        EBML,
        ebml_element(0x4286, 1) + ebml_element(0x42F7, 1) + ebml_element(0x42F2, 4) + ebml_element(0x42F3, 8)
        + ebml_element(DOC_TYPE, "matroska") + ebml_element(DOC_TYPE_VERSION, 4) + ebml_element(0x4285, 2),
    )  # fmt: skip
    info = ebml_element(INFO, ebml_element(TIMESTAMP_SCALE, 1_000_000) + ebml_element(0x4D80, "sft713") + ebml_element(0x5741, "sft713"))
    video = ebml_element(VIDEO, ebml_element(0xB0, width) + ebml_element(0xBA, height))
    entry = (
        ebml_element(TRACK_NUMBER, 1) + ebml_element(0x73C5, 1) + ebml_element(TRACK_TYPE, 1)
        + ebml_element(CODEC_ID, "V_MJPEG") + ebml_element(DEFAULT_DURATION, 10**9 * den // num) + video
    )  # fmt: skip
    body = info + ebml_element(TRACKS, ebml_element(TRACK_ENTRY, entry))
    for first in range(0, len(jpegs), 5):
        start = container_ms(first, num, den)
        cluster = ebml_element(CLUSTER_TIMESTAMP, start)
        for position in range(first, min(first + 5, len(jpegs))):
            relative = container_ms(position, num, den) - start
            block = ebml_number(1, track_bytes[position]) + relative.to_bytes(2, "big") + b"\x80" + jpegs[position]
            cluster += ebml_element(SIMPLE_BLOCK, block)
        body += ebml_element(CLUSTER, cluster)
    return header + ebml_element(SEGMENT, body)


# ---------------------------------------------------------------- JPEG

SOI, EOI, SOS, DHT, APP0, APP1 = 0xD8, 0xD9, 0xDA, 0xC4, 0xE0, 0xE1


def jpeg_segments(data: bytes) -> list[tuple[int, int, int]]:
    """(marker, start, end) of each segment from SOI to the SOS header."""
    assert data[:2] == b"\xff\xd8", "a JPEG starts with SOI"
    out, at = [], 2
    while data[at] == 0xFF:
        marker = data[at + 1]
        end = at + 2 + int.from_bytes(data[at + 2 : at + 4], "big")
        out.append((marker, at, end))
        at = end
        if marker == SOS:
            break
    return out


def jpeg_without(data: bytes, markers: set[int]) -> bytes:
    """The JPEG with each segment of the given markers removed."""
    for marker, start, end in reversed(jpeg_segments(data)):
        if marker in markers:
            data = data[:start] + data[end:]
    return data


def jpeg_size(data: bytes) -> tuple[int, int]:
    """(width, height) of the frame header."""
    for marker, start, _ in jpeg_segments(data):
        if marker in (0xC0, 0xC1, 0xC2):
            height, width = struct.unpack(">HH", data[start + 5 : start + 9])
            return width, height
    raise AssertionError("the JPEG has no frame header")


def exif_segment(orientation: int) -> bytes:
    """An APP1 segment with an EXIF orientation tag (0x0112)."""
    tiff = b"II*\x00" + struct.pack("<IH", 8, 1) + struct.pack("<HHIHH", 0x0112, 3, 1, orientation, 0) + bytes(4)
    payload = b"Exif\x00\x00" + tiff
    return b"\xff\xe1" + struct.pack(">H", len(payload) + 2) + payload


def exif_orientation(data: bytes) -> int | None:
    for marker, start, end in jpeg_segments(data):
        if marker == APP1 and data[start + 4 : start + 10] == b"Exif\x00\x00":
            tiff = data[start + 10 : end]
            order = "<" if tiff[:2] == b"II" else ">"
            (ifd,) = struct.unpack(order + "I", tiff[4:8])
            (count,) = struct.unpack(order + "H", tiff[ifd : ifd + 2])
            for i in range(count):
                tag, _, _, value = struct.unpack(order + "HHIH", tiff[ifd + 2 + 12 * i : ifd + 12 + 12 * i])
                if tag == 0x0112:
                    return value
    return None


# ---------------------------------------------------------------- ISO BMFF (section 9)


def boxes(data: bytes, at: int, end: int) -> list[tuple[bytes, int, int]]:
    """(kind, payload offset, end offset) of each complete box from `at` to `end`. A torn box ends the walk."""
    out = []
    while at + 8 <= end:
        size, kind = int.from_bytes(data[at : at + 4], "big"), data[at + 4 : at + 8]
        body = at + 8
        if size == 1:
            size, body = int.from_bytes(data[at + 8 : at + 16], "big"), at + 16
        elif size == 0:
            size = end - at
        if size < body - at or at + size > end:
            break
        out.append((kind, body, at + size))
        at += size
    return out


def box(data: bytes, at: int, end: int, *path: bytes) -> tuple[int, int]:
    """(payload offset, end offset) of the first box of a path of kinds."""
    for kind in path:
        found = [(body, stop) for k, body, stop in boxes(data, at, end) if k == kind]
        assert found, f"the box {kind} exists"
        at, end = found[0]
    return at, end


@dataclass
class Mp4:
    kinds: list = field(default_factory=list)  # the kinds of the complete top boxes
    traks: int = 0
    mvex: bool = False
    timescale: int = 0
    moov_samples: int = 0  # the entries of stts, stsc and stco, and the samples of stsz
    entry: bytes = b""  # the kind of the sample entry
    channels: int = 0
    pre_skip: int = 0
    output_gain: int = 0
    fragments: list = field(default_factory=list)  # each complete: tfdt, samples, tfhd_flags, tfdt_version, truns, trafs
    complete_end: int = 0  # the offset after the last complete fragment, or after the moov


def parse_mp4(data: bytes) -> Mp4:
    out = Mp4()
    top = boxes(data, 0, len(data))
    out.kinds = [kind for kind, _, _ in top]
    assert out.kinds[:2] == [b"ftyp", b"moov"], "the audio file starts with ftyp and moov (SFF-760)"
    _, moov, moov_end = top[1]
    out.complete_end = moov_end
    inside = [kind for kind, _, _ in boxes(data, moov, moov_end)]
    out.traks, out.mvex = inside.count(b"trak"), b"mvex" in inside
    media, media_end = box(data, moov, moov_end, b"trak", b"mdia")
    mdhd, _ = box(data, media, media_end, b"mdhd")
    out.timescale = int.from_bytes(data[mdhd + (20 if data[mdhd] == 1 else 12) :][:4], "big")
    table, table_end = box(data, media, media_end, b"minf", b"stbl")
    for kind, body, _ in boxes(data, table, table_end):
        if kind in (b"stts", b"stsc", b"stco", b"co64"):
            out.moov_samples += int.from_bytes(data[body + 4 : body + 8], "big")
        elif kind == b"stsz":
            out.moov_samples += int.from_bytes(data[body + 8 : body + 12], "big")
    stsd, stsd_end = box(data, table, table_end, b"stsd")
    (first_entry, entry, entry_end) = boxes(data, stsd + 8, stsd_end)[0]
    out.entry = first_entry
    dops, _ = box(data, entry + 28, entry_end, b"dOps")  # 28 bytes: the fields of an audio sample entry
    _, out.channels, out.pre_skip, _, out.output_gain = struct.unpack(">BBHIh", data[dops : dops + 10])
    trex, _ = box(data, moov, moov_end, b"mvex", b"trex")
    trex_duration = int.from_bytes(data[trex + 12 : trex + 16], "big")
    for index, (kind, body, stop) in enumerate(top):
        if kind != b"moof":
            continue
        if index + 1 >= len(top) or top[index + 1][0] != b"mdat":
            break  # the mdat of this fragment is torn or absent (SFF-792)
        trafs = [(b_, s_) for k_, b_, s_ in boxes(data, body, stop) if k_ == b"traf"]
        traf, traf_end = trafs[0]
        parts = boxes(data, traf, traf_end)
        tfhd = next(b_ for k_, b_, _ in parts if k_ == b"tfhd")
        tfdt = next(b_ for k_, b_, _ in parts if k_ == b"tfdt")
        truns = [b_ for k_, b_, _ in parts if k_ == b"trun"]
        tfhd_flags = int.from_bytes(data[tfhd + 1 : tfhd + 4], "big")
        at = tfhd + 8 + (8 if tfhd_flags & 1 else 0) + (4 if tfhd_flags & 2 else 0)
        duration = int.from_bytes(data[at : at + 4], "big") if tfhd_flags & 8 else trex_duration
        samples = 0
        for trun in truns:
            flags = int.from_bytes(data[trun + 1 : trun + 4], "big")
            count = int.from_bytes(data[trun + 4 : trun + 8], "big")
            if not flags & 0x100:
                samples += count * duration
                continue
            at = trun + 8 + (4 if flags & 1 else 0) + (4 if flags & 4 else 0)
            step = 4 * sum(1 for bit in (0x100, 0x200, 0x400, 0x800) if flags & bit)
            samples += sum(int.from_bytes(data[at + i * step :][:4], "big") for i in range(count))
        version = data[tfdt]
        out.fragments.append(
            {
                "tfdt": int.from_bytes(data[tfdt + 4 : tfdt + (12 if version == 1 else 8)], "big"),
                "tfdt_version": version, "tfhd_flags": tfhd_flags, "truns": len(truns), "trafs": len(trafs),
                "samples": samples,
            }  # fmt: skip
        )
        out.complete_end = top[index + 1][2]
    return out


def media_complete_end(path: Path) -> int:
    """The offset after the last complete block of a camera file, or the last complete fragment of an audio file."""
    data = path.read_bytes()
    if path.suffix == ".mkv":
        return parse_mkv(data).blocks_end
    return parse_mp4(data).complete_end


def torn_bytes_of_pair(media: Path) -> int:
    """`torn_bytes` of a device pair, as the sum of SFF-791."""
    sidecar = read_sidecar(media.with_suffix(".csv"))
    tail = 0 if sidecar.finished else media.stat().st_size - media_complete_end(media)
    return sidecar.torn + tail


def audio_usable_samples(media: Path) -> int:
    """The usable length of an audio file (SFF-785)."""
    sidecar = read_sidecar(media.with_suffix(".csv"))
    mp4 = parse_mp4(media.read_bytes())
    held = sum(fragment["samples"] for fragment in mp4.fragments) - mp4.pre_skip
    return min(sum(n for n in sidecar.integers("n_samples")), held)


# ---------------------------------------------------------------- decoding (decision G21H item 8)


def decode_jpeg(data: bytes):
    """Decode one stored frame with PyAV. Return a Pillow image in RGB."""
    av = pytest.importorskip("av")
    pytest.importorskip("PIL")
    context = av.CodecContext.create("mjpeg", "r")
    frames = context.decode(av.Packet(data)) + context.decode(None)
    assert len(frames) == 1, "PyAV decodes one frame from the stored bytes"
    return frames[0].to_image().convert("RGB")


def count_packets(path: Path) -> int:
    """The number of frames that the pinned FFmpeg (through PyAV) finds in a camera file."""
    av = pytest.importorskip("av")
    with av.open(str(path)) as container:
        return sum(1 for packet in container.demux(video=0) if packet.size)


def decode_audio(path: Path) -> list:
    """Decode an audio file with PyAV. Return one float array for each channel.

    PyAV drops the pre-skip samples and applies no output gain, so index 0 is sample 0 (SFF-766).
    """
    av = pytest.importorskip("av")
    with av.open(str(path)) as container:
        channels = None
        for frame in container.decode(audio=0):
            assert frame.format.name == "fltp" and frame.sample_rate == 48000
            channels = channels or [array.array("f") for _ in frame.planes]
            for channel, plane in zip(channels, frame.planes):
                channel.frombytes(bytes(plane)[: 4 * frame.samples])
    return channels


def click_onsets(samples) -> list[int]:
    """The first sample of each click: a magnitude of 0.3 or more after 100 ms of quiet (G01_CHOICES item 11)."""
    loud = [i for i, v in enumerate(samples) if abs(v) >= 0.3]
    return [i for k, i in enumerate(loud) if k == 0 or i - loud[k - 1] > 4800]


# ---------------------------------------------------------------- synthetic input of the writer

WIDTH, HEIGHT = 64, 48


def jpeg(position: int = 0, width: int = WIDTH, height: int = HEIGHT, colour=(30, 40, 80)) -> bytes:
    """A synthetic JPEG frame from Pillow: baseline, 4:2:0, with a JFIF segment and the standard tables."""
    image_module = pytest.importorskip("PIL.Image")
    image = image_module.new("RGB", (width, height), colour)
    x = position % (width - 8)
    image.paste((200, 200, 60), (x, 20, x + 8, 28))
    buffer = io.BytesIO()
    image.save(buffer, "JPEG", quality=90)
    return buffer.getvalue()


def yuyv(position: int = 0, width: int = WIDTH, height: int = HEIGHT) -> bytes:
    """A raw frame in YUYV 4:2:2: 2 bytes for each pixel."""
    return bytes([(40 + position) % 256, 128, (40 + position) % 256, 128]) * (width * height // 2)


def click_pcm(n_samples: int, clicks: list[int], channels: int = 1) -> bytes:
    """Interleaved s16 silence at 48 kHz with a click of 48 samples at each given sample index."""
    pcm = array.array("h", bytes(2 * n_samples * channels))
    for first in clicks:
        for i in range(48):
            for channel in range(channels):
                pcm[(first + i) * channels + channel] = (24000 if i % 12 < 6 else -24000) * (48 - i) // 48
    return pcm.tobytes()


def camera(index: int, **changes) -> dict:
    """The input of one camera of `TakeWriter` (INTERFACE_NOTES_capture.md)."""
    out = {
        "camera_key": None,
        "key_origin": "computed",
        "user_name": "Fake camera A" if index == 0 else None,
        "device": {
            "model": f"Synthetic Camera Model {index}", "os_name": f"Synthetic Camera {index}", "vendor_id": "ffff",
            "product_id": f"{index + 1:04x}", "serial": "FAKE-SERIAL-A" if index == 0 else None,
            "port_path": f"FAKE-PORT-{index}", "os_device_id": None, "backend": "media_foundation", "os_index": index,
        },
        "requested": {"width": WIDTH, "height": HEIGHT, "framerate": 30, "capture_format": "MJPG", "exposure_mode": "manual"},
        "controls": {"exposure_us": {"value": 4000, "auto": False}},
        "exposure_step": None,
        "nominal_rate": "30/1",
        "display_rotation": 0,
    }  # fmt: skip
    out.update(changes)
    return out


def microphone(channels: int = 1) -> dict:
    return {"device_name": "Synthetic Microphone", "host_api": "Windows WASAPI", "device_channels": channels}


def record_take(
    writer, folder: Path, cameras: list[dict] | None = None, audio: dict | None = None, *, rec: str = "synthetic_take",
    frames: int = 12, blocks: int = 25, gap_camera: int | None = 1, after=lambda: None, **options,
) -> dict:  # fmt: skip
    """Record a small synthetic take with `TakeWriter` and close it. Return the input, for the checks.

    Each camera gets `frames` JPEG frames. Camera `gap_camera` loses one source frame before position 5.
    The audio gets `blocks` blocks of 4,800 samples, with a click at sample 4,207 and then each 24,000.
    `after` is called after the take starts and after each write call (SFT-730).
    """
    cameras = [camera(0), camera(1)] if cameras is None else cameras
    take = writer.TakeWriter(folder, rec, cameras, audio, writer=WRITER, **options)
    after()
    start = take.take_start_host_ns
    sent = {"start": start, "jpegs": [[] for _ in cameras], "arrival_ns": [[] for _ in cameras], "source": [[] for _ in cameras]}
    for position in range(frames):
        for index in range(len(cameras)):
            data = jpeg(position, colour=(30 + 40 * index, 40, 80))
            number = 1000 + position + (1 if index == gap_camera and position >= 5 else 0)
            arrival = 33_333_333 * (position + 1) + 1000 * index
            take.write_frame(index, data, start + arrival, source_frame_number=number, sample_ns=start + arrival - 4_000_000)
            after()
            sent["jpegs"][index].append(data)
            sent["arrival_ns"][index].append(arrival)
            sent["source"][index].append(number)
    if audio is not None:
        channels = min(audio["device_channels"], 2)
        sent["clicks"] = list(range(4207, 4800 * blocks - 48, 24000))
        pcm = click_pcm(4800 * blocks, sent["clicks"], channels)
        size = 4800 * 2 * channels
        for block in range(blocks):
            host = 100_000_000 * (block + 1) + 14_000_000
            take.write_audio(pcm[block * size : (block + 1) * size], start + host, adc_ns=start + host - 2_000_000)
            after()
    take.close()
    return sent


def media_files(folder: Path, suffix: str) -> list[Path]:
    return sorted((folder / MEDIA).glob(f"*{suffix}"))


def load_json(path: Path) -> dict:
    return json.loads(path.read_bytes())


def capture_info_of(folder: Path) -> dict:
    manifest = load_json(folder / MANIFEST)
    return load_json(folder / f"{manifest['recording_name']}_info.json")


# ---------------------------------------------------------------- SFT-700: text files, integers, JSON, IDs, CRCs

MANIFEST_MEMBERS = [
    "skellyfileformat", "format_version", "format_prerelease", "writer", "take_uuid", "recording_name", "purpose",
    "state", "cameras", "audio", "calibration", "files", "warnings", "privacy", "summary",
]  # fmt: skip
MANIFEST_CAMERA = ["camera_key", "camera_label", "group_position", "video", "timing", "calibration_camera"]
MANIFEST_FILE = ["path", "role", "owner", "sha256"]
MANIFEST_WARNING = ["code", "source", "camera_key", "detail"]
SUMMARY = ["take_start_utc", "duration_s", "cameras", "audio", "calibration", "processing_runs", "warnings"]
SUMMARY_CAMERA = [
    "camera_label", "user_name", "model", "stored_px", "display_rotation", "nominal_fps", "gaps", "filled", "exposure_us",
]  # fmt: skip
SUMMARY_AUDIO = ["file", "sample_rate", "channels", "duration_s"]
CAPTURE_INFO = ["skellyfileformat", "format_version", "format_prerelease", "writer", "take_uuid", "camera_configs", "audio"]
CAMERA_CONFIG = ["camera_label", "user_name", "key_origin", "device", "requested", "controls", "exposure_step"]
DEVICE = ["model", "os_name", "vendor_id", "product_id", "serial", "port_path", "os_device_id", "backend", "os_index"]
REQUESTED = ["width", "height", "framerate", "capture_format", "exposure_mode"]
CAPTURE_AUDIO = ["device_name", "host_api", "device_channels"]
PROCESSING_INFO = ["skellyfileformat", "format_version", "format_prerelease", "writer", "take_uuid", "processed"]
PROCESSED = [
    "schema_version", "parquet_sha256", "recording_id", "parquet", "selected_run_id", "runs", "conventions",
    "export_inventories",
]  # fmt: skip
# The integer members of the manifest, the capture info JSON and the processing info JSON. A general
# rule is not possible: a text member can hold only digits (a serial, or `visibility` in G3).
INTEGER_MEMBERS = {
    "format_prerelease", "group_position", "os_index", "width", "height", "device_channels", "sample_rate", "channels",
    "display_rotation", "gaps", "filled", "schema_version", "selected_run_id", "sample_count",
}  # fmt: skip


def number_text(value: float) -> str:
    """The form of RFC 8785 for a number that is not an integer, from 1e-6 to 1e21."""
    return format(Decimal(repr(value)), "f")


def _check_json_text(path: Path, text: str) -> dict:
    def integer(literal: str) -> int:
        assert INTEGER.fullmatch(literal), f"{path.name}: the integer {literal} has the form of SFF-702"
        return int(literal)

    def other(literal: str) -> float:
        value = float(literal)
        assert not value.is_integer(), f"{path.name}: {literal} has an integer value and must have no fraction (SFF-702)"
        assert literal == number_text(value), f"{path.name}: {literal} is not the shortest form (SFF-702)"
        return value

    value = json.loads(text, parse_int=integer, parse_float=other)
    assert isinstance(value, dict), f"{path.name} has one object at the top (SFF-702)"

    def walk(node, key=None):
        if isinstance(node, dict):
            for name, child in node.items():
                walk(child, name)
        elif isinstance(node, list):
            for child in node:
                walk(child, key)
        elif key in INTEGER_MEMBERS:
            assert node is None or type(node) is int, f"{path.name}: the member {key} is an integer in a string (SFF-702)"

    walk(value)
    return value


def members(value: dict, expected: list[str], where: str) -> None:
    assert list(value) == expected, f"{where} has the members of its section, in order"


def check_manifest_members(manifest: dict) -> None:
    members(manifest, MANIFEST_MEMBERS, "the manifest")
    for item in manifest["cameras"]:
        members(item, MANIFEST_CAMERA, "a manifest camera")
    for item in manifest["files"]:
        members(item, MANIFEST_FILE, "a manifest file")
    for item in manifest["warnings"]:
        members(item, MANIFEST_WARNING, "a manifest warning")
    members(manifest["summary"], SUMMARY, "the summary")
    for item in manifest["summary"]["cameras"]:
        members(item, SUMMARY_CAMERA, "a summary camera")
    if manifest["summary"]["audio"] is not None:
        members(manifest["summary"]["audio"], SUMMARY_AUDIO, "the summary audio")


def check_capture_info_members(info: dict) -> None:
    members(info, CAPTURE_INFO, "the capture info JSON")
    for config in info["camera_configs"].values():
        members(config, CAMERA_CONFIG, "a camera config")
        members(config["device"], DEVICE, "a device")
        members(config["requested"], REQUESTED, "requested")
    if info["audio"] is not None:
        members(info["audio"], CAPTURE_AUDIO, "the capture info audio")


def _uuids(node, found: list) -> None:
    if isinstance(node, dict):
        for name, child in node.items():
            if name in ("take_uuid", "calibration_uuid") and isinstance(child, str):
                found.append(child)
            _uuids(child, found)
    elif isinstance(node, list):
        for child in node:
            _uuids(child, found)


def check_text_conventions(folder: Path) -> None:
    """SFT-700, for each CSV, JSON and TOML file of a take folder outside `exports/`."""
    uuids: list[str] = []
    paths = [p for p in sorted(folder.rglob("*")) if p.suffix in (".csv", ".json", ".toml") and "exports" not in p.parts]
    assert paths
    for path in paths:
        data = path.read_bytes()
        assert not data.startswith(b"\xef\xbb\xbf"), f"{path.name} has no BOM (SFF-700)"
        assert b"\r" not in data, f"{path.name} has LF line ends (SFF-700)"
        text = data.decode("utf-8")
        if path.suffix == ".toml":
            _uuids(tomllib.loads(text), uuids)
        elif path.suffix == ".json":
            value = _check_json_text(path, text)
            _uuids(value, uuids)
            kind = value.get("skellyfileformat")
            if kind == "recording_manifest":
                check_manifest_members(value)
            elif kind == "capture_info":
                check_capture_info_members(value)
            elif kind == "processing_info":
                members(value, PROCESSING_INFO, "the processing info JSON")
                members(value["processed"], PROCESSED, "`processed`")
        elif text.startswith("# skellyfileformat="):
            sidecar = read_sidecar(path)
            uuids.append(sidecar.header["take_uuid"])
            for key, value in sidecar.header.items():
                if key in INTEGER_KEYS or (key in INTEGER_OR_EMPTY_KEYS and value):
                    assert INTEGER.fullmatch(value), f"{path.name}: {key}={value} has the form of SFF-701"
            for part in sidecar.header.get("nominal_rate", "1/1").split("/"):
                assert INTEGER.fullmatch(part), f"{path.name}: nominal_rate has the form of SFF-701"
            assert not sidecar.bad_crc, f"{path.name}: each row has a correct CRC (SFF-704)"
            for row in sidecar.rows:
                assert HEX8.fullmatch(row["crc32"]), f"{path.name}: a CRC is 8 lowercase hexadecimal characters (SFF-704)"
                for column, value in row.items():
                    if column != "crc32":
                        # A time is an integer, relative to the take start. An absent value is an empty field (SFF-705).
                        assert value == "" or INTEGER.fullmatch(value), f"{path.name}: {column}={value}"
                assert all(row[column] != "" for column in ("arrival_ns", "host_ns", "flags") if column in row)
            for line in sidecar.footer:
                word, values = footer_values(line, sidecar.kind)
                for key, value in values.items():
                    if word in ("fit_segment", "end") or key in ("cut_bytes", "media_cut_bytes"):
                        assert INTEGER.fullmatch(value), f"{path.name}: {key}={value} has the form of SFF-701"
    for value in uuids:
        assert UUID4.fullmatch(value), f"{value} is 32 lowercase hexadecimal characters of a UUID version 4 (SFF-703)"


# ---------------------------------------------------------------- SFT-705: names and layout

RESERVED = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}
SUBFOLDERS = {MEDIA, "annotated_videos", "exports", "blender", "logs"}
LABEL = re.compile(r"[0-9a-f]{6,8}|cam[0-9]+")


def check_rec(rec: str) -> None:
    """SFF-715."""
    assert 1 <= len(rec.encode("utf-8")) <= 128
    assert not any(ord(c) < 32 or c == "\x7f" or c in './\\:*?"<>|' for c in rec)
    assert rec == rec.strip(" ") and rec.upper() not in RESERVED


def check_names_and_layout(folder: Path, label_length: int | None = 6) -> None:
    """SFT-705: each file has the name and the place of section 4. `label_length` None accepts `cam<N>` labels."""
    rec = load_json(folder / MANIFEST)["recording_name"]
    check_rec(rec)
    root_names = {
        MANIFEST, LOCK, f"{rec}_info.json", f"{rec}_recording_info.json", f"{rec}_camera_calibration.toml",
        f"{rec}_data.parquet", f"{rec}_realtime_journal.bin", f"{rec}.blend",
    }  # fmt: skip
    for path in folder.iterdir():
        if path.is_dir():
            assert path.name in SUBFOLDERS, f"the subfolder {path.name} is in the layout of section 4"
        else:
            assert path.name in root_names, f"the root file {path.name} has a name of section 4"
    labels = []
    for path in (folder / MEDIA).iterdir():
        assert path.is_file() and path.name.startswith(rec + "."), f"{path.name} starts with <rec>"
        label, _, suffix = path.name[len(rec) + 1 :].rpartition(".")
        assert (label == "audio" and suffix in ("m4a", "csv")) or (LABEL.fullmatch(label) and suffix in ("mkv", "csv")), path.name
        if label != "audio":
            labels.append(label)
            other = "csv" if suffix == "mkv" else "mkv"
            assert path.with_suffix("." + other).is_file(), f"{path.name} has its {other} file"
    if label_length is not None:
        assert all(re.fullmatch(f"[0-9a-f]{{{label_length}}}", label) for label in labels), f"each label has {label_length} characters"
    assert len(set(labels)) * 2 == len(labels), "each label is different (SFF-720)"
    assert not list(folder.rglob("synchronized_videos_README.md")), "no synchronized_videos_README.md exists (SFF-722)"


# ---------------------------------------------------------------- SFT-708: the manifest

HASHED_ROLES = {"capture_info", "processing_info", "blend", "blender_output", "annotated_video"}
NULL_HASH_ROLES = {"tracking", "export", "realtime_journal", "log"}


def thousandths(n: int) -> float:
    return n / 1000


def check_manifest(folder: Path) -> dict:
    """SFT-708: the members of the manifest, the `sha256` of each `files` item and the summary (SFF-723, SFF-728)."""
    manifest = load_json(folder / MANIFEST)
    check_manifest_members(manifest)
    assert manifest["skellyfileformat"] == "recording_manifest" and manifest["state"] in ("recording", "finished")
    assert [item["group_position"] for item in manifest["cameras"]] == list(range(len(manifest["cameras"])))
    assert [item["path"] for item in manifest["files"]] == sorted(item["path"] for item in manifest["files"])
    for item in manifest["files"]:
        if item["role"] in HASHED_ROLES:
            assert item["sha256"] == hashlib.sha256((folder / item["path"]).read_bytes()).hexdigest(), item["path"]
        else:
            assert item["role"] in NULL_HASH_ROLES and item["sha256"] is None, item["path"]
    summary = manifest["summary"]
    assert summary["warnings"] == sorted({item["code"] for item in manifest["warnings"]})
    info = capture_info_of(folder)
    recording = manifest["state"] == "recording"
    last_arrivals = []
    assert len(summary["cameras"]) == len(manifest["cameras"])
    for item, camera_summary in zip(manifest["cameras"], summary["cameras"]):
        sidecar = read_sidecar(folder / item["timing"])
        key = item["camera_key"]
        config = info["camera_configs"][key if key != "0" else f"0:{item['camera_label']}"]
        num, den = (int(part) for part in sidecar.header["nominal_rate"].split("/"))
        expected = {
            "camera_label": item["camera_label"],
            "user_name": config["user_name"],
            "model": config["device"]["model"],
            "display_rotation": int(sidecar.header["display_rotation"]),
            "nominal_fps": thousandths((2000 * num + den) // (2 * den)),
            "exposure_us": config["controls"].get("exposure_us", {}).get("value"),
            "stored_px": None, "gaps": None, "filled": None,
        }  # fmt: skip
        if not recording:
            (end,) = sidecar.lines("end")
            mkv = (folder / item["video"]).read_bytes()
            first = parse_mkv(mkv).blocks[0]
            width, height = jpeg_size(mkv[first.offset : first.offset + first.size])
            expected.update(stored_px=f"{width}x{height}", gaps=int(end["gaps"]), filled=int(end["filled"]))
            last_arrivals.append(int(sidecar.rows[-1]["arrival_ns"]))
        assert camera_summary == expected, f"the summary of camera {item['camera_label']} has the values of SFF-728"
    duration = None
    audio = manifest["audio"]
    if audio is None:
        assert summary["audio"] is None
    else:
        sidecar = read_sidecar(folder / audio["timing"])
        rate = int(sidecar.header["sample_rate"])
        if not recording:
            samples = int(sidecar.lines("end")[0]["samples"])
            duration = thousandths((2000 * samples + rate) // (2 * rate))
        expected = {"file": audio["audio"], "sample_rate": rate, "channels": int(sidecar.header["channels"]), "duration_s": duration}
        assert summary["audio"] == expected, "the summary has the `audio` object of SFF-728"
    if recording:
        assert summary["duration_s"] is None, "in a manifest with `state` `recording`, `duration_s` is null"
    elif last_arrivals:
        assert summary["duration_s"] == thousandths((max(last_arrivals) + 500_000) // 10**6)
    else:
        assert summary["duration_s"] == duration, "a take with no camera uses the audio value"
    return manifest


# ---------------------------------------------------------------- SFT-711: the camera file


def check_camera_file(mkv_path: Path) -> Mkv:
    """SFT-711: one `V_MJPEG` track, one keyframe SimpleBlock for each frame, index timestamps, no rotation."""
    data = mkv_path.read_bytes()
    sidecar = read_sidecar(mkv_path.with_suffix(".csv"))
    mkv = parse_mkv(data)
    assert mkv.doc_type == "matroska"
    assert len(mkv.tracks) == 1 and mkv.tracks[0]["codec"] == "V_MJPEG" and mkv.tracks[0]["type"] == 1, "one V_MJPEG track"
    assert mkv.tracks[0]["number"] < 128
    assert BLOCK_GROUP not in mkv.ids and len(mkv.blocks) == len(sidecar.rows), "one SimpleBlock for each frame"
    num, den = (int(part) for part in sidecar.header["nominal_rate"].split("/"))
    assert mkv.timestamp_scale == 1_000_000
    assert mkv.tracks[0]["default_duration"] == 10**9 * den // num, "DefaultDuration is the frame period, rounded down"
    for position, block in enumerate(mkv.blocks):
        assert block.track == mkv.tracks[0]["number"]
        assert block.flags & 0x80 and not block.flags & 0x06, "each block is a keyframe and has no lacing (SFF-733)"
        assert block.timestamp == container_ms(position, num, den), "the timestamps are the index timestamps of SFF-736"
        payload = data[block.offset : block.offset + block.size]
        assert exif_orientation(payload) is None, "no EXIF orientation exists (SFF-735)"
        # The input of the tests has no APPn segment but JFIF. So any other APPn segment is added data (SFF-737).
        assert all(marker == APP0 for marker, _, _ in jpeg_segments(payload) if 0xE0 <= marker <= 0xEF)
    assert not {PROJECTION, 0x7671, 0x7672, 0x7673, 0x7674, 0x7675} & mkv.ids, "no rotation element exists (SFF-735)"
    assert count_packets(mkv_path) == len(sidecar.rows), "FFmpeg counts the frames of the sidecar"
    return mkv


def check_no_overlay_file(folder: Path) -> None:
    """SFT-711: the take folder of a capture holds only the files that the capture writer writes."""
    rec = load_json(folder / MANIFEST)["recording_name"]
    allowed = {MANIFEST, LOCK, f"{rec}_info.json", MEDIA}
    assert {path.name for path in folder.iterdir()} <= allowed
    assert all(path.suffix in (".mkv", ".csv", ".m4a") for path in (folder / MEDIA).iterdir())


# ---------------------------------------------------------------- SFT-715: the common CSV rules


def check_sidecar_common(path: Path) -> Sidecar:
    """SFT-715: the header keys in order, the column line, rows with correct CRCs, the footer forms, `# end` last."""
    sidecar = read_sidecar(path)
    lines = sidecar.data.decode("utf-8").split("\n")
    assert sidecar.torn == 0 and lines[-1] == "", "each line ends with LF"
    keys, columns = (VIDEO_KEYS, VIDEO_COLUMNS) if sidecar.kind == "video" else (AUDIO_KEYS, AUDIO_COLUMNS)
    assert list(sidecar.header) == keys, "the header keys of the kind, in order (SFF-742)"
    assert lines[: len(keys)] == [f"# {key}={value}" for key, value in sidecar.header.items()]
    assert all(re.fullmatch(r"[a-z0-9_]+", key) for key in sidecar.header)
    assert sidecar.columns == columns, "the column line follows the header (SFF-743)"
    assert not sidecar.bad_crc and len(sidecar.rows) == len(sidecar.row_lines), "each row has its fields and a correct CRC"
    assert b'"' not in sidecar.data and b"'" not in sidecar.data, "no field is quoted (SFF-741)"
    assert all(" " not in line for line in sidecar.row_lines), "a field holds no space"
    assert sidecar.footer and sidecar.footer[-1].startswith("# end "), "the `# end` line is last (SFF-745)"
    assert len(keys) + 1 + len(sidecar.rows) + len(sidecar.footer) == len(lines) - 1, "no row follows a footer line"
    for line in sidecar.footer:
        footer_values(line, sidecar.kind)  # the keys in the order of the spec, with single spaces
        assert "  " not in line.split("fitter_params=")[0].split("repair_writer=")[0]
    return sidecar


# ---------------------------------------------------------------- SFT-717: the video sidecar


def identity_key(device: dict) -> str:
    """`camera_key` of the first of the forms 1, 2 and 3 of SFF-752 that applies."""
    start = f"{device['vendor_id'] or '0000'}:{device['product_id'] or '0000'}"
    if device["serial"] is not None:
        identity = f"{start}:serial:{device['serial']}"
    elif device["port_path"] is not None:
        identity = f"{start}:port:{device['port_path']}"
    else:
        identity = f"{start}:device:{device['os_device_id']}"
    return hashlib.sha256(identity.encode("utf-8")).digest()[:8].hex()


def check_video_sidecars(folder: Path, capture: bool = True) -> list[Sidecar]:
    """SFT-717: the take keys, the camera keys, the rows, the flags and the `# end` counts of a finished take."""
    sidecars = [read_sidecar(path) for path in media_files(folder, ".csv")]
    videos = [s for s in sidecars if s.kind == "video"]
    assert all([s.header[key] for key in TAKE_KEYS] == [sidecars[0].header[key] for key in TAKE_KEYS] for s in sidecars), (
        "the take keys are equal in each sidecar (SFF-749)"
    )
    configs = capture_info_of(folder)["camera_configs"]
    keys = [s.header["camera_key"] for s in videos]
    assert len(set(keys)) == len(keys), "no two cameras of a take have the same `camera_key`"
    for sidecar in videos:
        key = sidecar.header["camera_key"]
        if capture:
            assert key != "0", "`camera_key` is not 0 for skellycam"
            config = configs[key]
            if config["key_origin"] == "computed":
                assert key == identity_key(config["device"]), "a computed key is the hash of the identity string"
            else:
                assert config["key_origin"] in ("confirmed_by_user", "assigned") and HEX16.fullmatch(key) and int(key, 16)
        assert sidecar.integers("frame") == list(range(len(sidecar.rows))), "the rows count from 0"
        numbers, flags = sidecar.integers("source_frame_number"), sidecar.integers("flags")
        for k, flag in enumerate(flags):
            before = numbers[k - 1] if k else None
            known = k > 0 and numbers[k] is not None and before is not None
            assert bool(flag & GAP) == (known and numbers[k] not in (before, before + 1)), f"the flag `gap` of row {k}"
            assert bool(flag & REPEAT) == (known and numbers[k] == before), f"the flag `repeat` of row {k}"
            assert flag & ~(GAP | FILLED | ENCODE_SKIP | REPEAT) == 0
        (end,) = sidecar.lines("end")
        counts = [len(flags), *(sum(1 for flag in flags if flag & bit) for bit in (GAP, FILLED, ENCODE_SKIP))]
        assert [int(end[key]) for key in ("rows", "gaps", "filled", "encode_skips")] == counts, "the `# end` counts agree"
    assert len({len(s.rows) for s in videos}) == 1, "each camera file of the take has the same number of rows"
    return sorted(videos, key=lambda s: int(s.header["group_position"]))


# ---------------------------------------------------------------- SFT-720: the audio file and its sidecar


def check_audio_pair(m4a_path: Path) -> Mp4:
    """SFT-720: the boxes of SFF-760, the fragments, `dOps`, the `mfra` box, and the rows and counts of the sidecar."""
    mp4 = parse_mp4(m4a_path.read_bytes())
    sidecar = read_sidecar(m4a_path.with_suffix(".csv"))
    count = len(mp4.fragments)
    assert mp4.kinds == [b"ftyp", b"moov"] + [b"moof", b"mdat"] * count + [b"mfra"], "moof and mdat pairs, then mfra"
    assert mp4.traks == 1 and mp4.mvex and mp4.entry == b"Opus" and mp4.moov_samples == 0 and mp4.timescale == 48000
    for fragment in mp4.fragments:
        assert fragment["trafs"] == 1 and fragment["truns"] == 1 and fragment["tfdt_version"] == 1
        assert fragment["tfhd_flags"] & 0x020000, "tfhd has the flag default-base-is-moof"
    assert mp4.fragments[0]["tfdt"] == 0
    assert all(abs(fragment["samples"] - 48000) <= 960 for fragment in mp4.fragments[:-1]), "fragments of about 1 s"
    assert mp4.fragments[-1]["samples"] <= 48000 + 960
    assert mp4.channels in (1, 2) and mp4.channels == int(sidecar.header["channels"])
    assert mp4.output_gain == 0 and mp4.pre_skip > 0, "`dOps` has output gain 0 and a pre-skip"
    firsts, sizes, flags = (sidecar.integers(column) for column in ("first_sample", "n_samples", "flags"))
    assert firsts[0] == 0 and all(firsts[k] == firsts[k - 1] + sizes[k - 1] for k in range(1, len(firsts))), "contiguous rows"
    assert sidecar.integers("block") == list(range(len(firsts)))
    (end,) = sidecar.lines("end")
    silent = [size for size, flag in zip(sizes, flags) if flag & SILENCE]
    assert [int(end[key]) for key in ("rows", "samples", "gaps", "silence_samples")] == [len(firsts), sum(sizes), len(silent), sum(silent)]
    assert all(flag & ~(OVERFLOW | SILENCE) == 0 for flag in flags)
    return mp4


# ---------------------------------------------------------------- SFT-726: the fit


def check_fit(path: Path) -> None:
    """SFT-726: one `# fit` line, and segments that hold each position or row, in order, with no gap or overlap."""
    sidecar = read_sidecar(path)
    assert sidecar.finished
    fit_lines = [line for line in sidecar.footer if line.startswith("# fit ")]
    assert len(fit_lines) == 1, "a finished sidecar has one `# fit` line"
    match = re.fullmatch(r"# fit fitter=[^ ]+ fitter_version=[^ ]+ fitter_params=(.*)", fit_lines[0])
    assert match, "`fitter_params` is the last key of the `# fit` line"
    assert isinstance(json.loads(match.group(1)), dict), "`fitter_params` is a JSON object on one line"
    first, last, period = ("pos_first", "pos_last", "period_ps") if sidecar.kind == "video" else ("row_first", "row_last", "period_fs")
    segments = sidecar.lines("fit_segment")
    assert segments and sidecar.footer.index(fit_lines[0]) < min(i for i, line in enumerate(sidecar.footer) if line.startswith("# fit_segment"))
    expected = 0
    for segment in segments:
        assert int(segment[first]) == expected and int(segment[last]) >= expected, "no gap and no overlap"
        assert int(segment[period]) > 0
        expected = int(segment[last]) + 1
        if sidecar.kind == "audio":
            assert int(segment["n0"]) == int(sidecar.rows[int(segment[first])]["first_sample"])
    assert expected == len(sidecar.rows), "the segments hold each position or row"


# ---------------------------------------------------------------- SFT-703: the version fields


def check_version_fields(folder: Path, prerelease: int = 1) -> None:
    """SFT-703: `format_version` 2.0, `format_prerelease` and `writer` in each file of SFF-707 that the folder holds.

    The Parquet descriptor and the journal header are not in this check: checks_folder.py has their parsers.
    """
    values = []
    for path in sorted(folder.rglob("*")):
        if "exports" in path.parts or "blender" in path.parts or not path.is_file():
            continue
        data = path.read_bytes()
        if path.suffix == ".csv" and data.startswith(b"# skellyfileformat="):
            values.append((path.name, read_sidecar(path).header))
        elif path.suffix == ".json" and path.parent == folder:
            values.append((path.name, json.loads(data)))
        elif path.suffix == ".toml":
            values.append((path.name, tomllib.loads(data.decode("utf-8"))["metadata"]))
        elif path.suffix in (".mkv", ".m4a"):
            sidecar = read_sidecar(path.with_suffix(".csv"))
            for text in ("format_version", "format_prerelease", "skellyfileformat", sidecar.header["writer"]):
                assert text.encode() not in data, f"{path.name} holds no version field and no writer string (SFF-707)"
    assert values
    for name, value in values:
        assert value.get("format_version") == "2.0", f"{name} has `format_version` 2.0"
        assert int(value.get("format_prerelease", -1)) == prerelease, f"{name} has `format_prerelease` {prerelease} (SFF-710)"
        assert value.get("writer"), f"{name} has a `writer`"


# ---------------------------------------------------------------- SFT-713: the unusual camera file

UNUSUAL_KEY = hashlib.sha256(b"ffff:0001:port:FAKE-PORT-0").digest()[:8].hex()
UNUSUAL_TAKE_UUID = "00000000000040008000000000000713"
UNUSUAL_FRAMES = 8


def unusual_jpegs() -> list[bytes]:
    """Frames that test SFF-738: no JFIF, no DHT, an EXIF orientation tag (6: rotate by 90) and trailing bytes."""
    out = []
    for position in range(UNUSUAL_FRAMES):
        data = jpeg_without(jpeg(position), {APP0, DHT})
        out.append(data[:2] + exif_segment(6) + data[2:] + bytes(7))
    return out


def build_unusual_take(folder: Path) -> tuple[str, list[bytes], list[int]]:
    """Write the take of SFT-713: one camera pair and no other file. Return (name, stored frames, track bytes)."""
    jpegs = unusual_jpegs()
    track_bytes = [1 + position % 2 for position in range(len(jpegs))]
    data = build_mkv(jpegs, WIDTH, HEIGHT, track_bytes)
    label = UNUSUAL_KEY[:6]
    media = folder / MEDIA
    media.mkdir(parents=True)
    (media / f"sft713.{label}.mkv").write_bytes(data)
    header = {
        "skellyfileformat": "video_timing", "format_version": "2.0", "format_prerelease": 1, "writer": "sft713 1.0.0",
        "take_uuid": UNUSUAL_TAKE_UUID, "take_start_host_ns": 1000000000000, "take_start_utc_ns": 946684800000000000,
        "utc_offset_min": 0, "clock": "windows_qpc", "clock_hz": 10000000, "group_size": 1, "audio_count": 0,
        "group_position": 0, "camera_key": UNUSUAL_KEY, "camera_label": label, "nominal_rate": "30/1", "display_rotation": 0,
    }  # fmt: skip
    lines = [f"# {key}={value}" for key, value in header.items()] + [",".join(VIDEO_COLUMNS)]
    text = "".join(line + chr(10) for line in lines)
    for position, block in enumerate(parse_mkv(data).blocks):
        text += row_line([position, 100 + position, 33_400_000 * (position + 1), None, 0, block.offset, block.size])
    footer = [
        "# fit fitter=sft713 fitter_version=1.0.0 fitter_params={}",
        f"# fit_segment pos_first=0 pos_last={len(jpegs) - 1} t0_ns=33000000 period_ps=33400000000",
        f"# end rows={len(jpegs)} gaps=0 filled=0 encode_skips=0",
    ]
    text += "".join(line + chr(10) for line in footer)
    (media / f"sft713.{label}.csv").write_bytes(text.encode())
    return f"{MEDIA}/sft713.{label}.mkv", jpegs, track_bytes


# ---------------------------------------------------------------- the two readers and the scopes

IMPLS = ["python_full", "python_player", "js"]


def scope_of(impl: str) -> str:
    return "full" if impl == "python_full" else "player"


def result_bytes(impl: str, reader, js_reader, folder: Path) -> bytes:
    """The canonical result with records, from the Python reader (two scopes) or from the JavaScript reader."""
    if impl == "js":
        return js_reader(folder, records=True)
    return read_bytes(reader, folder, True, scope_of(impl))


_AUDIT: dict = {"events": None, "installed": False}


def _audit_hook(event: str, args) -> None:
    events = _AUDIT["events"]
    if events is not None and event in AUDIT_EVENTS:
        events.append((event, str(args[0]) if args else ""))


AUDIT_EVENTS = {"glob.glob", "glob.glob/2", "pathlib.Path.glob", "pathlib.Path.rglob", "os.listdir", "os.scandir"}
GLOB_EVENTS = AUDIT_EVENTS - {"os.listdir", "os.scandir"}


@contextlib.contextmanager
def audit():
    """Collect the audit events of Python for a folder listing and for a glob search, as (event, path)."""
    if not _AUDIT["installed"]:
        sys.addaudithook(_audit_hook)  # a hook cannot be removed: it is idle outside this context
        _AUDIT["installed"] = True
    _AUDIT["events"] = events = []
    try:
        yield events
    finally:
        _AUDIT["events"] = None


def sidecars_by_position(folder: Path) -> list[Sidecar]:
    """The video sidecars of a take with a manifest, in order of `group_position`."""
    return [read_sidecar(folder / item["timing"]) for item in load_json(folder / MANIFEST)["cameras"]]


def write_json(path: Path, value: dict) -> None:
    """Write a JSON file in the form of the golden folders: an indent of 2 spaces and one LF at the end."""
    path.write_bytes((json.dumps(value, indent=2, ensure_ascii=False) + chr(10)).encode("utf-8"))


def change_writer(folder: Path, new: str) -> None:
    """Change `writer` in each sidecar, in the manifest and in the capture info JSON of a capture-only take."""
    for path in media_files(folder, ".csv"):
        set_header(path, "writer", new)
    manifest = load_json(folder / MANIFEST)
    manifest["writer"] = new
    for item in manifest["files"]:
        if item["role"] == "capture_info":
            info = load_json(folder / item["path"])
            info["writer"] = new
            write_json(folder / item["path"], info)
            item["sha256"] = hashlib.sha256((folder / item["path"]).read_bytes()).hexdigest()
    write_json(folder / MANIFEST, manifest)


# ---------------------------------------------------------------- SFT-708, SFT-730: the manifest while it records


def check_recording_manifest(folder: Path) -> dict:
    """SFT-708: the manifest of a take that records is complete, with `state` `recording` and the nulls of SFF-728."""
    manifest = load_json(folder / MANIFEST)
    check_manifest_members(manifest)
    assert manifest["state"] == "recording"
    summary = manifest["summary"]
    assert summary["duration_s"] is None
    assert all(item[key] is None for item in summary["cameras"] for key in ("stored_px", "gaps", "filled"))
    assert summary["audio"] is None or summary["audio"]["duration_s"] is None
    return manifest


def check_whole_writes_hold_lock(events: list, paths: list[str]) -> None:
    """Each replace of a whole file is between a `lock` event and an `unlock` event of `.processing.lock`."""
    held, replaced = False, []
    for event, path in events:
        if path == LOCK and event in ("lock", "unlock"):
            assert held == (event == "unlock"), "the lock events are in pairs"
            held = event == "lock"
        elif event == "replace":
            assert path in paths, f"only a whole file is replaced: {path}"
            assert held, f"the writer holds {LOCK} while it replaces {path} (SFF-789)"
            replaced.append(path)
        elif path in paths:
            raise AssertionError(f"a whole file is not written in place: {event} {path} (SFF-786)")
    assert not held and set(replaced) == set(paths)


def check_killed_folder(folder: Path) -> None:
    """SFT-730: after a kill, each whole file is complete or absent, with at most a `.tmp`, and each live file is a valid prefix."""
    for path in folder.iterdir():
        name = path.name.removesuffix(".tmp")
        assert name in (MANIFEST, LOCK, MEDIA) or name.endswith("_info.json"), f"{path.name} is a file of a capture"
        if path.name == MANIFEST:
            manifest = load_json(path)
            check_manifest_members(manifest)
            assert manifest["state"] in ("recording", "finished")
        elif path.name.endswith("_info.json"):
            check_capture_info_members(load_json(path))
    assert (folder / LOCK).stat().st_size == 0, "the lock file is empty (SFF-789)"
    for path in (folder / MEDIA).iterdir() if (folder / MEDIA).is_dir() else []:
        data = path.read_bytes()
        if path.suffix == ".csv":
            sidecar = read_sidecar(path)
            assert not sidecar.bad_crc, f"{path.name}: each complete row has a correct CRC"
            if "skellyfileformat" in sidecar.header:
                keys = VIDEO_KEYS if sidecar.kind == "video" else AUDIO_KEYS
                assert list(sidecar.header) == keys[: len(sidecar.header)], f"{path.name}: the header is a prefix"
            for line in sidecar.footer:
                footer_values(line, sidecar.kind)
        elif path.suffix == ".mkv":
            assert data[:4] == b"\x1a\x45\xdf\xa3"[: len(data)]
            if len(data) > 4:
                assert all(data[block.offset : block.offset + 2] == b"\xff\xd8" for block in parse_mkv(data).blocks)
        else:
            assert path.suffix == ".m4a", path.name
            kinds = [kind for kind, _, _ in boxes(data, 0, len(data))]
            assert re.fullmatch(rb"(ftyp(moov((moofmdat)*(moof)?(mfra)?)?)?)?", b"".join(kinds)), f"{path.name}: {kinds}"


# ---------------------------------------------------------------- SFT-733: repair

REPAIR_LINE = re.compile(r"# repair cut_bytes=(0|[1-9][0-9]*) media_cut_bytes=(0|[1-9][0-9]*) repair_writer=.+")


def check_repaired_files(folder: Path, before: Path) -> None:
    """SFT-733: the sidecars and the audio file of a repaired take, against the files before the repair.

    Each byte before the cut is unchanged. Each sidecar has a fit, a repair line and an `# end` line.
    The audio file is cut after its last complete fragment. The camera file is not in this check:
    its check is provisional (SFF-797).
    """
    sidecars = media_files(folder, ".csv")
    assert sidecars
    for path in sidecars:
        old_path = before / MEDIA / path.name
        old, new = read_sidecar(old_path), check_sidecar_common(path)
        repair_lines = [line for line in new.footer if line.startswith("# repair ")]
        assert len(repair_lines) == 1 and REPAIR_LINE.fullmatch(repair_lines[0]), "the repair line has its three keys, in order"
        assert any(line.startswith("# fit ") for line in new.footer) and new.repaired, "a fit, a repair line and an `# end` line"
        (repair,) = new.lines("repair")
        cut = len(old.data) - int(repair["cut_bytes"])
        assert cut == old.rows_end, "the sidecar is cut after the last complete row with a correct CRC (SFF-795)"
        assert new.data[:cut] == old.data[:cut], "each byte before the cut is unchanged (SFF-794)"
        media = path.with_suffix(".m4a" if new.kind == "audio" else ".mkv")
        old_media, new_media = (before / MEDIA / media.name).read_bytes(), media.read_bytes()
        media_cut = len(old_media) - int(repair["media_cut_bytes"])
        assert new_media[:media_cut] == old_media[:media_cut], "each byte of the media file before the cut is unchanged"
        if new.kind == "audio":
            assert media_cut == parse_mp4(old_media).complete_end, "the audio file is cut after its last complete fragment"


def strip_cut_bytes(data: bytes) -> bytes:
    return re.sub(rb"cut_bytes=[0-9]+ media_cut_bytes=[0-9]+", b"cut_bytes=N media_cut_bytes=N", data)
