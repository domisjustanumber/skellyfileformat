# 64ER — The form of an unknown major, the rows of the reader fit of an audio file, and the counts of a refused pair

**Status:** absorbed into
[`spec/SPEC.md#11-clocks-the-fit-and-reader-timing`](../../spec/SPEC.md#11-clocks-the-fit-and-reader-timing),
[`spec/SPEC.md#20-opening-a-folder`](../../spec/SPEC.md#20-opening-a-folder),
[`spec/SPEC.md#23-the-reader-result`](../../spec/SPEC.md#23-the-reader-result),
2026-11-17 (commit to main; was accepted, 2026-11-17 (user; questions Q151 and
Q152 of round 8 of the review of the golden folders, and the reading of Q147; commit to main)).

## Decision

The user accepted items 1 and 2 of [ADR-SM53](SM53-choices-for-the-decisions-of-round-7.md) and
confirmed the reading of item 3. Items 1 and 2 keep the numbers of SM53. SM53 keeps only its
item 3, which is still proposed.

1. **The form of a header value of an unknown `major` (Q152).** A reader of a file with an unknown
   `major` checks the form of `camera_key` and `camera_label` with the rules of version 2.0
   (section 8, SFF-885). G10 `unknown_major_sidecar` holds this reading.
2. **The rows of the reader fit of an unfinished audio file (Q151).** When a reader computes the
   fit of an unfinished audio file (SFF-784), it uses each row that SFF-746 lets it use. It also
   uses a row whose block is not in `records` (SFF-792). So `reader_fit` of G5 uses the 21 rows.
3. **A refused pair and the take (Q147).** "A refused pair counts as a file of the take
   everywhere" ([ADR-783H](783H-text-corrections-of-the-second-golden-review.md) item 7) is about
   the counts of the files of the take only: the take state and `extra_files` (SFF-869). A refused
   pair stays out of the take-level checks
   ([ADR-XR63](XR63-reader-rules-of-the-golden-review.md) item 2).

## Reason

The user answered "agree to all" to the recommendations of round 8 on 2026-11-17. The user gave no
reason. The recommendations were: item 1 keeps the committed bytes of G10; item 2 keeps the text of
SFF-784 and the committed fit of G5; item 3 keeps ADR-783H item 7 and ADR-XR63 item 2 together
with no conflict.

## Consequences

- No golden byte changes.
- Before this entry, the spec and the choice files cited SM53 items 1 and 2 as proposed. They now
  cite this entry.

## Alternatives rejected

- Item 1: `camera_key` and `camera_label` null for a file with an unknown `major`, because the
  reader cannot know the form. G10 then changes.
- Item 2: the fit from the rows of `records` only. Then the last row of the fit is row 18 or
  row 8, and each `fitted_ns` of G5 changes.

## Open work

See [open-work.md](../open-work.md).
