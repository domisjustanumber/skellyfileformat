"""Conformance tests SFT-715 to SFT-724: timing sidecars and audio (SPEC.md sections 7 to 10).

The Pass text of each test is in spec/conformance.md. A test gets the reader or the writer from a
fixture, so it fails with one line until the implementation exists (decision G21H).
"""

from __future__ import annotations

import pytest

import checks_capture as c

G5_CASES = ["audio_clean_kill", "audio_torn_fragment"]


def _trace(events: list):
    return lambda event, path: events.append((event, path))


@pytest.mark.parametrize("channels", [1, 2], ids=["mono_as_g1", "stereo_as_g2"])
def test_sft_715_common_csv_rules(writer, tmp_path, channels):
    """SFT-715 Writer: the common CSV rules. Checks: SFF-741, SFF-742, SFF-743, SFF-744, SFF-745."""
    folder = tmp_path / "take"
    c.record_take(writer, folder, audio=c.microphone(channels))
    sidecars = c.media_files(folder, ".csv")
    assert len(sidecars) == 3
    for path in sidecars:
        c.check_sidecar_common(path)


@pytest.mark.parametrize("name", ["G01", "G02"])
def test_sft_715_check_on_golden(golden_or_skip, name):
    """SFT-715, the same check on the sidecars of G1 and G2. Checks: SFF-741 to SFF-745."""
    for path in c.media_files(golden_or_skip(name), ".csv"):
        c.check_sidecar_common(path)


@pytest.mark.parametrize(
    ("vector", "case"),
    [(vector, case) for vector in ("torn_row", "wrong_crc", "no_end_line") for case in G5_CASES] + [("cut_end_line", "G01")],
)
def test_sft_716_strict_reading(reader, golden_or_skip, variant, vector, case):
    """SFT-716 Reader: strict reading. Checks: SFF-746, SFF-747.

    The cameras of G5: 0 has a clean cut, 1 has a torn row of 37 bytes, 2 has a row with a wrong CRC.
    `torn_bytes` is compared with the sum of SFF-791, from parsers that do not use the test adapter.
    """
    if vector == "cut_end_line":
        folder = variant("G01")
        video = folder / c.load_json(folder / c.MANIFEST)["cameras"][0]["video"]
        path = video.with_suffix(".csv")
        data = path.read_bytes()
        path.write_bytes(data[: data.rindex(b"# end") + 8])  # in the middle of the `# end` line
        sidecar = c.read_sidecar(path)
        assert sidecar.torn == 8 and any(line.startswith("# fit ") for line in sidecar.footer)
        item = c.cameras_of(c.only_take(c.read(reader, folder)))[0]
        assert item["state"] == "unfinished"
        assert item["rows"] == len(sidecar.rows) > 0, "no data row after the first footer line, and no footer line counts"
        assert item["torn_bytes"] == c.torn_bytes_of_pair(video), "the bytes of the torn footer line are in `torn_bytes`"
        assert item["fit"] is False
        return
    folder = golden_or_skip("G05", case)
    index = {"no_end_line": 0, "torn_row": 1, "wrong_crc": 2}[vector]
    item = c.cameras_of(c.only_take(c.read(reader, folder)))[index]
    sidecar = c.read_sidecar(c.sidecar_path(folder, item["name"]))
    assert not sidecar.finished
    if vector == "torn_row":
        assert sidecar.torn == 37, "the golden sidecar has a torn row of 37 bytes"
        assert item["state"] == "unfinished"
    elif vector == "wrong_crc":
        assert sidecar.bad_crc and len(sidecar.row_lines) > len(sidecar.rows) + 1, "a wrong CRC, and rows after it"
        assert (item["state"], item["reason"]) == ("damaged", "crc_mismatch")
        assert item["rows"] == len(sidecar.rows), "the read stops at the row with the wrong CRC"
    else:
        assert item["state"] == "unfinished", "a sidecar with no `# end` line is `unfinished`"
    assert item["torn_bytes"] == c.torn_bytes_of_pair(folder / item["name"])


VECTORS_717 = ["take", "confirmed_key", "converter", "encoder_failure", "equal_source_frame_number", "empty_source_frame_number", "reader_gap_warning"]


@pytest.mark.parametrize("vector", VECTORS_717)
def test_sft_717_video_sidecar(writer, reader, golden_or_skip, tmp_path, vector):
    """SFT-717 Writer: the video sidecar. Checks: SFF-749, SFF-752, SFF-754, SFF-755, SFF-756, SFF-758, SFF-887.

    The check of the bit `filled` is provisional (test_sft_717_filled_bit_provisional).
    """
    folder = tmp_path / "take"
    if vector == "reader_gap_warning":
        folder = golden_or_skip("G01")
        gap_camera = c.sidecars_by_position(folder)[1]
        assert any(flag & c.GAP for flag in gap_camera.integers("flags")), "the gap of G1 has the flag `gap`"
        item = c.cameras_of(c.only_take(c.read(reader, folder)))[1]
        assert "gap" in item["warnings"], "a reader gives that camera file the file warning `gap`"
    elif vector == "take":
        c.record_take(writer, folder, audio=c.microphone())
        videos = c.check_video_sidecars(folder)
        flags = videos[1].integers("flags")
        assert flags[5] & c.GAP and flags[0] == 0, "the forced gap of camera 1 has the flag `gap`"
    elif vector == "confirmed_key":
        remembered = "0123456789abcdef"
        cameras = [c.camera(0), c.camera(1, camera_key=remembered, key_origin="confirmed_by_user")]
        c.record_take(writer, folder, cameras, c.microphone())
        videos = c.check_video_sidecars(folder)
        assert videos[1].header["camera_key"] == remembered, "the confirmed camera has the remembered key"
        assert c.capture_info_of(folder)["camera_configs"][remembered]["key_origin"] == "confirmed_by_user"
    elif vector == "converter":
        # A converter has one old time for each frame and no driver time.
        sent = c.record_take(writer, folder, [c.camera(0, camera_key="0", key_origin=None)], mode="conversion", sampled=False)
        (video,) = c.check_video_sidecars(folder, capture=False)
        assert video.integers("arrival_ns") == sent["arrival_ns"][0], "the converter writes the old time as `arrival_ns`"
        assert all(row["sample_ns"] == "" for row in video.rows), "`sample_ns` is empty when no driver time exists"
    else:
        raw = vector == "encoder_failure"
        requested = dict(c.camera(0)["requested"], capture_format="YUYV" if raw else "MJPG")
        take = writer.TakeWriter(folder, "synthetic_take", [c.camera(0, requested=requested)], None, writer=c.WRITER)
        # encoder_failure: the raw frame 2 has no bytes, so the JPEG encoder fails and no frame is stored.
        empty = vector == "empty_source_frame_number"
        numbers = [1000, 1001, 1002, 1003, 1004] if raw else [1000, None, 1005, 1006] if empty else [1000, 1001, 1001, 1002]
        for position, number in enumerate(numbers):
            data = c.yuyv(position) if raw else c.jpeg(position)
            if raw and position == 2:
                data = b""
            take.write_frame(0, data, take.take_start_host_ns + 33_333_333 * (position + 1), source_frame_number=number)
        take.close()
        (video,) = c.check_video_sidecars(folder)
        flags = video.integers("flags")
        if raw:
            assert len(flags) == 4 and flags[2] & c.ENCODE_SKIP, "the row after the encoder failure has `encode_skip`"
            assert int(video.lines("end")[0]["encode_skips"]) == 1
        elif empty:
            # Row 1 has no number, and row 2 follows it: `gap` is 0 in both, also with the jump from 1000 to 1005.
            assert video.rows[1]["source_frame_number"] == "" and flags[1:3] == [0, 0], "`gap` is 0 next to an empty number"
        else:
            assert flags[2] & c.REPEAT and not flags[2] & c.GAP, "the flag `repeat` and not the flag `gap`"


@pytest.mark.parametrize("case", ["take", "confirmed_key"])
def test_sft_717_check_on_golden(golden_or_skip, case):
    """SFT-717, the sidecar check on the two cases of G1. Checks: SFF-749, SFF-752, SFF-754, SFF-756, SFF-758."""
    folder = golden_or_skip("G01", case)
    videos = c.check_video_sidecars(folder)
    config = c.capture_info_of(folder)["camera_configs"][videos[1].header["camera_key"]]
    assert config["key_origin"] == ("computed" if case == "take" else "confirmed_by_user")
    assert sum(1 for flag in videos[1].integers("flags") if flag & c.GAP) == 1


@pytest.mark.provisional("the slot assembly of the skellycam plan and desk tests DT4 and DT7 (SFF-756)")
def test_sft_717_filled_bit_provisional(writer, tmp_path):
    """SFT-717, the provisional check: the writer writes 0 to the bit `filled`. Checks: SFF-756."""
    c.record_take(writer, tmp_path / "take")
    for sidecar in c.sidecars_by_position(tmp_path / "take"):
        assert not any(flag & c.FILLED for flag in sidecar.integers("flags"))
        assert sidecar.lines("end")[0]["filled"] == "0"


@pytest.mark.parametrize(
    ("case", "reason"),
    [("rate_0_1", "bad_rate"), ("rate_2_20_plus_1", "bad_rate"), ("rotation_45", "bad_rotation"), ("bad_label", "bad_label"), ("G04", None)],
)
def test_sft_718_rate_rotation_and_label(reader, golden_or_skip, truth, case, reason):
    """SFT-718 Reader: rate, rotation and label values. Checks: SFF-750, SFF-751, SFF-753."""
    if case != "G04":
        take = c.only_take(c.read(reader, golden_or_skip("G11", case)))
        invalid = [item for item in take["files"] if item["state"] == "invalid"]
        assert [item["reason"] for item in invalid] == [reason]
        return
    image_module = pytest.importorskip("PIL.Image")
    folder = golden_or_skip("G04")
    facts = truth("G04", "take")
    inset = facts["corner_px"] // 2
    assert sorted(camera["display_rotation"] for camera in facts["cameras"]) == [0, 90, 180, 270]
    for camera in facts["cameras"]:
        rotation = reader.camera_details(folder, camera["name"])["display_rotation"]
        assert rotation == camera["display_rotation"]
        stored = c.decode_jpeg(reader.read_frame(folder, camera["name"], 0))
        # Image.rotate turns counter-clockwise, so the clockwise rotation is the negative angle.
        upright = stored.rotate(-rotation, expand=True, resample=image_module.Resampling.NEAREST)
        width, height = upright.size
        points = {
            "top_left": (inset, inset), "top_right": (width - 1 - inset, inset),
            "bottom_left": (inset, height - 1 - inset), "bottom_right": (width - 1 - inset, height - 1 - inset),
        }  # fmt: skip
        for corner, point in points.items():
            found, want = upright.getpixel(point), camera["upright_corners"][corner]
            assert all(abs(a - b) <= 40 for a, b in zip(found, want)), f"{camera['name']}: the {corner} corner"


@pytest.mark.parametrize("source", [("G01", "take"), ("G06", "repaired")], ids=["finished", "repaired"])
def test_sft_719_rows_against_blocks(reader, variant, source):
    """SFT-719 Reader: rows against blocks. Checks: SFF-759.

    The input is a copy of G1 (a finished pair) or of G6 `repaired` (a repaired pair) in which the
    sidecar of camera 0 has one row more than the camera file has blocks. The row, the fit segment and
    the `# end` line are correct in all other points. A reader refuses a repaired pair as it refuses a
    finished pair (ADR-W5AK item 10).
    """
    folder = variant(*source)
    video = c.load_json(folder / c.MANIFEST)["cameras"][0]["video"]
    path = c.sidecar_path(folder, video)
    sidecar = c.read_sidecar(path)
    count, last = len(sidecar.rows), sidecar.rows[-1]
    row = c.row_line(
        [count, int(last["source_frame_number"]) + 1, int(last["arrival_ns"]) + 33_333_333, int(last["sample_ns"]) + 33_333_333,
         0, last["byte_offset"], last["byte_size"]]
    )  # fmt: skip
    footer = sidecar.data[sidecar.rows_end :].decode()
    footer = footer.replace(f"pos_last={count - 1}", f"pos_last={count}").replace(f"rows={count}", f"rows={count + 1}")
    path.write_bytes(sidecar.data[: sidecar.rows_end] + row.encode() + footer.encode())
    assert len(c.check_sidecar_common(path).rows) == count + 1
    (item,) = [item for item in c.only_take(c.read(reader, folder))["files"] if item["name"] == video]
    assert (item["state"], item["reason"]) == ("invalid", "bad_metadata")


@pytest.mark.parametrize("channels", [1, 2], ids=["mono_as_g1", "stereo_as_g2"])
def test_sft_720_audio_file_and_sidecar(writer, tmp_path, channels):
    """SFT-720 Writer: the audio file and its sidecar.

    Checks: SFF-760, SFF-761, SFF-762, SFF-764, SFF-767, SFF-768, SFF-769, SFF-770.
    """
    folder, events = tmp_path / "take", []
    c.record_take(writer, folder, audio=c.microphone(channels), trace=_trace(events))
    (path,) = c.media_files(folder, ".m4a")
    mp4 = c.check_audio_pair(path)
    assert mp4.channels == channels
    # The trace shows a flush after each packet that the muxer gives.
    audio_events = [event for event, name in events if name == f"{c.MEDIA}/{path.name}" and event in ("write", "flush")]
    assert audio_events.count("write") >= len(mp4.fragments)
    assert all(audio_events[i + 1 : i + 2] == ["flush"] for i, event in enumerate(audio_events) if event == "write")
    assert c.microphone()["device_name"].encode() not in path.with_suffix(".csv").read_bytes(), "no microphone name is in the sidecar"


@pytest.mark.parametrize("name", ["G01", "G02"])
def test_sft_720_check_on_golden(golden_or_skip, name):
    """SFT-720, the audio check on G1 and G2: the boxes, `dOps`, `mfra`, the rows and the counts. Checks: SFF-760 to SFF-770."""
    folder = golden_or_skip(name)
    (path,) = c.media_files(folder, ".m4a")
    assert c.check_audio_pair(path).channels == (1 if name == "G01" else 2)
    assert c.capture_info_of(folder)["audio"]["device_name"].encode() not in path.with_suffix(".csv").read_bytes()


def test_sft_721_opus_encoder_is_libopus(writer):
    """SFT-721 Release check: the Opus encoder is libopus. Checks: SFF-763."""
    assert writer.release_check()["opus_encoder"] == "libopus"


@pytest.mark.parametrize("vector", ["drop_of_4800_samples", "input_overflow"])
def test_sft_722_audio_gaps(writer, tmp_path, vector):
    """SFT-722 Writer: audio gaps. Checks: SFF-765, SFF-768."""
    folder = tmp_path / "take"
    take = writer.TakeWriter(folder, "synthetic_take", [c.camera(0)], c.microphone(), writer=c.WRITER)
    start = take.take_start_host_ns
    take.write_frame(0, c.jpeg(), start + 33_333_333, source_frame_number=1000)
    # The device timeline has 26 blocks of 4,800 samples. The device drops block 10: samples 48,000 to 52,799.
    clicks = [4207, 28207, 57007, 81007, 105007]
    pcm = c.click_pcm(26 * 4800, clicks)
    for block in range(26):
        if vector == "drop_of_4800_samples" and block == 10:
            continue
        take.write_audio(
            pcm[block * 9600 : (block + 1) * 9600],
            start + 100_000_000 * (block + 1),
            dropped_before=4800 if vector == "drop_of_4800_samples" and block == 11 else 0,
            overflow=vector == "input_overflow" and block == 7,
        )
    take.close()
    (path,) = c.media_files(folder, ".m4a")
    c.check_audio_pair(path)
    sidecar = c.read_sidecar(path.with_suffix(".csv"))
    flags = sidecar.integers("flags")
    if vector == "input_overflow":
        assert [k for k, flag in enumerate(flags) if flag & c.OVERFLOW] == [7], "the row of the input overflow has `overflow`"
        return
    (silent,) = [row for row, flag in zip(sidecar.rows, flags) if flag & c.SILENCE]
    assert (int(silent["first_sample"]), int(silent["n_samples"])) == (48000, 4800), "the row of the drop has the flag `silence`"
    (samples,) = c.decode_audio(path)
    assert max(abs(value) for value in samples[48000:52800]) < 0.02, "4,800 samples of silence at the drop"
    onsets = c.click_onsets(samples)
    assert len(onsets) == len(clicks) and all(abs(a - b) <= 2 for a, b in zip(onsets, clicks)), (
        "the click times of the decoded stream equal the device sample indexes"
    )


def test_sft_723_pre_skip_and_output_gain(reader, golden_or_skip, truth):
    """SFT-723 Reader: pre-skip and output gain. Checks: SFF-766."""
    folder = golden_or_skip("G01")
    name = truth("G01", "take")["audio"]["name"]
    mp4 = c.parse_mp4((folder / name).read_bytes())
    assert reader.audio_details(folder, name)["pre_skip"] == mp4.pre_skip, "`audio_details` gives the pre-skip of `dOps`"
    _check_decoded_clicks(folder, truth("G01", "take")["audio"])


def _check_decoded_clicks(folder, facts: dict) -> None:
    """Decode with PyAV, which drops the pre-skip samples and applies no output gain. Compare the click offsets."""
    path = folder / facts["name"]
    mp4 = c.parse_mp4(path.read_bytes())
    (samples,) = c.decode_audio(path)
    # Decoded sample 0 is the first sample after the pre-skip: else each click is `pre_skip` samples late.
    assert mp4.output_gain == 0 and mp4.pre_skip > 2
    onsets = c.click_onsets(samples)
    assert len(onsets) == len(facts["click_samples"])
    assert all(abs(a - b) <= 2 for a, b in zip(onsets, facts["click_samples"])), "the click offsets equal the source"


def test_sft_723_check_on_golden(golden_or_skip, truth):
    """SFT-723, the decode part on G1, which needs no reader. Checks: SFF-766."""
    _check_decoded_clicks(golden_or_skip("G01"), truth("G01", "take")["audio"])


@pytest.mark.provisional("the microphone latency test, A3 of the skellycam plan (SFF-771)")
def test_sft_724_audio_latency(reader, golden_or_skip, variant, truth):
    """SFT-724 (provisional) Reader: audio latency. Checks: SFF-771."""
    plain, changed = golden_or_skip("G01"), variant("G01")
    name = truth("G01", "take")["audio"]["name"]
    c.set_header(c.sidecar_path(changed, name), "audio_latency_ns", 5_000_000)
    for sample in (0, 1, 4207, 100_000, 143_999):
        fitted = reader.sample_time_ns(plain, name, sample)
        assert reader.sample_time_ns(changed, name, sample, microphone=True) == fitted - 5_000_000
