# 158N — Details that the spec text of the decisions Q94 and Q104 to Q130 needed

**Status:** proposed, 2026-11-16 (agent; the details that applying
[ADR-E68K](E68K-camera-match-repair-order-and-g5-g6-files.md),
[ADR-H2HQ](H2HQ-descriptor-members-deferred-points-and-old-audio.md),
[ADR-W5AK](W5AK-details-for-the-decisions-q83-to-q111.md) and
[ADR-1P4N](1P4N-timing-coverage-of-a-realtime-run-and-latency-at-the-fold.md) to the spec needed).

## Decision

The user did not decide these details. An agent wrote them into the spec text, so that the
accepted rules apply. The user must accept or change each of them.

1. **"If either is missing" in the camera match** (SFF-752, E68K item 1). Proposal: the test of
   `model` applies when `vendor_id` or `product_id` is null in the connected camera or in the
   remembered camera.
2. **The prompt** (SFF-752, E68K item 1). Proposal: the prompt shows the live preview of the
   connected camera, and `user_name`, `camera_label` and `model` of each candidate.
3. **Step 3 of a repair** (SFF-793, SFF-795, E68K item 3). The decision names the fit lines and
   `# end`. Proposal: step 3 also writes the `# repair` line, in three sub-steps: the fit lines to
   each sidecar, then the `# repair` line to each sidecar, then the `# end` line to each sidecar.
   This is the choice of the golden folders (`golden/CAPTURE_VECTORS_CHOICES.md` item 6): the
   case `interrupted_repair` of G06 stopped in the `# repair` sub-step, so each sidecar is
   `unfinished`.
4. **The reason of a sidecar alone with no readable `take_uuid`** (SFF-865, E68K item 5).
   SPEC.md has two reasons for header metadata (SFF-748). Proposal: `missing_metadata` when the
   header has no `take_uuid`, else `bad_metadata`. The folder warning is `orphan_file`: it is the
   SPEC.md warning for a file that belongs to no take.
5. **"Has a default"** (parts/parquet-descriptor.md, SFF-893, H2HQ item 2). Proposal: a member has
   a default when its row in the part gives one. So the reader accepts the absence of, for example,
   `anchor_segment_name`, `zero_offsets`, `sided` and each presentation member with a default.
   The rows of `tags` and `angle_names` give no default, so these stay required. The rule applies
   to `RecordedModel` and its nested types: the scope of the structure rules of the part.
6. **New test inputs** (conformance.md). SFT-719: a pair of `repaired` of G6 with one more row
   than blocks (W5AK item 10). SFT-761: a sidecar alone with no `take_uuid` key, and one with a
   `take_uuid` in a wrong form (E68K item 5). SFT-770: a sixth copy with no `anchor_segment_name`
   and with `observation_frame` null; the first copy removes a member whose row gives no default
   (H2HQ item 2). Each input is made at test time.
7. **A good data record of a sensor group** (SFF-834, 1P4N item 2). Proposal: a record of the type
   2 that is good in the scan of SFF-843, whose `channel_index` the header declares with the
   `sensor_group` of that group. A rejected record and a cut record do not count.
8. **The latency of `timing`** (SFF-834, 1P4N item 3). Proposal: "the counted records" are the
   records that count in SFF-845: for one channel and frame, only the last in file order. The
   lowest latency of a frame is the lowest over all channels of the group. `p50` and `p99` use the
   nearest-rank rule of the other stages, with k = `frames_processed`.
9. **The events of `timing`** (SFF-834, SFF-844, 1P4N item 5). Proposal: `events` of `timing` holds
   the events whose `stage` is `timing`, in journal order, as for the other stages. The fold writes
   an event into each sensor group that has a stage provenance for the stage of the event. The
   stage of a channel is its `stage` member. A failed fold writes no run, and SFF-845 keeps the
   journal.
10. **The test inputs of 1P4N** (SFT-751). Proposal: a journal, made at test time, with two records
    of one frame at different latencies in two channels; a journal with an event that names
    a stage of no channel of the header. After the repair of SFT-751, `latency_ms` is unchanged, and
    the test computes the expected latency from the times at the fold, not from the rewritten rows.
11. In the journal of G13, the data record of channel 0, frame 10, is 50 ms later than the
    other records (latency 83.0 ms). So the lowest latency of a frame and the latency of each
    record give different `p99` values, and the golden file can show a wrong `timing` rule. The
    `timing` values of ADR-1P4N do not change. `p99` of the stage `observations` is 83.0 ms.

## Reason

Each detail is the smallest text that makes the accepted rule exact. Item 4 keeps SFF-748 true
for each sidecar: a sidecar with no `take_uuid` key is `missing_metadata` there. Item 9 follows the
reference rules of the part: each stage of a stage provenance has a checkpoint or a channel of that
group and stage, and a realtime run has no checkpoints.

## Open work

See [open-work.md](../open-work.md).
