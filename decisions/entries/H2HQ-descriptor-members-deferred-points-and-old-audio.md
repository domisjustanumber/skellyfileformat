# H2HQ — Optional descriptor members, absent and null model members, the points that wait, the early audio of old skellycam recordings, the consolidation

**Status:** absorbed into
[`spec/SPEC.md#23-the-reader-result`](../../spec/SPEC.md#23-the-reader-result),
[`spec/parts/parquet-descriptor.md#processing`](../../spec/parts/parquet-descriptor.md#processing),
[`spec/parts/parquet-descriptor.md#structure-rules-and-writer-rules`](../../spec/parts/parquet-descriptor.md#structure-rules-and-writer-rules),
[`spec/legacy-annex.md#8-old-recordings-in-skellycam-and-freemocap`](../../spec/legacy-annex.md#8-old-recordings-in-skellycam-and-freemocap),
[`golden/G03_CHOICES.md#the-descriptor`](../../golden/G03_CHOICES.md#the-descriptor),
[`decisions/README.md#rules`](../README.md#rules),
2026-11-17 (commit to main; was accepted, 2026-11-16 (user; questions Q121 and Q125 to Q129 of round 3 of the review
of the golden folders)).

## Decision

The user accepted these rules. Each item gives its question number.

1. **`filtering` and `camera_assignment` (Q121).** The descriptor members `filtering` and
   `camera_assignment` are optional. A reader checks that each is an object only when it is
   present (parts/parquet-descriptor.md, section "Processing").
2. **Absent and null model members (Q125).** The reader accepts a descriptor model member that is
   absent when the member has a default. It accepts null for a member that is "omitted when null".
   A writer still writes these members as the part says (SFF-893).
3. **The other open points of the descriptor model types (Q126).** These points wait for the
   freemocap `sfn26` port: the check of `tracker_connections`, `segment_topology`, the number of
   joint angle names, upper-case Euler letters, and the pins of skellyforge and skellytracker. The
   spec keeps its text of 2026-11-16 until then.
4. **The version members of the export files (Q127).** The place of the version members in the
   export inventory and in the BVH metadata JSON is deferred with section 18.3
   ([ADR-E45D](E45D-spec-draft-v2-corrections-after-review.md) item 3).
5. **The early audio of old skellycam recordings (Q128).** Legacy playback does not correct the
   early audio (9 to 74 ms) of old skellycam recordings. Playback shows a note: the audio of
   recordings of that era can lead by up to about 74 ms. This is a skellycam playback
   rule. In skellyfileformat, it closes the open-work item S10b.
6. **The consolidation (Q129).** One consolidation entry supersedes in full each accepted entry
   that cannot be absorbed because a later entry changed one of its rules
   ([ADR-G9ER](G9ER-consolidation-of-the-pushed-entries.md); corrected on 2026-11-17: the Rules
   allow only a full supersession, so these entries are not absorbed). The consolidation changes
   no rule. It is done now, before the gate 2 review and before any push
   ([ADR-HH7B](HH7B-absorb-documents-and-clean-up-timing.md) item 2, Q155, which replaces the timing of Q129; corrected on 2026-11-17).

## Reason

The user answered "otherwise agree" to the recommendations of round 3 of the review on
2026-11-16. The user gave no reason for these items.

## Open work

See [open-work.md](../open-work.md).
