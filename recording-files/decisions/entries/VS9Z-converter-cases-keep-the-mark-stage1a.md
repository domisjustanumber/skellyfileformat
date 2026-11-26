# VS9Z — The converter cases keep the mark `stage1a`

**Status:** absorbed into [`conformance.md#the-stage-of-each-test`](../../conformance.md#the-stage-of-each-test), 2026-11-26 (commit on dom/v1-player-rules; was accepted, 2026-11-26 (user; answer Q858, [ADR-SY2H](SY2H-answers-q858-to-q861-converter-cases-and-legacy-readers.md)); was proposed, 2026-11-26 (agent; the text change of [ADR-A8Y2](../../../decisions/entries/A8Y2-skellysync-is-the-only-converter-of-old-recordings.md))).

## Decision

The owner did not decide this point. The agent chose it to write the text of A8Y2.

1. The converter cases `names_and_layout[camera_key_0]` of SFT-705 and `video_sidecar[converter]`
   of SFT-717 keep the mark `stage1a`. They now stand for the converter of skellysync, not of
   skellycam.
2. `conftest.py`, the stage tables and `tools/tests/test_conformance_stages.py` do not change.
3. The section [The stage of each test](../../conformance.md#the-stage-of-each-test) states the
   choice and links this entry.

## Reason

- A mark is a label, not a build stage
  ([ADR-YBT1](../../../decisions/entries/YBT1-spec-only-test-adapter-and-labels.md) item 4).
- The cases check writer rules of sections 4 and 8 (SFF-720, SFF-754 and the old time as
  `arrival_ns`). They need no file of a later stage and no skellysync decision.
- The user approved gate 2 for `stage1a` ([ADR-N1AM](N1AM-gate-2-approval-of-stage-1.md)). The
  mark `stage1b` is provisional. A move would make two approved cases provisional.

## Alternatives rejected

- Move the two cases to `stage1b`, with SFT-760 and G17: the cases would wait for the skellysync
  decisions that they do not need, and the stage tables, `conftest.py` and the gate 2 approval of
  stage 1 would change.
