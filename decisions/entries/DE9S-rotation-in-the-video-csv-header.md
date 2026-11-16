# DE9S — Frames stored unrotated; `display_rotation` in the video CSV header; one informative copy

**Status:** accepted, 2026-11-16 (user; whole-folder grilling, 2026-11-13 to 2026-11-16).

## Decision

1. A writer stores each camera frame as the camera sent it, in the orientation of the sensor. The
   writer does not rotate the pixels.
2. The header of each video CSV sidecar holds `display_rotation`: the rotation, in steps of 90
   degrees, that a reader applies to show the frame upright. The spec gives the key and its
   direction.
3. A writer does not write a rotation anywhere else, for example in a container element, a JPEG
   EXIF orientation tag or the `camera_configs` of the info JSON. A reader ignores an EXIF
   orientation tag in a JPEG.
4. One exception: the manifest `summary` shows the rotation of each camera. It is an informative
   copy. A reader must not use it ([ADR-5XNA](5XNA-folder-layout-names-and-manifest.md) item 6).
5. A reader that shows or processes frames applies `display_rotation` itself: the skellycam player,
   freemocap, the freemocap Blender addon and skellysync.
6. 2D tracking data and the calibration use the pixel space of the stored JPEG, in sensor
   orientation, before `display_rotation` ([ADR-P76Y](P76Y-tracking-parquet.md)).
7. A general viewer (for example VLC, or Blender with no add-on) shows the frames in sensor
   orientation. This is accepted.

This entry supersedes [ADR-68Z6](68Z6-rotation-in-metadata-only.md) in full. Items 1 and 5 restate
its items 1 and 4. Item 2 restates its item 2 with the video CSV header in place of the camera file
metadata. Item 3 restates its item 3, names `camera_configs`, and restates
[ADR-T24G](T24G-spec-v1-review-fixes-crash-fit-audio.md) item 12. Item 7 restates its item 5 with
VLC and Blender in place of Lichtblick. Items 4 and 6 are new.

## Reason

- The reasons of ADR-68Z6 stay: the camera JPEG bytes stay the camera's own bytes, and a rotated
  camera costs no CPU; one field is the only source of the rotation; a rotation flag gives different
  pictures in different readers.
- The human-readable overview must show the rotation, and the user accepted one marked copy for it.
- 2D data in the stored pixel space follows from the stored orientation.

## Evidence

- skellycam `dom/research`, `research/skellycam_recording/docs/whole_folder_spec_plan_20261113.md`,
  "Grilling log": round 2 Q9 and Q12; round 5 Q12 (local, not committed).
- `research/skellycam_recording/docs/spec_v0_revival_tracking_sidecars_20261113.md`, decision 4.

## Open work

[open-work.md](../open-work.md)
