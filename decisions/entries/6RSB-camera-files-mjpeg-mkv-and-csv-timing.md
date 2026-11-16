# 6RSB — Camera files: MJPEG in MKV with index timestamps, and one CSV timing sidecar

**Status:** accepted, 2026-11-16 (user; whole-folder grilling, 2026-11-13 to 2026-11-16).

## Decision

1. **Container.** A camera file is a Matroska file (RFC 9559) with one video track, `V_MJPEG`. Each
   frame is one JPEG image in one block. The file holds only the video and its container
   timestamps. All other data is in sidecars. The MCAP profile is withdrawn.
2. **Index timestamps.** The container timestamp of the frame at position k is k / nominal rate.
   A writer does not store measured times in the container. Blender and OpenCV count the frames of
   a file from these timestamps.
3. **No data in the frames.** A writer stores no timing data and no overlay in a JPEG frame.
4. **One CSV timing sidecar** for each camera file, `<rec>.<label>.csv`, next to it. It has one
   row for each frame, in file order. Each row holds the frame position, the arrival time, the
   sample time, the frame number of the camera, the flags (gaps, repeats, fills), the byte position
   and size of the frame in the MKV, and a CRC. Times are integer nanoseconds from the take start.
   A row has no wall-clock column. The header gives the take start in UTC and the UTC offset once.
5. **Header facts.** The CSV header holds what a reader needs to read that file alone: the format
   version, the take facts (`take_uuid`, the take start times, the UTC offset), `camera_key`,
   `camera_label`, the nominal rate, `display_rotation`, the group size and the position of the
   camera in the group, and the clock. The actual resolution, rate and frame count are only in the
   MKV and the CSV.
6. **Times.** The arrival time is the time on the host clock at which the writer received the
   frame. The sample time is the time that the capture driver gives, on the host clock, or absent.
   All files of a take use one host clock, which the header names. There is no legacy time: a
   conversion writer writes an old per-frame time as the arrival time.
7. **Nominal rate.** A rational `num/den`, each from 1 to 2^20. A reader refuses other values.
8. **`camera_key`** is the stable identity of a camera: a truncated SHA-256 of an identity string.
   It is a MUST for a skellycam capture writer. skellysync and the converter can write 0. A reader
   then links the camera by `camera_label` and gives a warning. `camera_key` is the only key that
   links the files of a camera: the manifest, the info JSON, the calibration TOML and the Parquet.
   `camera_label` is for people and for file names.
9. **The fit.** The writer computes the fitted time of each camera: the regular frame lattice on
   the host clock, from the arrival times and the sample times, as fit segments. Each segment gives
   its first and last frame position, the fitted time of its first frame in nanoseconds and the
   frame period as an exact integer. The segments are in position order, with no gap, and they hold
   each position of the file. A new segment starts where the camera stalls, restarts or changes rate.
   The writer names the fitter, its version and its parameters. The fitting method is the writer's
   choice. The spec defines how a reader evaluates a segment, with integers of unlimited size, so
   that every reader gets the same fitted times. Each row keeps its raw times, so that a later
   fitter can redo the fit.
10. **Player time.** The player time of a frame is its fitted time when the sidecar has a fit, and
    else its arrival time. A reader of an unfinished file uses the arrival times. The player time
    never decreases in one file.
11. **Frame shown.** A player shows, at take time t, the last frame whose player time is at or
    before t. It never computes a frame from its index and the frame rate.
12. **Strictly increasing times.** The times that a reader gives to freemocap for a camera strictly
    increase.

This entry supersedes [ADR-DK8S](DK8S-mcap-profile-files-and-names.md),
[ADR-752H](752H-timing-fields.md) and [ADR-MG7C](MG7C-fit-segments-by-position.md) in full.
- Item 6 restates 752H items 1, 3 and 4 with CSV columns in place of MCAP fields. Item 7 restates
  752H item 7. 752H items 2 and 6 (audio) are in [ADR-92TM](92TM-opus-audio-in-fragmented-mp4.md).
  752H item 5 (the encoder-skip log) is replaced by a CSV flag in
  [ADR-VPD9](VPD9-spec-draft-v2-details.md).
- Item 9 restates MG7C items 1, 2, 3, 5 and 7 and the fit cover of
  [ADR-T24G](T24G-spec-v1-review-fixes-crash-fit-audio.md) item 8, with the CSV in place of the
  `freemocap.timing` record. Item 10 restates MG7C item 8, T24G item 9 and DK8S item 11. MG7C items
  4 and 6 (sequence breakpoints) are withdrawn: each CSV row holds the camera frame number. MG7C
  item 9 (repair rebuilds the fit) is in [ADR-G1YG](G1YG-writing-crash-reading-and-repair.md).
- Item 8 restates the key rule of DK8S item 8. The label rule of DK8S item 8 is replaced by
  [ADR-5XNA](5XNA-folder-layout-names-and-manifest.md) item 4.
- DK8S items 1 to 7, 9, 10 and 12 (MCAP) are withdrawn.
- Items 1 to 5, 11 and 12 are new or from spec v0.

## Reason

- The freemocap Blender addon loads real video files. Blender reads an MJPEG MKV with index
  timestamps frame-exactly, and fails with real capture timestamps (DT-B1). So the user reversed
  the MCAP decision (skellycam plan D27).
- Without per-frame timing, gaps are invisible and a player cannot place frames of a crashed MKV.
- CSV is human-readable. Flushed for each row, it survives a kill as well as a binary file.

## Evidence

- skellycam `dom/research` (local, not committed):
  - `research/skellycam_recording/recording_upgrade/results/blender_mkv/FINDINGS.md` (DT-B1);
  - `research/skellycam_recording/docs/whole_folder_spec_plan_20261113.md`, "Grilling log": round
    1 C12; round 3 Q1, Q2; round 5 Q3, Q9, Q11, Q14.

## Alternatives rejected

- Binary `.skvt` sidecars (accepted 2026-11-13, then replaced): not human-readable.
- Real capture timestamps in the MKV: Blender and OpenCV count wrong frame numbers.

## Open work

[open-work.md](../open-work.md)
