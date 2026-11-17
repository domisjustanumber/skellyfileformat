# 1P4N — The coverage of the stage `timing` of a realtime run, and the latency at the time of the fold

**Status:** accepted, 2026-11-16 (user; questions Q94 and Q130 of round 4 of the review of the
golden folders).

## Decision

The user accepted these rules. Each item gives its question number.

1. **The origin of `timing` (Q94).** In a run that is folded from the realtime journal, the stage
   `timing` keeps `origin` `realtime` (SFF-834).
2. **The coverage of `timing` (Q94).** A frame is a `timing` hit when the realtime pipeline handled
   it at all: it has a good journal data record of any channel of its sensor group.
   `frames_processed` of `timing` counts these frames. In G13 this is 11 of 12: frame 9 has no
   record. `skips` is `{"no_record": frames_in_take − frames_processed}`, as for the other stages.
3. **The latency of `timing` (Q94).** There is one latency for each processed frame: the lowest
   latency of the counted records of that frame. For G13, the reviewer computed by hand `p50`
   26.5 ms and `p99` 34.3 ms. Verify these values when the golden generator runs.
4. **The text of the rule (Q94).** The rule text says that each frame has a time, and that this
   count is about the realtime pipeline, not about the `TIMESTAMPS` rows.
5. **Events (Q94).** A journal event can name `timing` or the stage of a channel that the journal
   header declares. The fold fails on each other event, and freemocap keeps the journal.
6. **The meaning of `origin` (Q94).** One sentence defines `origin`: `realtime` means that the run
   was folded from the journal.
7. **The latency is fixed at the fold (Q130).** The latency uses the group times of the frames as
   they were when the journal was folded. A repair that rewrites the times of a realtime run does
   not change `latency_ms`. A check of a repaired take must not compute the latency again from the
   rewritten rows.

## Reason

The user answered "agree to both" to review 2 of Q94 on 2026-11-16. The review gave these reasons.
`coverage` tells what the realtime pipeline did with the frames of the take. The null rows of the
Parquet already tell which values exist. The literal rule of
[ADR-6VRQ](6VRQ-spec-v2-details-part-13.md) item 38c counts the records of a channel of the stage.
A journal has no channel of the stage `timing` (SFF-841), so that rule gave 0 of 12 for G13. That
is false: the pipeline handled 11 frames. A provenance tells which attempt wrote a stage. The fold
writes the `timing` rows of a realtime run, so `realtime` is the correct origin.

## Consequences

- This entry changes item 38c of [ADR-6VRQ](6VRQ-spec-v2-details-part-13.md) for the stage
  `timing`. ADR-6VRQ is absorbed. SFF-834 states the changed rule and cites this entry next to it
  (the [Rules](../README.md#rules)). ADR-6VRQ keeps its status.
- [ADR-P76Y](P76Y-tracking-parquet.md) item 8 does not change.
- The golden generator makes G13 and the case `higher_minor_journal` of G10 again. This entry is
  the decision entry that `AGENTS.md` section 4 needs for these changes of the golden files. It
  closes item 44 of `golden/G10_G13_G14_CHOICES.md`.
- [ADR-158N](158N-details-for-the-decisions-of-round-3.md) (proposed) holds the details that the
  spec text of this entry needed.

## Alternatives rejected

- A `timing` hit for each frame with a `TIMESTAMPS` row: each frame of each run has one, so the
  count is always N of N. It tells nothing about the realtime pipeline.
- `timing` with `origin` `posthoc` and `coverage` null: a label that the user does not expect in a
  run that only the fold made. It also needs runs with mixed origins.
- The literal rule: 0 of N. It is false.
- Mixed origins in one run, and a rule that a journal header declares one or more channels: not
  needed. A header with no channels gives a true realtime run with 0 of N.

## Open work

See [open-work.md](../open-work.md).
