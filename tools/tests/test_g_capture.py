"""Cross-checks of the golden folders G2, G4, G5, G6, G11, G12 and G18 (golden/CAPTURE_VECTORS_CHOICES.md).

Each check reads the committed files and computes a value again from the text of the spec. Of the
generator, the checks use only the walk `complete_blocks`, which they compare with the offsets of
the CSV rows. `test_writer_gives_the_bytes_of_g1` runs the generator. The tests that decode media
skip when PyAV or Pillow is absent.
"""

from __future__ import annotations

import io
import json
import struct
import zlib
from pathlib import Path

import pytest

from goldgen.capture_cases import complete_blocks

from test_golden_files import GOLDEN, load, read_sidecar

G01_TAKE = GOLDEN / "G01" / "take"
MEDIA = "synchronized_videos"
CRASHED = [("G05", "audio_clean_kill"), ("G05", "audio_torn_fragment"), ("G06", "repaired"), ("G06", "interrupted_repair")]


def files_of(folder: Path) -> dict[str, bytes]:
    return {p.relative_to(folder).as_posix(): p.read_bytes() for p in folder.rglob("*") if p.is_file()}


def take_of(folder: str, case: str, scope: str = "full") -> dict:
    (take,) = load(GOLDEN / folder / f"{case}.{scope}.json")["takes"]
    return take


def split_sidecar(data: bytes) -> tuple[bytes, list[bytes], list[bytes], bytes]:
    """The header with the column line, the data row lines, the footer lines and the torn last line."""
    *lines, torn = data.split(b"\n")
    column = next(i for i, line in enumerate(lines) if not line.startswith(b"#"))
    rest = lines[column + 1 :]
    footer_at = next((i for i, line in enumerate(rest) if line.startswith(b"#")), len(rest))
    return b"\n".join(lines[: column + 1]) + b"\n", rest[:footer_at], rest[footer_at:], torn


def good_rows(rows: list[bytes]) -> int:
    """The number of rows before the first row with a wrong CRC (SFF-746)."""
    for count, line in enumerate(rows):
        body, crc = line.rsplit(b",", 1)
        if b"%08x" % zlib.crc32(body) != crc:
            return count
    return len(rows)


def media_tail(kind: str, media: bytes, rows: list[bytes]) -> tuple[int, int]:
    """The number of complete blocks or fragments, and the bytes after the last one (SFF-791)."""
    if kind == "camera":
        blocks = complete_blocks(media)
        offsets = [(int(f[5]), int(f[6])) for f in (row.split(b",") for row in rows)]
        assert blocks[: len(offsets)] == offsets[: len(blocks)], "the walk agrees with the offsets of the CSV rows"
        return len(blocks), len(media) - sum(blocks[-1])
    at, moof, fragments, end = 0, False, 0, 0
    while at + 8 <= len(media):
        size, box = struct.unpack(">I4s", media[at : at + 8])
        if at + size > len(media):
            break
        at += size
        if box == b"mdat" and moof:
            fragments, end = fragments + 1, at
        moof = box == b"moof"
        if box not in (b"moof", b"mdat"):
            end = at
    return fragments, len(media) - end


def _children(data: bytes) -> dict[bytes, bytes]:
    found, at = {}, 0
    while at + 8 <= len(data):
        size, kind = struct.unpack(">I4s", data[at : at + 8])
        found[kind], at = data[at + 8 : at + size], at + size
    return found


def held_samples(media: bytes) -> int:
    """The samples of the complete fragments, minus the pre-skip of `dOps` (SFF-785)."""
    dops = media.index(b"dOps")  # the one `dOps` box, in `moov`, before each fragment
    pre_skip = struct.unpack(">H", media[dops + 6 : dops + 8])[0]
    at, moof, held = 0, None, 0
    while at + 8 <= len(media):
        size, box = struct.unpack(">I4s", media[at : at + 8])
        if at + size > len(media):
            break
        if box == b"moof":
            moof = media[at + 8 : at + size]
        elif box == b"mdat" and moof is not None:
            parts = _children(_children(moof)[b"traf"])
            # tfhd has the flags of SFF-760 and a default duration, so the duration is at offset 8.
            held += int.from_bytes(parts[b"trun"][4:8], "big") * int.from_bytes(parts[b"tfhd"][8:12], "big")
            moof = None
        at += size
    return held - pre_skip


def whole_blocks(media: bytes, rows: list[bytes]) -> int:
    """The first rows whose every sample is in a complete fragment (SFF-792). `file_sample_offset` is 0."""
    held = held_samples(media)
    fields = [[int(f) for f in row.split(b",")[1:3]] for row in rows]
    return next((count for count, (first, n) in enumerate(fields) if first + n > held), len(rows))


# ---------------------------------------------------------------- the generator against G1


def test_writer_gives_the_bytes_of_g1():
    pytest.importorskip("av")
    pytest.importorskip("PIL")
    from goldgen import capture_cases, common, g01

    files, facts = capture_cases.finished_take(g01.TAKE, g01.cameras(), g01.audio())
    assert files == files_of(G01_TAKE)
    for scope in ("full", "player"):
        result = common.canonical_json(capture_cases.expected_result(facts, scope))
        assert result == (GOLDEN / "G01" / f"take.{scope}.json").read_bytes()


# ---------------------------------------------------------------- G2


def test_g02_is_g1_with_stereo_audio():
    base, stereo = files_of(G01_TAKE), files_of(GOLDEN / "G02" / "take")
    stem = f"{MEDIA}/g01_synthetic_take"
    changed = {name for name in base if base[name] != stereo[name]}
    assert set(base) == set(stereo)
    assert changed == {f"{stem}.audio.m4a", f"{stem}.audio.csv", "g01_synthetic_take_info.json", "recording_manifest.json"}

    def lines(name: str) -> tuple[set, set]:
        old, new = base[name].decode().split("\n"), stereo[name].decode().split("\n")
        assert len(old) == len(new)
        return {a for a, b in zip(old, new) if a != b}, {b for a, b in zip(old, new) if a != b}

    assert lines(f"{stem}.audio.csv") == ({"# channels=1"}, {"# channels=2"})
    assert lines("g01_synthetic_take_info.json") == ({'    "device_channels": 1'}, {'    "device_channels": 2'})
    old, new = lines("recording_manifest.json")
    assert {line.split(":")[0].strip() for line in old | new} == {'"sha256"', '"channels"'}
    # The reader result holds no fact of the channels.
    for scope in ("full", "player"):
        assert (GOLDEN / "G02" / f"take.{scope}.json").read_bytes() == (GOLDEN / "G01" / f"take.{scope}.json").read_bytes()


def test_g02_audio_decodes_to_two_channels():
    av = pytest.importorskip("av")
    truth = json.loads((GOLDEN / "G02" / "take.truth.json").read_bytes())
    with av.open(str(GOLDEN / "G02" / "take" / truth["audio"]["name"])) as container:
        (stream,) = container.streams
        assert (stream.codec_context.name, stream.sample_rate, stream.channels) == ("opus", 48000, 2)
        planes = [[], []]
        for frame in container.decode(stream):
            array = frame.to_ndarray()
            assert array.shape[0] == 2, "PyAV decodes Opus to planar float"
            planes[0] += array[0].tolist()
            planes[1] += array[1].tolist()
    first = truth["audio"]["click_samples"][0]
    left, right = (max(abs(v) for v in plane[first : first + 48]) for plane in planes)
    assert left > 0.3 and 0.35 < right / left < 0.65  # the right channel has half the level


# ---------------------------------------------------------------- G4


def test_g04_stored_frames_turn_to_the_upright_corner_colours():
    Image = pytest.importorskip("PIL.Image")
    truth = json.loads((GOLDEN / "G04" / "take.truth.json").read_bytes())
    half = truth["corner_px"] // 2
    assert [camera["display_rotation"] for camera in truth["cameras"]] == [0, 90, 180, 270]
    for camera in truth["cameras"]:
        media = (GOLDEN / "G04" / "take" / camera["name"]).read_bytes()
        header, rows, _ = read_sidecar((GOLDEN / "G04" / "take" / camera["name"]).with_suffix(".csv"))
        assert int(header["display_rotation"]) == camera["display_rotation"]
        for row in rows:
            stored = Image.open(io.BytesIO(media[int(row[5]) : int(row[5]) + int(row[6])])).convert("RGB")
            assert stored.size == (64, 48)  # SFF-735: the orientation of the sensor
            upright = stored.rotate(-camera["display_rotation"], expand=True)  # clockwise (SFF-751)
            width, height = upright.size
            places = {
                "top_left": (half, half), "top_right": (width - half, half),
                "bottom_right": (width - half, height - half), "bottom_left": (half, height - half),
            }  # fmt: skip
            for corner, place in places.items():
                pixel = upright.getpixel(place)
                assert all(abs(a - b) <= 16 for a, b in zip(pixel, camera["upright_corners"][corner])), corner


# ---------------------------------------------------------------- G5 and G6


@pytest.mark.parametrize(("folder", "case"), CRASHED)
def test_crashed_results_agree_with_the_files(folder, case):
    """`state`, `rows`, `torn_bytes` and the number of records, computed again from the bytes."""
    take = take_of(folder, case)
    truth = json.loads((GOLDEN / folder / f"{case}.truth.json").read_bytes())
    for item, facts in zip(take["files"], [*truth["cameras"], truth["audio"]]):
        media = (GOLDEN / folder / case / item["name"]).read_bytes()
        sidecar = (GOLDEN / folder / case / item["name"]).with_suffix(".csv").read_bytes()
        _, rows, footer, torn = split_sidecar(sidecar)
        good = good_rows(rows)
        blocks, tail = media_tail(item["kind"], media, rows)
        ended = bool(footer) and footer[-1].startswith(b"# end ") and not torn
        if good < len(rows):
            state = "damaged"
        elif not ended:
            state = "unfinished"
        else:
            state = "repaired" if any(line.startswith(b"# repair ") for line in footer) else "finished"
        assert (item["state"], item["reason"]) == (state, "crc_mismatch" if state == "damaged" else None)
        assert item["rows"] == good
        assert item["torn_bytes"] == len(torn) + (0 if ended else tail)  # SFF-791
        whole = blocks if item["kind"] == "camera" else whole_blocks(media, rows[:good])
        assert len(item["records"]) == min(good, whole)  # SFF-740, SFF-792
        assert item["fit"] is (state == "repaired") and ("missing_fit" in item["warnings"]) is (state != "repaired")
        if state == "repaired":
            assert tail == 0
        if "media_torn_bytes" in facts:
            assert (facts["sidecar_torn_bytes"], facts["media_torn_bytes"]) == (len(torn), tail)
    assert take_of(folder, case, "player") == take


def test_g05_vectors():
    clean, torn = files_of(GOLDEN / "G05" / "audio_clean_kill"), files_of(GOLDEN / "G05" / "audio_torn_fragment")
    audio = f"{MEDIA}/g05_synthetic_take.audio.m4a"
    assert {name for name in clean if clean[name] != torn[name]} == {audio} and set(clean) == set(torn)
    assert clean[audio].startswith(torn[audio])

    states = [item["state"] for item in take_of("G05", "audio_torn_fragment")["files"]]
    assert states == ["unfinished", "unfinished", "damaged", "unfinished"]
    names = [item["name"] for item in take_of("G05", "audio_torn_fragment")["files"]]
    parts = [split_sidecar(torn[name[:-4] + ".csv"]) for name in names]
    assert [len(torn_line) for _, _, _, torn_line in parts] == [0, 37, 0, 0]
    assert all(not footer for _, _, footer, _ in parts)
    assert [(good_rows(rows), len(rows)) for _, rows, _, _ in parts] == [(22, 22), (21, 21), (9, 22), (21, 21)]
    # Only the CRC field of the bad row is wrong, and each row after it is good.
    bad_rows = parts[2][1]
    assert good_rows(bad_rows[10:]) == 12 and int(bad_rows[9].rsplit(b",", 1)[1], 16) ^ 1 == zlib.crc32(
        bad_rows[9].rsplit(b",", 1)[0]
    )

    manifest = json.loads(torn["recording_manifest.json"])
    assert manifest["state"] == "recording" and manifest["warnings"] == []
    assert manifest["summary"]["duration_s"] is None and manifest["summary"]["audio"]["duration_s"] is None
    assert all(c["stored_px"] is c["gaps"] is c["filled"] is None for c in manifest["summary"]["cameras"])  # SFF-728
    tmp = torn["recording_manifest.json.tmp"]
    assert torn["recording_manifest.json"].startswith(tmp) and len(tmp) < len(torn["recording_manifest.json"])
    for scope in ("full", "player"):
        result = load(GOLDEN / "G05" / f"audio_torn_fragment.{scope}.json")
        assert result["folder_warnings"] == ["stray_tmp"] and result["other_files"] == []  # SFF-790


def test_g05_audio_fit_of_the_reader():
    """SFF-784, from the rows of the sidecar."""
    for case in ("audio_clean_kill", "audio_torn_fragment"):
        take = take_of("G05", case)
        truth = json.loads((GOLDEN / "G05" / f"{case}.truth.json").read_bytes())
        sidecar = (GOLDEN / "G05" / case / take["files"][-1]["name"]).with_suffix(".csv").read_bytes()
        rows = [[int(f) for f in row.split(b",")[:6]] for row in split_sidecar(sidecar)[1]]
        (_, n_a, _, _, t_a, _), (last, n_b, _, _, t_b, _) = rows[0], rows[-1]
        fit = {"row_first": 0, "row_last": last, "n0": n_a, "t0_ns": t_a, "period_fs": (t_b - t_a) * 10**6 // (n_b - n_a)}
        assert truth["audio"]["reader_fit"] == fit
        expected = [[*row[:4], t_a + (row[1] - n_a) * fit["period_fs"] // 10**6] for row in rows]  # SFF-779
        media = (GOLDEN / "G05" / case / take["files"][-1]["name"]).read_bytes()
        whole = truth["audio"]["complete_blocks"]
        assert whole == len([row for row in rows if row[1] + row[2] <= held_samples(media)]) == {False: 19, True: 9}[case.endswith("torn_fragment")]
        assert truth["audio"]["held_samples"] == held_samples(media)
        assert take["files"][-1]["records"] == expected[:whole], "only the blocks in the complete fragments (SFF-792)"


def test_g05_audio_fit_from_kept_rows_differs():
    """ADR-3GWN: a fit from only the rows in `records` gives other `fitted_ns` than SFF-784."""
    for case in ("audio_clean_kill", "audio_torn_fragment"):
        take = take_of("G05", case)
        sidecar = (GOLDEN / "G05" / case / take["files"][-1]["name"]).with_suffix(".csv").read_bytes()
        records = take["files"][-1]["records"]
        rows = [[int(f) for f in row.split(b",")[:6]] for row in split_sidecar(sidecar)[1]][: len(records)]
        (_, n_a, _, _, t_a, _), (_, n_b, _, _, t_b, _) = rows[0], rows[-1]
        period_fs = (t_b - t_a) * 10**6 // (n_b - n_a)
        wrong = [t_a + (row[1] - n_a) * period_fs // 10**6 for row in rows]
        assert max(abs(w - r[4]) for w, r in zip(wrong, records)) > 10_000


def test_g06_repair_changes_no_byte_before_its_cut():
    before = files_of(GOLDEN / "G05" / "audio_torn_fragment")
    for case in ("repaired", "interrupted_repair"):
        after = files_of(GOLDEN / "G06" / case)
        truth = json.loads((GOLDEN / "G06" / f"{case}.truth.json").read_bytes())
        for facts in [*truth["cameras"], truth["audio"]]:
            media, sidecar = facts["name"], facts["name"][:-4] + ".csv"
            assert after[media] == before[media][: len(before[media]) - facts["media_cut_bytes"]]  # SFF-794
            kept = before[sidecar][: len(before[sidecar]) - facts["cut_bytes"]]
            assert after[sidecar].startswith(kept)
            head, rows, footer, torn = split_sidecar(after[sidecar])
            assert head + b"".join(row + b"\n" for row in rows) == kept and good_rows(rows) == len(rows)
            words = [line.split(b" ")[1].decode() for line in footer]
            repair = (
                f"# repair cut_bytes={facts['cut_bytes']} media_cut_bytes={facts['media_cut_bytes']} "
                "repair_writer=skellyfileformat-goldgen 1.0.0"
            ).encode()
            if case == "repaired":  # SFF-795: the fit lines, the repair line and the `# end` line
                assert words == ["fit", "fit_segment", "repair", "end"] and footer[2] == repair and not torn
                assert f"# end rows={len(rows)} ".encode() in footer[3] + b" "
            else:  # SFF-798: no `# end` line
                assert words[:2] == ["fit", "fit_segment"] and "end" not in words
                assert words[2:] in ([], ["repair"]) and (footer[2:] == [repair] or repair.startswith(torn))
                assert len(torn) == facts["sidecar_torn_bytes"]
    same = {name for name in after if before.get(name) == after[name]}
    assert {"recording_manifest.json", "recording_manifest.json.tmp", "g05_synthetic_take_info.json"} <= same


def test_g06_manifest_after_the_repair():
    """SFF-793: `state`, the summary and `camera_gap`. No other member changes."""
    old = json.loads((GOLDEN / "G05" / "audio_torn_fragment" / "recording_manifest.json").read_bytes())
    new = json.loads((GOLDEN / "G06" / "repaired" / "recording_manifest.json").read_bytes())
    assert not (GOLDEN / "G06" / "repaired" / "recording_manifest.json.tmp").exists()
    assert {key for key in old if old[key] != new[key]} == {"state", "warnings", "summary"} and list(old) == list(new)
    assert new["state"] == "finished" and new["summary"]["warnings"] == ["camera_gap"]
    assert [w["camera_key"] for w in new["warnings"]] == [new["cameras"][0]["camera_key"]]
    ends, last_arrival_ns = [], []
    for camera in new["cameras"]:
        _, rows, footer = read_sidecar(GOLDEN / "G06" / "repaired" / camera["timing"])
        ends.append(dict(pair.split("=") for pair in footer[-1].split(" ")[2:]))
        last_arrival_ns.append(int(rows[-1][2]))
    assert [(c["gaps"], c["filled"]) for c in new["summary"]["cameras"]] == [(int(e["gaps"]), 0) for e in ends]
    assert new["summary"]["duration_s"] == (max(last_arrival_ns) + 500_000) // 10**6 / 1000  # SFF-728
    # SFF-728 and SFF-795: the `# end` line of the cut audio sidecar, 9 blocks of 4,800 samples.
    audio = new["audio"]["timing"]
    _, rows, footer = read_sidecar(GOLDEN / "G06" / "repaired" / audio)
    media = (GOLDEN / "G06" / "repaired" / new["audio"]["audio"]).read_bytes()
    assert len(rows) == 9 == len([row for row in rows if int(row[1]) + int(row[2]) <= held_samples(media)])
    assert footer[-1] == "# end rows=9 samples=43200 gaps=0 silence_samples=0"
    assert new["summary"]["audio"]["duration_s"] == 0.9


# ---------------------------------------------------------------- G11

G11_CASES = {  # the case: the line of G1, the new line (None: no line), the reason
    "leading_zero": ("1,501,70571479,,0,1181,861,", "1,0501,70571479,,0,1181,861,", "bad_metadata"),
    "plus_sign": ("1,501,70571479,,0,1181,861,", "1,501,+70571479,,0,1181,861,", "bad_metadata"),
    "row_integer_2_53": ("1,501,70571479,,0,1181,861,", "1,9007199254740992,70571479,,0,1181,861,", "bad_metadata"),
    "rate_0_1": ("# nominal_rate=30/1", "# nominal_rate=0/1", "bad_rate"),
    "rate_2_20_plus_1": ("# nominal_rate=30/1", "# nominal_rate=1048577/1", "bad_rate"),
    "rotation_45": ("# display_rotation=0", "# display_rotation=45", "bad_rotation"),
    "bad_label": ("# camera_label=d20676", "# camera_label=nothex", "bad_label"),
    "missing_key": ("# nominal_rate=30/1", None, "missing_metadata"),
    "unknown_clock": ("# clock=windows_qpc", "# clock=fake_clock", "bad_metadata"),
}


def test_g11_has_each_case_of_the_spec():
    assert {p.name for p in (GOLDEN / "G11").iterdir() if p.is_dir()} == set(G11_CASES)


@pytest.mark.parametrize("case", G11_CASES)
def test_g11_case_is_g1_with_one_changed_line(case):
    old_line, new_line, reason = G11_CASES[case]
    base, vector = files_of(G01_TAKE), files_of(GOLDEN / "G11" / case)
    sidecar = f"{MEDIA}/g01_synthetic_take.d20676.csv"
    assert set(base) == set(vector) and {name for name in base if base[name] != vector[name]} == {sidecar}
    old, new = base[sidecar].decode().split("\n"), vector[sidecar].decode().split("\n")
    (index,) = [i for i, line in enumerate(old) if line.startswith(old_line)]
    if new_line is None:
        assert new == old[:index] + old[index + 1 :]
    else:
        assert new[:index] + new[index + 1 :] == old[:index] + old[index + 1 :] and new[index].startswith(new_line)
        if not new_line.startswith("#"):  # the changed row has a correct CRC
            body, crc = new[index].rsplit(",", 1)
            assert body + "," == new_line and f"{zlib.crc32(body.encode()):08x}" == crc

    take, good = take_of("G11", case), take_of("G01", "take", "player")
    refused = take["files"][1]
    assert (refused["state"], refused["reason"]) == ("invalid", reason)
    assert refused["rows"] is refused["torn_bytes"] is refused["fit"] is refused["records"] is None
    assert refused["camera_label"] == (None if case == "bad_label" else "d20676")
    assert (refused["name"], refused["camera_key"]) == (good["files"][1]["name"], good["files"][1]["camera_key"])
    # One camera file is `finished`, so the reader does not evaluate the row counts (SFF-872).
    assert take | {"files": None} == good | {"files": None}
    assert [take["files"][0], take["files"][2]] == [good["files"][0], good["files"][2]]
    assert take_of("G11", case, "player") == take


# ---------------------------------------------------------------- G12


def test_g12_fitted_times_follow_the_fit_lines():
    """SFF-777 and SFF-779 for each row, from the footer of each sidecar."""
    take = take_of("G12", "take")
    seen = []
    for item in take["files"]:
        _, rows, footer = read_sidecar((GOLDEN / "G12" / "take" / item["name"]).with_suffix(".csv"))
        segments = [
            {key: int(value) for key, value in (pair.split("=") for pair in line.split(" ")[2:])}
            for line in footer
            if line.startswith("# fit_segment ")
        ]
        seen.append(len(segments))
        times = []
        if item["kind"] == "audio":
            for s in segments:
                for row in rows[s["row_first"] : s["row_last"] + 1]:
                    times.append(s["t0_ns"] + (int(row[1]) - s["n0"]) * s["period_fs"] // 10**6)
            assert segments[0]["period_fs"] * 4800 % 10**6, "a `period_fs` with a remainder"
        elif not segments:
            times = [int(row[2]) for row in rows]  # SFF-781: the arrival time
        for s in segments if item["kind"] == "camera" else []:
            for row in rows[s["pos_first"] : s["pos_last"] + 1]:
                d = int(row[1]) - int(rows[s["pos_first"]][1])
                times.append(s["t0_ns"] + d * s["period_ps"] // 1000)
        assert [record[4] for record in item["records"]] == times and times == sorted(times)  # SFF-782
        assert item["fit"] is bool(segments) and item["state"] == "finished"
    assert seen == [2, 1, 0, 1, 1]


def test_g12_vectors():
    cameras = take_of("G12", "take")["files"][:4]
    sidecars = [read_sidecar((GOLDEN / "G12" / "take" / c["name"]).with_suffix(".csv")) for c in cameras]
    flags = [[int(row[4]) for row in rows] for _, rows, _ in sidecars]
    assert flags[0] == [0, 0, 0, 1, *[0] * 8] and flags[1] == flags[2] == [0] * 12
    assert flags[3] == [4, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0]  # `encode_skip` in row 0, `repeat` in row 7
    assert [c["warnings"] for c in cameras] == [
        ["gap", "prerelease"], ["prerelease"], ["missing_fit", "prerelease"], ["encode_skip", "prerelease"],
    ]  # fmt: skip
    assert "period_ps=33333333333" in sidecars[1][2][1]  # 1000 does not divide it
    times = [record[4] for record in cameras[3]["records"]]
    assert times[6] == times[7] and len(set(times)) == 11  # the two equal fitted times
    states = {link["check"]: link["state"] for link in take_of("G12", "take")["links"]}
    assert states["frames"] == "ok" and take_of("G12", "take", "player") != take_of("G12", "take")


# ---------------------------------------------------------------- G18


def _sof(jpeg: bytes) -> bytes:
    """The frame header of a baseline JPEG, from its length field: the size, the components and their factors."""
    at = jpeg.index(b"\xff\xc0")
    return jpeg[at + 4 : at + 2 + int.from_bytes(jpeg[at + 2 : at + 4], "big")]


def test_g18_missing_rows_against_the_files():
    """`missing` rows, placeholders and the short file of G18 (decision 6AT7; SFF-754, SFF-756, SFF-758, SFF-885)."""
    folder = GOLDEN / "G18" / "take"
    manifest = json.loads((folder / "recording_manifest.json").read_bytes())
    take = take_of("G18", "take")
    assert [item["state"] for item in take["files"]] == ["finished", "finished", "repaired"]
    for item, camera, summary in zip(take["files"], manifest["cameras"], manifest["summary"]["cameras"]):
        _, rows, footer = read_sidecar(folder / camera["timing"])
        media = (folder / camera["video"]).read_bytes()
        blocks = complete_blocks(media)
        missing = [int(row[4]) & 16 != 0 for row in rows]
        with_bytes = [(int(row[5]), int(row[6])) for row in rows if row[5]]
        assert blocks == with_bytes and item["rows"] == len(rows) == 12  # SFF-759: a block for each row with a `byte_offset`
        if item["state"] == "repaired":
            assert len(media) == sum(blocks[-1]), "no byte after the last block (SFF-894)"
        assert f"missing={sum(missing)} " in footer[-1] and summary["missing"] == sum(missing)
        frames = [media[o : o + s] for (o, s), m in zip(blocks, missing) if not m]
        for (offset, size), is_missing in zip(blocks, missing):
            if is_missing:  # SFF-756: the size, the components and the factors of the frames
                assert _sof(media[offset : offset + size]) == _sof(frames[0])
        for record, row in zip(item["records"], rows):
            assert (record[2] is None) == (row[2] == "") and (record[4] is None) == (row[2] == "")  # SFF-781
    assert [len(blocks) for blocks in [complete_blocks((folder / c["video"]).read_bytes()) for c in manifest["cameras"]]] == [12, 12, 8]
    assert [w["code"] for w in manifest["warnings"]] == ["camera_dead", "camera_dead", "camera_file_short"]


def test_g18_placeholders_decode_to_black():
    av = pytest.importorskip("av")
    pytest.importorskip("PIL")
    folder = GOLDEN / "G18" / "take"
    for csv in sorted((folder / MEDIA).glob("*.csv")):
        _, rows, _ = read_sidecar(csv)
        media = csv.with_suffix(".mkv").read_bytes()
        for row in rows:
            if int(row[4]) & 16 and row[5]:
                context = av.CodecContext.create("mjpeg", "r")
                (frame,) = context.decode(av.Packet(media[int(row[5]) : int(row[5]) + int(row[6])])) + context.decode(None)
                assert max(high for _, high in frame.to_image().convert("RGB").getextrema()) <= 16
