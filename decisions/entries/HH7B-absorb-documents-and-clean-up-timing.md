# HH7B — More absorb documents, the time of the clean-up, and the old skellycam audio in the legacy annex

**Status:** absorbed into
[`decisions/README.md#rules`](../README.md#rules),
[`spec/legacy-annex.md#8-old-recordings-in-skellycam-and-freemocap`](../../spec/legacy-annex.md#8-old-recordings-in-skellycam-and-freemocap),
2026-11-17 (commit to main; was accepted, 2026-11-17 (user; questions Q154 to Q157 of the
clean-up of the decision log; commit to main)).

## Decision

The user accepted these rules ("agree to all", and "Q157 - yes" for the detail of item 1). Each
item gives its question number.

1. **The golden documents are absorb documents (Q154).** `golden/README.md` and the files
   `golden/*_CHOICES.md` are absorb documents. They state the conventions of the golden folders.
   [`AGENTS.md`](../../AGENTS.md#4-project-rules) already requires an entry for a change of a
   golden file.
   - The normative parts (Q157): the Rules also list the normative parts `spec/parts/*.md` of
     `spec/SPEC.md` as absorb documents, because `SPEC.md` makes them normative and entries link
     into them. An agent added this detail. The user confirmed it on 2026-11-17 ("Q157 - yes";
     corrected on 2026-11-17).
2. **The time of the clean-up (Q155).** The absorb pass and the consolidation entry of
   [ADR-H2HQ](H2HQ-descriptor-members-deferred-points-and-old-audio.md) item 6 are done now,
   before the gate 2 review and before any push. This replaces the time of Q129 ("after the gate 2
   review").
3. **The old skellycam audio (Q156).** `spec/legacy-annex.md` states the skellycam playback rule
   of ADR-H2HQ item 5: the legacy playback does not correct the early audio of old skellycam
   recordings, and a note says that the audio of that era can lead by up to about 74 ms. The annex
   is an absorb document, so ADR-H2HQ can be absorbed.

The Rules of the index list the new absorb documents (items 1 and 3).

## Reason

The index was at 13,899 of its 14,000 characters. Most Active entries could not be absorbed
because their rules were in documents that were not absorb documents, or because a later entry
changed one of their rules.

## Consequences

- Item 2 is a one-off action. This commit group does it: the absorb pass and
  [ADR-G9ER](G9ER-consolidation-of-the-pushed-entries.md).

## Open work

See [open-work.md](../open-work.md).
