"""Golden folder G6 (spec/SPEC.md Appendix A): the case `audio_torn_fragment` of G5 after a repair, in
the cases `repaired` and `interrupted_repair`.

No repair tool exists, so this module applies the rules of SPEC.md section 12 (SFF-793 to SFF-798)
to the bytes of G5. A repaired camera pair keeps only the frames with a complete row and a complete
block, so its sidecar and its camera file have the same number of frames. A repaired audio sidecar
keeps only the blocks whose every sample is in a complete fragment (SFF-795). PROVISIONAL, as G5 (decision G21H item 6): the repair of a camera file waits for
desk test DT-R1 (SFF-797).
"""

from __future__ import annotations

import zlib
from pathlib import Path

from goldgen import capture_cases, common, g05

TORN_REPAIR_LINE_BYTES = 20


def repair(pair: dict, sidecar: bytes, media: bytes) -> dict:
    """The parts of the repair of one device pair. It reads the bytes of the crash, not the input of G5."""
    # SFF-795: the sidecar is cut at its first bad row: a row that is not complete or has a wrong CRC.
    assert sidecar.startswith(pair["head"])
    ends = [len(pair["head"])]  # the end of the head and of each good row
    while (end := sidecar.find(b"\n", ends[-1])) >= 0:
        body, _, crc = sidecar[ends[-1] : end].rpartition(b",")
        if b"%08x" % zlib.crc32(body) != crc:
            break
        ends.append(end + 1)
    rows = len(ends) - 1
    if pair["kind"] == "camera":
        # SFF-797: the repair keeps the frames that have a complete row and a complete block, so rows = blocks.
        blocks = capture_cases.complete_blocks(media)
        rows = min(rows, len(blocks))
        media_end = sum(blocks[rows - 1])
    else:
        media_end = capture_cases.complete_fragments(media)[-1][1]  # SFF-796
        # SFF-795 (ADR-7JJJ item 2): the sidecar keeps only the blocks whose every sample is in the kept file.
        rows = capture_cases.whole_blocks(pair["rows"][:rows], capture_cases.held_samples(media[:media_end]))
    at = ends[rows]
    assert sidecar[:at] == pair["head"] + b"".join(pair["lines"][:rows])
    # The fit of the repair is the line that made the rows, as each fit of the golden folders.
    segments = [(s[0], min(s[1], rows - 1), *s[2:]) for s in pair["segments"] if s[0] < rows]
    cuts = {"cut_bytes": len(sidecar) - at, "media_cut_bytes": len(media) - media_end}
    return {
        "media": media[:media_end], "sidecar": sidecar[:at], "rows": rows, "segments": segments, "cuts": cuts,
        "complete": rows,
        "fit_lines": "".join(line + "\n" for line in capture_cases.fit_lines(pair["kind"], segments)).encode(),
        "repair_line": (
            f"# repair cut_bytes={cuts['cut_bytes']} media_cut_bytes={cuts['media_cut_bytes']} "
            f"repair_writer={common.WRITER}\n"
        ).encode(),
        "end_line": (capture_cases.end_line(pair["kind"], pair["rows"][:rows]) + "\n").encode(),
    }  # fmt: skip


def build(out: Path) -> None:
    crashed = g05.crashed_take(torn_audio=True)
    pairs = crashed["pairs"]
    repairs = [repair(pair, crashed["files"][pair["timing"]], crashed["files"][pair["name"]]) for pair in pairs]

    def truth(extra: list[dict]) -> dict:
        entries = [{"name": pair["name"]} | r["cuts"] | e for pair, r, e in zip(pairs, repairs, extra)]
        return {"audio": entries[-1], "cameras": entries[:-1]}

    # `repaired`: the whole repair. The write of the manifest replaces the old `.tmp` file (SFF-786, SFF-793).
    files = {path: data for path, data in crashed["files"].items() if not path.endswith(".tmp")}
    files |= capture_cases.folder_files(g05.TAKE, crashed["cameras"], pairs, crashed["audio"], [r["rows"] for r in repairs])
    items = []
    for pair, r in zip(pairs, repairs):
        files |= {pair["name"]: r["media"], pair["timing"]: r["sidecar"] + r["fit_lines"] + r["repair_line"] + r["end_line"]}
        items.append(capture_cases.item(pair, "repaired", r["rows"], r["segments"], complete=r["complete"]))  # SFF-795
    capture_cases.write_files(out / "repaired", files)
    capture_cases.write_results(out, "repaired", capture_cases.take_facts(g05.TAKE, items), truth=truth([{}] * 4))

    # `interrupted_repair`: a repair does each step for the whole take before the next step: it cuts every
    # media file, then every sidecar, then writes the footer lines of every sidecar, then the manifest
    # (ADR-E68K item 3). This repair cut each file and wrote the fit lines of
    # each sidecar. It stopped in the write of the `# repair` line of camera 2. It wrote no `# end` line
    # and no manifest, so each sidecar is `unfinished` (CAPTURE_VECTORS_CHOICES.md item 6).
    files = dict(crashed["files"])
    tails = [r["repair_line"] for r in repairs[:2]] + [repairs[2]["repair_line"][:TORN_REPAIR_LINE_BYTES], b""]
    items = []
    for pair, r, tail in zip(pairs, repairs, tails):
        files |= {pair["name"]: r["media"], pair["timing"]: r["sidecar"] + r["fit_lines"] + tail}
        torn = 0 if tail.endswith(b"\n") else len(tail)  # SFF-746: a torn footer line
        items.append(capture_cases.item(pair, "unfinished", r["rows"], None, complete=r["complete"], torn_bytes=torn))
    fit = capture_cases.reader_audio_fit(pairs[-1]["rows"][: repairs[-1]["rows"]])
    extra = [{"sidecar_torn_bytes": 0 if tail.endswith(b"\n") else len(tail)} for tail in tails]
    extra[-1]["reader_fit"] = dict(zip(("row_first", "row_last", "n0", "t0_ns", "period_fs"), fit))
    capture_cases.write_files(out / "interrupted_repair", files)
    capture_cases.write_results(
        out, "interrupted_repair", capture_cases.take_facts(g05.TAKE, items), ("stray_tmp",), truth(extra)
    )
