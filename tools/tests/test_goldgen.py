"""Tests of the golden generator (tools/goldgen), and cross-checks of the media files of G1.

The tests of the media files need the dependency group ``golden``. Each of them skips when PyAV or
Pillow is absent. The cross-checks read the committed files with PyAV and Pillow. They do not use
the code path that wrote the files, except `ebml_children`.
"""

from __future__ import annotations

import array
import io
import json
import struct
from fractions import Fraction
from pathlib import Path

import pytest
from goldgen import common

from test_golden_files import G01_CASES, footer_values, read_sidecar, relative

# ---------------------------------------------------------------- common.py, standard library only


def test_csv_row_has_the_crc_of_the_bytes_before_its_comma():
    assert common.csv_row(["123456789"]) == "123456789,cbf43926\n"  # the check value of CRC-32/ISO-HDLC
    # An empty field for an absent value, and a CRC with a leading zero (SFF-704).
    assert common.csv_row([42, 543, 1470861856, None, 0, 36019, 882]) == "42,543,1470861856,,0,36019,882,031a5259\n"


def test_sidecar_layout():
    text = common.sidecar({"skellyfileformat": "video_timing", "clock_hz": None}, ["frame"], [[0]], ["# end rows=1"])
    assert text == b"# skellyfileformat=video_timing\n# clock_hz=\nframe,crc32\n0,f4dbdf21\n# end rows=1\n"


def test_fitted_times_round_down():
    assert common.video_fitted_ns(5, 1999, 1) == 6 and common.video_fitted_ns(5, 1999, 3) == 10  # SFF-777
    assert common.audio_fitted_ns(7, 20_833_333_333, 100, 48_100) == 7 + 999_999_999  # SFF-779
    assert common.fit_line() == "# fit fitter=goldgen-truth fitter_version=1.0.0 fitter_params={}"


def test_container_timestamp_rounds_half_up():
    assert [common.container_ms(k, Fraction(30, 1)) for k in (0, 1, 2, 3)] == [0, 33, 67, 100]
    assert common.container_ms(15, Fraction(30000, 1001)) == 501  # 500.5 ms


def test_canonical_json():
    value = {"b": [1, None, True], "a": {"é": "é\n\"", "A": -3}}
    with pytest.raises(AssertionError):
        common.canonical_json(value)  # a key that is not ASCII
    value["a"]["e"] = value["a"].pop("é")
    assert common.canonical_json(value) == '{"a":{"A":-3,"e":"é\\n\\""},"b":[1,null,true]}'.encode()
    for outside in (1.5, 2**53, {"x": 0.0}):
        with pytest.raises(AssertionError):
            common.canonical_json(outside)


def test_small_helpers(tmp_path):
    assert common.camera_key("abc") == "ba7816bf8f01cfea"  # the start of the SHA-256 test vector "abc"
    assert (common.thousandths(30000), common.thousandths(29970)) == (30, 29.97)
    assert common.file_json({"b": 1, "a": 29.97}) == b'{\n  "b": 1,\n  "a": 29.97\n}\n'
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "b").write_bytes(b"abc")
    (tmp_path / "a").write_bytes(b"")
    (tmp_path / "SHA256SUMS").write_bytes(b"old")
    assert common.sums_text(tmp_path) == (
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  a\n"
        "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad  sub/b\n"
    )


def test_expected_result_scopes():
    facts = {"take_uuid": "u", "recording_name": "r", "files": [], "info_path": "r_info.json"}
    states = {
        scope: {link["check"]: link["state"] for link in common.expected_result(facts, scope)["takes"][0]["links"]}
        for scope in ("full", "player")
    }
    assert list(states["full"]) == list(common.LINK_CHECKS)
    assert {c for c in states["full"] if states["full"][c] != states["player"][c]} == {"frames"}


# ---------------------------------------------------------------- the media builders


def test_mkv_holds_the_jpeg_bytes_unchanged(tmp_path):
    pytest.importorskip("av")
    pytest.importorskip("PIL")
    jpegs = [common.jpeg_frame(64, 48, p, 0, flash=p == 1) for p in range(3)]
    assert jpegs[0] == common.jpeg_frame(64, 48, 0, 0, flash=False) and len(set(jpegs)) == 3
    common.build_mkv(tmp_path / "a.mkv", jpegs, Fraction(30, 1), 64, 48)
    common.build_mkv(tmp_path / "b.mkv", jpegs, Fraction(30, 1), 64, 48)
    data = (tmp_path / "a.mkv").read_bytes()
    assert data == (tmp_path / "b.mkv").read_bytes()
    assert [data[at : at + size] for at, size in common.mkv_payloads(data)] == jpegs


# ---------------------------------------------------------------- G1: the media files

INFO, TRACKS, TRACK_ENTRY, VIDEO = 0x1549A966, 0x1654AE6B, 0xAE, 0xE0
TIMESTAMP_SCALE, TRACK_NUMBER, FLAG_LACING, CODEC_ID, DEFAULT_DURATION = 0x2AD7B1, 0xD7, 0x9C, 0x86, 0x23E383
PROJECTION = 0x7670


def children(data: bytes, at: int, size: int) -> list[tuple[int, bytes]]:
    return [(i, data[a : a + s]) for i, a, s in common.ebml_children(data, at, at + size)]


@pytest.mark.parametrize("case", G01_CASES, ids=relative)
def test_g01_camera_files(case):
    av = pytest.importorskip("av")
    image_module = pytest.importorskip("PIL.Image")
    truth = json.loads(case.with_name(case.name + ".truth.json").read_bytes())
    result = json.loads(case.with_name(case.name + ".full.json").read_bytes())
    audio_header, _, audio_footer = read_sidecar(case / Path(truth["audio"]["name"]).with_suffix(".csv"))
    fit = footer_values(audio_footer, "fit_segment")
    click_ns = [
        int(fit["t0_ns"]) + (n + int(audio_header["file_sample_offset"])) * int(fit["period_fs"]) // 10**6
        for n in truth["audio"]["click_samples"]
    ]  # SFF-779, SFF-784

    for camera, item in zip(truth["cameras"], result["takes"][0]["files"]):
        data = (case / camera["name"]).read_bytes()
        header, rows, _ = read_sidecar(case / Path(camera["name"]).with_suffix(".csv"))
        rate = Fraction(header["nominal_rate"])

        with av.open(str(case / camera["name"])) as container:
            (stream,) = container.streams
            packets = [p for p in container.demux(stream) if p.size]
            assert (stream.codec_context.name, stream.time_base) == ("mjpeg", Fraction(1, 1000))
            assert len(packets) == len(rows)  # SFF-759
            bright = []
            for position, (packet, row) in enumerate(zip(packets, rows)):
                at, size = int(row[5]), int(row[6])
                jpeg = bytes(packet)
                assert data[at : at + size] == jpeg and jpeg[:2] == b"\xff\xd8" and jpeg[-2:] == b"\xff\xd9"
                assert packet.is_keyframe
                assert packet.pts == (2 * position * rate.denominator * 1000 + rate.numerator) // (2 * rate.numerator)
                image = image_module.open(io.BytesIO(jpeg))
                assert image.size == (64, 48) and "exif" not in image.info  # SFF-735
                pixels = image.convert("L").tobytes()
                if sum(pixels) / len(pixels) > 200:
                    bright.append(position)
        assert bright == camera["flash_positions"]
        flash_ns = [item["records"][p][4] for p in bright]
        assert all(abs(f - c) < 1_000_000 for f, c in zip(flash_ns, click_ns, strict=True))  # SFT-729

        # The elements that section 6 gives.
        top = list(common.ebml_children(data, 0, len(data)))
        assert data[:4] == b"\x1a\x45\xdf\xa3" and b"matroska" in data[: top[0][1] + top[0][2]]
        segment = children(data, top[1][1], top[1][2])
        (info,) = [payload for i, payload in segment if i == INFO]
        info = dict(children(info, 0, len(info)))
        assert int.from_bytes(info[TIMESTAMP_SCALE], "big") == 1_000_000  # SFF-736
        (tracks,) = [payload for i, payload in segment if i == TRACKS]
        entries = [payload for i, payload in children(tracks, 0, len(tracks)) if i == TRACK_ENTRY]
        assert len(entries) == 1  # SFF-732
        entry = dict(children(entries[0], 0, len(entries[0])))
        assert entry[CODEC_ID] == b"V_MJPEG" and entry[TRACK_NUMBER] == b"\x01" and entry[FLAG_LACING] == b"\x00"
        period_ns = (2 * 10**9 * rate.denominator + rate.numerator) // (2 * rate.numerator)
        assert int.from_bytes(entry[DEFAULT_DURATION], "big") == period_ns
        assert PROJECTION not in dict(children(entry[VIDEO], 0, len(entry[VIDEO])))  # SFF-735
        for at, size in common.mkv_payloads(data):
            assert data[at - 4] == 0x81 and data[at - 1] == 0x80, "track 1, a keyframe, no lacing (SFF-733)"


def boxes(data: bytes, at: int, end: int) -> list[tuple[bytes, bytes]]:
    found = []
    while at < end:
        size, kind = struct.unpack(">I4s", data[at : at + 8])
        found.append((kind, data[at + 8 : at + size]))
        at += size
    assert at == end
    return found


def inside(data: bytes, *path: bytes) -> bytes:
    for kind in path:
        (data,) = [payload for k, payload in boxes(data, 0, len(data)) if k == kind]
    return data


@pytest.mark.parametrize("case", G01_CASES, ids=relative)
def test_g01_audio_file(case):
    av = pytest.importorskip("av")
    truth = json.loads(case.with_name(case.name + ".truth.json").read_bytes())["audio"]
    data = (case / truth["name"]).read_bytes()
    _, _, footer = read_sidecar(case / Path(truth["name"]).with_suffix(".csv"))

    # The boxes of SFF-760 and SFF-761.
    top = boxes(data, 0, len(data))
    kinds = [kind for kind, _ in top]
    fragments = (len(kinds) - 3) // 2
    assert kinds == [b"ftyp", b"moov"] + [b"moof", b"mdat"] * fragments + [b"mfra"]  # SFF-764
    moov = dict(top)[b"moov"]
    assert [k for k, _ in boxes(moov, 0, len(moov))].count(b"trak") == 1 and inside(moov, b"mvex")
    media = inside(moov, b"trak", b"mdia")
    assert struct.unpack(">I", inside(media, b"mdhd")[12:16]) == (48000,)
    table = inside(media, b"minf", b"stbl")
    assert all(struct.unpack(">I", inside(table, k)[4:8]) == (0,) for k in (b"stts", b"stsc", b"stco"))
    entry = inside(table, b"stsd")[8:]
    assert entry[4:8] == b"Opus"
    dops = dict(boxes(entry, 36, len(entry)))[b"dOps"]
    version, channels, pre_skip, input_rate, gain, family = struct.unpack(">BBHIhB", dops)
    assert (version, channels, input_rate, gain, family) == (0, 1, 48000, 0, 0)  # SFF-762

    held, times = 0, []
    for kind, payload in top:
        if kind != b"moof":
            continue
        (traf,) = [p for k, p in boxes(payload, 0, len(payload)) if k == b"traf"]
        parts = boxes(traf, 0, len(traf))
        assert [k for k, _ in parts] == [b"tfhd", b"tfdt", b"trun"]
        tfhd, tfdt, trun = (p for _, p in parts)
        flags = int.from_bytes(tfhd[1:4], "big")
        assert flags & 0x020000 and flags & 0x000008 and tfdt[0] == 1, "default-base-is-moof; tfdt version 1"
        times.append(int.from_bytes(tfdt[4:12], "big"))
        assert int.from_bytes(trun[1:4], "big") & 0x000100 == 0, "each sample has the default duration"
        held += int.from_bytes(trun[4:8], "big") * int.from_bytes(tfhd[8:12], "big")
    assert times == [0, 48000, 96000, 144000][:fragments]
    assert held - pre_skip == int(footer_values(footer, "end")["samples"])  # SFF-785

    # Decode, without the pre-skip samples (SFF-766). PyAV drops them.
    samples = array.array("f")
    with av.open(str(case / truth["name"])) as container:
        assert container.streams[0].codec_context.name == "opus"
        for frame in container.decode(audio=0):
            assert frame.format.name == "fltp" and frame.sample_rate == 48000
            samples.frombytes(bytes(frame.planes[0])[: 4 * frame.samples])
    loud = [i for i, v in enumerate(samples) if abs(v) >= 0.3]  # the click has 0.73; the codec rings below 0.12 before it
    onsets = [i for k, i in enumerate(loud) if k == 0 or i - loud[k - 1] > 4800]
    assert len(onsets) == len(truth["click_samples"])
    assert all(abs(found - click) <= 2 for found, click in zip(onsets, truth["click_samples"]))  # SFT-723
