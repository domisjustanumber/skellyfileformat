# CE4D — Rotation: frames stored unrotated, rotation in the sidecar header only

**Status:** accepted, 2026-11-12 (user).

## Decision

1. A writer stores each camera frame as the camera sent it, in the orientation of the sensor. The
   writer does not rotate the pixels.
2. Each video timing sidecar header holds `display_rotation`: the rotation, in steps of 90 degrees,
   that a reader applies to show the frame upright. The spec gives the field and its direction.
3. A writer does not write a container rotation flag, for example Matroska
   `Projection`/`ProjectionPoseRoll`.
4. A reader that shows or processes frames applies `display_rotation` itself: the skellycam player,
   freemocap and skellysync.
5. A general video player (for example VLC) shows the frames in sensor orientation. This is
   accepted.

## Reason

- The camera JPEG bytes stay the camera's own bytes, and a rotated camera costs no CPU.
- One field in the header is the only source of the rotation.
- A container flag gives different pictures in different readers. OpenCV rotates by default, PyAV
  and VLC do not. VLC 3.0.24 honours no rotation flag in MKV, so a flag does not make the files
  upright in VLC.

## Consequences

- freemocap must apply `display_rotation`. Today skellycam bakes the rotation into the pixels, so
  freemocap sees rotated frames. For a camera with a rotation other than 0, a recording in the new
  format gives freemocap unrotated frames until freemocap applies the field.
- In VLC and other general players, a camera that was mounted on its side shows on its side.

## Evidence

- The rotation flag test
  ([FINDINGS](https://github.com/domisjustanumber/skellycam/blob/6bfd7f8b0f1407be6120e1f1c126912d97955c59/research/skellycam_recording/recording_upgrade/results/rotation_flag/FINDINGS.md)):
  VLC 3.0.24 showed every rotated MKV unrotated (`ProjectionPoseRoll` from PyAV or the FFmpeg CLI,
  a `rotate` tag, 90/180/270 degrees, 720p and 1080p); it rotated only H.264 in MP4. OpenCV 5.0.0
  auto-rotates; PyAV 19.0.2 reports the rotation and does not rotate the pixels.
- The manifest field review lists rotation as the one display need with no source in the files
  today
  ([manifest_field_review.md](https://github.com/domisjustanumber/skellycam/blob/a4b1565b2aa1afe3c3c73e03974740c2471d91b1/research/skellycam_recording/docs/manifest_field_review.md)).
- These files are on the `dom/research` branch of the skellycam fork. That branch is not
  force-pushed, so the permalinks stay valid.

## Alternatives rejected

- Rotate the pixels with a lossless JPEG transform: every player shows the frame upright, but it
  costs 2.0–2.2 ms per frame at 720p and 6.8–8.9 ms at 1080p, and the stored bytes are no longer
  the camera's bytes.
- The header field plus a container flag: FFmpeg tools and OpenCV rotate, VLC and PyAV do not, so
  readers give different pictures of one file.

## Not repeated

- Do not test VLC orientation with the scene filter or the rc `snapshot` command. They save the
  picture before VLC applies orientation, so they show a file that VLC rotates on screen as
  unrotated.
