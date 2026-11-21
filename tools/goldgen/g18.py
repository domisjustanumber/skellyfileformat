"""Golden folder G18 (spec/SPEC.md Appendix A): missing frames, in the case `take`.

A finished take of three cameras with 12 frames each and no audio (decision 6AT7):

- camera 0: a frame with a capture error at position 4: a `missing` row that keeps the times of the
  frame, with a placeholder block (SFF-756);
- camera 1: the camera stops after position 6, and its process still runs: rows 7 to 11 are
  `missing`, with no times and with placeholder blocks, and the manifest has `camera_dead`;
- camera 2: its process is killed in the write of block 8. The program completes the pair (SFF-894):
  the camera file ends after block 7, rows 8 to 11 are `missing` with empty byte fields and no times,
  the sidecar has a `# repair` line and no fit line, and the manifest has `camera_dead` and
  `camera_file_short`.
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
FRAMES = 12
ERROR_POSITION = 4  # camera 0
LAST_FRAME = {1: 6, 2: 7}  # the last row that is not `missing`, of cameras 1 and 2
KILL_CUT_BYTES = 37  # the bytes of block 8 that camera 2 wrote before the kill
REASONS = {1: "stopped", 2: "hang"}


def placeholder(width: int, height: int) -> bytes:
    """The black baseline JPEG of SFF-756, with the size and the sampling factors of `common.jpeg_frame`."""
    from PIL import Image

    buffer = io.BytesIO()
    Image.new("RGB", (width, height), (0, 0, 0)).save(buffer, "JPEG", quality=90)
    return buffer.getvalue()


def cameras() -> list[dict]:
    lattices = [(33_483_200, 33_333_400_000), (33_133_500, 33_333_333_333), (33_250_000, 33_333_300_000)]
    made = [
        capture_cases.camera(
            index, [(1000, 500, 2000)[index] + p for p in range(FRAMES)], [(0, FRAMES - 1, *lattices[index])],
            sample_ns=index == 0, **({"segments": []} if index == 2 else {}),
        )
        for index in range(3)
    ]  # fmt: skip
    black = placeholder(64, 48)
    for index, camera in enumerate(made):
        missing = {ERROR_POSITION} if index == 0 else set(range(LAST_FRAME[index] + 1, FRAMES))
        camera["flags"] = dict.fromkeys(missing, capture_cases.MISSING)
        camera["jpegs"] = [
            black if p in missing else common.jpeg_frame(64, 48, p, camera["shade"], False) for p in range(FRAMES)
        ]
        if index:  # the camera gave no frame: no source frame number and no times (SFF-756)
            camera["rows"] = [row if p not in missing else (None, None, None) for p, row in enumerate(camera["rows"])]
    return made


def build(out: Path) -> None:
    take_cameras = cameras()
    pairs = capture_cases.device_pairs(TAKE, take_cameras, None)

    # Camera 2: the kill cut the camera file in block 8, after its row 7. The completion cuts the
    # file after block 7, appends no byte to it, and appends the rows 8 to 11 with no block (SFF-894).
    short = pairs[2]
    blocks = capture_cases.complete_blocks(short["before"])
    end = sum(blocks[LAST_FRAME[2]])
    assert len(short["before"]) >= end + KILL_CUT_BYTES, "the muxer gave block 8 to its output"
    short["after"] = short["before"][:end]
    for row in short["rows"][LAST_FRAME[2] + 1 :]:
        row[5:7] = [None, None]
    short["lines"] = [common.csv_row(row).encode() for row in short["rows"]]

    warnings = [
        {"code": "camera_dead", "source": "skellycam", "camera_key": pairs[index]["camera_key"],
         "detail": f"last_frame={LAST_FRAME[index]} reason={REASONS[index]}"}
        for index in (1, 2)
    ] + [
        {"code": "camera_file_short", "source": "skellycam", "camera_key": short["camera_key"],
         "detail": f"blocks={LAST_FRAME[2] + 1} rows={FRAMES}"}
    ]  # fmt: skip  SFF-727
    files = capture_cases.folder_files(TAKE, take_cameras, pairs, None, [FRAMES] * 3, tuple(warnings))
    for pair in pairs[:2]:
        files |= {pair["name"]: pair["after"], pair["timing"]: capture_cases.finished_sidecar(pair)}
    repair_line = f"# repair cut_bytes=0 media_cut_bytes={KILL_CUT_BYTES} repair_writer={common.WRITER}\n"
    end_line = capture_cases.end_line("camera", short["rows"]) + "\n"
    files |= {short["name"]: short["after"], short["timing"]: short["head"] + b"".join(short["lines"]) + (repair_line + end_line).encode()}

    items = [capture_cases.item(pair, "finished", FRAMES, pair["segments"]) for pair in pairs[:2]]
    items.append(capture_cases.item(short, "repaired", FRAMES, None))  # SFF-794: each row is usable
    capture_cases.write_files(out / "take", files)
    capture_cases.write_results(out, "take", capture_cases.take_facts(TAKE, items))
