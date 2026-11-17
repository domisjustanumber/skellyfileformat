# 0HS2 — Wording of the audio repair and the audio records

**Status:** absorbed into
[`spec/SPEC.md#5-the-recording-manifest`](../../spec/SPEC.md#5-the-recording-manifest),
[`spec/SPEC.md#12-writing-crashed-files-and-repair`](../../spec/SPEC.md#12-writing-crashed-files-and-repair),
[`spec/SPEC.md#23-the-reader-result`](../../spec/SPEC.md#23-the-reader-result),
[`spec/conformance.md#writing-crashed-files-and-repair-section-12`](../../spec/conformance.md#writing-crashed-files-and-repair-section-12),
2026-11-17 (commit to main; was accepted, 2026-11-17 (user; question Q158 of round 9, "agree to
all": items 1, 3, 4 and 5); was proposed, 2026-11-17 (agent; text corrections from an independent
review of the spec after round 8)). Item 2 was accepted, 2026-11-17 (user; "accept 0HS2 item 2"),
and moved to
[ADR-FB8P](FB8P-refused-pairs-rotation-member-invalid-files-audio-records-legacy-subfolders.md)
item 4.

## Decision

An agent wrote items 1, 3, 4 and 5. The user accepted them on 2026-11-17 (Q158). No rule changes,
and no golden byte changes. Item 2 is in ADR-FB8P item 4 now.

1. **The audio that a repair keeps (SFF-728, SFF-795, SFF-796).** "Count only the audio that the
   repair keeps" had two readings: the 47,688 samples that the cut audio file holds, or the
   43,200 samples of the kept rows. The golden `repaired` of G6 has 0.9 s, the sum of `n_samples`
   of the kept rows (SFF-769). The text now says "the samples of the kept rows".
2. **`rows` of an unfinished audio file (SFF-792, SFT-732). Moved to ADR-FB8P item 4 (accepted
   by the user on 2026-11-17).** The text said that `rows` "counts each
   complete row (SFF-746)". In SFF-746, a complete row can have a wrong CRC. The text now uses the
   words of section 23 and SFF-740: each row that SFF-746 lets the reader use.
3. **The term "has a complete fragment" (SFF-792, SFF-795, SFF-796, section 23).** The defined test
   is that each sample of the block is in a complete fragment, and a block can be in two fragments.
   The short term is removed. Each place states the test.
4. **The steps of the audio repair (SFF-796).** The text read as if the repair cut the audio
   sidecar and wrote the repair line in step 1 of SFF-793. It did not give the bad-row minimum of
   SFF-795. The text now gives the step of each action, and n is the smaller of the rows before the
   first bad row and the first rows whose block has each sample in a complete fragment.
5. **The packets of an incomplete `mdat` (SFT-732).** A new sentence says that a reader must not
   count the packets of an incomplete `mdat` that a decoder can still decode. In G5
   `audio_torn_fragment`, FFmpeg 9.0.2 decodes 70,728 samples (14 whole blocks), and the correct
   `records` has 9 blocks.

## Reason

An independent review found that these texts can be read in two ways, or do not agree with the
golden results or with the step order of SFF-793. Each correction is the smallest text change that
gives one reading. The reading in each case is the one that the golden bytes hold.

## Open work

See [open-work.md](../open-work.md).
