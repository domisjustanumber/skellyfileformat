"""SFT-760: skellysync folders (SPEC.md section 19)."""

from __future__ import annotations

import checks_folder as checks
import pytest


@pytest.mark.provisional("the skellysync decisions D-Q, D-FPS, D-HDR, D-DRIFT and D-AUDIO (SFF-862, SFF-863)")
def test_sft_760_skellysync_folder(reader, golden_or_skip):
    """SFT-760 (provisional) Writer and reader: a skellysync folder. Checks: SFF-862, SFF-863."""
    folder = golden_or_skip("G17")
    sidecars = sorted((folder / checks.MEDIA).glob("*.csv"))
    assert sidecars and (folder / "recording_manifest.json").is_file()
    assert all(checks.header(sidecar)["clock"] == "synthetic" for sidecar in sidecars)
    take = checks.the_take(checks.read(reader, folder))
    assert len(take["files"]) == len(sidecars), "the folder holds device pairs"
    assert all("missing_fit" not in item["warnings"] for item in take["files"])
