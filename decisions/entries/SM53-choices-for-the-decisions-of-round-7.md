# SM53 — Choices for the decisions of round 7: the truth and the audio jitter of G5

**Status:** proposed, 2026-11-17 (agent; the details that the generator and the spec needed to apply
[ADR-783H](783H-text-corrections-of-the-second-golden-review.md),
[ADR-7JJJ](7JJJ-audio-repair-refused-header-values-and-the-rules-of-w5ak.md) and
[ADR-3GWN](3GWN-jitter-in-the-g5-audio-rows-after-the-cut.md)).

## Decision

The user did not decide these choices. An agent made them to apply the decisions of round 7 and
ADR-3GWN. The user must accept or change them. Items 1 and 2 of this entry were accepted on
2026-11-17 and moved to
[ADR-64ER](64ER-unknown-major-form-audio-fit-rows-and-refused-pair-counts.md) items 1 and 2.

3. **The truth file of G5 (golden/README.md).** The audio entry of `<case>.truth.json` also holds
   `held_samples` (SFF-785) and `complete_blocks`, the number of blocks whose every sample is in a
   complete fragment (SFF-792). `tools/tests/test_g_capture.py` computes them again from the bytes.
4. **The jitter of the G5 audio rows (ADR-3GWN).** The generator adds a fixed list of offsets to
   `adc_ns`: −25,000 ns in row 19 and +40,000 ns in row 20 (`AUDIO_JITTER_NS` of
   `tools/goldgen/g05.py`). Rows 19 and 20 are after the cut in both cases (19 and 9 blocks in
   `records`), so the two cases keep one audio input. Row 20 is the last row of the reader fit, so
   `period_fs` changes from 20833356458 to 20833773125. `t0_ns` stays 12344678. A fit from only the
   rows in `records` keeps 20833356458. Its `fitted_ns` are up to 36,001 ns early in
   `audio_clean_kill` (block 18) and up to 16,001 ns early in `audio_torn_fragment` (block 8). Each
   offset is less than 0.05 % of a block of 100 ms. The `adc_ns` values still increase, and each
   `adc_ns` is still before the `host_ns` of its row. The spec gives no other limit for `adc_ns`
   (section 10). Alternative: a jitter in each row after the cut of each case. Then the audio sidecars
   of the two cases differ, and the cases do not differ only in the audio file (item 27 of
   golden/CAPTURE_VECTORS_CHOICES.md).

## Reason

Choice 3 gives the tests the numbers of item 9 of ADR-783H. It is a golden convention of the same
kind as the choice lists of the golden folders. Choice 4 is the smallest change that makes both
cases of G5 tell the two fits apart, and it changes no byte of G06.

## Open work

See [open-work.md](../open-work.md).
