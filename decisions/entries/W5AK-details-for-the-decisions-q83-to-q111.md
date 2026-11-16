# W5AK — Details that the spec text of the decisions Q83 to Q111 needed

**Status:** proposed, 2026-11-16 (agent; the details that applying
[ADR-B6WH](B6WH-repair-equal-pair-cut-and-no-normal-end.md),
[ADR-XR63](XR63-reader-rules-of-the-golden-review.md) and
[ADR-2MQE](2MQE-tests-prerelease-serial-and-exports.md) to the spec needed).

## Decision

The user did not decide these details. An agent wrote them into the spec text, so that the
accepted rules apply. The user must accept or change each of them.

1. **How a reader reads a repaired camera file** (SFF-794). The user decided that "a reader accepts"
   a repaired camera file with no normal end. Proposal: the reader reads it as SFF-740 gives for an
   unfinished camera file. G06 already does this.
2. **The number of kept frames** (SFF-795, SFF-797). Proposal: the repair keeps the first n rows and
   the first n blocks. n is the smaller of two numbers: the rows before the first bad row, and the
   complete blocks. This joins B6WH items 1 and 4 with "row k belongs to block k" (SFF-740). The
   rule is only for a camera pair: B6WH item 1 names no audio pair, so the audio rules do not
   change.
3. **The usable frames of SFF-754.** Proposal: for a finished or a repaired camera file, the number
   of usable frames is `rows`. For an unfinished camera file, it counts the usable rows that have a
   complete block.
4. **The roles of a rebuild** (SFF-731). Proposal: `<rec>_info.json` is `capture_info`,
   `<rec>_recording_info.json` is `processing_info`, `<rec>_camera_calibration.toml` is
   `calibration`, `<rec>_data.parquet` is `tracking`, `<rec>_realtime_journal.bin` is
   `realtime_journal` and `<rec>.blend` is `blend`. The TOML gets the role of XR63 item 3, so the
   `no_manifest` case of G7 changes from null to `calibration`.
5. **A folder file of another take** (SFF-889). Proposal: the item stays in the `folder_files` of
   the take that has it (the manifest lists it, or its fixed name has the `<rec>` of the take).
   The rule "a folder file of this format with no take is in `other_files`" then applies only
   when the folder has no take.
6. **The warning `prerelease` of an `unsupported_version` file** (SFF-891). Proposal: the file
   gets the warning only when the reader can read its `format_prerelease` and the value is above 0.
7. **The check of `key_origin`** (SFF-803). Proposal: null passes when `camera_key` is 0, as
   section 13 gives. Another value makes the capture info JSON `invalid`, with the reason
   `bad_schema`.
8. **The scope `player` and a folder with no take** (SFF-892). The user decided that such a folder
   is `unreadable` in the two scopes, but a `player` reader reads no TOML, Parquet or journal.
   Proposal: only to give `folder_state`, and only when the folder has no take, the `player`
   reader looks for the mark of SFF-875 in each TOML, Parquet and journal of the root. It reads
   only the part of the file that holds the mark. The item stays `not_in_format` in `other_files`,
   with no `orphan_file`. The JavaScript reader then needs to read the `[metadata]` table of a
   TOML, the key-value metadata of a Parquet footer and the header record of a journal.
9. **New test inputs** (conformance.md). SFT-736: G3 with the `key_origin` `"remembered"`,
   changed at test time. SFT-762: G11, whose `invalid` sidecars must cause no
   `take_fact_mismatch` and no `summary_stale`. SFT-764: a copy of `v1i` with its key in a nested
   object, and a copy of `v0_0_x` with the files of `v1a`. SFT-703 and SFT-763 got pass sentences
   for XR63 items 4, 6 and 7. SFT-717 got an external sentence for 2MQE item 10.
10. **Not applied: a repaired pair whose counts differ.** SFF-759 refuses only a finished pair
    whose rows and blocks differ. After B6WH item 1, a repair gives equal counts. The spec does not
    say if a reader also refuses a repaired pair with different counts. Proposal: SFF-759 also
    applies to a repaired pair. This text is not in the spec.

## Reason

Each detail is the smallest text that makes the accepted rule exact. Items 1, 4 and 6 follow the
choices of the golden folders. Item 8 keeps the cost of the `player` scope low: the reader reads
the marks only for a folder that has no take.

## Alternatives rejected

- Item 8: a `player` reader that finds a TOML, a Parquet or a journal by its file name. A legacy
  v1 folder also has a TOML in its root, so a name is not a mark (SFF-718).

## Open work

See [open-work.md](../open-work.md).
