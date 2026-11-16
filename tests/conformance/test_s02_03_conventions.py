"""Conformance tests SFT-700 to SFT-704: conventions and versioning (SPEC.md sections 2 and 3).

The Pass text of each test is in spec/conformance.md. A test gets the reader or the writer from a
fixture, so it fails with one line until the implementation exists (decision G21H).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import checks_capture as c

GOLDEN = Path(__file__).resolve().parents[2] / "golden"


def test_sft_700_text_integers_json_ids_crcs(writer, tmp_path):
    """SFT-700 Writer: text files, integers, JSON, IDs and CRCs.

    Checks: SFF-700, SFF-701, SFF-702, SFF-703, SFF-704, SFF-705.
    The package writer writes the files of a capture (G1). The golden check below covers G3.
    """
    folder = tmp_path / "take"
    sent = c.record_take(writer, folder, audio=c.microphone())
    c.check_text_conventions(folder)
    # Each row time is relative to the take start.
    for index, sidecar in enumerate(c.sidecars_by_position(folder)):
        assert sidecar.integers("arrival_ns") == sent["arrival_ns"][index]
        assert sidecar.integers("sample_ns") == [arrival - 4_000_000 for arrival in sent["arrival_ns"][index]]


@pytest.mark.parametrize("name", ["G01", "G03"])
def test_sft_700_check_on_golden(golden_or_skip, name):
    """SFT-700, the same check on the files of a golden folder. Checks: SFF-700 to SFF-705."""
    c.check_text_conventions(golden_or_skip(name))


@pytest.mark.parametrize(
    ("case", "reason"),
    [
        ("leading_zero", "bad_metadata"),
        ("plus_sign", "bad_metadata"),
        ("missing_key", "missing_metadata"),
        ("row_integer_2_53", "bad_metadata"),
    ],
)
def test_sft_701_integer_and_value_forms(reader, golden_or_skip, case, reason):
    """SFT-701 Reader: integer and value forms. Checks: SFF-701, SFF-748.

    Each case of G11 is a copy of G1 with one changed video sidecar, so one file is `invalid`.
    """
    folder = golden_or_skip("G11", case)
    take = c.only_take(c.read(reader, folder))
    invalid = [item for item in take["files"] if item["state"] == "invalid"]
    assert [item["reason"] for item in invalid] == [reason]


@pytest.mark.parametrize("vector", ["take_start_near_2_62", "take_starts_differ_by_1_near_2_62", "row_time_2_53_python", "row_time_2_53_js"])
def test_sft_702_64_bit_integers_in_javascript(reader, js_reader, variant, vector):
    """SFT-702 Reader: 64-bit integers in JavaScript. Checks: SFF-706."""
    folder = variant("G01")
    if vector == "take_start_near_2_62":
        for path in c.media_files(folder, ".csv"):
            c.set_header(path, "take_start_host_ns", 2**62 - 1_000_003)
        python = c.read_bytes(reader, folder, records=True, scope="player")
        assert js_reader(folder, records=True) == python, "the JS reader gives the same times as the Python reader"
        return
    if vector == "take_starts_differ_by_1_near_2_62":
        # 2^62 - 1 and 2^62 - 2 are the same float64, so a reader that parses the header with a float sees no disagreement.
        for index, path in enumerate(c.media_files(folder, ".csv")):
            c.set_header(path, "take_start_host_ns", 2**62 - 1 - (index > 0))
        python = c.read_bytes(reader, folder, records=True, scope="player")
        assert "take_fact_mismatch" in c.only_take(json.loads(python))["warnings"], "the two take starts differ by 1 ns (SFF-706, SFF-871)"
        assert js_reader(folder, records=True) == python, "the JS reader gives the same result as the Python reader"
        return
    changed = c.load_json(folder / c.MANIFEST)["cameras"][0]
    c.set_row(folder / changed["timing"], 10, "arrival_ns", 2**53)
    if vector == "row_time_2_53_python":
        result = c.read(reader, folder, scope="player")
    else:
        result = json.loads(js_reader(folder))
    (item,) = [item for item in c.only_take(result)["files"] if item["name"] == changed["video"]]
    assert (item["state"], item["reason"]) == ("invalid", "bad_time")


VECTORS_703 = [
    "writer_output",
    "pair_version_is_of_its_sidecar",
    "unknown_major_sidecar",
    "unknown_major_folder_file",
    *(f"higher_minor:{impl}" for impl in c.IMPLS),
    "higher_minor_journal",
    *(f"prerelease:{impl}" for impl in ("python_full", "python_player", "js")),
    *(f"prerelease_0:{impl}" for impl in ("python_full", "python_player", "js")),
]


@pytest.mark.parametrize("vector", VECTORS_703)
def test_sft_703_version_fields_and_rules(reader, writer, js_reader, golden_or_skip, expected, tmp_path, vector):
    """SFT-703 Writer and reader: version fields and rules.

    Checks: SFF-707, SFF-708, SFF-709, SFF-710, SFF-711, SFF-712, SFF-714, SFF-891.
    SFF-714 has no case in version 2.0. The two sentences about the export inventory, the BVH
    metadata JSON and the other files of section 18 are external (test_sft_703_external).
    """
    vector, _, impl = vector.partition(":")
    if vector == "writer_output":
        folder = tmp_path / "take"
        c.record_take(writer, folder, audio=c.microphone())
        c.check_version_fields(folder)  # also: no media file holds one of the three fields
    elif vector == "pair_version_is_of_its_sidecar":
        folder = golden_or_skip("G01")
        for item in c.only_take(c.read(reader, folder))["files"]:
            details = (reader.camera_details if item["kind"] == "camera" else reader.audio_details)(folder, item["name"])
            header = c.read_sidecar(c.sidecar_path(folder, item["name"])).header
            found = (details["format_version"], details["format_prerelease"], details["writer"])
            assert found == (header["format_version"], int(header["format_prerelease"]), header["writer"])
    elif vector == "unknown_major_sidecar":
        result = c.read(reader, golden_or_skip("G10", vector))
        states = [item["state"] for item in c.only_take(result)["files"]]
        assert states.count("unsupported_version") == 1, "the file with the unknown `major` is `unsupported_version`"
        assert result["legacy"] is None and result["folder_state"] != "legacy", "it is not legacy"
    elif vector == "unknown_major_folder_file":
        take = c.only_take(c.read(reader, golden_or_skip("G10", vector)))
        (item,) = [item for item in take["folder_files"] if item["role"] == "capture_info"]
        assert item["state"] == "unsupported_version"
    elif vector == "higher_minor":
        # The file reads, and each unknown key, column, member, TOML key and flag bit is ignored: the
        # result is the committed result. The TOML vectors are in the scope `full` only.
        folder = golden_or_skip("G10", "higher_minor")
        assert c.result_bytes(impl, reader, js_reader, folder) == expected("G10", "higher_minor", c.scope_of(impl))
    elif vector == "higher_minor_journal":
        folder = golden_or_skip("G10", "higher_minor_journal")
        golden_or_skip("G13")

        def journal(result: dict) -> dict:
            (item,) = [item for item in c.only_take(result)["folder_files"] if item["role"] == "realtime_journal"]
            return item

        found = journal(c.read(reader, folder, scope="full"))
        assert found == journal(json.loads(expected("G10", "higher_minor_journal", "full")))
        base = journal(json.loads(expected("G13", "take", "full")))
        assert found["records"] == base["records"] + 1, "the good record of the unknown type 200 counts in `records`"
    else:
        folder = golden_or_skip("G01") if vector == "prerelease" else golden_or_skip("G10", "prerelease_0")
        take = c.only_take(json.loads(c.result_bytes(impl, reader, js_reader, folder)))
        items = take["files"] + take["folder_files"]
        assert items and all(("prerelease" in item["warnings"]) == (vector == "prerelease") for item in items)


def _result_files():
    return sorted(path.relative_to(GOLDEN).as_posix() for path in GOLDEN.glob("G[0-9][0-9]/*.full.json"))


@pytest.mark.parametrize("target", ["G01/take", "G01/confirmed_key", "G03/take", "G10/prerelease_0", "results"])
def test_sft_703_check_on_golden(golden_or_skip, target):
    """SFT-703, the checks that the golden files can show with no reader. Checks: SFF-707, SFF-710, SFF-891.

    `results`: in each committed result, each device pair that a reader reads has the file warning
    `prerelease`. The only exception is the case `prerelease_0` of G10.
    """
    if target != "results":
        name, case = target.split("/")
        c.check_version_fields(golden_or_skip(name, case), prerelease=0 if case == "prerelease_0" else 1)
        return
    for path in _result_files():
        result = c.load_json(GOLDEN / path)
        for take in result["takes"]:
            for item in take["files"]:
                if item["rows"] is not None:  # not `invalid` and not `unsupported_version`
                    assert ("prerelease" in item["warnings"]) == (not path.endswith("/prerelease_0.full.json")), path


def test_sft_703_descriptor_and_journal_header_on_golden(golden_or_skip):
    """SFT-703, the Parquet descriptor of G3 and the journal header of G13 have the three fields (SFF-707, SFF-710)."""
    import checks_folder as f

    descriptor = f.descriptor(f.one(golden_or_skip("G03"), "*_data.parquet"))
    golden_or_skip("G13")
    header = f.journal_header(f.scan_journal(f.one(golden_or_skip("G13"), "*_realtime_journal.bin").read_bytes()))
    for name, value in (("the Parquet descriptor", descriptor), ("the journal header", header)):
        assert value.get("format_version") == "2.0" and value.get("format_prerelease") == 1 and value.get("writer"), name


@pytest.mark.external("freemocap, Blender addon")
def test_sft_703_external():
    """SFT-703, the external sentences. Checks: SFF-707.

    The export inventory and the BVH metadata JSON also have the three fields. No other file of
    SPEC.md section 18 holds one of the three fields.
    """


@pytest.mark.parametrize("vector", ["writer_string", "doc_type_version"])
def test_sft_704_writer_string_and_container_version(reader, variant, vector):
    """SFT-704 Reader: the writer string and container versions do not change the result. Checks: SFF-712, SFF-713."""
    first, second = variant("G01"), variant("G01")
    if vector == "writer_string":
        c.change_writer(second, "another-writer 9.9.9")
    else:
        for path in c.media_files(second, ".mkv"):
            data = bytearray(path.read_bytes())
            at = c.parse_mkv(bytes(data)).doc_type_version_at
            assert data[at] == 4, "the golden camera file has DocTypeVersion 4"
            data[at] = 2
            path.write_bytes(data)
    for scope in ("full", "player"):
        assert c.read_bytes(reader, first, scope=scope) == c.read_bytes(reader, second, scope=scope)
