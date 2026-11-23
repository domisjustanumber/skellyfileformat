# 76NN — Details of the format changes F-1 to F-10 that an independent review found

**Status:** accepted, 2026-11-21 (user; the user accepted the 13 items as one set, on `main`, not
pushed; was proposed, 2026-11-21 (an agent wrote these details to complete
[ADR-6AT7](6AT7-format-changes-f1-to-f10-missing-frames-and-short-files.md) and
[ADR-5B03](5B03-choices-for-the-format-changes-f1-to-f10.md), after an independent review of the
first text; branch dom/f1-f10)).

## Decision

Neither skellycam `specs/recorder.md` section 13 nor ADR-5B03 gives these details. The spec states
each item, with a citation of this entry.

1. **SFF-740.** The j-th row with byte fields belongs to the j-th complete block. A reader uses no
   row after the first row with byte fields whose block is not complete.
2. **SFF-782.** The strict player time counts only the positions that have a player time.
3. **SFF-754.** For an unfinished camera file, the usable frames also count the usable `missing`
   rows with no block.
4. **SFF-757.** A row with no block has both byte fields empty.
5. **SFF-752.** "Cannot read the values of the identity string" and "not 0" in the paragraph of the
   provisional key. A writer that writes a provisional key for a camera does not make an assigned
   key (form 4) for that camera.
6. **The tail repair** (SFF-793 to SFF-795, SFF-797). A program runs it only after the question of
   SFF-793 and the agreement of the user. Step 1 appends the placeholder blocks, and step 2 appends
   the cut rows again. Its `# repair` line has the bytes that it cut from the sidecar in
   `cut_bytes`, and `media_cut_bytes` 0.
7. **The rows that a repair keeps** (SFF-795). The first n rows with byte fields, and, when n is
   the number of rows with byte fields before the first bad row, the `missing` rows with empty byte
   fields that follow them, up to the first bad row.
8. **SFF-828** (provisional, open work). A frame with no strict player time has no camera
   `timestamp_s`, and the group mean counts only the cameras that have one.
9. **A camera file with no block** (SFF-754) holds no Cluster: only the elements before the first
   Cluster. The record said "only the EBML header, the Segment and the Tracks". That text forbids
   the Info element, which holds the TimestampScale of SFF-736.
10. **Definitions and one reader rule.** The mode size is the width and the height of the capture
    mode that the writer opened (SFF-756). The number of rows of the take of SFF-894 is the number of
    multi-camera frames that the program counted, or, when it counted none, the largest number of rows
    of the other sidecars. The spec uses one term, "rows with byte fields" (SFF-759, SFF-795). A reader
    refuses a pair (`invalid`, `bad_metadata`) when a row has one empty byte field and one that is not
    empty, a row has empty byte fields and no flag `missing`, or a row with byte fields follows a
    row with empty byte fields (SFF-759).
11. **Wording.** SFF-733 says "each block holds one JPEG image (a frame or a placeholder)". SFF-781:
    a row with no `arrival_ns` has no player time "also when the file has a fit". SFF-783: no frame
    "before its first player time". SFF-729 compares `missing` only when the summary and the `# end`
    line both hold it.
12. **`stored_px`** (SFF-728) is the size of the first stored JPEG that is not a placeholder, as the
    skellycam recorder writes it. The mode size of ADR-5B03 item 5 applies when there is none.
13. **The test inputs.** The case `no_block` of G18 (item 53 of `golden/CAPTURE_VECTORS_CHOICES.md`),
    the detail function `short_file_counts(folder, name)` and the vectors of SFT-719 and SFT-773.

## Reason

- Items 1 to 4: the player spec of skellycam (6.7, 6.11) has the same rules. The record needs them
  for a reader to read a short file.
- Item 5: form 4 applies to each camera with no forms 1 to 3, so the two keys must not both apply.
- Items 6 and 7: without them, SFF-793, SFF-794, SFF-795 and SFF-797 contradict each other, and a
  kept row could break the rule that `frame` increases by 1.
- Item 8: without it, SFF-828 gives a time to a frame with no time.
- Items 9 to 12: the review found each gap. Item 9 is the file that the muxer writes, and item 12 is
  the value of the recorder.
- Item 13: the smallest inputs for the new rules: a file with no block, and F-10 with no earlier
  real frame.

## Alternatives rejected

- Item 9: the text of the record as it stands. No muxer of the recorder can write that file.
- Item 10: no reader rule for wrong byte fields. Two readers could read such a file in two ways.

## Not repeated

- No test of the tail repair: it is a MAY, and no writer does it yet.

## Open work

See [open-work.md](../open-work.md).
