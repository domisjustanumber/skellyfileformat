"""Golden folder G18 (spec/SPEC.md Appendix A): missing frames, in the cases `take` and `no_block`.

`take` is a finished take of three cameras with 12 frames each and no audio (decision 6AT7):

- camera 0: a frame with a capture error at position 4: a `missing` row that keeps the times of the
  frame, with a placeholder block (SFF-756);
- camera 1: the camera stops after position 6, and its process still runs: rows 7 to 11 are
  `missing`, with no times and with placeholder blocks, and the manifest has `camera_dead`;
- camera 2: its process hangs in the write of block 8 and ends. The program completes the pair
  (SFF-894): the camera file ends after block 7, rows 8 to 11 are `missing` with empty byte fields
  and no times, the sidecar has a `# repair` line and no fit line, and the manifest has
  `camera_dead` and `camera_file_short`.

`no_block` has two cameras with 6 frames each (decision 76NN item 13). Row 0 of camera 0 is a
`missing` row with its times. The process of camera 1 hangs before its first block reaches the
file: its camera file holds no Cluster, and each of its rows is `missing` with no block.
"""

from __future__ import annotations

import io
from pathlib import Path

from goldgen import capture_cases, common

TAKE = {
    "rec": "g18_synthetic_take",
    "take_uuid": "00000000000040008000000000000018",
    "take_start_host_ns": 1_000_000_000_000,
    "take_start_utc_ns": 946_684_800_000_000_000,  # 2000-01-01T00:00:00Z
    "utc_offset_min": 0,
    "clock": "windows_qpc",
    "clock_hz": 10_000_000,
}
NO_BLOCK_TAKE = TAKE | {"take_uuid": "00000000000040008000000000000118"}
KILL_CUT_BYTES = 37  # the bytes of the next block that the camera process wrote before it ended
LATTICES = [(33_483_200, 33_333_400_000), (33_133_500, 33_333_333_333), (33_250_000, 33_333_300_000)]


def placeholder(width: int, height: int) -> bytes:
    """The black baseline JPEG of SFF-756, with the size and the sampling factors of `common.jpeg_frame`."""
    from PIL import Image

    buffer = io.BytesIO()
    Image.new("RGB", (width, height), (0, 0, 0)).save(buffer, "JPEG", quality=90)
    return buffer.getvalue()


def cameras(frames: int, missing: list[set], timed: list[bool], fitted: list[bool]) -> list[dict]:
    """Synthetic cameras. A `missing` row keeps its times when its camera is `timed` (SFF-756)."""
    black = placeholder(64, 48)
    made = []
    for index, (rows, keep, fit) in enumerate(zip(missing, timed, fitted)):
        camera = capture_cases.camera(
            index, [(1000, 500, 2000)[index] + p for p in range(frames)], [(0, frames - 1, *LATTICES[index])],
            sample_ns=index == 0, **({} if fit else {"segments": []}),
        )  # fmt: skip
        camera["flags"] = dict.fromkeys(rows, capture_cases.MISSING)
        camera["jpegs"] = [
            black if p in rows else common.jpeg_frame(64, 48, p, camera["shade"], False) for p in range(frames)
        ]
        if not keep:  # the camera gave no frame: no source frame number and no times
            camera["rows"] = [row if p not in rows else (None, None, None) for p, row in enumerate(camera["rows"])]
        made.append(camera)
    return made


def first_cluster(data: bytes) -> int:
    """The offset of the first Cluster element of a camera file."""
    for top_id, top_at, top_size in common.ebml_children(data, 0, len(data)):
        if top_id == common.SEGMENT:
            at = top_at
            for element_id, payload_at, size in common.ebml_children(data, top_at, min(top_at + top_size, len(data))):
                if element_id == common.CLUSTER:
                    return at
                at = payload_at + size
    raise AssertionError("the file has no Cluster")


def complete_short(pair: dict, last_frame: int | None) -> bytes:
    """The completion of SFF-894: cut the camera file after block `last_frame` (or before the first
    Cluster), empty the byte fields of each later row, and give the footer lines."""
    blocks = capture_cases.complete_blocks(pair["before"])
    end = first_cluster(pair["before"]) if last_frame is None else sum(blocks[last_frame])
    assert len(pair["before"]) >= end + KILL_CUT_BYTES, "the muxer gave the next bytes to its output"
    pair["after"] = pair["before"][:end]
    for row in pair["rows"][0 if last_frame is None else last_frame + 1 :]:
        row[5:7] = [None, None]
    pair["lines"] = [common.csv_row(row).encode() for row in pair["rows"]]
    repair = f"# repair cut_bytes=0 media_cut_bytes={KILL_CUT_BYTES} repair_writer={common.WRITER}\n"
    return pair["head"] + b"".join(pair["lines"]) + (repair + capture_cases.end_line("camera", pair["rows"]) + "\n").encode()


def write_case(out: Path, case: str, take: dict, take_cameras: list[dict], dead: dict, short: dict) -> None:
    """`dead`: {index: (last_frame, reason)} for `camera_dead`. `short`: {index: last_frame} of a short file."""
    frames = len(take_cameras[0]["rows"])
    for index in [index for index, last in short.items() if last is None]:
        # With six equal placeholders, the pinned muxer gave no Cluster to its output before `close()`.
        # The stand-in muxes frames instead. The file is cut before the first Cluster, so no frame is in it.
        camera = take_cameras[index]
        camera["jpegs"] = [common.jpeg_frame(64, 48, p, camera["shade"], False) for p in range(frames)]
    pairs = capture_cases.device_pairs(take, take_cameras, None)
    sidecars = {index: complete_short(pairs[index], last) for index, last in short.items()}
    warnings = [
        {"code": "camera_dead", "source": "skellycam", "camera_key": pairs[index]["camera_key"],
         "detail": f"last_frame={'none' if last is None else last} reason={reason}"}
        for index, (last, reason) in dead.items()
    ] + [
        {"code": "camera_file_short", "source": "skellycam", "camera_key": pairs[index]["camera_key"],
         "detail": f"blocks={0 if last is None else last + 1} rows={frames}"}
        for index, last in short.items()
    ]  # fmt: skip  SFF-727: in order of group_position, `camera_dead` first
    files = capture_cases.folder_files(take, take_cameras, pairs, None, [frames] * len(pairs), tuple(warnings))
    items = []
    for index, pair in enumerate(pairs):
        files |= {pair["name"]: pair["after"], pair["timing"]: sidecars.get(index) or capture_cases.finished_sidecar(pair)}
        if index in short:
            items.append(capture_cases.item(pair, "repaired", frames, None))  # SFF-794: each row is usable
        else:
            items.append(capture_cases.item(pair, "finished", frames, pair["segments"]))
    capture_cases.write_files(out / case, files)
    capture_cases.write_results(out, case, capture_cases.take_facts(take, items))


def build(out: Path) -> None:
    take_cameras = cameras(12, [{4}, set(range(7, 12)), set(range(8, 12))], [True, False, False], [True, True, False])
    write_case(out, "take", TAKE, take_cameras, {1: (6, "stopped"), 2: (7, "hang")}, {2: 7})
    no_block = cameras(6, [{0}, set(range(6))], [True, False], [True, False])
    write_case(out, "no_block", NO_BLOCK_TAKE, no_block, {1: (None, "hang")}, {1: None})
