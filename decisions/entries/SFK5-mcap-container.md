# SFK5 — MCAP is the container: JPEG frames and timing in MCAP messages; no MKV, no sidecar, no embed

**Status:** accepted, 2026-11-13 (user).

## Decision

1. Each file of the format is an MCAP file, as the MCAP specification defines it
   (https://mcap.dev/spec). The format is a profile of MCAP. It uses only the records and the
   fields that MCAP defines.
2. A camera frame is one MCAP Message with the schema `foxglove.CompressedImage` and
   `format: "jpeg"`. The `data` field holds the JPEG bytes as the camera or the encoder gave them.
3. For each frame, the file holds the arrival time, the sample time (or a value that means absent)
   and the source frame number. The spec maps each of them to an MCAP field: the Message
   `log_time`, the Message `publish_time`, the Message `sequence` or the `timestamp` field of the
   schema.
4. The facts about the file and its recording are in MCAP Metadata records or in the `metadata` map
   of the MCAP Channel record. The spec gives the record names and the keys.
5. There is no timing sidecar, no Matroska file, no attachment, no embed step, no live or final
   offset and no Segment UID. MCAP's own indexes, CRCs and summary replace them.
6. A reader opens a file that has no summary, for example after a crash. It reads each complete
   chunk in file order. The spec defines this read and the result.
7. The player time never decreases in one file.
8. The recording manifest is `<rec>.skellyrec.json`.
9. The spec fixes no other file names. The media file names and the folder names belong to the
   writer (skellycam's own spec). The file extension `.mcap` is the MCAP extension.

This entry supersedes [ADR-FGK2](FGK2-video-sidecar-record-size.md),
[ADR-3KH3](3KH3-finalisation-embed-fallback.md) and
[ADR-WD1R](WD1R-file-attachment-and-mime-names.md) in full. Item 7 restates ADR-FGK2 item 5. Items 8
and 9 restate ADR-WD1R items 4 and 5. Item 3 keeps the arrival time, the sample time and the source
frame number of ADR-FGK2 item 3. The legacy time and the encoder-skip flag of ADR-FGK2 wait for a
profile choice ([open-work.md](../open-work.md)). All other rules of the three entries are
withdrawn.

## Reason

- The user wants to implement an existing standard, not to invent one. A player reads the format
  through a custom reader in all cases: MJPEG does not play in a browser `<video>` element, and the
  user dropped VLC compatibility on the same day.
- MCAP is open (MIT), versioned and documented. It has maintained readers and writers in Python,
  TypeScript, Rust, C++, Go and Swift, and a CLI with `recover`, `doctor` and `merge`.
- Its records give the timing fields, the indexes, the CRCs and the recovery path that the custom
  sidecar specified. Most blockers of the third spec review were in the embed and recovery rules
  that this entry removes.
- It has room for later GigE Vision cameras: raw images (`foxglove.RawImage`), a device clock per
  camera and per-frame chunk data as more channels.

## Consequences

- `spec/SPEC.md` and `spec/conformance.md` v0 must be rewritten as an MCAP profile. The sections on
  the MKV profile, the sidecar byte layouts, embedding, offsets and the sidecar names go.
- General video tools (ffmpeg, VLC, OpenCV) do not read the files. A tool that needs a video file
  needs an export, which copies the JPEG bytes unchanged.
- freemocap reads frames through a skellyfileformat reader (phase 2 of the skellycam plan).

## Evidence

- Claims checked against `mcap` 1.6.0, `@mcap/core` 2.4.0 and the MCAP CLI 0.4.0, with
  measurements: skellycam `dom/research`,
  `research/skellycam_recording/docs/mcap_check_20261113.md` and
  `research/skellycam_recording/recording_upgrade/scripts/mcap_check/check_mcap.py` (local commit,
  not pushed). Overhead: 196 B for each frame with one chunk for each frame (220 B with the
  protobuf wrapper). A file cut at 60 %: the streaming read gives each complete chunk (180 of 300);
  the seeking reader gives none.

## Alternatives rejected

- Keep MKV with the custom sidecar (spec v0): a new format to specify and maintain; its embed and
  recovery rules failed three reviews.
- Matroska with real timestamps and a custom data track, as in the Azure Kinect recordings: it
  still needs a custom track format, and real timestamps make OpenCV miscount frames.
- XDF (Lab Streaming Layer): good clock model, but no video in the file.
- NWB and BIDS: archive layouts, not live recording formats. They can be export targets.

## Not repeated

- Do not read a crashed file with `make_reader()` or with the default `log_time_order=True` of
  `NonSeekingReader.iter_messages()` (`mcap` 1.6.0). Both give no messages from a file with no
  summary.
- The Python writer does not write the data section CRC unless `enable_data_crcs=True`.

## Open work

[open-work.md](../open-work.md)
