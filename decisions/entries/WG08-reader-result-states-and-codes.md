# WG08 — The reader result: file and folder states, reason and warning codes, take counting and the JSON form

**Status:** proposed, 2026-11-13 (spec v1 review; the agent proposes, the user decides each item).

## Decision

Each item is separate. The user can accept or reject each one. The source of each item in the
review is in brackets.

1. **In this format.** An MCAP file is in this format when its Header `profile` is `freemocap` and
   it has a `freemocap.format` record, with any `major`. A file with an unknown `major` has the
   state `unsupported_version`. [B3]
2. **File states**, in the order in which a reader reports the first that applies:
   `unsupported_version`, `invalid`, `damaged`, `unfinished`, `repaired`, `finished`; and
   `not_in_format`. A file that the spec makes a reader refuse is `invalid`, with one reason code.
   [B2]
3. **Reason codes and their causes.** `bad_metadata` (a value form, an unknown `clock_id`, a bad
   `take_uuid` or `opus_head`, a second `freemocap.format` record), `bad_rate`, `bad_rotation`,
   `bad_label` (the label form, or a topic that does not hold the label), `bad_schema` (a schema
   name, encoding or field number, or channels other than the spec gives), `missing_metadata` (a
   required record or key is absent), `bad_time` (a time 2^53 ns or more from the take start),
   `bad_chunking` ([ADR-T24G](T24G-spec-v1-review-fixes-crash-fit-audio.md) item 5) and `crc_mismatch` (the reason of `damaged`). [B2, S5]
4. **Warning scope.** Take warnings: `incomplete_take`, `duplicate_label`, `take_fact_mismatch`,
   `extra_files`. File warnings: `missing_fit`, `encode_skip`, `opus_head_mismatch`, `prerelease`.
   [B4.6, S14, S16]
5. **Where a file goes.** A file of this format whose `take_uuid` a reader can read is in the
   `files` of its take, also when it is `invalid`. Other files are in `other_files`. [B2, B3]
6. **Audio count.** `freemocap.recording` has the key `audio_count` (0 or 1). [S14]
7. **Take counting.** The camera files of a take are its files of the kind `camera`. A take with
   fewer camera files than `group_size`, or fewer audio files than `audio_count`, is `incomplete`.
   A take with more gets the warning `extra_files`. [S14]
8. **Folder states.** `ok` (one or more takes), `unreadable` (no take, but one or more files of
   this format), `legacy` (no file of this format, and one or more other regular files) and `empty`.
   [B3]
9. **Null members.** Each item has each member that the spec lists for it. A member that does not
   apply is null. [B4.3]
10. **Integer types.** The spec gives the JSON type of each integer member, not of each value. A
    time or a period in a Metadata value (`t0_ns`, `period_ps`) is always a JSON string. A position
    and a `sequence` are JSON numbers. [B4.1]
11. **Times in the result.** A time in `records` is relative to `take_start_host_ns`, as a JSON
    number. It can be negative. [B4.2]
12. **Sort orders.** Takes by `take_uuid`; files by the camera order, then by the bytes of the file
    name, then the audio file; `other_files` by the bytes of the name; each `warnings` array by code
    point. [B4.4, B4.5]
13. **Record forms.** An audio record is `[position, log_time, timestamp]`, where position counts the
    packets from 0. `torn_bytes` is the file length minus the end of the last complete record before
    the stop, so a damaged file counts the damaged chunk and the bytes after it. [B4.7]
14. **Prerelease files.** The Python and JavaScript readers of this package read a file with
    `prerelease` > 0 and give it the warning `prerelease`. Another reader can refuse it as
    `unsupported_version`. [S16]

## Reason

- The golden files compare the results of two readers byte for byte (ADR-5G42), so each of these
  questions needs one answer.
- Item 1: an unknown `major` must not make a folder `legacy` (README versioning).
- Item 6: without it, a lost audio file is not seen.
- Item 10: with a type for each value, the type of a member would change between files.
- Item 11: relative times keep the golden files readable. Item 3 (`bad_time`) keeps them exact in
  a JavaScript number.

## Evidence

- skellycam `dom/research` (local commit, not pushed):
  `research/skellycam_recording/docs/spec_v1_review_20261113.md`.

## Alternatives rejected

- `not_in_format` for a refused file (draft v1 SFT-006): it conflicts with the definition of the
  format.
