# Z641 — Guidance for programs in the spec, the scope of a gate 2 approval, and no push before gate 2

**Status:** superseded by [YBT1](YBT1-spec-only-test-adapter-and-labels.md), 2026-11-17 (commit to main; was absorbed, 2026-11-17 (commit to main; was accepted, 2026-11-17 (user; questions Q161, Q163 and Q164 of
round 9, Q166 and Q167 of round 10, and Q182 of round 13; "agree to all"))).

## Decision

The user accepted these items. Each item gives its question number.

1. **Guidance for programs (Q161).** The spec states the three kept rules that
   [ADR-G9ER](G9ER-consolidation-of-the-pushed-entries.md) restated as text, because no absorb
   document stated them. They are rules of the programs, not of the format. The spec marks each of
   them "Guidance for programs: ...", as it marks the privacy notice of section 22 and the badge of
   SFF-835. They add no requirement and no SFF ID.
   - Section 8, from ADR-VPD9 item 6, a rule of skellycam: the flag `encode_skip` replaces the log
     message of an encoder skip.
   - Section 17, from ADR-Q9X2 items 2 and 7, rules of freemocap: the journal writer is a node of
     its own in the freemocap realtime pipeline: a subscriber with its own queue, so that the
     aggregator and the cameras never wait for the disk. The journal is the binary file of
     freemocap. The rule that skellycam writes only standard media and human-readable sidecars does
     not apply to it.

   ADR-G9ER links these two headings in place of the text.
2. **The scope of a gate 2 approval (Q163, Q166).** The user approves gate 2 for each stage of
   [ADR-CPM2](CPM2-stages-of-the-implementation.md). The approval of a stage covers the
   conformance tests and the golden folders of that stage in `spec/conformance.md`. A test that uses
   an `exports/` folder only as input, for example to check that a reader ignores it (Q166), is in
   the stage of its folder. A test of the content of an export file waits with section 18.3. The
   approval does not cover the provisional points that wait for a desk test or a hardware test. For
   these, the implementation writes only the provisional behaviour that the spec gives now. On
   2026-11-17, the user had not approved gate 2 for a stage. (Corrected in place by [ADR-CPM2](CPM2-stages-of-the-implementation.md): the
   approval was for all tests and G1 to G16, and did not cover the skellysync folders and G17. They
   are stage 1b now.)
3. **No push before gate 2 (Q164, Q182).** skellyfileformat is not pushed before the user approves
   gate 2. The user's approval of stage 1 ends this agreement (Q182). The agent still asks the user
   before the first push. From that push on, an entry cannot be corrected in place. The agreement
   ends at the approval, so the gate 2 item of [open-work.md](../open-work.md) states it.
   (Corrected in place by Q182: the item did not say which stage approval ends the agreement.)
4. **The order of implementation (Q167).** In each stage, after the gate 2 approval of that stage,
   the implementation starts with the Python reader. The Python writer is next. The JavaScript
   reader is last. The JavaScript reader is built only in stage 1. (Corrected in place by [ADR-CPM2](CPM2-stages-of-the-implementation.md):
   the order was for the whole implementation.)

## Reason

- Item 1: these three rules were the last reason why ADR-G9ER stayed Active. A rule of a program
  that the format does not need is guidance, as in section 22 and SFF-835.
- Item 2: an agent must know which parts the approval covers before it starts the implementation.
  Section 4 of `AGENTS.md` holds the gate steps, and the open-work item of gate 2 goes away at the
  approval. So `AGENTS.md` states the scope.
- Item 3: each correction from the gate 2 review can then change the entries in place, because an
  entry that is not pushed can change in each part ([Rules](../README.md#rules)).
- Item 4: the tests check the reader directly against the golden folders. The tests check the
  writer when the reader reads back the files that the writer writes. The JavaScript reader must
  give the same bytes as the Python reader. Step 5 of the gate order in section 4 of `AGENTS.md`
  states the order.

## Consequences

- ADR-G9ER is absorbed, and the index has no Active entry.

## Open work

See [open-work.md](../open-work.md).
