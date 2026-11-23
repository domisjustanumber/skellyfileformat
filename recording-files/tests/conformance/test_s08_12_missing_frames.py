"""Conformance tests SFT-771 to SFT-773: missing frames and short files (SPEC.md sections 5, 6, 8, 11 and 12).

The Pass text of each test is in recording-files/conformance.md. A test gets the reader or the writer from a
fixture, so it fails with one line until the implementation exists (decision G21H). The changes
F-1 to F-10 are in decision 6AT7.
"""

from __future__ import annotations

import re

import pytest

import checks_capture as c

FRAMES, ERROR_POSITION, LAST_FRAME = 8, 2, 4
MISSING_ROWS = {ERROR_POSITION, *range(LAST_FRAME + 1, FRAMES)}  # of camera 1
REASON = "test stop"
DEAD = re.compile(r"last_frame=(0|[1-9][0-9]*|none) reason=(.*)")  # SFF-727, SFF-895
SHORT = re.compile(r"blocks=(0|[1-9][0-9]*) rows=(0|[1-9][0-9]*)")


def sof(data: bytes) -> tuple:
    """(marker, width, height, the H/V factors of each component) of the frame header of a JPEG."""
    for marker, start, _ in c.jpeg_segments(data):
        if 0xC0 <= marker <= 0xCF and marker not in (c.DHT, 0xC8, 0xCC):
            height, width, count = data[start + 5] << 8 | data[start + 6], data[start + 7] << 8 | data[start + 8], data[start + 9]
            return marker, width, height, tuple(data[start + 11 + 3 * i] for i in range(count))
    raise AssertionError("the JPEG has no frame header")


def test_sft_771_missing_rows_and_placeholder(writer, tmp_path):
    """SFT-771 Writer: `missing` rows and the placeholder.

    Checks: SFF-727, SFF-728, SFF-734, SFF-754, SFF-755, SFF-756, SFF-757, SFF-758.
    """
    folder = tmp_path / "take"
    take = writer.TakeWriter(folder, "synthetic_take", [c.camera(0), c.camera(1)], None, writer=c.WRITER)
    start, sent = take.take_start_host_ns, {0: {}, 1: {}}
    for position in range(FRAMES):
        for index in (0, 1):
            if index == 1 and position > LAST_FRAME:
                continue
            arrival = start + 33_333_333 * (position + 1) + 1000 * index
            data = None if (index, position) == (1, ERROR_POSITION) else c.jpeg(position, colour=(30 + 40 * index, 40, 80))
            # `data` None: a frame with a capture error. The writer gets its times and no JPEG.
            take.write_frame(index, data, arrival, source_frame_number=1000 + position, sample_ns=arrival - 4_000_000)
            sent[index][position] = (data, 1000 + position, arrival - start, arrival - 4_000_000 - start)
        if position == LAST_FRAME:
            take.camera_stopped(1, REASON)
    take.close()

    videos = c.check_video_sidecars(folder)
    layout = sof(c.jpeg(0))[1:]
    for index, sidecar in enumerate(videos):
        data = sidecar.path.with_suffix(".mkv").read_bytes()
        blocks = c.parse_mkv(data).blocks
        assert len(sidecar.rows) == len(blocks) == FRAMES
        missing = MISSING_ROWS if index == 1 else set()
        for position, (row, block) in enumerate(zip(sidecar.rows, blocks)):
            payload = data[block.offset : block.offset + block.size]
            assert (int(row["byte_offset"]), int(row["byte_size"])) == (block.offset, block.size)
            assert bool(int(row["flags"]) & c.MISSING) == (position in missing), f"camera {index}, row {position}"
            fields = [row[key] for key in ("source_frame_number", "arrival_ns", "sample_ns")]
            if position not in missing or position == ERROR_POSITION:
                assert fields == [str(value) for value in sent[index][position][1:]], "the times of the frame stay"
            else:
                assert fields == ["", "", ""], "the camera gave no frame: no source frame number and no times"
            if position in missing:
                assert sof(payload) == (0xC0, *layout), "a baseline JPEG with the size and the factors of the frames"
                assert max(high for _, high in c.decode_jpeg(payload).getextrema()) <= 16, "the placeholder is black"
            else:
                assert payload == sent[index][position][0], "the other blocks hold the bytes that the test sent"
        assert sidecar.lines("end")[0]["missing"] == str(len(missing))
    manifest = c.check_manifest(folder)
    assert [camera["missing"] for camera in manifest["summary"]["cameras"]] == [0, len(MISSING_ROWS)]
    dead = [w for w in manifest["warnings"] if w["code"] == "camera_dead"]
    key = videos[1].header["camera_key"]
    assert dead == [{"code": "camera_dead", "source": "skellycam", "camera_key": key, "detail": f"last_frame={LAST_FRAME} reason={REASON}"}]


def _g18_camera(folder, index: int):
    manifest = c.load_json(folder / c.MANIFEST)
    camera = manifest["cameras"][index]
    return manifest, camera, c.read_sidecar(folder / camera["timing"]), (folder / camera["video"]).read_bytes()


@pytest.mark.parametrize(("case", "index"), [("take", 2), ("no_block", 1)])
def test_sft_772_golden_part(golden_or_skip, case, index):
    """SFT-772, the golden part: a short file of G18 that the program completed. It needs no reader.

    Checks: SFF-727, SFF-754, SFF-795, SFF-894. The camera file of `no_block` holds no block.
    """
    folder = golden_or_skip("G18", case)
    manifest, camera, sidecar, data = _g18_camera(folder, index)
    blocks = c.parse_mkv(data).blocks
    with_bytes = [row for row in sidecar.rows if row["byte_offset"]]
    assert len(blocks) == len(with_bytes) < len(sidecar.rows), "as many blocks as rows with byte fields"
    if blocks:
        assert len(data) == blocks[-1].offset + blocks[-1].size, "no byte after the last block"
    else:
        assert data.startswith(bytes.fromhex("1a45dfa3")) and bytes.fromhex("1f43b675") not in data, "no Cluster (SFF-754)"
    assert sidecar.rows[: len(with_bytes)] == with_bytes
    for row in sidecar.rows[len(with_bytes) :]:
        assert int(row["flags"]) & c.MISSING and not any(row[key] for key in ("byte_offset", "byte_size", "arrival_ns", "sample_ns"))
    others = [c.read_sidecar(folder / other["timing"]) for k, other in enumerate(manifest["cameras"]) if k != index]
    assert {len(other.rows) for other in others} == {len(sidecar.rows)}, "as many rows as the other sidecars"
    assert sidecar.footer[-2].startswith("# repair ") and sidecar.footer[-1].startswith("# end "), "the last two lines"
    assert not sidecar.lines("fit_segment") and sidecar.repaired
    warnings = {w["code"]: w["detail"] for w in manifest["warnings"] if w["camera_key"] == camera["camera_key"]}
    assert set(warnings) == {"camera_dead", "camera_file_short"}
    last = max((k for k, row in enumerate(sidecar.rows) if not int(row["flags"]) & c.MISSING), default=None)
    assert DEAD.fullmatch(warnings["camera_dead"]).group(1) == ("none" if last is None else str(last))
    assert SHORT.fullmatch(warnings["camera_file_short"]).groups() == (str(len(blocks)), str(len(sidecar.rows)))


@pytest.mark.external("skellycam")
def test_sft_772_external():
    """SFT-772, the external sentences: a kill, a hang and a failed write of a camera of a skellycam take.

    Checks: SFF-727, SFF-754, SFF-793, SFF-795, SFF-894.
    """


VECTORS_773 = {  # the vector: (the camera of the changed `detail`, the code, the new `detail`)
    "g18": None,
    "none": (1, "camera_dead", "last_frame=none reason=hang"),
    "leading_zero": (1, "camera_dead", "last_frame=06 reason=hang"),
    "no_form": (1, "camera_dead", "frame=6"),
    "short_leading_zero": (2, "camera_file_short", "blocks=08 rows=12"),
    "short_no_rows": (2, "camera_file_short", "blocks=8"),
}


@pytest.mark.parametrize("vector", [*VECTORS_773, "no_block"])
def test_sft_773_camera_lost_at(reader, variant, expected, vector):
    """SFT-773 Reader: camera lost at frame N. Checks: SFF-895.

    `camera_lost_at(folder, name)` gives N of SFF-895, and `short_file_counts(folder, name)` gives
    `[b, r]` of SFF-895, or None.
    """
    case = "no_block" if vector == "no_block" else "take"
    folder = variant("G18", case)
    manifest = c.load_json(folder / c.MANIFEST)
    names = [camera["video"] for camera in manifest["cameras"]]
    lost, counts = ([None, 0], [None, [0, 6]]) if case == "no_block" else ([None, 7, 8], [None, None, [8, 12]])
    change = VECTORS_773.get(vector)
    if change is not None:
        index, code, detail = change
        key = manifest["cameras"][index]["camera_key"]
        (warning,) = [w for w in manifest["warnings"] if w["camera_key"] == key and w["code"] == code]
        warning["detail"] = detail
        c.write_json(folder / c.MANIFEST, manifest)
        if code == "camera_dead":
            lost[index] = 0 if vector == "none" else None
        else:
            counts[index] = None
    assert [reader.camera_lost_at(folder, name) for name in names] == lost
    assert [None if found is None else list(found) for found in (reader.short_file_counts(folder, name) for name in names)] == counts
    assert c.read_bytes(reader, folder) == expected("G18", case, "full"), "the codes are not warnings of the reader result"
