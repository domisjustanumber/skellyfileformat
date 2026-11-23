"""Golden folder G8 (recording-files/SPEC.md Appendix A): a renamed take folder, in the case `renamed`.

The case is G3 in a folder with another name: `renamed` in place of `take`. No file inside the take
folder changes (SFF-717). A reader finds `<rec>` in the manifest, not in the folder name, so each
expected result has the bytes of the result of G3 (SFT-706, SFF-718, SFF-824).
"""

from __future__ import annotations

from pathlib import Path

from goldgen import g03


def build(out: Path) -> None:
    g03.build(out)
    for name in ("take", "take.full.json", "take.player.json", "take.truth.json"):
        (out / name).rename(out / name.replace("take", "renamed", 1))
