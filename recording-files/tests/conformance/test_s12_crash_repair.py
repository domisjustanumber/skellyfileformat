"""Conformance tests SFT-730 to SFT-734: writing, crashed files and repair (SPEC.md section 12).

The Pass text of each test is in recording-files/conformance.md. A test gets the reader or the writer from a
fixture, so it fails with one line until the implementation exists (decision G21H).
"""

from __future__ import annotations

import os
import subprocess
import sys
import threading
from pathlib import Path

import pytest

import checks_capture as c

HERE = Path(__file__).resolve().parent
GOLDEN = HERE.parents[1] / "golden"
G5_CASES = ["audio_clean_kill", "audio_torn_fragment"]
REPAIR_WRITER = "skellycam 2.0.1"

# The child process of SFT-730. It records the take of `record_take` and writes one line after the
# take starts and after each write call, then waits for one byte on standard input. The test sends the
# byte for each step but the last one that it wants, and then kills the child: the kill point is exact.
# The child imports the Python adapter of SKELLYSPECS_ADAPTER (conftest.py), with the sys.path of the
# test process. The test runs the child only after the adapter worked in the test process.
CHILD = """
import importlib, os, sys
sys.path[:0] = sys.argv[2].split(os.pathsep)
adapter = importlib.import_module(os.environ["SKELLYSPECS_ADAPTER"])
import checks_capture as c
c.record_take(adapter, c.Path(sys.argv[1]), audio=c.microphone(), after=lambda: (print("step", flush=True), sys.stdin.buffer.read(1)))
"""
KILL_POINTS = 50  # the take has 1 + 2 * 12 + 25 = 50 steps before `close`


def _trace(events: list):
    return lambda event, path: events.append((event, path))


def test_sft_730_whole_files_and_live_files(writer, tmp_path):
    """SFT-730 Writer: whole files and live files. This is the part of the writer of the test adapter.

    Checks: SFF-786, SFF-787, SFF-788, SFF-789.
    The check of the forced write to disk is provisional (test_sft_730_fsync_provisional).
    """
    # A take with no kill: each whole file is replaced in one rename, while the writer holds the lock.
    folder, events = tmp_path / "take", []
    c.record_take(writer, folder, audio=c.microphone(), trace=_trace(events))
    c.check_whole_writes_hold_lock(events, [c.MANIFEST, "synthetic_take_info.json"])
    assert (folder / c.LOCK).is_file() and (folder / c.LOCK).stat().st_size == 0, "the lock is on the empty file"
    assert not list(folder.rglob("*.tmp"))
    live = {f"{c.MEDIA}/{path.name}" for path in (folder / c.MEDIA).iterdir()}
    assert not [event for event in events if event[0] == "replace" and event[1] in live], "a live file is written by appends only"

    # A kill at 50 points of a take.
    for point in range(1, KILL_POINTS + 1):
        killed = tmp_path / f"killed_{point}"
        process = subprocess.Popen(  # noqa: S603
            [sys.executable, "-c", CHILD, str(killed), os.pathsep.join([str(HERE), *sys.path])],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            for step in range(point):
                line = process.stdout.readline()
                assert line, f"the writer ran to kill point {point}: {process.stderr.read().decode()[-500:]}"
                if step < point - 1:
                    process.stdin.write(b"x")
                    process.stdin.flush()
        finally:
            process.kill()
            process.wait()
            for pipe in (process.stdin, process.stdout, process.stderr):
                pipe.close()
        c.check_killed_folder(killed)
        # After a kill, the lock file that no process holds does not stop the next writer.
        assert (killed / c.LOCK).is_file()
        writer.repair_take(killed, writer=REPAIR_WRITER)
        assert c.load_json(killed / c.MANIFEST)["state"] == "finished", f"kill point {point}"


def _hold_lock(path: Path):
    """Take the lock of SFF-789 for this OS on `path` (ADR-6AT7 item 7). Return a function that releases it."""
    handle = open(path, "r+b")  # noqa: SIM115
    if sys.platform == "win32":
        import msvcrt

        msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)  # `LockFile` of byte 0, for 1 byte

        def release() -> None:
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            handle.close()
    else:
        import fcntl

        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)

        def release() -> None:
            fcntl.flock(handle, fcntl.LOCK_UN)
            handle.close()

    return release


def test_sft_730_lock_form(writer, tmp_path):
    """SFT-730, the form of the lock: while the test holds it, the writer does not replace the manifest. Checks: SFF-789.

    The writer can wait for the lock or refuse the write. The test accepts both.
    """
    folder = tmp_path / "take"
    take = writer.TakeWriter(folder, "synthetic_take", [c.camera(0)], None, writer=c.WRITER)
    take.write_frame(0, c.jpeg(0), take.take_start_host_ns + 33_333_333, source_frame_number=0)
    before = (folder / c.MANIFEST).read_bytes()
    outcome = []

    def close() -> None:
        try:
            take.close()
            outcome.append(None)
        except Exception as error:  # noqa: BLE001  a refusal of the write is allowed
            outcome.append(error)

    release = _hold_lock(folder / c.LOCK)
    thread = threading.Thread(target=close, daemon=True)
    try:
        thread.start()
        thread.join(1.0)
        assert (folder / c.MANIFEST).read_bytes() == before, "no replace of the manifest while the test holds the lock"
    finally:
        release()
    thread.join(30.0)
    assert not thread.is_alive() and len(outcome) == 1
    if outcome[0] is None:
        assert c.load_json(folder / c.MANIFEST)["state"] == "finished"


@pytest.mark.provisional("the measurement of the cost of fsync (SFF-788)")
def test_sft_730_fsync_provisional(writer, tmp_path):
    """SFT-730, the provisional check: a writer forces each live file to disk about once a second. Checks: SFF-788."""
    events = []
    c.record_take(writer, tmp_path / "take", audio=c.microphone(), trace=_trace(events))
    assert [event for event in events if event[0] == "fsync"]


@pytest.mark.external("freemocap")
def test_sft_730_external():
    """SFT-730, the external sentences. Checks: SFF-786, SFF-789.

    A kill during freemocap processing. freemocap holds `.processing.lock` while it writes a folder
    file whole. freemocap appends to the journal without the lock.
    """


@pytest.mark.parametrize("case", G5_CASES)
def test_sft_731_stray_temporary_files(reader, golden_or_skip, case):
    """SFT-731 Reader: stray temporary files. Checks: SFF-790."""
    folder = golden_or_skip("G05", case)
    assert list(folder.glob("*.tmp")), "the golden case has a `.tmp` manifest"
    found = c.read_bytes(reader, folder)
    assert b".tmp" not in found, "the `.tmp` manifest is in no list of the result"
    assert c.json.loads(found)["folder_warnings"].count("stray_tmp") == 1


@pytest.mark.parametrize("target", [*(f"G05/{case}" for case in G5_CASES), "G01/take", "G06/repaired"])
def test_sft_732_unfinished_files(reader, golden_or_skip, target):
    """SFT-732 Reader: unfinished files. Checks: SFF-791, SFF-792.

    `torn_bytes` is compared with the sum of SFF-791, from parsers that do not use the test adapter.
    """
    folder = golden_or_skip(*target.split("/"))
    take = c.only_take(c.read(reader, folder, records=True))
    assert take["files"]
    for item in take["files"]:
        sidecar = c.read_sidecar(c.sidecar_path(folder, item["name"]))
        if not target.startswith("G05"):
            assert sidecar.finished and item["torn_bytes"] == 0, "`torn_bytes` is 0 for a finished and for a repaired pair"
            continue
        assert item["state"] in ("unfinished", "damaged")
        assert item["rows"] == len(sidecar.rows), "the file reads to its last complete record"
        assert item["torn_bytes"] == c.torn_bytes_of_pair(folder / item["name"])
        if item["kind"] == "audio":  # SFF-792: only the blocks whose every sample is in a complete fragment
            assert len(item["records"]) == c.audio_whole_blocks(folder / item["name"]) < item["rows"]
    if target == "G05/audio_torn_fragment":
        audio = folder / c.audio_of(take)["name"]
        assert audio.stat().st_size > c.media_complete_end(audio), "the golden audio file has a torn fragment"
        details = reader.audio_details(folder, c.audio_of(take)["name"])
        assert details["usable_samples"] == c.audio_usable_samples(audio), "the torn audio fragment is ignored"


def _repair(writer, folder: Path, events: list | None = None) -> None:
    writer.repair_take(folder, writer=REPAIR_WRITER, trace=_trace([] if events is None else events))


VECTORS_733 = [
    *(f"reads_in_place:{case}" for case in G5_CASES),
    *(f"repair:{case}" for case in G5_CASES),
    "no_manifest",
    "interrupted_repair_reads",
    "repair_of_interrupted_repair",
    "stopped_in_end_pass",
]


def _stopped_in_end_pass(variant) -> Path:
    """A copy of G6 `repaired` with the manifest of `interrupted_repair` and no `# end` line in its last sidecar."""
    folder = variant("G06", "repaired")
    (folder / c.MANIFEST).write_bytes((GOLDEN / "G06" / "interrupted_repair" / c.MANIFEST).read_bytes())
    last = c.media_files(folder, ".csv")[-1]
    kept, end = last.read_bytes().rstrip(b"\n").rsplit(b"\n", 1)
    assert end.startswith(b"# end "), "the last line of a repaired sidecar is its `# end` line"
    last.write_bytes(kept + b"\n")
    return folder


@pytest.mark.parametrize("vector", VECTORS_733)
def test_sft_733_repair(writer, reader, golden_or_skip, variant, vector):
    """SFT-733 Writer: repair. This is the part that needs no user.

    Checks: SFF-793, SFF-794, SFF-795, SFF-796, SFF-797, SFF-798.
    The check of the repaired camera file is provisional (test_sft_733_camera_file_provisional).
    """
    vector, _, case = vector.partition(":")
    if vector == "reads_in_place":
        folder = variant("G05", case)
        before = c.snapshot(folder)
        take = c.only_take(c.read(reader, folder, records=True))
        assert all(item["state"] in ("unfinished", "damaged") for item in take["files"]), "the reader reads the files in place"
        assert c.snapshot(folder) == before
    elif vector == "repair":
        original, folder, events = golden_or_skip("G05", case), variant("G05", case), []
        old = c.load_json(folder / c.MANIFEST)
        _repair(writer, folder, events)
        c.check_repaired_files(folder, original)
        take = c.only_take(c.read(reader, folder))
        assert [item["state"] for item in take["files"]] == ["repaired"] * len(take["files"]), "the reader reports `repaired`"
        new = c.check_manifest(folder)  # the summary has the values of the repaired files
        assert new["state"] == "finished" and new["writer"] == REPAIR_WRITER
        for sidecar in c.sidecars_by_position(folder):
            # `source` is the program that ran the repair (SFF-793): REPAIR_WRITER is skellycam.
            gap = {"code": "camera_gap", "source": "skellycam", "camera_key": sidecar.header["camera_key"]}
            has = any(gap.items() <= item.items() for item in new["warnings"])
            assert has == (int(sidecar.lines("end")[0]["gaps"]) > 0), "`camera_gap` for a repaired video sidecar with gaps"
        assert all(item in new["warnings"] for item in old["warnings"])
        same = [key for key in c.MANIFEST_MEMBERS if key not in ("state", "writer", "summary", "warnings")]
        assert {key: new[key] for key in same} == {key: old[key] for key in same}, "no other member changes"
        # The repair writes the manifest after the media files and the sidecars, while it holds the lock.
        # A media file or a sidecar may be changed by a rename: the Pass text does not forbid it.
        whole = [event for event in events if not (event[0] == "replace" and event[1].startswith(c.MEDIA + "/"))]
        c.check_whole_writes_hold_lock(whole, [c.MANIFEST])
        replaced = max(i for i, event in enumerate(events) if event == ("replace", c.MANIFEST))
        written = [i for i, (_, path) in enumerate(events) if path.startswith(c.MEDIA + "/")]
        assert written and all(i < replaced for i in written), "the repair calls the trace for its media files and sidecars, before the manifest"
        # The repair cuts every media file before it writes a sidecar (ADR-E68K item 3).
        # The trace does not show a cut and an append of a sidecar as two kinds, so the order of
        # steps 2 and 3 is checked only on G6 `interrupted_repair` (test_sft_733_check_on_golden).
        changes = [(i, path) for i, (event, path) in enumerate(events) if path.startswith(c.MEDIA + "/") and event not in ("read", "fsync")]
        media = [i for i, path in changes if not path.endswith(".csv")]
        sidecars = [i for i, path in changes if path.endswith(".csv")]
        assert media and sidecars and max(media) < min(sidecars), "each media file is cut before the first write to a sidecar"
    elif vector == "no_manifest":
        folder = variant("G05", "audio_torn_fragment")
        (folder / c.MANIFEST).unlink()
        _repair(writer, folder)
        assert not (folder / c.MANIFEST).exists(), "a copy of G5 with no manifest gets no manifest from the repair"
        assert all(c.read_sidecar(path).repaired for path in c.media_files(folder, ".csv"))
    elif vector == "interrupted_repair_reads":
        folder = golden_or_skip("G06", "interrupted_repair")
        take = c.only_take(c.read(reader, folder))
        for item in take["files"]:
            assert item["state"] == "unfinished" and item["fit"] is False and "missing_fit" in item["warnings"]
        assert c.load_json(folder / c.MANIFEST)["state"] == "recording", "`state` of the manifest is `recording`"
    elif vector == "stopped_in_end_pass":  # some sidecars repaired, the others unfinished (ADR-158N item 12)
        first, second = variant("G05", "audio_torn_fragment"), _stopped_in_end_pass(variant)
        last = c.media_files(second, ".csv")[-1].name
        states = {Path(item["name"]).with_suffix(".csv").name: item["state"] for item in c.only_take(c.read(reader, second))["files"]}
        assert states == {name: "unfinished" if name == last else "repaired" for name in states}
        assert c.load_json(second / c.MANIFEST)["state"] == "recording"
        _repair(writer, first)
        _repair(writer, second)
        files = [{name: c.strip_cut_bytes((folder / name).read_bytes()) for name in c.snapshot(folder) if not name.endswith(".tmp")} for folder in (first, second)]
        assert files[0] == files[1], "a new repair finishes the rest: the files of the repair of G5, except for the two cut counts"
    else:
        first, second = variant("G05", "audio_torn_fragment"), variant("G06", "interrupted_repair")
        _repair(writer, first)
        _repair(writer, second)
        files = [{name: c.strip_cut_bytes((folder / name).read_bytes()) for name in c.snapshot(folder) if not name.endswith(".tmp")} for folder in (first, second)]
        assert files[0] == files[1], "a repair of the interrupted repair gives the same files, except for the two cut counts"


def test_sft_733_check_on_golden(golden_or_skip):
    """SFT-733, the checks that G5 and G6 show with no repair run. Checks: SFF-793, SFF-794, SFF-795, SFF-796, SFF-798."""
    before = golden_or_skip("G05", "audio_torn_fragment")
    repaired, interrupted = golden_or_skip("G06", "repaired"), golden_or_skip("G06", "interrupted_repair")
    c.check_repaired_files(repaired, before)
    assert c.check_manifest(repaired)["state"] == "finished"
    assert c.load_json(interrupted / c.MANIFEST)["state"] == "recording"
    for path in c.media_files(interrupted, ".csv"):
        assert not c.read_sidecar(path).finished, "each sidecar of the interrupted repair has no `# end` line last"
    assert any(b"# repair " in path.read_bytes() for path in c.media_files(interrupted, ".csv"))
    # A repair cuts every media file, then every sidecar, then writes the footer lines (ADR-E68K
    # item 3). The repair stopped in the footer lines, so each cut is done.
    for path in c.media_files(interrupted, ".mkv") + c.media_files(interrupted, ".m4a"):
        assert path.read_bytes() == (repaired / c.MEDIA / path.name).read_bytes(), f"{path.name} is cut"
    for path in c.media_files(interrupted, ".csv"):
        cut, done = c.read_sidecar(path), c.read_sidecar(repaired / c.MEDIA / path.name)
        assert cut.data[: cut.rows_end] == done.data[: done.rows_end], f"{path.name} is cut"


@pytest.mark.provisional("desk test DT-R1 (SFF-797)")
@pytest.mark.parametrize("case", G5_CASES)
def test_sft_733_camera_file_provisional(writer, golden_or_skip, variant, case):
    """SFT-733, the provisional check: the repaired camera file. Checks: SFF-794, SFF-797.

    The file keeps the complete blocks that have a row in the repaired sidecar, and no other block, so
    rows = blocks. It is the old file cut after the last of these blocks: the repair writes no normal end.
    """
    original, folder = golden_or_skip("G05", case), variant("G05", case)
    _repair(writer, folder)
    for path in c.media_files(folder, ".mkv"):
        old, new = (original / c.MEDIA / path.name).read_bytes(), path.read_bytes()
        rows = len(c.read_sidecar(path.with_suffix(".csv")).rows)
        blocks = c.parse_mkv(old).blocks
        assert 0 < rows <= len(blocks) and new == old[: blocks[rows - 1].end], "the file is cut after the block of its last row"
        assert len(c.parse_mkv(new).blocks) == rows


def test_sft_733_missing_rows_with_no_block(writer, reader, variant, expected):
    """SFT-733, the repair keeps the `missing` rows with no block (ADR-6AT7 item 2). Checks: SFF-795.

    The input is a copy of G18 whose sidecar of camera 2 has no `# repair` line and no `# end` line,
    and whose manifest has `state` `recording`.
    """
    folder = variant("G18")
    manifest = c.load_json(folder / c.MANIFEST)
    manifest["state"] = "recording"
    c.write_json(folder / c.MANIFEST, manifest)
    camera = manifest["cameras"][2]
    timing, video = folder / camera["timing"], folder / camera["video"]
    sidecar, media = c.read_sidecar(timing), video.read_bytes()
    timing.write_bytes(sidecar.data[: sidecar.rows_end])
    _repair(writer, folder)
    repaired = c.read_sidecar(timing)
    assert repaired.repaired and repaired.row_lines == sidecar.row_lines, "the repair keeps each row"
    assert video.read_bytes() == media, "the repair changes no byte of the camera file"
    item = c.cameras_of(c.only_take(c.read(reader, folder, records=True)))[2]
    want = c.cameras_of(c.only_take(c.json.loads(expected("G18", "take", "full"))))[2]
    assert (item["state"], item["rows"]) == ("repaired", want["rows"])
    assert [record[:4] for record in item["records"]] == [record[:4] for record in want["records"]]


@pytest.mark.external("user")
def test_sft_733_external():
    """SFT-733, the external sentences. Checks: SFF-793.

    The program asks the question before it repairs, also at start-up. skellycam asks about its own
    take. freemocap asks one time for the take. Nothing changes before the user agrees.
    """


def _golden_cases() -> list[str]:
    cases = [f"{path.parent.name}/{path.name.removesuffix('.full.json')}" for path in GOLDEN.glob("G[0-9][0-9]/*.full.json")]
    return sorted(case for case in cases if (GOLDEN / case).is_dir())


@pytest.mark.parametrize("case", _golden_cases())
def test_sft_734_reader_changes_nothing(reader, variant, case):
    """SFT-734 Reader: the reader changes nothing, for each case of each golden folder that is built. Checks: SFF-799.

    The reader reads a copy that keeps the modification times, so a fault cannot change a golden file.
    """
    folder = variant(*case.split("/"))
    before = c.snapshot(folder)
    for scope in ("full", "player"):
        c.read_bytes(reader, folder, scope=scope)
    assert c.snapshot(folder) == before
