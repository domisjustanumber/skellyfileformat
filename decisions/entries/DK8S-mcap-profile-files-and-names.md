# DK8S — MCAP profile: one file per device, profile `freemocap`, protobuf, names and topics

**Status:** accepted, 2026-11-13 (user).

## Decision

1. Each file of the format is an MCAP file, as the MCAP specification defines it
   (https://mcap.dev/spec). The format is a profile of MCAP. It uses only the records and the
   fields that MCAP defines.
2. A take has one MCAP file for each device: one for each camera and one for the microphone.
3. The MCAP Header `profile` is `freemocap`. The Header `library` holds the writer string, for
   example `skellycam 2.1.3`.
4. The message encoding is `protobuf`. Each file embeds the schemas that it uses, with the names
   that the schema publisher gives (`foxglove.CompressedImage`, `foxglove.CompressedAudio`,
   `foxglove.Log`).
5. A camera frame is one Message with the schema `foxglove.CompressedImage` and `format: "jpeg"`.
   The `data` field holds the JPEG bytes as the camera or the encoder gave them.
6. The topics carry the device label: `/cameras/<camera_label>/image`,
   `/cameras/<camera_label>/log` and `/microphones/<label>/audio`.
7. The Metadata records have the names `freemocap.format` (`major`, `minor`, `prerelease`),
   `freemocap.recording` (the facts of the take) and `freemocap.timing` (the fit and the sequence
   breakpoints of a camera file). The facts of one device are in the `metadata` map of its MCAP
   Channel record: for example `camera_label`, `camera_key`, `nominal_rate`, `display_rotation`,
   `frames_per_chunk` and the Opus header fields. The spec gives each key.
8. `camera_label` and `camera_key` keep their spec v0 rules: a label of 1 to 16 characters from
   `A`–`Z`, `a`–`z`, `0`–`9`, `_` and `-`, different for each camera of a take; the key is a
   truncated SHA-256 of an identity string, never the raw serial number.
9. There is no timing sidecar, no Matroska file, no attachment, no embed step, no live or final
   offset and no Segment UID.
10. A reader opens a file that has no summary. It reads each complete chunk in file order. The
    spec defines this read and its result.
11. The player time never decreases in one file.
12. The spec fixes no file names. The media file names and the folder names belong to the writer.
    The file extension is `.mcap`.

This entry supersedes [ADR-SFK5](SFK5-mcap-container.md) in full. Items 1, 5, 9, 10 and 11 restate
its items 1, 2, 5, 6 and 7. Item 7 states the names that its item 4 left to the spec. Item 12
restates its item 9. Its item 3 (which times each frame holds) is now
[ADR-752H](752H-timing-fields.md). Its item 8 (the recording manifest) is withdrawn: the user
dropped the manifest on the same day, and the whole-recording entry that supersedes ADR-41VF
records it.

## Reason

- The reasons of ADR-SFK5 stay: implement an existing standard; a custom reader is needed in all
  cases.
- The user chose one file per device over one file per take, after the single-writer test.
- The user chose `freemocap` as the profile name.
- Lichtblick merges open files by topic, so each device needs its own topic.
- MCAP's Header `library` field is defined as a free-form writer name for debugging, so the writer
  string needs no metadata key.

## Evidence

- skellycam `dom/research` (local commits, not pushed):
  - `research/skellycam_recording/docs/mcap_profile_decisions_20261113.md` (Q1, Q2, Q4, Q21, Q22b);
  - `research/skellycam_recording/recording_upgrade/results/mcap_single_writer/FINDINGS.md`;
  - `research/skellycam_recording/recording_upgrade/results/lichtblick_check/FINDINGS.md`.

## Alternatives rejected

- One file for each take with one writer process: it would need a new frame path from the camera
  processes to the writer, and it makes one process a single point of failure.
- `profile` = `skellyfileformat`: the user chose `freemocap`.
- FlatBuffers, ROS 2 or JSON encodings: protobuf has the widest library support, and JSON would
  base64 the JPEG bytes.

## Open work

[open-work.md](../open-work.md)
