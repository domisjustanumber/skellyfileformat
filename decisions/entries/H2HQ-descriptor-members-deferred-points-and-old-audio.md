# H2HQ — Optional descriptor members, absent and null model members, the points that wait, the early audio of old skellycam recordings, the consolidation after gate 2

**Status:** accepted, 2026-11-16 (user; questions Q121 and Q125 to Q129 of round 3 of the review
of the golden folders).

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
6. **The consolidation (Q129).** One consolidation entry supersedes the changed lines of the
   accepted entries that cannot be absorbed. Then these entries are absorbed. The consolidation
   changes no rule. It is done after the gate 2 review, not before.

## Reason

The user answered "otherwise agree" to the recommendations of round 3 of the review on
2026-11-16. The user gave no reason for these items.

## Open work

See [open-work.md](../open-work.md).
