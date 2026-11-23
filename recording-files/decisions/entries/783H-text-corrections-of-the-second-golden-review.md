# 783H — Text corrections from the second review of the golden results

**Status:** absorbed into
[`spec/SPEC.md#12-writing-crashed-files-and-repair`](../../SPEC.md#12-writing-crashed-files-and-repair),
[`spec/SPEC.md#16-tracking-parquet`](../../SPEC.md#16-tracking-parquet),
[`spec/SPEC.md#20-opening-a-folder`](../../SPEC.md#20-opening-a-folder),
[`spec/SPEC.md#21-legacy-folders`](../../SPEC.md#21-legacy-folders),
[`spec/SPEC.md#23-the-reader-result`](../../SPEC.md#23-the-reader-result),
[`spec/conformance.md#conventions-and-versioning-sections-2-and-3`](../../conformance.md#conventions-and-versioning-sections-2-and-3),
[`spec/conformance.md#tracking-parquet-section-16`](../../conformance.md#tracking-parquet-section-16),
[`spec/conformance.md#opening-a-folder-section-20`](../../conformance.md#opening-a-folder-section-20),
[`golden/G07_G09_CHOICES.md#g9-the-files`](../../golden/G07_G09_CHOICES.md#g9-the-files),
[`golden/G10_G13_G14_CHOICES.md#4-spec-gaps-contradictions-and-ambiguities`](../../golden/G10_G13_G14_CHOICES.md#4-spec-gaps-contradictions-and-ambiguities),
2026-11-17 (commit to main; was accepted, 2026-11-17 (user; questions Q144, Q145, Q147, Q148 and Q150 of round 7 of the
review of the golden folders; commit to main; was proposed, 2026-11-16, by an agent, from the
second independent review of the golden expected results)).

## Decision

The user accepted these corrections. Items 1 to 6 make the text agree with decided rules and with
the golden folders (Q144). No golden byte changes for them. Items 7 to 10 are the details that the
spec needs to apply
[ADR-FB8P](FB8P-refused-pairs-rotation-member-invalid-files-audio-records-legacy-subfolders.md).
Each of them gives its question number.

1. **SFT-703 and the version cases.** The sentence "each file has `format_version` 2.0" names its
   inputs: the output of each writer, G1, G3 and the case `prerelease_0` of G10. The other cases of
   G10 hold a higher `minor` or an unknown `major`. The warning `prerelease` is on each file of a
   golden case that holds `format_prerelease`, as SPEC.md Appendix A says
   ([ADR-2MQE](2MQE-tests-prerelease-serial-and-exports.md) item 2). A file that does not hold it
   has no warning.
2. **SFF-834, `frames_processed`.** For each stage, `frames_processed` counts the frames with one
   or more good data records (SFF-843), as for the stage `timing`
   ([ADR-158N](158N-details-for-the-decisions-of-round-3.md) item 7). G13 gives 11 with the two
   readings, so its bytes do not change.
3. **SFT-748 and the Parquet of G12.** The Parquet `equal_fitted_times.parquet` declares no
   channel. So the test checks only the time rules on it: each row is a `TIMESTAMPS` row of
   `capture` with the component `timestamp_s`, its value is its `timestamp_s`, `frame_number` is
   the position of the frame, and the times are the strict player times (SFF-828). "Every row rule"
   applies to the Parquet of G3.
4. **SFT-763 and the vector `recording_id`.** Each vector of G9 other than `recording_id` gives
   `mismatch` in its check. The Parquet of `recording_id` is `invalid` with `take_fact_mismatch`,
   so no check evaluates it.
5. **`golden/G10_G13_G14_CHOICES.md`, item 44.** The file no longer says that item 44 is open:
   [ADR-1P4N](1P4N-timing-coverage-of-a-realtime-run-and-latency-at-the-fold.md) decided it.
6. **`golden/G07_G09_CHOICES.md`, item 11 (the case `camera_key` of G09).** The changed key keeps
   `key_origin` `computed`, and it is not the hash of its `device` values. A reader does not check
   this (SFF-803), so the case has one fault for a reader.
7. **A refused pair and the take (Q147; SFF-869, FB8P item 1).** A refused audio pair (`invalid` or
   `unsupported_version`) counts as a present file for the take state, the same as a refused
   camera pair. A refused pair of either kind counts as a file of the take wherever the reader counts
   the files of the take: for the take state and for `extra_files`. A refused pair stays out of the
   take-level checks ([ADR-64ER](64ER-unknown-major-form-audio-fit-rows-and-refused-pair-counts.md) item 3, Q147; corrected on 2026-11-17).
8. **"No `records`" (Q148; SFF-885, FB8P item 3).** "No `records`" is `records` null, not an empty
   list. The same holds for a file with an unknown major version (`unsupported_version`). G9, G10
   `unknown_major_sidecar` and G11 have null.
9. **A block of an interrupted audio file (Q145; SFF-792, FB8P item 4).** A block of audio that is
   only partly inside the complete fragments is not usable. `records` of an interrupted audio file
   holds a block only when each sample of the block, from `first_sample` to `first_sample` +
   `n_samples` − 1, is in a complete fragment.
10. **The legacy subfolders (Q150; SFF-875, FB8P item 5).** The subfolders that a reader MAY read
    for the legacy recognition are exactly `SyncedVideos/`, `RawVideos/`,
    `synchronized_videos/timestamps/`, `output_data/` and `output_data/raw_data/`.

## Reason

The user answered "Q144 - yes", then "agree to all" to the recommendations of round 7 on
2026-11-17. The user gave no reason. Each correction is the smallest text change that makes the
spec, the test list and the choice files agree with the decided rules and with the golden bytes.
Before the decision, items 7 to 10 also held text that the user did not decide. That text moved to
[ADR-7JJJ](7JJJ-audio-repair-refused-header-values-and-the-rules-of-w5ak.md) item 11 (the form of
a header value, Q149) and to
[ADR-SM53](SM53-choices-for-the-decisions-of-round-7.md) (proposed).

## Consequences

- Item 9 changed the golden results of G5 (both cases) and of the case `interrupted_repair` of G6.
  The audio item of `audio_clean_kill` has 19 `records` of 21 rows, and the audio item of
  `audio_torn_fragment` has 9.
- A refused pair with an audio sidecar, and a refused third camera pair, are new test-time vectors
  of SFT-762.

## Open work

See [open-work.md](../open-work.md).

_Edited 2026-11-23 (commit to main): link repair._
