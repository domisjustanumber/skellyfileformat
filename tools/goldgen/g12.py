"""Golden folder G12 (spec/SPEC.md Appendix A): the fit vectors, in the case `take`.

Four cameras with 12 frames each, and audio of 0.4 s of silence:

- camera 0: two fit segments, and one lost source frame before position 3;
- camera 1: a `period_ps` that 1000 does not divide, so SFF-777 rounds down;
- camera 2: a finished sidecar with no fit line;
- camera 3: the flag `encode_skip` in row 0, and the flag `repeat` in row 7, so rows 6 and 7 have
  equal fitted times;
- audio: a `period_fs` that 10^6 does not divide, so SFF-779 rounds down.

Beside the case, `equal_fitted_times.parquet` holds the capture times of camera 3 (SFT-748).
"""

from __future__ import annotations

from pathlib import Path

from goldgen import capture_cases, common
from goldgen import folder_common as fc

TAKE = {
    "rec": "g12_synthetic_take",
    "take_uuid": "00000000000040008000000000000012",
    "take_start_host_ns": 1_000_000_000_000,
    "take_start_utc_ns": 946_684_800_000_000_000,  # 2000-01-01T00:00:00Z
    "utc_offset_min": 0,
    "clock": "windows_qpc",
    "clock_hz": 10_000_000,
}
FRAMES = 12
AUDIO_T0_NS, AUDIO_PERIOD_FS = 12_345_678, 20_833_333_333
BLOCK_SAMPLES, BLOCKS = 4800, 4
EQUAL_TIMES_CAMERA, EQUAL_TIMES_PARQUET = 3, "equal_fitted_times.parquet"


def cameras() -> list[dict]:
    last = FRAMES - 1
    return [
        # The camera stalls after position 5. It starts again later, at another rate.
        capture_cases.camera(
            0, [1000, 1001, 1002, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011, 1012],
            [(0, 5, 33_483_200, 33_333_400_000), (6, last, 400_000_000, 33_366_700_000)],
            sample_ns=True,
        ),
        capture_cases.camera(1, [500 + p for p in range(FRAMES)], [(0, last, 33_133_500, 33_333_333_333)]),
        capture_cases.camera(2, [2000 + p for p in range(FRAMES)], [(0, last, 33_250_000, 33_333_300_000)], segments=[]),
        # The JPEG encoder failed on source frame 300, so the first stored frame has `encode_skip`.
        # Row 0 never has `gap` (SFF-756). The camera gave source frame 307 two times.
        capture_cases.camera(
            3, [301, 302, 303, 304, 305, 306, 307, 307, 308, 309, 310, 311],
            [(0, last, 66_800_000, 33_333_400_000)],
            flags={0: capture_cases.ENCODE_SKIP},
        ),
    ]  # fmt: skip


def audio() -> dict:
    def fitted(n: int) -> int:
        return common.audio_fitted_ns(AUDIO_T0_NS, AUDIO_PERIOD_FS, 0, n)

    return {
        "config": {"device_name": "Synthetic Microphone", "host_api": "Windows WASAPI", "device_channels": 1},
        "t0_ns": AUDIO_T0_NS,
        "period_fs": AUDIO_PERIOD_FS,
        "click_samples": [],
        "rows": [
            (
                b * BLOCK_SAMPLES,
                BLOCK_SAMPLES,
                fitted((b + 1) * BLOCK_SAMPLES) + 2_000_000 + b * 7_919 % 500_009,  # after the last sample
                fitted(b * BLOCK_SAMPLES) + b * 31 % 2_001 - 1_000,
            )
            for b in range(BLOCKS)
        ],
    }


def build(out: Path) -> None:
    files, facts = capture_cases.finished_take(TAKE, cameras(), audio())
    capture_cases.write_files(out / "take", files)
    capture_cases.write_results(out, "take", facts)

    # The Parquet of SFT-748, beside the case: the capture TIMESTAMPS of camera 3, whose rows 6 and 7
    # have equal fitted times. The strict times differ by 1 ns (SFF-782, SFF-828).
    item = facts["files"][EQUAL_TIMES_CAMERA]
    times = [fc.seconds(ns) for ns in fc.strict_ns([record[4] for record in item["records"]])]
    group = fc.sensor_group_name([item["camera_key"]])
    channel = {
        "sensor_group": group, "source": f"camera:{item['camera_label']}", "reference_frame": None,
        "kind": "TIMESTAMPS", "names": ["capture"], "components": {"timestamp_s": "s"}, "stage": "timing",
        "dtype": "float64",
    }  # fmt: skip
    descriptor = {"runs": {"0": {"sensor_groups": {group: {"sample_count": len(times)}}}}}  # only what the vector needs
    fc.write_parquet(out / EQUAL_TIMES_PARQUET, descriptor, [(0, channel, times, lambda frame, n, c: times[frame])])
