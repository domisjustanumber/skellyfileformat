# MG7C — Fit segments keyed by frame position, in the `freemocap.timing` Metadata record

**Status:** superseded by [6RSB](6RSB-camera-files-mjpeg-mkv-and-csv-timing.md), 2026-11-16 (commit to main; was accepted, 2026-11-13).

## Decision

1. Before `finish()`, a capture writer computes the fitted time of each camera: the regular frame
   lattice of the camera on the host clock, from the arrival times and the sample times.
2. The writer stores the fit in the `freemocap.timing` Metadata record of the camera file, as a list
   of fit segments. Each segment gives its first and last frame position (`pos_first`, `pos_last`),
   the fitted time of its first frame in nanoseconds, and the frame period as an exact integer. A
   new segment starts where the camera stalls, restarts or changes rate.
3. The segments are in order of position, with no gap between them.
4. A camera restart or a wrap of `sequence` needs no special rule. A reader gets the `sequence` of a
   frame from the breakpoints (item 6).
5. The record also names the fitter, its version and its parameters. The fitting method is the
   writer's choice. The spec defines only how a reader evaluates a segment, with integer
   arithmetic, so that every reader gets the same fitted times.
6. The record also holds the sequence breakpoints: the (position in the file, `sequence`) pairs
   where `sequence` does not increase by exactly 1, starting with the first frame. A reader gets the
   `sequence` of any frame from them without reading the frame.
7. Each frame keeps its raw arrival time and sample time ([ADR-752H](752H-timing-fields.md)), so a
   later fitter can redo the fit.
8. The player time of a frame is its fitted time when the file has the record, else its arrival
   time.
9. The repair of a crashed file rebuilds the breakpoints and the fit.

This entry supersedes [ADR-FF01](FF01-fit-and-breakpoints-in-metadata.md) in full. Items 1, 5, 6,
7, 8 and 9 restate its items 1, 3, 4, 5, 6 and 7. Item 2 restates its item 2 with position keys in
place of `sequence` keys. Items 3 and 4 are new.

## Reason

- A camera restart can reset its frame number, so one `sequence` value can be in two segments of
  one file. A position is unique in a file.
- With `sequence` keys, a wrap made the order of the segments differ from the file order.
- From ADR-FF01: arrival times jitter by 4.6–4.8 ms standard deviation per frame, and a fit was
  within 0.56 ms of flash ground truth. Stored segments give every reader the same times, and the
  fitting method can improve with no format change. The MCAP summary holds no `sequence`, so the
  breakpoints let a reader find dropped frames without a scan. A Metadata record needs no custom
  schema.

## Evidence

- skellycam `dom/research` (local commits, not pushed):
  - `research/skellycam_recording/docs/spec_v1_review_20261113.md` (B1) and the answers of the
    user in it;
  - `research/usb_cameras/docs/timestamp_accuracy_options.md` (jitter and fit accuracy);
  - `research/skellycam_recording/docs/mcap_profile_decisions_20261113.md` (Q7, Q13a, Q13b);
  - `research/skellycam_recording/recording_upgrade/results/mcap_electron/FINDINGS.md` task 2.

## Alternatives rejected

- Keep `sequence` keys and forbid a repeated `sequence` in one file: a camera restart would have to
  end the file.
- Readers compute the fit: the fitting method would become normative.
- A separate fit file per camera: it brings back the file-pairing rules.
- Fit segments in a custom schema appended after `finish()`: needs an MCAP append step.

## Open work

[open-work.md](../open-work.md)
