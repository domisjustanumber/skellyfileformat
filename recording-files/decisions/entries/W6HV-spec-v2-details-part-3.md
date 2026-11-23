# W6HV — Spec draft v2 details, part 3: journal values and camera row alignment

**Status:** absorbed into
[`spec/SPEC.md#8-video-timing-sidecar`](../../SPEC.md#8-video-timing-sidecar),
[`spec/SPEC.md#16-tracking-parquet`](../../SPEC.md#16-tracking-parquet),
[`spec/SPEC.md#17-realtime-journal`](../../SPEC.md#17-realtime-journal),
[`spec/SPEC.md#20-opening-a-folder`](../../SPEC.md#20-opening-a-folder),
[`spec/SPEC.md#appendix-a-golden-folders`](../../SPEC.md#appendix-a-golden-folders),
2026-11-16 (commit to main; was accepted, 2026-11-16).

## Decision

An independent review found 18 groups of ambiguous points in spec draft v2. An agent proposed one
resolution for each, in parts 3 to 8. The user accepted each item of each part on 2026-11-16, with
the recommended option of each CHOICE. The recommended option is the text of the item. Parts 1 and 2 are [ADR-VPD9](VPD9-spec-draft-v2-details.md)
and [ADR-3D33](3D33-spec-draft-v2-details-folder-files.md). "Basis" gives the source: (1) an
accepted entry; (2) code or research evidence; (3) the simplest rule that gives the same reader
result in each reader. "CHOICE" marks a design choice that had a plausible alternative. An item keeps
its number in all parts.

This part holds items 1 and 2. The other parts are [ADR-Q4BK](Q4BK-spec-v2-details-part-4.md)
(items 3 and 4), [ADR-0XX2](0XX2-spec-v2-details-part-5.md) (5 to 8),
[ADR-ATW0](ATW0-spec-v2-details-part-6.md) (9 to 13),
[ADR-DM9S](DM9S-spec-v2-details-part-7.md) (14 to 17) and
[ADR-72QQ](72QQ-spec-v2-details-part-8.md) (18 and 19).

1. **Journal** (SFF-839 to SFF-845; SFT-756 to SFT-758; G13).
   - a. `frame_number` of a data record is the Parquet `frame_number` of SFF-827: the position of
     the multi-camera frame in the camera files of the take. The writer writes no record for a frame
     outside the take. Basis (1), [ADR-VPD9](VPD9-spec-draft-v2-details.md) item 13.
   - b. A journal header must not declare a channel of the kind `TIMESTAMPS`. A reader refuses such a
     journal (`bad_schema`). Basis (1), [ADR-VPD9](VPD9-spec-draft-v2-details.md) item 13 ("a
     journal holds no time as a data value").
   - c. CHOICE. The fold writes each event record into `coverage.events` of the stage that the event
     names, for each sensor group: an array of the event objects, in journal order. Basis (1),
     [ADR-Q9X2](Q9X2-realtime-tracking-journal.md) item 3: the events must not be lost.
   - d. The digest of SFF-845 is the SHA-256 of these bytes: for each channel in order of
     `channel_index`, for each `frame_number` in increasing order, the n × k values in record order,
     each as a little-endian float32. When two records have the same channel and frame, only the
     last in file order counts. A missing value (NaN in the journal, null in the Parquet) is the
     bytes `00 00 C0 7F`. The count is the number of these values. A null row of a frame with no
     record is not in the count or the digest. Basis (3).
   - e. `processed_ns` is the host-clock time at which the pipeline finished the result. The fold
     uses it only for `latency_ms`: `processed_ns` minus the group time of the frame (SFF-828), with
     nearest-rank percentiles. Basis (3).
   - f. The fields of a record have no padding. A data payload has 22 + 4 × n × k bytes. Basis (3).

2. **Camera row alignment** (SFF-754, SFF-756, SFF-827, SFF-872; SFT-717, SFT-748; G1, G3, G9).
   - a. Row k of each video sidecar of a take is multi-camera frame k. The finished camera files of
     one take have the same number of rows. Basis (2): skellycam at 169caf637 lets a camera grab only
     when its frame count is at or below each other count
     (`skellycam/core/camera_group/camera_orchestrator.py`, lines 118 to 131), and the finalizer
     refuses different frame counts (`skellycam/core/recorders/recording_finalizer.py`, lines 166 to
     170).
   - b. The link check `frames` is also `mismatch` when the finished camera files of a take have
     different row counts. In an unfinished take, the counts can differ. A reader then uses the
     frames from 0 to the smallest count minus 1 as multi-camera frames. G9 gets this vector.
     Basis (3).
   - c. CHOICE. "Grid" means the sequence of multi-camera frames. Bit 1 `filled` becomes
     provisional. A writer of version 2.0 writes 0 to it, because the lockstep gate copies no frame.
     Its meaning stays: the writer copied the JPEG of the row before, because the camera gave no new
     frame for this multi-camera frame. It waits for the slot assembly of the skellycam plan, row
     2.2, and for desk tests DT4 and DT7. Basis (2): the research plan keeps lockstep now and leaves
     the fill rule open.
   - d. CHOICE. Add bit 3 (8) `repeat`: the source frame number is equal to that of the row before.
     `gap` is then set when the number is not the number before plus 1 and not the number before.
     Basis (1), [ADR-6RSB](6RSB-camera-files-mjpeg-mkv-and-csv-timing.md) item 4 ("gaps, repeats,
     fills"), and draft v0 SFF-170.

## Reason

- Each item removes a point at which two readers, or a reader and a golden result, can differ.
- An accepted entry or the current code decides most items. The CHOICE items need the user. Each
  has one alternative, which is not rejected.

## Consequences

- New: the flag bit `repeat` and the member `coverage.events`.

## Evidence

- skellycam at 169caf637: `skellycam/core/camera_group/camera_orchestrator.py` and
  `skellycam/core/recorders/recording_finalizer.py` (item 2a).
- skellyspecs at 38ad0d6, `spec/SPEC.md`: draft v0 SFF-170 and SFF-171.
- skellycam `dom/research` (local, not committed): `research/CAPTURE_AND_RECORDING_PLAN.md` row 2.2;
  `research/skellycam_recording/docs/spec_v0_revival_tracking_sidecars_20261113.md` sections 4 and
  8; `research/skellycam_recording/docs/realtime_tracking_storage_20261115.md` sections 3 to 5.

## Open work

[open-work.md](../open-work.md)

_Edited 2026-11-23 (commit to main): link repair._

_Edited 2026-11-23 (commit to main): rename._
