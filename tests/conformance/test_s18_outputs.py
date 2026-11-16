"""SFT-741 to SFT-745: Blender outputs, annotated videos, exports and logs (SPEC.md section 18)."""

from __future__ import annotations

import checks_folder as checks
import pytest


@pytest.mark.external("Blender addon")
def test_sft_741_blender_outputs():
    """SFT-741 (external: Blender addon) Writer: Blender outputs. Checks: SFF-847, SFF-848, SFF-849. No golden part."""
    checks.not_run_here()


@pytest.mark.external("freemocap")
def test_sft_742_annotated_videos():
    """SFT-742 (external: freemocap) Writer: annotated videos. Checks: SFF-850, SFF-851, SFF-852, SFF-853. No golden part."""
    checks.not_run_here()


@pytest.mark.external("freemocap")
def test_sft_743_exports():
    """SFT-743 (external: freemocap) Writer: exports. Checks: SFF-854 to SFF-859. No golden part: G3 holds no export."""
    checks.not_run_here()


def test_sft_744_hidden_export_files(reader, variant):
    """SFT-744 Reader: hidden export files. Checks: SFF-860."""
    folder = variant("G03")
    (folder / "exports" / ".staging-1").mkdir(parents=True)
    (folder / "exports" / ".staging-1" / "part.csv").write_bytes(b"frame_number\r\n")
    (folder / "exports" / ".publication.json").write_bytes(b"{}\n")
    raw = checks.read_bytes("full", reader, None, folder)
    assert b".staging-1" not in raw and b".publication.json" not in raw and b"part.csv" not in raw


@pytest.mark.external("freemocap")
def test_sft_745_logs():
    """SFT-745 (external: freemocap) Writer: logs. Checks: SFF-861. No golden part."""
    checks.not_run_here()
