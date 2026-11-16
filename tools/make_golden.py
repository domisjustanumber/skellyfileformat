#!/usr/bin/env python3
"""Write or check the golden folders of spec/SPEC.md Appendix A (decision G21H).

Usage::

    uv run --group golden python tools/make_golden.py [--only G01] [--check]

With no switch, the tool writes each golden folder that it knows into ``golden/`` and writes its
``SHA256SUMS``. It deletes the old folder first. ``--only`` selects one folder. ``--check`` changes
no file: it makes each folder again in a temporary directory and compares the sums with the
committed ``SHA256SUMS``. The bytes are the same only on the reference platform (golden/README.md).
"""

from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
from pathlib import Path

from goldgen import common, g01

GOLDEN = Path(__file__).resolve().parents[1] / "golden"
FOLDERS = {"G01": g01.build}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--only", choices=sorted(FOLDERS))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    failed = False
    for name in [args.only] if args.only else sorted(FOLDERS):
        target = GOLDEN / name
        if not args.check:
            shutil.rmtree(target, ignore_errors=True)
            FOLDERS[name](target)
            (target / "SHA256SUMS").write_text(common.sums_text(target), encoding="utf-8", newline="\n")
            print(f"{name}: written")
            continue
        with tempfile.TemporaryDirectory() as temporary:
            FOLDERS[name](Path(temporary) / name)
            new = common.sums_text(Path(temporary) / name).splitlines()
        sums = target / "SHA256SUMS"
        old = sums.read_text(encoding="utf-8").splitlines() if sums.is_file() else []
        different = sorted({line.split("  ", 1)[1] for line in set(new) ^ set(old)})
        print(f"{name}: " + ("the same" if not different else "DIFFERENT: " + ", ".join(different)))
        failed = failed or bool(different)
    return int(failed)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
