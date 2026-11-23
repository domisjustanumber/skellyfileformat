# 68Z6 — Frames stored unrotated; `display_rotation` in the camera file's metadata only

**Status:** superseded by [DE9S](DE9S-rotation-in-the-video-csv-header.md), 2026-11-16 (commit to main; was accepted, 2026-11-13).

## Decision

1. A writer stores each camera frame as the camera sent it, in the orientation of the sensor. The
   writer does not rotate the pixels.
2. The metadata of each camera file ([ADR-SFK5](SFK5-mcap-container.md) item 4) holds
   `display_rotation`: the rotation, in steps of 90 degrees, that a reader applies to show the frame
   upright. The spec gives the key and its direction.
3. A writer does not write a rotation anywhere else, for example in a message field, a transform
   message or a JPEG EXIF orientation tag.
4. A reader that shows or processes frames applies `display_rotation` itself: the skellycam player,
   freemocap and skellysync.
5. A general viewer (for example Lichtblick) shows the frames in sensor orientation. This is
   accepted.

This entry supersedes [ADR-CE4D](CE4D-rotation-in-header-only.md) in full. Items 1 and 4 restate
its items 1 and 4. Item 2 restates its item 2 with "camera file metadata" in place of "video timing
sidecar header". Item 3 restates its item 3 (no container rotation flag) for MCAP. Item 5 restates
its item 5 with Lichtblick in place of VLC ([ADR-WD9A](WD9A-lichtblick-reference-viewer.md)).

## Reason

- The reasons of ADR-CE4D stay: the camera JPEG bytes stay the camera's own bytes and a rotated
  camera costs no CPU; one field is the only source of the rotation; a rotation flag gives different
  pictures in different readers.
- The sidecar header no longer exists ([ADR-SFK5](SFK5-mcap-container.md)).

## Open work

[open-work.md](../open-work.md)
