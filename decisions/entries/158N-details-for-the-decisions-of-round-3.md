# 158N — Details of the decisions Q94 and Q104 to Q138: camera match, repair step 3 and an interrupted repair, sidecar with no `take_uuid`, "has a default", `timing` coverage, orphan folder file

**Status:** absorbed into
[`spec/SPEC.md#8-video-timing-sidecar`](../../spec/SPEC.md#8-video-timing-sidecar),
[`spec/SPEC.md#12-writing-crashed-files-and-repair`](../../spec/SPEC.md#12-writing-crashed-files-and-repair),
[`spec/SPEC.md#16-tracking-parquet`](../../spec/SPEC.md#16-tracking-parquet),
[`spec/SPEC.md#17-realtime-journal`](../../spec/SPEC.md#17-realtime-journal),
[`spec/SPEC.md#20-opening-a-folder`](../../spec/SPEC.md#20-opening-a-folder),
[`spec/SPEC.md#23-the-reader-result`](../../spec/SPEC.md#23-the-reader-result),
[`spec/parts/parquet-descriptor.md#structure-rules-and-writer-rules`](../../spec/parts/parquet-descriptor.md#structure-rules-and-writer-rules),
[`spec/conformance.md#timing-sidecars-sections-7-8-and-10`](../../spec/conformance.md#timing-sidecars-sections-7-8-and-10),
[`spec/conformance.md#tracking-parquet-section-16`](../../spec/conformance.md#tracking-parquet-section-16),
[`spec/conformance.md#opening-a-folder-section-20`](../../spec/conformance.md#opening-a-folder-section-20),
[`spec/conformance.md#tracking-parquet-the-reader-and-the-models-section-16`](../../spec/conformance.md#tracking-parquet-the-reader-and-the-models-section-16),
[`golden/G10_G13_G14_CHOICES.md#choices`](../../golden/G10_G13_G14_CHOICES.md#choices),
2026-11-17 (commit to main; was accepted, 2026-11-16 (user; questions Q131 to Q138 of round 5 of the review of the
golden folders; commit to main; was proposed, 2026-11-16, with the details that applying
[ADR-E68K](E68K-camera-match-repair-order-and-g5-g6-files.md),
[ADR-H2HQ](H2HQ-descriptor-members-deferred-points-and-old-audio.md),
[ADR-W5AK](W5AK-details-for-the-decisions-q83-to-q111.md) and
[ADR-1P4N](1P4N-timing-coverage-of-a-realtime-run-and-latency-at-the-fold.md) to the spec needed)).

## Decision

The user accepted these rules. Each item gives its question number.

1. **"Either ID missing" in the camera match (Q138).** The test of `model` applies when
   `vendor_id` or `product_id` is null in the connected camera or in the remembered camera
   (SFF-752).
2. **The prompt (Q138).** The prompt shows the live preview of the connected camera, and for each
   candidate its `user_name`, `camera_label` and `model` (SFF-752).
3. **Step 3 of a repair (Q132).** Step 3 has three passes, each across all sidecars: the fit
   lines, then the `# repair` lines, then the `# end` lines (SFF-793, SFF-795). The case
   `interrupted_repair` of G06 stopped in the `# repair` pass, so each sidecar is `unfinished`.
4. **The reason of a sidecar alone with no readable `take_uuid` (Q134).** The reason is
   `missing_metadata` when the header has no `take_uuid` line, and `bad_metadata` when the value
   has the wrong form (SFF-748). The folder warning is `orphan_file` (SFF-865).
5. **"Has a default" (Q135).** The reader accepts an absent member only when the row of the member
   in the descriptor part gives a default. `tags` and `angle_names` stay required. The rule applies
   to `RecordedModel` and its nested types (SFF-893).
6. **Test inputs.** The test inputs that a test makes at test time for SFT-719 (a pair of
   `repaired` of G6 with one more row than blocks), SFT-761 (a sidecar alone with no `take_uuid`
   line, and one with a `take_uuid` in a wrong form) and SFT-770 (a copy with no
   `anchor_segment_name` and with `observation_frame` null) are accepted.
7. **A good data record of a sensor group (Q136).** A data record that is good in the journal scan
   (SFF-843) and whose `channel_index` the header declares with the `sensor_group` of that group. A
   rejected record and a cut record do not count (SFF-834).
8. **The latency of `timing` (Q136).** For one channel and frame, only the last record in file
   order counts (SFF-845). The lowest latency of a frame is the lowest over all channels of the
   group. `p50` and `p99` use the nearest-rank rule of the other stages, with k =
   `frames_processed`.
9. **The events of `timing` (Q136).** `events` of `timing` holds the events that name `timing`, in
   journal order. The fold writes an event into each sensor group that has a stage provenance for
   the stage of the event. The stage of a channel is its `stage` member. A failed fold writes no run, and SFF-845 keeps the journal.
10. **The test inputs of SFT-751.** A journal with two records of one frame at different latencies
    in two channels, and a journal with an event that names a stage of no channel of the header,
    each made at test time, are accepted. After the repair of SFT-751, `latency_ms` is unchanged, and the
    test computes the expected latency from the times at the fold, not from the rewritten rows.
11. **The G13 journal (Q137).** The data record of channel 0, frame 10, is 50 ms later than the
    other records (latency 83.0 ms). So `p99` of the stage `observations` is 83.0 ms, and a wrong
    `timing` rule gives a different `p99`. The user accepted this change of the golden file.
12. **An interrupted repair (Q131).** A repair that stops in step 3 can leave some sidecars
    `repaired` and the others `unfinished`. An interrupted repair leaves the manifest in the state
    `recording`. The program asks again, and a new repair finishes the rest (SFF-793, SFF-798).
    This replaces the words "never half repaired" of ADR-E68K item 3.
13. **A folder file with no take in a folder with a take (Q133).** A folder file of this format
    that no manifest lists, and whose name has the `<rec>` of no take, is in `other_files` as in a
    folder with no take: state `invalid`, reason `take_fact_mismatch`, and the folder warning
    `orphan_file` (SFF-889). This adds to ADR-W5AK item 5.

## Reason

The user answered "agree with all" to the questions Q131 to Q138 of round 5 on 2026-11-16. Item
12 closes the short window between two `# end` writes, which "never half repaired" did not cover.
Item 13 gives a state to a file that had none.

## Open work

See [open-work.md](../open-work.md).
