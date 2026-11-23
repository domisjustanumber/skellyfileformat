"""Golden folder G2 (recording-files/SPEC.md Appendix A): G1 with stereo audio, in the case `take`.

The take keys, the cameras and the audio rows are those of G1, so each camera file and each video
sidecar has the bytes of G1. The left channel is the audio of G1. The right channel is the same
signal at half the level, so that a test can tell the channels apart.
"""

from __future__ import annotations

import array
from pathlib import Path

from goldgen import capture_cases, common, g01


def build(out: Path) -> None:
    audio = g01.audio()
    left = array.array("h", common.click_pcm(sum(n for _, n, _, _ in audio["rows"]), audio["click_samples"]))
    pcm = array.array("h", bytes(4 * len(left)))
    pcm[0::2], pcm[1::2] = left, array.array("h", [sample // 2 for sample in left])
    audio |= {"channels": 2, "pcm": pcm.tobytes(), "config": audio["config"] | {"device_channels": 2}}
    cameras = g01.cameras()
    files, facts = capture_cases.finished_take(g01.TAKE, cameras, audio)
    capture_cases.write_files(out / "take", files)
    truth = {
        "audio": {"name": facts["files"][-1]["name"], "click_samples": audio["click_samples"], "peaks": [24000, 12000]},
        "cameras": [
            {"name": item["name"], "flash_positions": camera["flash_positions"]}
            for item, camera in zip(facts["files"], cameras)
        ],
    }
    capture_cases.write_results(out, "take", facts, truth=truth)
