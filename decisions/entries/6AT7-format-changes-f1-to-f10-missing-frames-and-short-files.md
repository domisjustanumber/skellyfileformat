# 6AT7 — Format changes F-1 to F-10: missing frames, short files, a provisional key, the lock and three player rules

**Status:** absorbed into
[`spec/SPEC.md#1-scope-and-terms`](../../spec/SPEC.md#1-scope-and-terms),
[`spec/SPEC.md#5-the-recording-manifest`](../../spec/SPEC.md#5-the-recording-manifest),
[`spec/SPEC.md#6-camera-files`](../../spec/SPEC.md#6-camera-files),
[`spec/SPEC.md#8-video-timing-sidecar`](../../spec/SPEC.md#8-video-timing-sidecar),
[`spec/SPEC.md#11-clocks-the-fit-and-reader-timing`](../../spec/SPEC.md#11-clocks-the-fit-and-reader-timing),
[`spec/SPEC.md#12-writing-crashed-files-and-repair`](../../spec/SPEC.md#12-writing-crashed-files-and-repair),
[`spec/SPEC.md#13-capture-info-json`](../../spec/SPEC.md#13-capture-info-json),
[`spec/SPEC.md#23-the-reader-result`](../../spec/SPEC.md#23-the-reader-result),
[`spec/SPEC.md#appendix-a-golden-folders`](../../spec/SPEC.md#appendix-a-golden-folders),
[`spec/conformance.md#missing-frames-and-short-files-sections-5-6-8-11-and-12`](../../spec/conformance.md#missing-frames-and-short-files-sections-5-6-8-11-and-12),
2026-11-21 (branch dom/f1-f10, not pushed; was accepted, 2026-11-21 (user; the user decided the ten
changes on 2026-11-19 and 2026-11-20 in skellycam, and on 2026-11-21 the user gave this project the
sole control of this repository)).

## Decision

The user decided these ten changes of the format. The record is in skellycam: ADR-J3QP (M1 to M10,
C2, C3), ADR-P98T (one list F-1 to F-10) and section 13 of `specs/recorder.md` on the skellycam
branch dom/integration. That section is the source of the text. An agent wrote the text into the
spec in the style of the spec. The format version stays 2.0 with `format_prerelease` 1: this is an
internal draft change (SFF-710, SFF-714). [ADR-5B03](5B03-choices-for-the-format-changes-f1-to-f10.md)
holds the choices of the agent for the points that the record does not decide.

1. **F-1, `missing` rows and the placeholder.** Flag bit 4 (16) `missing`: the camera gave no
   usable frame for the row. A capture writer writes it for a frame with a capture error, and for
   each multi-camera frame after the last frame of a camera that stopped during the take. The block
   of a `missing` row is a black baseline JPEG with the size, the number of components and the H/V
   factors of the frames of the camera (the mode size and 2x1, 1x1, 1x1 when the writer knows no
   frame). A `missing` row keeps the source frame number and the times of a frame with an error, and
   has them empty when the camera gave no frame. The `# end` line gets `missing=<M>` before
   `encode_skips`. Each summary camera gets `missing` after `filled`, and `summary_stale` also
   compares it. `duration_s` uses the last row that holds an `arrival_ns`. A row with no
   `arrival_ns` has no player time, and the strict player time skips it. `rows` counts the
   `missing` rows, and a `records` item of a row with no time has null times (SFF-728, SFF-729,
   SFF-745, SFF-754 to SFF-758, SFF-781, SFF-782, SFF-885, section 8).
2. **F-2, the short file.** A camera file has one block for each row, with two exceptions: when the
   process that writes it is killed or hangs, and when a write to it fails, the file ends early.
   Each row after its last block is `missing`, with empty `byte_offset` and `byte_size`, and has no
   block. A camera file can hold no block: then it holds only the EBML header, the Segment and the
   Tracks. SFF-759 counts the rows with a `byte_offset`. A `missing` row with empty byte fields is
   usable when it is complete and its CRC is correct (SFF-740). The repair keeps such rows before
   its cut, and they do not count as blocks. A later repair MAY replace the tail of a short file with
   placeholders (SFF-795).
3. **F-3, two exceptions to unchanged camera bytes** (SFF-734): the placeholder of a `missing` row,
   and the standard tables of ITU-T T.81 Annex K.3, inserted as one DHT segment immediately before
   the first SOS of a JPEG with no DHT segment before it. No other byte changes.
4. **F-4, the completion of a take by its own writer** (SFF-894). When the process that writes a
   camera pair ends during a take with no normal end of its files, the program that records the
   take completes the pair at the end of the same take, in the same run, after that process ended:
   the cuts of SFF-795, no byte appended to the camera file, a `missing` row with empty byte fields
   for each multi-camera frame up to the rows of the take, then the `# repair` line and the `# end`
   line. It writes fit lines only when it has a fitter. It does not ask the user (an exception to
   SFF-793). A reader reports the pair as `repaired`.
5. **F-5, three warning codes** (SFF-727, SFF-895): `camera_dead` with the `detail`
   `last_frame=<p> reason=<text>`, `camera_file_short` with `blocks=<b> rows=<r>`, and `take_error`
   with the error text and the camera of the error or null. A write error gives
   `camera_file_short` and `take_error`, and no `camera_dead`. A reader parses the two `detail`
   forms as keys and values. A player shows "camera lost at frame N", with N = p + 1, or 0 for `none`.
6. **F-6, a provisional key.** The `key_origin` value `provisional`: a capture writer that cannot
   read the identity of SFF-752 made the key from its own camera identifier. The key is not stable,
   and a program does not remember it. A reader accepts the four values (SFF-752, SFF-803, section 13).
7. **F-7, the lock on each OS** (SFF-789). Windows: an exclusive lock of byte 0 for 1 byte
   (`LockFileEx` with `LOCKFILE_EXCLUSIVE_LOCK`, or `LockFile`). Linux and macOS: `flock` with
   `LOCK_EX` on the whole file.
8. **F-8, equal player times** (SFF-783): the player shows the highest of the positions.
9. **F-9, when a player checks the block count** (SFF-759): a player MAY show frames before it
   counts the blocks, and then checks the order of the blocks while it reads. The reader result
   does not use this order.
10. **F-10, a `missing` row in a player** (SFF-783): the player shows the last frame before it that
    is not `missing`, with the mark "no frame", and never shows the placeholder as a picture. A
    program that ignores the flag shows black.

New tests SFT-771 to SFT-773, and new parts of twelve older tests. The golden folder G18 shows
F-1, F-2 and F-4. Each sidecar and manifest of G1 to G16 gets the `missing` count. No committed
reader result of G1 to G16 changes.

## Reason

- A camera can fail in the middle of a take while the other cameras go on. One block for each row
  keeps OpenCV and Blender correct: they read frame i as row i (skellycam ADR-J3QP Evidence).
- A killed process cannot add blocks to its file, so the short file and its completion are
  necessary. The completion lets a take end `finished` with no question.
- A player needs a rule for a lost camera, a tie and the order of its checks. Two programs must
  use one lock form.

## Consequences

- The skellycam reader and writer of commit d67679a must follow this text.
- freemocap: a frame with no strict player time has no `timestamp_s` of SFF-828 yet
  ([open-work.md](../open-work.md)).

## Open work

See [open-work.md](../open-work.md).
