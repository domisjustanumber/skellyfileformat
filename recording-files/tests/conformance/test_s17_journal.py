"""SFT-756 to SFT-759: the realtime journal (SPEC.md section 17).

freemocap writes the journal (decision G21H item 4). The writer tests of this file are checks on G13.
"""

from __future__ import annotations

import json

import checks_folder as checks
import pytest


@pytest.mark.external("freemocap")
def test_sft_756_journal_records():
    """SFT-756 (external: freemocap) Writer: journal records. Checks: SFF-839, SFF-840, SFF-841, SFF-842."""
    checks.not_run_here()


def test_sft_756_golden_part(golden_or_skip):
    """SFT-756, golden part: the good records of the journal of G13. Checks: SFF-839, SFF-840, SFF-841."""
    assert checks.journal_faults(golden_or_skip("G13")) == []


def _good_records(data: bytes, with_end: bool = False) -> list[bytes]:
    """The bytes of each good record of a journal, without the end record."""
    good = checks.scan_journal(data)["good"]
    return [checks.frame_record(kind, payload) for _, kind, payload in good if with_end or kind != checks.END]


def _one_channel(data: bytes, **members) -> bytes:
    """The journal with a header that declares one channel, with changed members."""
    offset, _, payload = checks.scan_journal(data)["good"][0]
    header = json.loads(payload)
    header["channels"] = [header["channels"][0] | members]
    record = checks.frame_record(checks.HEADER, json.dumps(header, separators=(",", ":")).encode())
    return data[:offset] + record + data[offset + 13 + len(payload) :]


def _cut_record() -> bytes:
    """The start of a record whose `length` goes past the end of the file: a cut record (SFF-843)."""
    return checks.MAGIC + (2**20).to_bytes(4, "little") + bytes([checks.DATA]) + bytes(10)


# The name of each input, the journal bytes that it makes from the G13 journal, the state and the reason
# of the item, and the counts that the Pass text names (the test also computes each count with the scan).
JOURNALS = {
    "g13": (lambda data: data, "damaged", "crc_mismatch", {}),
    "float64_channel": (lambda data: _one_channel(data, dtype="float64"), "invalid", "bad_schema", None),
    "timestamps_channel": (lambda data: _one_channel(data, kind="TIMESTAMPS"), "invalid", "bad_schema", None),
    "good_records_and_torn_tail": (
        lambda data: b"".join(_good_records(data)) + _good_records(data)[-1][:-5], "unfinished", None, {"rejected_records": 0},
    ),
    "good_records_and_no_end_record": (
        lambda data: b"".join(_good_records(data)), "unfinished", None, {"rejected_records": 0, "torn_bytes": 0},
    ),
    "cut_record_before_a_good_record": (
        lambda data: b"".join(_good_records(data)[:-1]) + _cut_record() + _good_records(data)[-1],
        None, None, {"rejected_records": 1, "torn_bytes": 0},
    ),
    "ends_with_2_bytes_of_magic": (lambda data: b"".join(_good_records(data)) + b"SK", None, None, {"torn_bytes": 2}),
}  # fmt: skip


@pytest.mark.parametrize("name", JOURNALS)
def test_sft_757_damaged_journals(reader, variant, golden_or_skip, name):
    """SFT-757 Reader: damaged journals. Checks: SFF-843. A test of the scope `full` only."""
    make, state, reason, counts = JOURNALS[name]
    folder = variant("G13")
    path = checks.one(folder, "*_realtime_journal.bin")
    data = make(path.read_bytes())
    path.write_bytes(data)
    scan = checks.scan_journal(data)
    item = checks.folder_file(checks.the_take(checks.read(reader, folder)), "_realtime_journal.bin")
    if state is not None:
        assert (item["state"], item["reason"]) == (state, reason)
    if counts is None:  # a journal that the reader refuses: SFT-757 gives no counts for it
        return
    assert checks.journal_counts(scan) | counts == checks.journal_counts(scan), "the scan of the test gives the counts of the Pass text"
    assert {member: item[member] for member in checks.JOURNAL_MEMBERS} == checks.journal_counts(scan)
    if name == "g13":
        want = checks.folder_file(checks.the_take(checks.committed(golden_or_skip("G13"))), "_realtime_journal.bin")
        assert item == want, "the item has the three members of the committed result"
        good = len(_good_records(data, with_end=True))
        assert scan["rejected_records"] >= 1 and scan["torn_tail"] and item["records"] == good


@pytest.mark.external("freemocap, user")
def test_sft_758_journal_after_the_fold():
    """SFT-758 (external: freemocap, user) Writer: the journal after the fold. Checks: SFF-793, SFF-845."""
    checks.not_run_here()


def test_sft_758_golden_part(golden_or_skip):
    """SFT-758, golden part: the count and the digest of the check, on G13. Checks: SFF-845.

    The test computes the two values from the journal with the rule of SFF-845. They equal the values of
    the folded run of the Parquet.
    """
    folder = golden_or_skip("G13")
    count, digest = checks.journal_digest(folder)
    assert count > 0 and (count, digest) == checks.parquet_digest(folder)


@pytest.mark.provisional("the journal load test and the kill test DT11 (SFF-846)")
def test_sft_759_load_and_kill_tests_of_the_journal():
    """SFT-759 (provisional) Load and kill tests of the journal. Checks: SFF-846. The test has no input in this repository."""
    checks.not_run_here()
