# FF01 — The fitted time as fit segments, and the sequence breakpoints, in a `freemocap.timing` Metadata record

**Status:** accepted, 2026-11-13 (user).

## Decision

1. Before `finish()`, a capture writer computes the fitted time of each camera: the regular frame
   lattice of the camera on the host clock, from the arrival times and the sample times.
2. The writer stores the fit in the `freemocap.timing` Metadata record of the camera file, as a list
   of fit segments. Each segment gives its first and last camera frame number (`sequence`), the
   fitted time of its first frame in nanoseconds, and the frame period as an exact integer. A new
   segment starts where the camera stalls, restarts or changes rate.
3. The record also names the fitter, its version and its parameters. The fitting method is the
   writer's choice. The spec defines only how a reader evaluates a segment, with integer
   arithmetic, so that every reader gets the same fitted times.
4. The record also holds the sequence breakpoints: the (position in the file, `sequence`) pairs
   where `sequence` does not increase by exactly 1, starting with the first frame. A reader gets the
   `sequence` of any frame from them without reading the frame.
5. Each frame keeps its raw arrival time and sample time ([ADR-752H](752H-timing-fields.md)), so a
   later fitter can redo the fit.
6. The player time of a frame is its fitted time when the file has the record, else its arrival
   time.
7. The repair of a crashed file ([ADR-S4FG](S4FG-writing-crash-and-repair.md)) rebuilds the
   breakpoints and the fit.

This entry supersedes [ADR-0YV1](0YV1-fitted-time-in-sidecar.md) in full. Items 1 and 6 restate its
items 1 to 3, with "before `finish()`" for "at finalisation". Item 2 replaces its item 4 (the fitted
time in each sidecar record): the fitted time is in the file, as segments. Items 3, 4, 5 and 7 are
new.

## Reason

- Arrival times jitter by 4.6–4.8 ms standard deviation per frame, with outliers up to 47 ms. A fit
  was within 0.56 ms of flash ground truth on the C922 and the C930e
  (`research/usb_cameras/docs/timestamp_accuracy_options.md` in skellycam). freemocap pairs frames
  across cameras by time, and audio must line up with video.
- Stored segments give every reader the same times. The fitting method can improve without a
  format change.
- The MCAP summary holds no `sequence` (Electron desk test). Without breakpoints, a reader must read
  every frame header or scan the file to find dropped frames, and a fit by file position puts every
  frame after a drop too early.
- A Metadata record is a standard MCAP record, so this needs no custom schema. The writer already
  holds every time before `finish()`, so nothing is appended to a finished file.

## Evidence

- skellycam `dom/research` (local commits, not pushed):
  - `research/skellycam_recording/docs/mcap_profile_decisions_20261113.md` (Q7, Q13a, Q13b);
  - `research/skellycam_recording/recording_upgrade/results/mcap_electron/FINDINGS.md` task 2.

## Alternatives rejected

- Readers compute the fit: the fitting method would become normative and would need an exact port
  to JavaScript.
- A separate fit file per camera: it brings back the file-pairing rules.
- Fit segments in a custom schema appended after `finish()`: needs an MCAP append step and a custom
  schema.

## Open work

[open-work.md](../open-work.md)
