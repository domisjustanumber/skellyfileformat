"""Golden folder G5 (recording-files/SPEC.md Appendix A): a crashed take, in the cases `audio_clean_kill` and
`audio_torn_fragment`.

The take is in the state that a loss of power leaves: each live file is a prefix of the bytes that
its writer gave to the operating system (SFF-787), and no file has a normal end. The two cases
differ only in the audio file.

PROVISIONAL (decision G21H item 6): each camera file is a stand-in. It is a prefix of the bytes that
the pinned FFmpeg muxer gave to its output before `close()`. The real bytes of a killed camera file
wait for the desk tests DT-R1 and DT5. recording-files/golden/CAPTURE_VECTORS_CHOICES.md says what the bytes hold.
"""

from __future__ import annotations

import struct
from pathlib import Path

from goldgen import capture_cases, g01

TAKE = {
    "rec": "g05_synthetic_take",
    "take_uuid": "00000000000040008000000000000005",
    "take_start_host_ns": 1_000_000_000_000,
    "take_start_utc_ns": 946_684_800_000_000_000,  # 2000-01-01T00:00:00Z
    "utc_offset_min": 0,
    "clock": "windows_qpc",
    "clock_hz": 10_000_000,
}
# The muxer gives a Cluster of 5 frames to its output when frame 5 of the next Cluster arrives. So 26
# frames give the offsets of blocks 0 to 24. No file of the take holds more than 22 rows or 20 blocks.
MUXED = 26
AUDIO_BLOCKS = 21  # 2.1 s: the muxer gave two fragments of 1 s to its output
# ADR-3GWN, ADR-SM53 item 4: ns added to `adc_ns` of rows that are after the cut of `records` in both cases (19 and 9
# blocks), so the reader fit from all rows (SFF-784) differs from a fit from the rows of `records`.
AUDIO_JITTER_NS = {19: -25_000, 20: 40_000}
TORN_ROW_BYTES = 37
# For each camera: the rows that the writer wrote, and the end of the camera file. `in_block` k is a
# cut 100 bytes into the JPEG of block k. Without it, the file ends after block 19, the end of a Cluster.
CRASH = (
    {"rows": 22, "in_block": 17},  # a clean cut of the sidecar
    {"rows": 21, "in_block": 15, "torn_row": True},  # then the first 37 bytes of row 21
    {"rows": 22, "bad_crc_row": 9},
)


def cameras() -> list[dict]:
    sources = [
        [1000 + d for d in range(MUXED + 1) if d != 5],  # the camera lost one source frame before position 5
        [500 + p for p in range(MUXED)],
        [2000 + p for p in range(MUXED)],
    ]
    lattices = [(33_483_200, 100_000_200_000), (33_133_500, 99_999_750_000), (33_250_000, 100_000_100_000)]
    return [
        capture_cases.camera(
            index, sources[index], [(0, MUXED - 1, *lattices[index])], rate=(10, 1), sample_ns=index == 0
        )
        for index in range(3)
    ]


def audio() -> dict:
    """The first 2.1 s of the audio of G1, with the jitter of `AUDIO_JITTER_NS`."""
    whole = g01.audio()
    rows = [(*row[:3], row[3] + AUDIO_JITTER_NS.get(b, 0)) for b, row in enumerate(whole["rows"][:AUDIO_BLOCKS])]
    samples = sum(n for _, n, _, _ in rows)
    return whole | {"rows": rows, "click_samples": [n for n in whole["click_samples"] if n + 48 <= samples]}


def _wrong_crc(line: bytes) -> bytes:
    body, crc = line[:-1].rsplit(b",", 1)
    return body + b",%08x\n" % (int(crc, 16) ^ 1)


def crashed_take(torn_audio: bool) -> dict:
    """The files of a case as {path: bytes}, with the input, the `files` items and the truth of the case."""
    take_cameras, take_audio = cameras(), audio()
    pairs = capture_cases.device_pairs(TAKE, take_cameras, take_audio)
    files = capture_cases.folder_files(TAKE, take_cameras, pairs, take_audio, None)  # the manifest of the take start
    # A write of the manifest that the crash stopped (SFF-786). A reader does not read it (SFF-790).
    manifest = files[capture_cases.MANIFEST]
    files[capture_cases.MANIFEST + ".tmp"] = manifest[: len(manifest) // 2]

    items, truth_cameras = [], []
    for pair, crash in zip(pairs, CRASH):
        blocks = capture_cases.complete_blocks(pair["before"])
        complete = crash.get("in_block", 20)
        end = sum(blocks[complete - 1])  # the end of the last complete block
        media = pair["before"][: blocks[complete][0] + 100 if "in_block" in crash else end]
        assert capture_cases.complete_blocks(media) == blocks[:complete]

        lines = pair["lines"][: crash["rows"]]
        bad = crash.get("bad_crc_row")
        if bad is not None:
            lines[bad] = _wrong_crc(lines[bad])
        torn = pair["lines"][crash["rows"]][:TORN_ROW_BYTES] if crash.get("torn_row") else b""
        assert b"\n" not in torn and len(torn) in (0, TORN_ROW_BYTES)
        files |= {pair["name"]: media, pair["timing"]: pair["head"] + b"".join(lines) + torn}
        items.append(
            capture_cases.item(
                pair,
                "unfinished" if bad is None else "damaged",  # SFF-747, SFF-746
                crash["rows"] if bad is None else bad,  # SFF-746: the read stops at the row with the wrong CRC
                None,  # SFF-747: no `# end` line, so no fit
                complete=complete,
                torn_bytes=len(torn) + len(media) - end,  # SFF-791
                reason=None if bad is None else "crc_mismatch",
            )
        )
        truth_cameras.append(
            {
                "name": pair["name"], "complete_blocks": complete, "sidecar_torn_bytes": len(torn),
                "media_torn_bytes": len(media) - end, "bad_crc_row": bad,
            }
        )  # fmt: skip

    pair = pairs[-1]
    (_, first_end), (second, second_end) = capture_cases.complete_fragments(pair["before"])
    assert second_end == len(pair["before"])
    moof_size = struct.unpack(">I", pair["before"][second : second + 4])[0]
    # The torn file ends in the middle of the `mdat` of the second fragment. Its `moof` is whole.
    cut = second + moof_size + (second_end - second - moof_size) // 2 if torn_audio else second_end
    end = first_end if torn_audio else second_end
    files |= {pair["name"]: pair["before"][:cut], pair["timing"]: pair["head"] + b"".join(pair["lines"])}
    held = capture_cases.held_samples(pair["before"][:cut])
    whole = capture_cases.whole_blocks(pair["rows"], held)  # SFF-792: `records` holds only these blocks
    items.append(capture_cases.item(pair, "unfinished", len(pair["rows"]), None, complete=whole, torn_bytes=cut - end))
    fit = capture_cases.reader_audio_fit(pair["rows"])  # SFF-784: from the rows that the reader uses (SFF-746)
    truth = {
        "audio": {
            "name": pair["name"], "complete_fragments": 1 if torn_audio else 2, "held_samples": held,
            "complete_blocks": whole, "sidecar_torn_bytes": 0, "media_torn_bytes": cut - end,
            "reader_fit": dict(zip(("row_first", "row_last", "n0", "t0_ns", "period_fs"), fit)),
        },
        "cameras": truth_cameras,
    }  # fmt: skip
    return {
        "files": files, "pairs": pairs, "cameras": take_cameras, "audio": take_audio, "truth": truth,
        "facts": capture_cases.take_facts(TAKE, items),
    }  # fmt: skip


def build(out: Path) -> None:
    for case, torn_audio in (("audio_clean_kill", False), ("audio_torn_fragment", True)):
        crashed = crashed_take(torn_audio)
        capture_cases.write_files(out / case, crashed["files"])
        capture_cases.write_results(out, case, crashed["facts"], ("stray_tmp",), crashed["truth"])  # SFF-790
