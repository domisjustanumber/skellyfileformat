# 77Z3 — Finalisation: embed the sidecars, verify, then delete the separate files

**Status:** accepted, 2026-11-12 (user; backfilled from the skellycam plan rev 3.8).

## Decision

1. At finalisation, the writer appends the video timing sidecar to the camera MKV as a Matroska
   attachment at the end of the file. It appends the `.skau` to the `.mka` in the same way.
2. The writer deletes a separate sidecar file only after the embed verifies: the attachment SHA
   matches, and the media blocks did not change.
3. skellycam deletes its native `.audio.flac` file only after each FLAC frame CRC and the decoded
   sample count of the `.mka` match.
4. The offsets and the Segment UID in a sidecar refer to the final bytes of the file.

## Reason

- One file for each camera then holds its own timing. A separate file can become lost.
- An attachment at the end of the file changes only 25–26 header bytes. The frame offsets do not
  move, and VLC, ffprobe and OpenCV read the file as before.

## Evidence

- [sidecar_embedding FINDINGS](https://github.com/domisjustanumber/skellycam/blob/a65e540053073c58f01ef2c8c8297901f6d9517f/research/skellycam_recording/recording_upgrade/results/sidecar_embedding/FINDINGS.md): the attachment at the end of
  the file; the SeekHead always has room, also for files larger than 4 GiB; the offset rules.
- [flac_skau FINDINGS](https://github.com/domisjustanumber/skellycam/blob/a65e540053073c58f01ef2c8c8297901f6d9517f/research/skellycam_recording/recording_upgrade/results/flac_skau/FINDINGS.md): the `.skau` embedding and the verification.
- Plan rows S4, S9 and D16, and section 2.7 ([plan](https://github.com/domisjustanumber/skellycam/blob/a65e540053073c58f01ef2c8c8297901f6d9517f/research/CAPTURE_AND_RECORDING_PLAN.md)). The skellycam plan and its evidence are on the `dom/research` branch of the skellycam fork. That branch is not force-pushed, so the permalinks stay valid.

## Not repeated

- Do not use `ffmpeg -attach`. It puts the attachment before the clusters, and every frame offset
  moves.
- A remux moves every frame and changes the Segment UID. After a remux, rebuild the offsets by a
  scan of the final bytes.
