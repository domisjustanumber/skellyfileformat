# SM53 — Choices for the decisions of round 7: the form of an unknown major, the rows of the reader fit, the truth of G5

**Status:** proposed, 2026-11-17 (agent; the details that the generator and the spec needed to apply
[ADR-783H](783H-text-corrections-of-the-second-golden-review.md) and
[ADR-7JJJ](7JJJ-audio-repair-refused-header-values-and-the-rules-of-w5ak.md)).

## Decision

The user did not decide these choices. An agent made them to apply the decisions of round 7. The
user must accept or change each of them.

1. **The form of a header value of an unknown `major` (SFF-885).** A reader of a file with an
   unknown `major` checks `camera_key` and `camera_label` with the form of version 2.0 (section 8).
   G10 `unknown_major_sidecar` holds this reading (G10_G13_G14_CHOICES.md item 41). The text came
   from ADR-783H item 7 before the decision, and Q149 does not state it.
2. **The rows of the reader fit of an unfinished audio file (SFF-784).** The reader computes its fit
   from each row that SFF-746 lets it use, also from a row whose block is not in `records` (SFF-792).
   So `reader_fit` of G5 uses the 21 rows, and the `fitted_ns` of the 19 or 9 records come from that
   fit. Alternative: the fit from the rows of `records` only. Then the last row of the fit is row 18
   or row 8, and each `fitted_ns` of G5 changes.
3. **The truth file of G5 (golden/README.md).** The audio entry of `<case>.truth.json` also holds
   `held_samples` (SFF-785) and `complete_blocks`, the number of blocks whose every sample is in a
   complete fragment (SFF-792). `tools/tests/test_g_capture.py` computes them again from the bytes.

## Reason

Q145 says that a partial block "is not usable". SFF-784 says that the fit comes from "the rows that
it uses (SFF-746)", and SFF-746 counts each complete row. The two texts do not say if a row with a
partial block is a row that the reader uses for the fit. Choice 2 keeps the text of SFF-784 and the
committed fit of G5. Choice 1 keeps the committed bytes of G10. Choice 3 gives the tests the numbers
of item 9 of ADR-783H.

## Alternatives rejected

- Choice 1: `camera_key` and `camera_label` null for a file with an unknown `major`, because the
  reader cannot know the form. G10 then changes.

## Open work

See [open-work.md](../open-work.md).
