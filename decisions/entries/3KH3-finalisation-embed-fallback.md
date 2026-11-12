# 3KH3 — Finalisation: embed when the appender can, verify, delete; recover an interrupted embed

**Status:** accepted, 2026-11-12 (user).

## Decision

1. At finalisation, the writer appends the video timing sidecar to the camera MKV as a Matroska
   attachment at the end of the file. It appends the audio timing sidecar to the `.mka` in the same
   way.
2. The writer embeds each sidecar when the appender does not refuse. The appender refuses a file
   with an unknown-size Segment, a Segment that does not end at the end of the file, a first Segment
   child that is not a SeekHead, an existing Attachments element, or no room for one more Seek
   entry. When it refuses, the separate sidecar is the final form, and a header flag
   (`separate_final`) tells this.
3. The writer deletes a separate sidecar file only after the embed verifies. The embed verifies
   when the SHA-256 of the embedded data is equal to the SHA-256 of the separate sidecar, the
   locator finds the attachment, and the CRCs of the first frame and the last frame are equal to
   their records. The appender writes only in the SeekHead span, the Segment size and after the old
   end of the file, so it cannot move a frame.
4. skellycam deletes its native `.flac` file only after each FLAC frame CRC and the decoded sample
   count of the `.mka` match.
5. The offsets and the Segment UID in a sidecar refer to the final bytes of the file.
6. The sidecar header has a `finalised` flag. The writer sets it as the last change to the separate
   sidecar before the embed. A separate sidecar without `finalised` shows that finalisation did not
   complete.
7. An interrupted embed leaves bytes after the end of the Segment, or an Attachments element at the
   end of the Segment that the SeekHead does not reference. A reader then uses the separate sidecar.
   A recovery cuts the file at the old end of the Segment, restores the Segment size and embeds again
   from the separate sidecar.
8. The finalisation order for each file, the appender steps and the order of the manifest write are
   in [SPEC.md section 9](../../spec/SPEC.md#9-embedding-and-finalisation).

This entry supersedes [ADR-77Z3](77Z3-finalisation-embed-verify-delete.md) in full. Items 1, 4 and
5 restate its items 1, 3 and 4. Item 2 makes its item 1 depend on the appender. Item 3 defines the
check of its item 2. Items 6 and 7 are new.

## Reason

- One file for each camera then holds its own timing. A separate file can become lost.
- An attachment at the end of the file changes only 25–26 header bytes. The frame offsets do not
  move, and VLC, ffprobe and OpenCV read the file as before.
- A file from another writer, or a file with no room in its SeekHead, cannot take the attachment.
  The separate sidecar then stays the final form. That is better than a failed finalisation.
- A check of each frame after the embed reads the whole file: minutes for 16 cameras of 1 h. The
  appender cannot move a frame, so a check of the attachment and of two frames is enough.
- The appender flushes after each of its three steps. Each interrupted state is then one of two
  states that a reader can detect, and the separate sidecar still exists in both.

## Evidence

- [sidecar_embedding FINDINGS](https://github.com/domisjustanumber/skellycam/blob/a65e540053073c58f01ef2c8c8297901f6d9517f/research/skellycam_recording/recording_upgrade/results/sidecar_embedding/FINDINGS.md):
  the attachment at the end of the file; the SeekHead always has room in FFmpeg files, also for
  files larger than 4 GiB; only header bytes change.
- [flac_skau FINDINGS](https://github.com/domisjustanumber/skellycam/blob/a65e540053073c58f01ef2c8c8297901f6d9517f/research/skellycam_recording/recording_upgrade/results/flac_skau/FINDINGS.md):
  the audio sidecar embedding and the verification.

## Alternatives rejected

- A check of every frame after the embed: too slow, and the appender cannot move a frame.
- Embedding as a SHOULD only: then most finalised recordings could keep separate files with no
  reason.

## Not repeated

- Do not use `ffmpeg -attach`. It puts the attachment before the clusters, and every frame offset
  moves.
- A remux moves every frame and changes the Segment UID. After a remux, rebuild the offsets by a
  scan of the final bytes.
