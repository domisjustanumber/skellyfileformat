# SY2H — Answers Q858 to Q861: the converter cases, the readers of legacy folders and two texts that stay

**Status:** absorbed into [`README.md#scope-normative`](../../README.md#scope-normative), [`SPEC.md#21-legacy-folders`](../../SPEC.md#21-legacy-folders), [`conformance.md#the-stage-of-each-test`](../../conformance.md#the-stage-of-each-test), [`legacy-annex.md#8-old-recordings-in-skellycam-and-freemocap`](../../legacy-annex.md#8-old-recordings-in-skellycam-and-freemocap), [`README.md#implementations`](../../README.md#implementations), 2026-11-26 (commit on dom/v1-player-rules; was accepted, 2026-11-26 (user; answers Q858 to Q861 of the owner session of 2026-11-26, "agree to all")).

## Decision

The owner accepted the recommendation of each question.

1. **Q858.** [ADR-VS9Z](VS9Z-converter-cases-keep-the-mark-stage1a.md) is accepted. The converter
   cases `names_and_layout[camera_key_0]` of SFT-705 and `video_sidecar[converter]` of SFT-717
   keep the mark `stage1a`.
2. **Q859.** The code that reads legacy folders is in skellycam, skellysync and freemocap. The
   Scope section of `README.md` and section 21 of `SPEC.md` name skellysync. skellysync reads old
   recordings because it is their only converter
   ([ADR-A8Y2](../../../decisions/entries/A8Y2-skellysync-is-the-only-converter-of-old-recordings.md)).
3. **Q860.** The title of legacy annex section 8, "Old recordings in skellycam and freemocap",
   stays. Its anchor is linked from status lines.
4. **Q861.** The sentence "skellycam converts no recording" stays broad. It is not narrowed to "no
   old recording".

## Reason

- Q858: the cases need no file of a later stage and no skellysync decision (VS9Z).
- Q859: a converter of old recordings must read them. The two sentences named only skellycam and
  freemocap.
- Q860: a new title needs link repairs and adds no meaning.
- Q861: skellycam converts no recording of any kind
  ([ADR-46NQ](../../../decisions/entries/46NQ-old-recordings-play-as-they-are-no-upgrade-converter.md),
  [ADR-A8Y2](../../../decisions/entries/A8Y2-skellysync-is-the-only-converter-of-old-recordings.md)).
