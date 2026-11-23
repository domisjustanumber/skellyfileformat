# VPD9 — Spec draft v2 details, part 1: structure, names, media files, timing and writing

**Status:** superseded by [G9ER](G9ER-consolidation-of-the-pushed-entries.md),
2026-11-17 (commit to main; was accepted, 2026-11-16 (user; gate 1 review of spec draft v2, item by item)).

## Decision

The user's decisions ([ADR-2C9V](../../../decisions/entries/2C9V-whole-take-folder-scope-and-package.md) to
[ADR-QS7B](QS7B-blender-outputs-and-exports.md)) do not fix these details. An agent proposed them in
spec draft v2. The user accepted each item at gate 1, and changed item 13. Part 2 is
[ADR-3D33](3D33-spec-draft-v2-details-folder-files.md).

The user also confirmed these rules of the draft at gate 1: the file names are a MUST for a writer;
both `camera_key` and `camera_label` stay, and a program links by `camera_key`; the name that a user
gives a camera is only the member `user_name` and is in no file name.

1. **Spec structure.** One `spec/SPEC.md`, with the normative part
   `spec/parts/parquet-descriptor.md` and the informative `spec/legacy-annex.md`. The IDs of v2 start
   at SFF-700 and SFT-700 and are numbered in file order. The blocks of 50 IDs for each section are
   dropped: only SFF-681 to SFF-999 are free. The withdrawn v0 and v1 IDs are in section 0.
2. **Version fields.** Each file has `format_version` (the text `major.minor`), `format_prerelease`
   (an integer) and `writer`.
3. **`<rec>`.** 1 to 128 bytes of UTF-8, with no control character, no `.`, none of
   `/ \ : * ? " < > |`, no space at an end, and no Windows device name.
4. **Labels and keys.** `camera_label` is the first 6 hexadecimal characters of `camera_key`, or 7 or
   8 when two cameras collide, or `cam<N>` when the key is 0. `camera_key` is the first 8 bytes of the
   SHA-256 of the identity string: the serial number when there is one, else the port path, with the
   vendor and product IDs.
5. **CSV dialect.** A kind line `# skellyspecs=video_timing` or `audio_timing`, then
   `# key=value` header lines, one column line, the rows, then footer lines (`# fit`, `# fit_segment`,
   `# repair`, `# end`). The row CRC covers the bytes before the comma that precedes it. An empty
   field is absent. No legacy columns (`recording_frame_number`,
   `timestamp.from_recording_start.sec`): the reader goes into freemocap.
6. **Video sidecar.** Columns `frame`, `source_frame_number`, `arrival_ns`, `sample_ns`, `flags`,
   `byte_offset`, `byte_size`, `crc32`. Flag bits `gap`, `filled`, `encode_skip`; the flag replaces
   the encoder-skip log message. The byte offsets are live (provisional until desk test DT5). A
   finished sidecar has one row for each block of its MKV.
7. **Audio sidecar.** The tested layout: `block`, `first_sample`, `n_samples`, `host_ns`, `adc_ns`,
   `flags`, `crc32`. Flag bits `overflow` and `silence`. `file_sample_offset` is 0.
8. **Fit lines.** The video fit is in the footer, with the rules of ADR-6RSB item 9: segments by
   position, `t0_ns` and `period_ps`, evaluated by the source frame numbers. The audio fit uses
   segments by row, `n0`, `t0_ns` and an integer `period_fs`. A reader without a fit fits the rows
   (`adc_ns`, else `host_ns`).
9. **Clock names.** `windows_qpc`, `linux_monotonic`, `macos_uptime_raw` and `synthetic`.
10. **Camera file.** `DefaultDuration` is the frame period. A camera that sends raw frames is encoded
    to JPEG. H.264 capture is refused.
11. **Audio file.** The box layout of SPEC.md section 9. A clean close writes the last fragment and an
    `mfra`.
12. **Repair.** The line `# repair cut_bytes=<n> repair_writer=<writer>`. The repair of a camera file
    is provisional until desk test DT-R1. freemocap holds `.processing.lock` for each folder file.
13. **Journal.** The magic `SKRJ`; record types 1 (header), 2 (data), 3 (event) and 4 (end); float32
    values with NaN for missing; `frame_number` is the take frame number, as `i32` (the user changed
    it from `i64`). Each journal channel declares the `dtype` `float32`, and a reader refuses another
    `dtype`. A journal holds no time as a data value: the fold takes each time of the realtime run
    from the timing sidecars. Before the delete, a check compares the value count and a SHA-256 of
    the folded values.
14. **skellysync.** A skellysync folder has device pairs and a manifest only, with the `synthetic`
    clock, and its audio in a separate file (spec v0 revival, decision 6).

## Reason

- Each item is a detail that the spec needs and that no decision fixes. The tests of the research
  support items 5 to 8 and 11.
- Item 1: 319 free IDs are not enough for 23 sections of 50.

## Evidence

skellycam `dom/research` (local, not committed):
- `research/skellycam_recording/recording_upgrade/results/audio_single_file/FINDINGS.md` §3 (the audio
  CSV layout, 160 kills);
- `research/skellycam_recording/docs/camera_info_placement_20261115.md` §2 (the CSV header sketch);
- `research/skellycam_recording/docs/realtime_tracking_storage_20261115.md` §3 (the journal framing).

## Alternatives rejected

- Keep the legacy CSV columns: no reader outside freemocap needs them.
- A float rate in the audio fit: readers would get different times.

_Edited 2026-11-23 (commit to main): link repair._

_Edited 2026-11-23 (commit to main): rename._
