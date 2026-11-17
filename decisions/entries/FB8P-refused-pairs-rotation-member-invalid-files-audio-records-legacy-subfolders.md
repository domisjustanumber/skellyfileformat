# FB8P — A refused camera pair, a `rotation` member in the capture info JSON, an `invalid` file, the `records` of an interrupted audio file, the legacy subfolders

**Status:** accepted, 2026-11-16 (user; questions Q139 to Q143 of round 6 of the review of the
golden folders).

## Decision

The user accepted these rules. Each item gives its question number.

1. **A refused camera pair (Q139).** A camera pair that is `invalid` or `unsupported_version`
   counts as a present file for the take state (SFF-869): the take stays `complete`. The result
   shows `camera_key` and `camera_label` of the refused sidecar when the reader can read the header
   line. The state of the file is the report.
2. **A `rotation` member in the capture info JSON (Q140).** A capture info JSON of version 2.0
   that holds the forbidden member `rotation` stays `present`. The link check `rotation` is
   `mismatch` (SFF-800, SFF-872).
3. **An `invalid` file (Q141).** An `invalid` file has the warning `prerelease` when the reader can
   read `format_prerelease` and the value is above 0 (SFF-891). It has no `records` (SFF-885).
4. **An interrupted audio file (Q142).** `rows` counts the complete rows. `records` holds only the
   blocks that have a complete fragment. This is the rule of an unfinished camera file (SFF-740,
   [ADR-B6WH](B6WH-repair-equal-pair-cut-and-no-normal-end.md) item 2).
5. **The legacy subfolders (Q143).** Only for the legacy recognition, a reader MAY read the named
   subfolders that the legacy signals list, and no other subfolder. This is an exception to the
   scan limit of SFF-721.

## Reason

The user answered "agree with all" to the recommendations of round 6 on 2026-11-16. The user gave
no reason. Each item closes a gap of the second review of the golden results (GAP-1, GAP-2, GAP-3,
GAP-6 and GAP-7). Items 1, 2, 3 and 5 are the readings that G9, G10, G11 and G15 hold.

## Consequences

- Item 4 does not agree with the committed results of G5 (both cases) and of the case
  `interrupted_repair` of G6. Their unfinished audio items hold each of the 21 rows in `records`,
  but the audio file has only 2 or 1 complete fragments. These golden files did not change
  ([open-work.md](../open-work.md)).
- [ADR-783H](783H-text-corrections-of-the-second-golden-review.md) (proposed) gives the details
  that the spec needs to apply these items.

## Alternatives rejected

- Item 1: the take `incomplete` with `incomplete_take`, and `camera_key` and `camera_label` null.
- Item 2: the file `invalid` with `bad_schema`. The check `rotation` is then `ok`, which
  contradicts SFT-763.
- Item 3: `warnings` `[]`, and `records` `[]`.

## Open work

See [open-work.md](../open-work.md).
