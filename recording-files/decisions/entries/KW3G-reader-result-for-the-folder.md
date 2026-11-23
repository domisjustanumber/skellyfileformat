# KW3G — One canonical reader result for the folder: file states, codes, folder files and link checks

**Status:** superseded by [G9ER](G9ER-consolidation-of-the-pushed-entries.md),
2026-11-17 (commit to main; was accepted, 2026-11-16 (user; whole-folder grilling, 2026-11-13 to 2026-11-16)).

## Decision

1. **Canonical result.** The spec defines one JSON result of opening a take folder. The Python
   reader, the JavaScript reader (for its part of the folder) and the golden files are compared with
   it. The result is serialised with the JSON Canonicalization Scheme (RFC 8785).
2. **File states**, in the order in which a reader reports the first that applies:
   `unsupported_version`, `invalid`, `damaged`, `unfinished`, `repaired`, `finished`; and
   `not_in_format`. A file that the spec makes a reader refuse is `invalid`, with one reason code.
3. **Reason codes** keep their meanings: `bad_metadata` (a value form, an unknown clock, a bad
   `take_uuid`), `missing_metadata` (a required field is absent), `bad_rate`, `bad_rotation`,
   `bad_label`, `bad_time` (a time 2^53 ns or more from the take start) and `crc_mismatch` (the
   reason of `damaged`). The spec gives each cause for each file.
4. **Warnings.** Take warnings: `incomplete_take`, `duplicate_label`, `take_fact_mismatch`,
   `extra_files`. File warnings: `missing_fit`, `encode_skip`, `prerelease`. The spec adds the
   warnings of the folder, for example `manifest_missing`, a stray `.tmp`, a camera with
   `camera_key` 0, a realtime run, and the named warnings of known-bad legacy data
   ([ADR-CZQ9](CZQ9-read-old-write-new-and-legacy-recognition.md)).
5. **Folder section.** The result lists each folder file with its state, and the result of each
   cross-file link check: `take_uuid`, `camera_key`, frame ranges, dimensions, rotation, file
   references and hashes.
6. **Private data.** The result has `may_contain_private_data`
   ([ADR-T8PK](T8PK-privacy-notice-and-no-code-in-files.md)).
7. **Where a file goes.** A file of this format whose `take_uuid` a reader can read is in the
   `files` of its take, also when it is `invalid`. Other files are in `other_files`.
8. **Take counting.** The camera files of a take are its files of the kind `camera`. A take with
   fewer camera files than `group_size`, or fewer audio files than `audio_count` (0 or 1), is
   `incomplete`. A take with more gets the warning `extra_files`.
9. **Folder states.** `ok` (one or more takes), `unreadable` (no take, but one or more files of this
   format), `legacy` (no file of this format, and one or more other regular files) and `empty`. A
   `legacy` folder also reports the family and the release range.
10. **Null members.** Each item has each member that the spec lists for it. A member that does not
    apply is null.
11. **Integer types.** The spec gives the JSON type of each integer member.
12. **Times in the result** are relative to `take_start_host_ns`, as JSON numbers. They can be
    negative.
13. **Sort orders.** Takes by `take_uuid`; files by the camera order, then by the bytes of the file
    name, then the audio file; `other_files` by the bytes of the name; each `warnings` array by
    code point.
14. **Prerelease files.** The Python and JavaScript readers of this package read a file with
    `prerelease` > 0 and give it the warning `prerelease`. Another reader can refuse it as
    `unsupported_version`.
15. **skellysync files** get no `missing_fit` warning, because skellysync writes no fit.
16. **Read only.** A reader never creates, moves, renames or changes a file of the folder.

This entry supersedes [ADR-WG08](WG08-reader-result-states-and-codes.md) in full.
- Items 2, 7, 8, 10 and 14 restate WG08 items 2, 5, 7, 9 and 14. Item 8 also restates WG08 item 6
  without the MCAP record. Items 12 and 13 restate WG08 items 11 and 12. Item 9 restates WG08 item
  8 and adds the legacy family.
- Item 3 restates WG08 item 3 without the MCAP causes: `bad_schema`, `bad_chunking` and the
  `opus_head` cause are withdrawn. Item 4 restates WG08 item 4 without `opus_head_mismatch`, and
  adds the folder warnings. Item 11 restates WG08 item 10 without the MCAP Metadata strings.
- WG08 item 1 (the MCAP test for "in this format") is replaced by the recognition rules of
  [ADR-5XNA](5XNA-folder-layout-names-and-manifest.md) item 11. WG08 item 13 (record forms) is
  replaced by the spec of the CSV rows.
- Item 1 restates [ADR-TDB5](../../../decisions/entries/TDB5-whole-recording-no-manifest.md) item 4 and
  [ADR-5G42](5G42-gate1-names.md) item 4. Item 15 restates
  [ADR-T24G](T24G-spec-v1-review-fixes-crash-fit-audio.md) item 15 without `clock_id` 128.
- Items 5, 6 and 16 are new.

## Reason

- A defined result makes the readers and the golden files comparable byte for byte.
- A reader of the whole folder must report every file and the links between them, not only the
  media files.
- The reasons of ADR-WG08 stay: a fixed vocabulary of states and codes lets each program tell the
  user the same thing.

## Evidence

- skellycam `dom/research`, `research/skellycam_recording/docs/whole_folder_spec_plan_20261113.md`,
  "Grilling log": round 2 Q15; round 5 Q8 (local, not committed).
- freemocap `RECORDING_CONTRACT.md` forbids a reader to rename or change files.

## Open work

[open-work.md](../open-work.md)

_Edited 2026-11-23 (commit to main): link repair._
