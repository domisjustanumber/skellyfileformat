# FB8P — A refused camera pair, a `rotation` member in the capture info JSON, an `invalid` file, the `records` of an interrupted audio file, the legacy subfolders

**Status:** absorbed into
[`spec/SPEC.md#12-writing-crashed-files-and-repair`](../../spec/SPEC.md#12-writing-crashed-files-and-repair),
[`spec/SPEC.md#20-opening-a-folder`](../../spec/SPEC.md#20-opening-a-folder),
[`spec/SPEC.md#21-legacy-folders`](../../spec/SPEC.md#21-legacy-folders),
[`spec/SPEC.md#23-the-reader-result`](../../spec/SPEC.md#23-the-reader-result),
2026-11-17 (commit to main; was accepted, 2026-11-16 (user; questions Q139 to Q143 of round 6 of
the review of the golden folders; commit to main)).

## Decision

The user accepted these rules. Each item gives its question number.

1. **A refused camera pair (Q139).** A camera pair that is `invalid` or `unsupported_version`
   counts as a present file for the take state (SFF-869): the take stays `complete`. The result
   shows `camera_key` and `camera_label` of the refused sidecar when the reader can read the header
   line and the value has the correct form ([ADR-7JJJ](7JJJ-audio-repair-refused-header-values-and-the-rules-of-w5ak.md) item 11, Q149). A refused audio
   pair counts in the same way ([ADR-783H](783H-text-corrections-of-the-second-golden-review.md) item 7; corrected on 2026-11-17). The state of the file
   is the report.
2. **A `rotation` member in the capture info JSON (Q140).** A capture info JSON of version 2.0
   that holds the forbidden member `rotation` stays `present`. The link check `rotation` is
   `mismatch` (SFF-800, SFF-872).
3. **An `invalid` file (Q141).** An `invalid` file has the warning `prerelease` when the reader can
   read `format_prerelease` and the value is above 0 (SFF-891). It has `records` null, not `[]` (SFF-885;
   [ADR-783H](783H-text-corrections-of-the-second-golden-review.md) item 8, Q148, corrected on 2026-11-17).
4. **An interrupted audio file (Q142).** `rows` counts each row that SFF-746 lets the reader use
   (SFF-792; the words of section 23 and SFF-740). In SFF-746, a complete row can have a wrong
   CRC, so "the complete rows" was not correct. This is the text of
   [ADR-0HS2](0HS2-wording-of-the-audio-repair-and-the-audio-records.md) item 2, which the user
   accepted on 2026-11-17 (corrected on 2026-11-17). `records` holds only the
   blocks whose every sample is in a complete fragment ([ADR-783H](783H-text-corrections-of-the-second-golden-review.md) item 9, Q145;
   corrected on 2026-11-17). This is the rule of an unfinished camera file (SFF-740,
   [ADR-B6WH](B6WH-repair-equal-pair-cut-and-no-normal-end.md) item 2).
5. **The legacy subfolders (Q143).** Only for the legacy recognition, a reader MAY read the named
   subfolders that the legacy signals list, and no other subfolder. This is an exception to the
   scan limit of SFF-721.

## Reason

The user answered "agree with all" to the recommendations of round 6 on 2026-11-16. The user gave
no reason. Each item closes a gap of the second review of the golden results (GAP-1, GAP-2, GAP-3,
GAP-6 and GAP-7). Items 1, 2, 3 and 5 are the readings that G9, G10, G11 and G15 hold.

## Consequences

- Item 4 did not agree with the committed results of G5 (both cases) and of the case
  `interrupted_repair` of G6. Their unfinished audio items hold each of the 21 rows in `records`,
  but the audio file has only 2 or 1 complete fragments. [ADR-783H](783H-text-corrections-of-the-second-golden-review.md) item 9 then changed these golden files (corrected on 2026-11-17).
- [ADR-783H](783H-text-corrections-of-the-second-golden-review.md) (accepted on 2026-11-17) gives the details
  that the spec needs to apply these items.

## Alternatives rejected

- Item 1: the take `incomplete` with `incomplete_take`, and `camera_key` and `camera_label` null.
- Item 2: the file `invalid` with `bad_schema`. The check `rotation` is then `ok`, which
  contradicts SFT-763.
- Item 3: `warnings` `[]`, and `records` `[]`.

## Open work

See [open-work.md](../open-work.md).
