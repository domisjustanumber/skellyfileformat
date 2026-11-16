"""Conformance tests SFT-725 to SFT-729: clocks, the fit and reader timing (SPEC.md section 11).

The Pass text of each test is in spec/conformance.md. A test gets the reader or the writer from a
fixture, so it fails with one line until the implementation exists (decision G21H).
"""

from __future__ import annotations

import bisect
import json
import re
import sys
import time

import pytest

import checks_capture as c

G5_CASES = ["audio_clean_kill", "audio_torn_fragment"]


def _keys(node, found: set) -> set:
    if isinstance(node, dict):
        found.update(node)
        for child in node.values():
            _keys(child, found)
    elif isinstance(node, list):
        for child in node:
            _keys(child, found)
    return found


@pytest.mark.parametrize(
    "vector",
    [pytest.param("windows_writer", marks=pytest.mark.skipif(sys.platform != "win32", reason="the Windows checks need Windows")), "unknown_clock"],
)
def test_sft_725_clock_and_take_start(writer, reader, golden_or_skip, tmp_path, vector):
    """SFT-725 Writer and reader: the clock and the take start. Checks: SFF-772, SFF-773, SFF-774.

    The checks on Linux and macOS are provisional (test_sft_725_linux_macos_provisional).
    """
    if vector == "unknown_clock":
        take = c.only_take(c.read(reader, golden_or_skip("G11", "unknown_clock")))
        invalid = [item for item in take["files"] if item["state"] == "invalid"]
        assert [item["reason"] for item in invalid] == ["bad_metadata"]
        return
    folder = tmp_path / "take"
    c.record_take(writer, folder, audio=c.microphone())
    _check_clock(folder, "windows_qpc")


def _check_clock(folder, clock: str) -> None:
    sidecars = [c.read_sidecar(path) for path in c.media_files(folder, ".csv")]
    assert len(sidecars) == 3 and all(sidecar.header["clock"] == clock for sidecar in sidecars)
    starts = {(s.header["take_start_host_ns"], s.header["take_start_utc_ns"], s.header["utc_offset_min"]) for s in sidecars}
    assert len(starts) == 1, "each file has the same take start"
    # No time-zone name is written: no key for one, and no name of the local time zone in a text file.
    keys = set()
    for sidecar in sidecars:
        keys.update(sidecar.header)
    texts = [sidecar.data for sidecar in sidecars]
    for path in folder.glob("*.json"):
        texts.append(path.read_bytes())
        _keys(json.loads(texts[-1]), keys)
    assert not [key for key in keys if re.search(r"time_?zone|(^|_)tz(_|$)", key)]
    assert not [name for name in time.tzname if name and any(name.encode() in text for text in texts)]


@pytest.mark.provisional("the timing tests T-S7 on Linux and macOS (SFF-773)")
def test_sft_725_linux_macos_provisional(writer, tmp_path):
    """SFT-725, the provisional checks: `linux_monotonic` on Linux and `macos_uptime_raw` on macOS. Checks: SFF-773."""
    c.record_take(writer, tmp_path / "take", audio=c.microphone())
    _check_clock(tmp_path / "take", {"linux": "linux_monotonic", "darwin": "macos_uptime_raw"}[sys.platform])


def test_sft_726_fit(writer, tmp_path):
    """SFT-726 Writer: the fit. Checks: SFF-775, SFF-776, SFF-778."""
    folder = tmp_path / "take"
    c.record_take(writer, folder, audio=c.microphone())
    sidecars = c.media_files(folder, ".csv")
    assert len(sidecars) == 3
    for path in sidecars:
        c.check_fit(path)


def test_sft_726_check_on_golden(golden_or_skip):
    """SFT-726, the same check on the sidecars of G1. Checks: SFF-775, SFF-776, SFF-778."""
    for path in c.media_files(golden_or_skip("G01"), ".csv"):
        c.check_fit(path)


@pytest.mark.parametrize("impl", c.IMPLS)
@pytest.mark.parametrize("vector", ["committed", "different_fitter"])
def test_sft_727_fit_evaluation(reader, js_reader, golden_or_skip, variant, expected, vector, impl):
    """SFT-727 Reader: fit evaluation, in Python and JS. Checks: SFF-777, SFF-779, SFF-780.

    The committed values are the `player_ns` and `fitted_ns` of the committed results of G12.
    """
    folder = golden_or_skip("G12")
    if vector == "different_fitter":
        folder = variant("G12")
        line = b'# fit fitter=another-fitter fitter_version=9.9.9 fitter_params={"window":[1,2],"text":"a b"}'
        for path in c.media_files(folder, ".csv"):
            path.write_bytes(re.sub(rb"(?m)^# fit .*$", line, path.read_bytes()))
    assert c.result_bytes(impl, reader, js_reader, folder) == expected("G12", "take", c.scope_of(impl))


@pytest.mark.parametrize("target", ["G01/take", "G12/take", "G05/audio_clean_kill", "G05/audio_torn_fragment"])
def test_sft_728_player_time_and_frame_shown(reader, golden_or_skip, target):
    """SFT-728 Reader: player time and the frame shown. Checks: SFF-781, SFF-782, SFF-783.

    The fitted times are computed here from the fit lines of each sidecar, with no use of the package.
    """
    name = target.split("/")[0]
    folder = golden_or_skip(*target.split("/"))
    cameras = c.cameras_of(c.only_take(c.read(reader, folder, records=True)))
    fitted_cameras = []
    for item in cameras:
        sidecar = c.read_sidecar(c.sidecar_path(folder, item["name"]))
        player = [record[4] for record in item["records"]]
        has_fit = sidecar.finished and bool(sidecar.lines("fit_segment"))
        fitted_cameras.append(has_fit)
        if has_fit:
            assert player == c.video_fitted_ns(sidecar), "the player time is the fitted time"
            assert "missing_fit" not in item["warnings"]
        else:
            arrival = sidecar.integers("arrival_ns")[: len(player)]  # from the sidecar, not from the `records`
            assert [record[2] for record in item["records"]] == arrival and player == arrival, "the player time is the arrival time"
            assert "missing_fit" in item["warnings"]
        assert all(a <= b for a, b in zip(player, player[1:])), "the player time never decreases"
        equal = [k for k in range(len(player) - 1) if player[k] == player[k + 1]]
        strict = [player[0]]  # SFF-782: s(0) = p(0), s(k) = max(p(k), s(k - 1) + 1)
        for value in player[1:]:
            strict.append(max(value, strict[-1] + 1))
        assert reader.camera_details(folder, item["name"])["strict_ns"] == strict, "the times for freemocap strictly increase (SFF-782)"
        if name == "G12" and item is cameras[3]:
            assert equal, "camera 3 of G12 has two rows with equal fitted times, and `records` hold the two equal times"
        # At each test time t, the frame shown is the last frame with a player time at or before t.
        times = {player[0] - 1, player[-1] + 10**9}
        for value in player:
            times.update((value - 1, value, value + 1))
        for t in sorted(times):
            shown = bisect.bisect_right(player, t) - 1
            assert reader.position_at(folder, item["name"], t) == (shown if shown >= 0 else None)
    assert fitted_cameras == {"G01": [True, True], "G12": [True, True, False, True], "G05": [False, False, False]}[name]


def _audio_fit(folder, name: str) -> tuple[c.Sidecar, list[dict]]:
    """The sidecar of the audio file and the fit that a reader uses: the fit lines, else the fit of SFF-784."""
    sidecar = c.read_sidecar(c.sidecar_path(folder, name))
    return sidecar, (c.audio_fit_of_lines(sidecar) if sidecar.finished else c.audio_fit_of_reader(sidecar))


VECTORS_729 = [
    "click_times:G01/take",
    *(f"reader_fit:G05/{case}" for case in G5_CASES),
    *(f"fitted_ns:{target}:{impl}" for target in ("G01/take", *(f"G05/{case}" for case in G5_CASES)) for impl in c.IMPLS),
    "one_row:G05/audio_clean_kill",
    "silence_row:G05/audio_clean_kill",
    *(f"usable_length:{target}" for target in ("G01/take", *(f"G05/{case}" for case in G5_CASES))),
]


@pytest.mark.parametrize("vector", VECTORS_729)
def test_sft_729_audio_mapping_and_length(reader, js_reader, golden_or_skip, variant, truth, vector):
    """SFT-729 Reader: audio mapping and length. Checks: SFF-784, SFF-785.

    The fit of the reader and the usable length are computed here from the golden files, with the
    formulas of SFF-784 and SFF-785 and no use of the package. `reader_fit` of the truth file of G5
    is the committed value.
    """
    vector, target, impl = (vector.split(":") + [""])[:3]
    folder = golden_or_skip(*target.split("/"))
    facts = truth(*target.split("/"))
    name = facts["audio"]["name"]

    if vector == "click_times":
        take = c.only_take(c.read(reader, folder, records=True))
        for j, click in enumerate(facts["audio"]["click_samples"]):
            click_ns = reader.sample_time_ns(folder, name, click)
            for camera in facts["cameras"]:
                (item,) = [item for item in take["files"] if item["name"] == camera["name"]]
                flash_ns = item["records"][camera["flash_positions"][j]][4]
                assert abs(click_ns - flash_ns) < 1_000_000, "each click is within 1 ms of the matching video flash"
    elif vector == "reader_fit":
        item = c.audio_of(c.only_take(c.read(reader, folder)))
        assert item["fit"] is False and "missing_fit" in item["warnings"]
        sidecar, segments = _audio_fit(folder, name)
        (found,) = reader.audio_details(folder, name)["fit_segments"]
        assert {key: found[key] for key in ("n0", "t0_ns", "period_fs")} == {key: segments[0][key] for key in ("n0", "t0_ns", "period_fs")}
        assert segments[0] == facts["audio"]["reader_fit"], "the committed values are the values of SFF-784"
    elif vector == "fitted_ns":
        sidecar, segments = _audio_fit(folder, name)
        item = c.audio_of(c.only_take(json.loads(c.result_bytes(impl, reader, js_reader, folder))))
        assert len(item["records"]) == len(sidecar.rows)
        for block, first_sample, _, _, fitted_ns in item["records"]:
            assert fitted_ns == c.audio_fitted_ns(segments, block, first_sample)
    elif vector == "one_row":
        folder = variant(*target.split("/"))
        path = c.sidecar_path(folder, name)
        sidecar = c.read_sidecar(path)
        first_row_end = sidecar.data.index(sidecar.row_lines[0].encode()) + len(sidecar.row_lines[0]) + 1
        path.write_bytes(sidecar.data[:first_row_end])
        item = c.audio_of(c.only_take(c.read(reader, folder, records=True)))
        assert [record[4] for record in item["records"]] == [None], "each `fitted_ns` is null"
        assert list(reader.audio_details(folder, name)["fit_segments"]) == [], "the reader computes no fit"
        assert reader.sample_time_ns(folder, name, 0) is None, "the reader maps no sample to take time"
    elif vector == "silence_row":
        changed = variant(*target.split("/"))
        path = c.sidecar_path(changed, name)
        rows = len(c.read_sidecar(path).rows)
        assert rows >= 3
        c.set_row(path, rows // 2, "flags", c.SILENCE)
        assert c.audio_of(c.only_take(c.read(reader, changed)))["rows"] == rows == c.audio_of(c.only_take(c.read(reader, folder)))["rows"]
        assert reader.audio_details(changed, name)["fit_segments"] == reader.audio_details(folder, name)["fit_segments"]
    else:
        usable = c.audio_usable_samples(folder / name)
        assert reader.audio_details(folder, name)["usable_samples"] == usable
        assert reader.sample_time_ns(folder, name, usable - 1) is not None
        assert reader.sample_time_ns(folder, name, usable) is None, "no audio is scheduled after the usable length"
