# N6KY — Spec draft v2 details, part 14: writer rules, journal scan, NPZ files

**Status:** absorbed into
[`spec/SPEC.md#16-tracking-parquet`](../../spec/SPEC.md#16-tracking-parquet),
[`spec/SPEC.md#17-realtime-journal`](../../spec/SPEC.md#17-realtime-journal),
[`spec/SPEC.md#22-privacy-and-safety`](../../spec/SPEC.md#22-privacy-and-safety),
[`spec/SPEC.md#23-the-reader-result`](../../spec/SPEC.md#23-the-reader-result),
[`spec/parts/parquet-descriptor.md#structure-rules-and-writer-rules`](../../spec/parts/parquet-descriptor.md#structure-rules-and-writer-rules),
2026-11-16 (commit to main; was accepted, 2026-11-16).

## Decision

This part holds items 40, 42, 43 and 45 of the proposals that
[ADR-0JVZ](0JVZ-spec-v2-details-part-9.md) introduces. The user accepted them on 2026-11-16, with
the recommended option of each CHOICE. Each alternative stays as a record. Item 44 (the identity
string of a camera with no serial number and no port path) is not in this entry: the user did not
accept it, and the point is in [open-work.md](../open-work.md). Item 41 (a count in the column Type and a
count in the column Rule) is not in this part: parts/parquet-descriptor.md, section "Structure
rules and writer rules", already states its rule.

40. **Writer rules in the text of a type** (parts/parquet-descriptor.md). The part says: "Each
    rule that is not a structure rule is a writer rule, at each place of this part." The column
    "Rule", the lists "Writer rules" and the sentences "Writer rule" are examples. A rule in the
    text of a type, for example "`weight` (float; more than 0)", is also a writer rule. Basis (1):
    [ADR-W5JC](W5JC-nested-model-types-in-the-descriptor-part.md) item 3.

42. **Names of the journal counts** (SFF-834, SFF-843, SFF-885, section 17; SFT-751, SFT-757; G13).
    CHOICE. The array `records` of a `files` item and the integer `records` of the journal item
    keep their names. The member of the journal end record changes from `records` to
    `data_records`: the number of data records that the writer wrote. `journal_crc_rejects` of
    `coverage` is `rejected_records` of the journal at the time of the fold. It also counts a
    record with a wrong `length`. Basis (1): [ADR-72QQ](72QQ-spec-v2-details-part-8.md) items 19a
    and 19b. Alternative: the journal item gets `good_records` in place of `records`. This changes
    item 19a of that entry.

43. **Journal scan** (SFF-843, SFF-885; SFT-757; G13). The scan starts at offset 0. At each step,
    it finds the first `magic` at or after its position. o is the offset of that `magic`.
    - The record is **cut** when the file ends before o + 8, or when `length` is from 1 to 2^26
      and the file ends before o + 12 + `length`.
    - A record that is not cut is **rejected** when `length` is not from 1 to 2^26, or when
      `crc32` is wrong. Else it is **good**.
    - After a good record, the scan goes on at o + 12 + `length`. After each other `magic`, it
      goes on at o + 4. The scan ends when it finds no `magic`.
    - `records` is the number of good records, of each type.
    - The first cut record after the last good record is the torn tail. `torn_bytes` is the number
      of bytes from its o to the end of the file. A cut record with a good record after it is a
      rejected record (a wrong `length`). A rejected record after the start of the torn tail does
      not count.
    - With no torn tail, `torn_bytes` is the number of bytes (1 to 3) of a start of `magic` at
      the end of the file, else 0. Bytes that hold no `magic` count in no member.
    - The journal has an end record when a good record of the type 4 exists.

    Basis (1): [ADR-Q9X2](Q9X2-realtime-tracking-journal.md) item 6 and
    [ADR-72QQ](72QQ-spec-v2-details-part-8.md) items 19a and 19b; (3).

45. **NPZ files** (SFF-884; SFT-767; G16). For an NPZ file that the manifest lists, the reader
    reads the ZIP directory and, for each member whose name ends in `.npy`, only the NPY header.
    It inflates only the bytes of the header when the member is compressed. It reads no other
    member. A `descr` of an object type in one member makes the `folder_files` item `invalid`, with
    the reason `code_in_file`. A file that is not a ZIP file, or a member with no NPY header, makes
    the item `invalid`, with the reason `bad_schema`. The same reason applies to an NPY file with
    no NPY header. SFF-887 adds this cause. Basis (1):
    [ADR-DM9S](DM9S-spec-v2-details-part-7.md) item 15c; (3).

## Reason

- Item 40: the part must say which rules the reader checks.
- Item 42: one name with two meanings in one file family causes a wrong count in a reader.
- Item 43: G13 has a record with a wrong CRC, a hole of zeros and a torn tail. Its three counts
  need one scan rule.
- Item 45: SFF-884 gave no rule for the members of an NPZ file.

## Evidence

- skellycam `dom/research` (local, not committed):
  `research/skellycam_recording/docs/realtime_tracking_storage_20261115.md` section 3: the recovery
  of the framed journal is "scan for magic, check len and CRC, skip bad records, stop at the torn
  tail, report counts". It gives no rule for the points of item 43.

## Open work

[open-work.md](../open-work.md)
