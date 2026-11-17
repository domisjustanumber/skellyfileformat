"""Conformance tests SFT-711 to SFT-714: camera files (SPEC.md section 6).

The Pass text of each test is in spec/conformance.md. A test gets the reader or the writer from a
fixture, so it fails with one line until the implementation exists (decision G21H).
"""

from __future__ import annotations

import pytest

import checks_capture as c


@pytest.mark.parametrize("vector", ["two_cameras", "four_rotations", "rate_30000_1001", "rate_1001_1"])
def test_sft_711_camera_file(writer, tmp_path, vector):
    """SFT-711 Writer: the camera file. Checks: SFF-732, SFF-733, SFF-735, SFF-736, SFF-737.

    `two_cameras` is the input of G1 and `four_rotations` is the input of G4. The frame count of
    Blender is external (test_sft_711_external).
    """
    folder = tmp_path / "take"
    if vector == "rate_1001_1":
        with pytest.raises(ValueError):
            writer.TakeWriter(folder, "synthetic_take", [c.camera(0, nominal_rate="1001/1")], None, writer=c.WRITER)
        return
    cameras = {
        "two_cameras": [c.camera(0), c.camera(1)],
        "four_rotations": [c.camera(index, display_rotation=90 * index) for index in range(4)],
        "rate_30000_1001": [c.camera(0, nominal_rate="30000/1001")],
    }[vector]
    sent = c.record_take(writer, folder, cameras, c.microphone() if vector == "two_cameras" else None, gap_camera=None)
    sidecars = c.sidecars_by_position(folder)
    assert len(sidecars) == len(cameras)
    for index, sidecar in enumerate(sidecars):
        path = sidecar.path.with_suffix(".mkv")
        mkv = c.check_camera_file(path)
        data = path.read_bytes()
        # The writer adds nothing to a JPEG, so the bytes have no APPn timing data (SFF-737).
        assert [data[b.offset : b.offset + b.size] for b in mkv.blocks] == sent["jpegs"][index]
        if vector == "rate_30000_1001":
            assert mkv.tracks[0]["default_duration"] == 33_366_666
    c.check_no_overlay_file(folder)


@pytest.mark.parametrize("target", ["G01/take", "G04/take"])
def test_sft_711_check_on_golden(golden_or_skip, target):
    """SFT-711, the camera file check on a golden folder. Checks: SFF-732, SFF-733, SFF-735, SFF-736, SFF-737."""
    files = c.media_files(golden_or_skip(*target.split("/")), ".mkv")
    assert files
    for path in files:
        c.check_camera_file(path)


@pytest.mark.external("Blender")
def test_sft_711_external():
    """SFT-711, the external sentence: Blender (pinned) counts the same number of frames. Checks: SFF-733."""


@pytest.mark.parametrize("vector", ["mjpeg_source", "raw_source", "h264_request"])
def test_sft_712_jpeg_bytes(writer, tmp_path, vector):
    """SFT-712 Writer: JPEG bytes. Checks: SFF-734.

    `mjpeg_source` is the synthetic form of the sentence about an MJPEG camera: the block payloads
    are the bytes that the test sent. The run with test hardware is external (test_sft_712_external).
    """
    folder = tmp_path / "take"
    if vector == "mjpeg_source":
        sent = c.record_take(writer, folder)
        for index, sidecar in enumerate(c.sidecars_by_position(folder)):
            data = sidecar.path.with_suffix(".mkv").read_bytes()
            assert [data[b.offset : b.offset + b.size] for b in c.parse_mkv(data).blocks] == sent["jpegs"][index]
        return
    requested = dict(c.camera(0)["requested"], capture_format="YUYV" if vector == "raw_source" else "H264")
    if vector == "h264_request":
        with pytest.raises(ValueError):
            writer.TakeWriter(folder, "synthetic_take", [c.camera(0, requested=requested)], None, writer=c.WRITER)
        return
    take = writer.TakeWriter(folder, "synthetic_take", [c.camera(0, requested=requested)], None, writer=c.WRITER)
    for position in range(5):
        arrival = take.take_start_host_ns + 33_333_333 * (position + 1)
        take.write_frame(0, c.yuyv(position), arrival, source_frame_number=position)
    take.close()
    (path,) = c.media_files(folder, ".mkv")
    data = path.read_bytes()
    blocks = c.parse_mkv(data).blocks
    assert len(blocks) == 5
    for block in blocks:
        payload = data[block.offset : block.offset + block.size]
        assert c.decode_jpeg(payload).size == (c.WIDTH, c.HEIGHT), "a raw source gives valid JPEG frames"


@pytest.mark.external("capture hardware")
def test_sft_712_external():
    """SFT-712, the external sentence: the block payloads are the bytes that an MJPEG camera sent. Checks: SFF-734."""


def test_sft_713_jpeg_and_block_parsing(reader, tmp_path):
    """SFT-713 Reader: JPEG and block parsing. Checks: SFF-738, SFF-739.

    The test builds the camera file at run time (decision G21H item 7): JPEGs with no JFIF, no DHT,
    trailing bytes and an EXIF orientation tag, in blocks with track numbers of 1 and 2 bytes.
    """
    folder = tmp_path / "take"
    name, jpegs, _ = c.build_unusual_take(folder)
    (item,) = c.only_take(c.read(reader, folder, records=True))["files"]
    assert item["state"] == "finished" and item["rows"] == len(jpegs) and len(item["records"]) == len(jpegs)
    blocks = c.parse_mkv((folder / name).read_bytes()).blocks
    assert [list(span) for span in reader.frame_spans(folder, name)] == [[b.offset, b.size] for b in blocks]
    for position, stored in enumerate(jpegs):
        data = reader.read_frame(folder, name, position)
        assert data == stored, "the reader returns the stored bytes: the bytes of the block payload"
        assert c.decode_jpeg(data).size == (c.WIDTH, c.HEIGHT), "PyAV decodes each frame"
    assert reader.camera_details(folder, name)["display_rotation"] == 0, "the reader gives no rotation from the EXIF tag"


def test_sft_713_built_file_self_test(tmp_path):
    """SFT-713, a self-test of the camera file that the test builds. It needs no reader. Checks: SFF-738, SFF-739."""
    name, jpegs, track_bytes = c.build_unusual_take(tmp_path / "take")
    path = tmp_path / "take" / name
    data = path.read_bytes()
    mkv = c.parse_mkv(data)
    assert set(track_bytes) == {1, 2} and [b.track_bytes for b in mkv.blocks] == track_bytes
    assert [b.track for b in mkv.blocks] == [1] * len(jpegs) and mkv.tracks[0]["codec"] == "V_MJPEG"
    assert [data[b.offset : b.offset + b.size] for b in mkv.blocks] == jpegs
    for stored in jpegs:
        markers = [marker for marker, _, _ in c.jpeg_segments(stored)]
        assert c.APP0 not in markers and c.DHT not in markers, "no JFIF and no DHT"
        assert c.exif_orientation(stored) == 6 and stored.endswith(b"\xff\xd9" + bytes(7)), "an EXIF tag and trailing bytes"
        assert c.decode_jpeg(stored).size == (c.WIDTH, c.HEIGHT)
    assert c.count_packets(path) == len(jpegs), "the pinned FFmpeg finds each frame"
    sidecar = c.check_sidecar_common(path.with_suffix(".csv"))
    assert [(int(row["byte_offset"]), int(row["byte_size"])) for row in sidecar.rows] == [(b.offset, b.size) for b in mkv.blocks]


def _check_unfinished_camera_files(reader, folder, method: str) -> None:
    take = c.only_take(c.read(reader, folder, records=True))
    cameras = c.cameras_of(take)
    assert len(cameras) == 3
    for item in cameras:
        data = (folder / item["name"]).read_bytes()
        sidecar = c.read_sidecar(c.sidecar_path(folder, item["name"]))
        blocks = c.parse_mkv(data).blocks  # the complete blocks, by a walk that does not use the test adapter
        usable = min(len(sidecar.rows), len(blocks))
        assert item["rows"] == len(sidecar.rows), "`rows` is the number of usable CSV rows"
        assert [record[0] for record in item["records"]] == list(range(usable)), "`records` holds only the usable frames"
        spans = reader.frame_spans(folder, item["name"], method=method)
        assert [list(span) for span in spans] == [[b.offset, b.size] for b in blocks[:usable]]
        for k in range(usable):  # row k belongs to the k-th complete block
            assert reader.read_frame(folder, item["name"], k) == data[blocks[k].offset : blocks[k].offset + blocks[k].size]


@pytest.mark.parametrize("case", ["audio_clean_kill", "audio_torn_fragment"])
def test_sft_714_unfinished_camera_file(reader, golden_or_skip, case):
    """SFT-714 Reader: an unfinished camera file, found by a walk. Checks: SFF-740, SFF-757."""
    _check_unfinished_camera_files(reader, golden_or_skip("G05", case), "walk")


@pytest.mark.provisional("desk test DT5 (SFF-757)")
@pytest.mark.parametrize("case", ["audio_clean_kill", "audio_torn_fragment"])
def test_sft_714_csv_offsets_provisional(reader, golden_or_skip, case):
    """SFT-714, the provisional check: the reader finds the same frames from the CSV offsets. Checks: SFF-740, SFF-757."""
    _check_unfinished_camera_files(reader, golden_or_skip("G05", case), "csv")
