"""Golden folder G4 (recording-files/SPEC.md Appendix A): four cameras with `display_rotation` 0, 90, 180 and 270.

Each camera stores frames of 64 x 48 pixels in the orientation of its sensor (SFF-735). The upright
picture of each camera has one colour in each corner. `take.truth.json` holds these colours. A stored
frame is the upright picture after a turn of `display_rotation` degrees counter-clockwise, so the
clockwise turn of SFF-751 gives the upright picture again. The take has no audio.
"""

from __future__ import annotations

import io
from pathlib import Path

from goldgen import capture_cases

TAKE = {
    "rec": "g04_synthetic_take",
    "take_uuid": "00000000000040008000000000000004",
    "take_start_host_ns": 1_000_000_000_000,
    "take_start_utc_ns": 946_684_800_000_000_000,  # 2000-01-01T00:00:00Z
    "utc_offset_min": 0,
    "clock": "windows_qpc",
    "clock_hz": 10_000_000,
}
FRAMES = 6
CORNER_PX = 16  # one MCU of a 4:2:0 JPEG, so the colour of a corner does not mix with the field
UPRIGHT_CORNERS = {
    "top_left": [220, 30, 30], "top_right": [30, 200, 30], "bottom_right": [30, 30, 220], "bottom_left": [220, 220, 30],
}  # fmt: skip


def stored_jpeg(rotation: int, position: int) -> bytes:
    from PIL import Image, ImageDraw

    width, height = (64, 48) if rotation % 180 == 0 else (48, 64)
    upright = Image.new("RGB", (width, height), (60, 60, 60))
    draw = ImageDraw.Draw(upright)
    for corner, colour in UPRIGHT_CORNERS.items():
        x = 0 if corner.endswith("left") else width - CORNER_PX
        y = 0 if corner.startswith("top") else height - CORNER_PX
        draw.rectangle((x, y, x + CORNER_PX - 1, y + CORNER_PX - 1), fill=tuple(colour))
    draw.rectangle((20 + position, 20, 27 + position, 27), fill=(200, 200, 200))  # it moves to the right
    stored = upright.rotate(rotation, expand=True)  # Pillow turns counter-clockwise
    assert stored.size == (64, 48)
    buffer = io.BytesIO()
    stored.save(buffer, "JPEG", quality=90)
    return buffer.getvalue()


def cameras() -> list[dict]:
    return [
        capture_cases.camera(
            index,
            [1000 * (index + 1) + p for p in range(FRAMES)],
            [(0, FRAMES - 1, 33_483_200 - 110_000 * index, 33_333_400_000 - 50_000 * index)],
            sample_ns=index == 0,
            display_rotation=90 * index,
            jpegs=[stored_jpeg(90 * index, p) for p in range(FRAMES)],
        )
        for index in range(4)
    ]


def build(out: Path) -> None:
    files, facts = capture_cases.finished_take(TAKE, cameras(), None)
    capture_cases.write_files(out / "take", files)
    truth = {
        "corner_px": CORNER_PX,
        "cameras": [
            {"name": item["name"], "display_rotation": 90 * index, "upright_corners": UPRIGHT_CORNERS}
            for index, item in enumerate(facts["files"])
        ],
    }
    capture_cases.write_results(out, "take", facts, truth=truth)
