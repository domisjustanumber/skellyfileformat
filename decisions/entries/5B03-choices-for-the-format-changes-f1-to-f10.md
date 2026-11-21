# 5B03 — Choices of the agent for the format changes F-1 to F-10

**Status:** accepted, 2026-11-21 (user; the user accepted the eight items, branch dom/f1-f10, not
pushed; was proposed, 2026-11-21 (an agent chose these items to apply
[ADR-6AT7](6AT7-format-changes-f1-to-f10-missing-frames-and-short-files.md))).

## Decision

The record of ADR-6AT7 does not decide these points. The spec states each item, with a citation of
this entry. [ADR-76NN](76NN-details-for-the-format-changes-f1-to-f10.md) completes items 4, 5 and
8.

1. **The take time of a `missing` row with no player time** (SFF-783, F-10). A take time t is in a
   `missing` row when that row is the last row whose player time is at or before t. It is also in a
   `missing` row with no player time when the player shows the multi-camera frame of that row at t.
   How a player selects that multi-camera frame is its choice.
2. **No earlier frame that is not `missing`** (SFF-783, F-10). The player shows no frame of the
   camera, with the mark "no frame".
3. **The completion after a failed write** (SFF-894, F-2, F-4). The program completes a camera pair
   after a write to its camera file failed in the same way as after a kill or a hang, with no
   question to the user.
4. **The steps of a repair that replaces the tail of a short file** (SFF-794, SFF-795, F-2). It cuts
   the sidecar before its first row with empty byte fields. It appends a placeholder block to the
   camera file for each cut row, and appends each cut row again with the byte fields of its
   placeholder. SFF-794 allows this one append to a media file.
5. **Two summary values** (SFF-728, F-1, F-2). When the camera file holds no block, `stored_px` is
   the mode size of SFF-756, as the skellycam recorder writes it. When no video sidecar holds an `arrival_ns`, `duration_s` is the audio value, or null when
   the take has no audio.
6. **The order of the four Annex K.3 tables** in the inserted DHT segment is the choice of the writer
   (SFF-734, F-3). SFT-712 accepts each order.
7. **The reader rule of F-5 is a player rule** (SFF-895). When a `detail` does not parse, the player
   shows the warning of the code with no frame number. The codes of SFF-727 are not warnings of the
   reader result: SFF-887 does not change. The recorder text says "the take warning of the code".
   SFF-887 has a closed list, so the text says "the warning" of the player.
8. **The test inputs.** The golden folder G18 and items 48 to 52 of
   `golden/CAPTURE_VECTORS_CHOICES.md`. The test adapter gets `write_frame` with `data` None for a
   capture error, `TakeWriter.camera_stopped(index, reason)` and the detail function
   `camera_lost_at(folder, name)`, and `strict_ns` skips a frame with no player time
   (`tests/conformance/INTERFACE_NOTES_capture.md`). SFT-730 takes the lock in the test process
   and accepts a writer that waits or refuses.

## Reason

- Items 1 and 2: SFF-783 must say what a player shows in each case. The skellycam player selects the
  image by time and the mark by the multi-camera frame, and it shows no image before the first real
  row. Item 1 allows that and adds no time to a row with no time.
- Item 3: a write error makes the same short file as a kill (SFF-754). Without item 3, SFF-793 makes
  the program ask the user, and the recorder of skellycam completes it with no question.
- Item 4: SFF-794 forbids each change before a cut and each append to a media file. The tail cannot
  change in another way.
- Item 5: the summary rules gave no value for these two new cases.
- Item 6: any order decodes the same, and the record gives none.
- Item 7: the manifest warnings were never warnings of the reader result. A change of SFF-887 is a
  larger change than the record asks for.
- Item 8: the smallest inputs that test the new rules through the test adapter.

## Alternatives rejected

- Item 1: a time for a row with no time from the other cameras. The format has no time of a
  multi-camera frame, and F-1 says that such a row has no player time.
- Item 7: new take warnings `camera_dead` and `camera_file_short` in SFF-887. That changes each
  reader result of a take with these codes.

## Open work

See [open-work.md](../open-work.md).
