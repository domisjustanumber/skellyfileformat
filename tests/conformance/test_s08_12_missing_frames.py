"""Conformance tests SFT-771 to SFT-773: missing frames and short files (SPEC.md sections 5, 6, 8, 11 and 12).

The Pass text of each test is in spec/conformance.md. A test gets the reader or the writer from a
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


def test_sft_772_golden_part(golden_or_skip):
    """SFT-772, the golden part: camera 2 of G18, a short file that the program completed. It needs no reader.

    Checks: SFF-727, SFF-754, SFF-795, SFF-894.
    """
    folder = golden_or_skip("G18")
    manifest, camera, sidecar, data = _g18_camera(folder, 2)
    blocks = c.parse_mkv(data).blocks
    with_bytes = [row for row in sidecar.rows if row["byte_offset"]]
    assert len(blocks) == len(with_bytes) < len(sidecar.rows), "as many blocks as rows with a `byte_offset`"
    assert len(data) == blocks[-1].offset + blocks[-1].size, "no byte after the last block"
    assert sidecar.rows[: len(with_bytes)] == with_bytes
    for row in sidecar.rows[len(with_bytes) :]:
        assert int(row["flags"]) & c.MISSING and not any(row[key] for key in ("byte_offset", "byte_size", "arrival_ns", "sample_ns"))
    others = [c.read_sidecar(folder / other["timing"]) for other in manifest["cameras"][:2]]
    assert {len(other.rows) for other in others} == {len(sidecar.rows)}, "as many rows as the other sidecars"
    assert sidecar.footer[-2].startswith("# repair ") and sidecar.footer[-1].startswith("# end "), "the last two lines"
    assert not sidecar.lines("fit_segment") and sidecar.repaired
    warnings = {w["code"]: w["detail"] for w in manifest["warnings"] if w["camera_key"] == camera["camera_key"]}
    assert set(warnings) == {"camera_dead", "camera_file_short"}
    last = max(k for k, row in enumerate(sidecar.rows) if not int(row["flags"]) & c.MISSING)
    assert DEAD.fullmatch(warnings["camera_dead"]).group(1) == str(last)
    assert SHORT.fullmatch(warnings["camera_file_short"]).groups() == (str(len(blocks)), str(len(sidecar.rows)))


@pytest.mark.external("skellycam")
def test_sft_772_external():
    """SFT-772, the external sentences: a kill, a hang and a failed write of a camera of a skellycam take.

    Checks: SFF-727, SFF-754, SFF-793, SFF-795, SFF-894.
    """


@pytest.mark.parametrize(
    ("detail", "lost_at"),
    [(None, None), ("last_frame=none reason=hang", 0), ("last_frame=06 reason=hang", None), ("frame=6", None)],
    ids=["g18", "none", "leading_zero", "no_form"],
)
def test_sft_773_camera_lost_at(reader, variant, expected, detail, lost_at):
    """SFT-773 Reader: camera lost at frame N. Checks: SFF-895.

    `camera_lost_at(folder, name)` of the Python reader gives N of SFF-895, or None.
    """
    folder = variant("G18")
    manifest = c.load_json(folder / c.MANIFEST)
    names = [camera["video"] for camera in manifest["cameras"]]
    if detail is not None:
        (warning,) = [w for w in manifest["warnings"] if w["camera_key"] == manifest["cameras"][1]["camera_key"]]
        warning["detail"] = detail
        c.write_json(folder / c.MANIFEST, manifest)
    found = [reader.camera_lost_at(folder, name) for name in names]
    assert found == ([None, 7, 8] if detail is None else [None, lost_at, 8])
    assert c.read_bytes(reader, folder) == expected("G18", "take", "full"), "the codes are not warnings of the reader result"
