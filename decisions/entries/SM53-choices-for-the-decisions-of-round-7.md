# SM53 — Choices for the decisions of round 7: the truth of G5

**Status:** proposed, 2026-11-17 (agent; the details that the generator and the spec needed to apply
[ADR-783H](783H-text-corrections-of-the-second-golden-review.md) and
[ADR-7JJJ](7JJJ-audio-repair-refused-header-values-and-the-rules-of-w5ak.md)).

## Decision

The user did not decide this choice. An agent made it to apply the decisions of round 7. The user
must accept or change it. Items 1 and 2 of this entry were accepted on 2026-11-17 and moved to
[ADR-64ER](64ER-unknown-major-form-audio-fit-rows-and-refused-pair-counts.md) items 1 and 2.

3. **The truth file of G5 (golden/README.md).** The audio entry of `<case>.truth.json` also holds
   `held_samples` (SFF-785) and `complete_blocks`, the number of blocks whose every sample is in a
   complete fragment (SFF-792). `tools/tests/test_g_capture.py` computes them again from the bytes.

## Reason

Choice 3 gives the tests the numbers of item 9 of ADR-783H. It is a golden convention of the same
kind as the choice lists of the golden folders.

## Open work

See [open-work.md](../open-work.md).
