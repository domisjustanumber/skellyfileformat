# 783H — Text corrections from the second review of the golden results

**Status:** proposed, 2026-11-16 (agent; corrections that make the text agree with decided rules,
from the second independent review of the golden expected results).

## Decision

The user did not decide these corrections. An agent made them so that the text agrees with the
decided rules and with the golden folders. No golden byte changes. The user must accept or change
each of them.

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

## Reason

Each correction is the smallest text change that makes the spec, the test list and the choice
files agree with the decided rules and with the golden bytes. The review found that the golden
results follow the spec, and that these sentences did not.

## Open work

See [open-work.md](../open-work.md).
