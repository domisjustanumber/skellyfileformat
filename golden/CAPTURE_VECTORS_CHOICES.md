# Choices made for G2, G4, G5, G6, G11 and G12 that the spec does not give

**Accepted by the user on 2026-11-16 as conventions of the golden folders**
([ADR-2MQE](../decisions/entries/2MQE-tests-prerelease-serial-and-exports.md) item 7). An item is a
rule of the format only where the spec states it. A decision of the same day replaced items 2, 3
and 4 ([ADR-B6WH](../decisions/entries/B6WH-repair-equal-pair-cut-and-no-normal-end.md)). Each of
these items gives its decision. Item 6 is open.

This file is for the six golden folders that `tools/goldgen/capture_cases.py` makes: G02, G04, G05,
G06, G11 and G12. Most choices apply to more than one folder, so the folders have one file.
The conventions of [G01_CHOICES.md](G01_CHOICES.md) apply and are not repeated here: the writer
string, the take keys, the frame size of 64 × 48 pixels, the JPEG quality, the fit `goldgen-truth`,
the JSON white space, the synthetic devices, `SHA256SUMS` and `<case>.truth.json`.
`tools/tests/test_g_capture.py` checks the files against the spec text.

G05 and G06 are **provisional**
([ADR-G21H](../decisions/entries/G21H-gate-2-tests-location-and-interfaces.md) item 6). They wait for
the desk tests DT-R1 and DT5.

## 1. Contradictions and points that the user decided

1. **`reason` of a `damaged` file.** SFF-746 and SFT-716 say that a row with a wrong CRC makes the
   file `damaged` with the reason `crc_mismatch`. Choice: the result of camera 2 of G05 has `state`
   `damaged` and `reason` `crc_mismatch`, as the spec says. `tools/tests/test_golden_files.py`
   accepts a reason for the states `invalid` and `damaged`.
2. **A repair makes each camera pair equal.** Decision
   ([ADR-B6WH](../decisions/entries/B6WH-repair-equal-pair-cut-and-no-normal-end.md) items 1 and
   4): the repair cuts a sidecar at its first bad row (a row that is not complete or that has a
   wrong CRC). It cuts the sidecar and the camera file back to the frames that have a complete row
   and a complete block. So after the repair, rows = blocks. In G06, camera 0 keeps 17 frames (22
   rows, 17 blocks), camera 1 keeps 15 (21 rows and a torn row, 15 blocks) and camera 2 keeps 9 (9
   good rows, 20 blocks). Before this decision, the generator cut each file on its own, and the
   pairs of G06 `repaired` had 22/17, 21/15 and 9/20 rows and blocks. That did not agree with
   SFF-759. The audio pair has no such rule: its sidecar keeps its 21 rows (item 5).
3. **The repaired camera file gets no normal end.** Decision (ADR-B6WH item 3): the repair writes
   no Cues and does not write the SeekHead again, because these writes change bytes before the cut.
   The repaired camera file is the crashed file, cut after the block of its last kept row. Nothing
   is appended. When the cut is in a Cluster, the size of that Cluster still goes past the end of
   the file. SFF-797 is provisional (DT-R1).
4. **The repaired audio file gets no `mfra` box.** Decision (ADR-B6WH item 3): the repaired audio
   file is the crashed file, cut after its last complete fragment. A reader accepts the file.
5. **A sidecar with more samples than its audio file.** The muxer holds the open fragment in memory,
   so the crashed audio file holds less audio than the 21 rows of its sidecar (100,800 samples).
   SFF-795 keeps each row. So the repaired sidecar has `samples=100800`, and the repaired file holds
   one fragment. SFF-785 gives the usable length. The manifest summary has `duration_s` 2.1, from
   the `# end` line (SFF-728).
6. **`interrupted_repair` needs a repair that works in steps across the files. OPEN.** Appendix A
   says that each sidecar of the case is `unfinished`. A repair that finishes one pair before it
   starts the next cannot leave this state: the pairs before the stop are `repaired`, and camera 2
   is still `damaged`. Choice: the repair cuts each media file and each sidecar (with the cuts of
   item 2), then writes the fit lines of each sidecar, then the `# repair` lines, then the `# end`
   lines, then the manifest. It stopped in the write of the `# repair` line of camera 2. On
   2026-11-16, the user decided the order "for each pair, cut the media file, then cut the sidecar,
   then append the fit lines and `# end`; the manifest is last". That order does not agree with
   this case and with Appendix A. The user must decide which one changes
   ([open-work.md](../decisions/open-work.md)). Until then, G06 keeps this case.
7. **SFT-768 and the `gap` warning of G12.** SFT-768 names camera 0 as the only camera of G12 with
   the warning `gap`. A frame that the encoder lost makes a jump of the source frame number, and so
   the flag `gap` on the same row (SFF-756). Choice: the `encode_skip` row of camera 3 is row 0,
   where `gap` is always 0. So SFT-768 stays true. Alternative: an `encode_skip` row in the middle,
   with the flags 5, and a change of SFT-768.

## 2. Choices for the reader results (all folders)

8. **`records` of an `invalid` item** (SFF-885). The spec gives null for `rows`, `torn_bytes` and
   `fit`, and says nothing for `records`. Choice: null ("a member that does not apply is null").
   Alternative: `[]`.
9. **`warnings` of an `invalid` item** (SFF-891, Appendix A). Choice: `["prerelease"]`, because
   Appendix A says that each file of each case has the warning. It has no `gap`: it has no usable
   row. Alternative: `[]`.
10. **An `invalid` pair and the take** (SFF-869). SFF-865 takes only a sidecar with no media file out
    of the count of camera files. Choice: a pair with an `invalid` sidecar counts, so each take of
    G11 is `complete`, with no `incomplete_take`. Alternative: `incomplete`.
11. **An `invalid` sidecar and the take checks** (SFF-729, SFF-871, SFF-872). Choice: a reader takes
    only `take_uuid`, `group_position`, `camera_key` and `camera_label` from a sidecar that it
    refuses. So G11 has no `summary_stale` (cases `rate_0_1`, `rate_2_20_plus_1`, `rotation_45`,
    `bad_label`) and no `take_fact_mismatch` (case `unknown_clock`: `clock` is a take key). The
    parts of the link checks that need that sidecar are not evaluated (SFF-872). `take_uuid`,
    `camera_key` and `rotation` are `ok` from their other parts. The user decided the same rule on
    2026-11-16: a refused sidecar causes no `summary_stale` and no `take_fact_mismatch`
    ([ADR-XR63](../decisions/entries/XR63-reader-rules-of-the-golden-review.md)).
12. **"Usable rows" for the file warnings** (SFF-887). Choice: the rows that SFF-746 lets the reader
    use, also a row whose block is not complete. In each folder here, the flagged rows have complete
    blocks, so the two readings give the same result.
13. **`player_ns` of a `damaged` file** (SFF-781). The file has no `# end` line, so it has no fit
    that the reader uses: `fit` false, `missing_fit` and the arrival time, as for `unfinished`.
14. **`torn_bytes` needs a walk** (SFF-791). "After its last complete block" counts blocks, not rows.
    Camera 2 of G05 has 20 complete blocks and 9 usable rows. Its media part is 0. A reader that
    finds blocks only from the CSV offsets gets another number.
15. **Take state of a crashed take** (SFF-869). Each crashed, damaged or repaired pair counts as a
    file. So each take of G05 and G06 is `complete` with `warnings` `[]`.

## 3. G02

16. Appendix A says "G1 with stereo audio". Choice: the same `take_uuid`, `<rec>`, cameras and audio
    rows as G1 (convention 19 of G01_CHOICES.md). Only four files differ from `G01/take`: the audio
    file, one line of the audio sidecar (`channels=2`), `device_channels` of the capture info JSON,
    and in the manifest the `sha256` of that JSON and `summary.audio.channels`. Alternative: a new
    `take_uuid`.
17. The spec gives no content for the two channels. Choice: the left channel is the audio of G1. The
    right channel is the same signal at half the level (peak 12,000). The bitrate setting is
    256 kbit/s (SFF-762). `take.truth.json` has the truth of G1 and `audio.peaks`.
18. The reader result holds no fact of the channels, so the two results of G02 have the bytes of the
    results of `G01/take`.

## 4. G04

19. Appendix A does not say if G4 has audio. Choice: no audio. `audio_count` is 0, and `audio` is
    null in the manifest, in its summary and in the capture info JSON. Alternative: the audio of G1.
20. Stored size. Choice: each camera stores 64 × 48 pixels, the orientation of the sensor (SFF-735).
    The upright picture of the cameras with 90 and 270 is 48 × 64 pixels. Alternative: one upright
    picture of 64 × 48 for each camera, and stored frames of 48 × 64.
21. Colours. The upright picture has a field of (60, 60, 60) and a corner of 16 × 16 pixels in each
    corner: top left (220, 30, 30), top right (30, 200, 30), bottom right (30, 30, 220), bottom left
    (220, 220, 30). A light square moves 1 pixel to the right in each frame. A stored frame is the
    upright picture after a turn of `display_rotation` degrees counter-clockwise. The test accepts a
    difference of 16 in each channel at the centre of a corner.
22. Six frames for each camera, `nominal_rate` 30/1, source frame numbers from 1000, 2000, 3000 and
    4000. Only camera 0 has `sample_ns`. `take_uuid` ends in `0004`, and `<rec>` is
    `g04_synthetic_take`.

## 5. G05

23. **The stand-in camera file (provisional).** The generator muxes 26 JPEG frames with PyAV into a
    seekable sink in memory, with the muxer options `fflags=+bitexact` and `flush_packets=1`. It
    copies the bytes of the sink before `close()`. The copy holds: the EBML header; a Segment with
    an unknown size (`01 FF FF FF FF FF FF FF`); a Void of 152 bytes in the place of the SeekHead;
    Info, with a Void in the place of its CRC-32 and a Void in the place of `Duration`; Tracks;
    Tags; and one Cluster for each 5 frames, each with a known size and a CRC-32 element. It holds
    no SeekHead, no Duration, no Cues and no frame of the Cluster that the muxer still holds in
    memory. Each Cluster and each block has the bytes and the offset that it has in the finished
    file. Each camera file of G05 is a prefix of that copy:
    - camera 0: the copy cut 100 bytes into the JPEG of block 17. 17 complete blocks, 107 bytes
      after block 16;
    - camera 1: the copy cut 100 bytes into the JPEG of block 15. 15 complete blocks, 123 bytes
      after block 14 (the start of a Cluster and part of a block);
    - camera 2: the first four Clusters. 20 complete blocks, no byte after block 19.

    A real writer must flush each block (SFF-787). How it does that with this muxer is not decided
    (DT5). So the real file can differ.
24. The scenario is a loss of power, about 2.1 s after the take start. Each live file is a prefix of
    the bytes that its writer gave to the operating system. Rows for frames 20 and 21 exist, and
    their blocks do not: the `byte_offset` of these rows is the place that the block gets in a
    longer file (SFF-757, provisional).
25. `nominal_rate` is 10/1, so that 2.1 s need only 22 frames. Two audio fragments of 1 s need that
    time.
26. Sidecars. Camera 0: 22 rows and a clean end. One source frame is lost before position 5, so
    that the repair of G06 gives `camera_gap`. Camera 1: 21 rows, then the first 37 bytes of row 21
    (the cut is in the CRC field). Camera 2: 22 complete rows. Row 9 has a wrong CRC: its CRC field
    is the correct CRC with the lowest bit changed. Audio: 21 rows of 4,800 samples and a clean end.
    No sidecar has a footer line.
27. Audio. The audio is the first 2.1 s of the audio of G1. The copy before `close()` holds `ftyp`,
    `moov` and two complete fragments. `audio_clean_kill` is that copy. `audio_torn_fragment` is
    that copy, cut in the middle of the `mdat` of the second fragment: its `moof` is complete. The
    two cases differ only in this file.
28. The old manifest is the manifest of the take start: `state` `recording`, `warnings` `[]`, and
    null in `duration_s`, `stored_px`, `gaps` and `filled` (SFF-724, SFF-728). The capture info JSON
    is present (SFF-801). `recording_manifest.json.tmp` holds the first half of the bytes of the old
    manifest: a write that the crash stopped. It is not valid JSON. Alternative: a complete new
    manifest. The take has no `.processing.lock` file.
29. `take.truth.json` of each case holds, for each file, `complete_blocks` or `complete_fragments`,
    `sidecar_torn_bytes` and `media_torn_bytes`, and for audio the fit of the reader (`reader_fit`,
    SFF-784, for SFT-729).

## 6. G06

30. G06 has the `take_uuid` and the `<rec>` of G05 (`g05_synthetic_take`). It is the same take.
31. The fit of the repair (SFF-795 says "computes the fit from the rows"). Choice: the line that made
    the rows, with `fitter=goldgen-truth`, one segment from row 0 to the last kept row. A real
    repair computes its fit from the rows.
32. `repair_writer` and the manifest `writer` are `skellyfileformat-goldgen 1.0.0`. So `writer` of
    the manifest does not change in the repair, and the test sees a change only in `state`,
    `warnings` and `summary`.
33. The repair writes the manifest by SFF-786, through `recording_manifest.json.tmp`. So the case
    `repaired` has no `.tmp` file and no `stray_tmp`. `interrupted_repair` keeps the old manifest
    and the old `.tmp` file.
34. In `interrupted_repair`, the torn `# repair` line of camera 2 has 20 bytes. Cameras 0 and 1 have
    a complete `# repair` line. The audio sidecar has only the fit lines.

## 7. G11

35. Each case changes the sidecar of camera 1. Camera 0 stays valid, so the rule "the camera with
    the lowest `group_position`" (SFF-871) never needs a refused file.
36. The three row vectors change row 1 and give the row a new, correct CRC. So the row has one
    fault. `leading_zero`: `source_frame_number` `0501`. `plus_sign`: `arrival_ns` `+70571479`.
    `row_integer_2_53`: `source_frame_number` `9007199254740992`.
37. The header vectors: `nominal_rate=0/1`; `nominal_rate=1048577/1`; `display_rotation=45`;
    `camera_label=nothex` (not hexadecimal, not the start of the key; the file names do not
    change); no `nominal_rate` line (`missing_key`); `clock=fake_clock`.
38. The folder has 2.3 MB, because each of the nine cases is a whole copy of `G01/take`.

## 8. G12

39. Twelve frames for each camera and four audio blocks of 4,800 samples of silence. `take_uuid`
    ends in `0012`.
40. Camera 0: segments for positions 0 to 5 (`t0_ns` 33483200, `period_ps` 33333400000) and 6 to 11
    (`t0_ns` 400000000, `period_ps` 33366700000). Source frame 1003 is lost, so row 3 has `gap`. In
    the second segment, d counts from the source frame number of position 6.
41. Camera 1: `period_ps` 33333333333. Camera 2: the footer is only the `# end` line. Audio:
    `period_fs` 20833333333.
42. Camera 3: "two rows with equal fitted times" has no cause in the spec. Choice: row 7 has the
    source frame number of row 6 and the flag `repeat` (8), so d is equal. Alternative: a second
    segment that starts at the last fitted time of the first. The JPEG of row 7 is not a copy of the
    JPEG of row 6.
45. **The Parquet of SFT-748** ([ADR-2MQE](../decisions/entries/2MQE-tests-prerelease-serial-and-exports.md)
    item 5). Choice: `G12/equal_fitted_times.parquet`, beside the case, so that the reader result of
    the take does not change. It holds one channel: `TIMESTAMPS` `capture` of camera 3, in the
    sensor group of that camera alone, with the 12 strict player times of SFF-782 in seconds
    (SFF-828). Its descriptor holds only `runs.0.sensor_groups`, because the vector needs only the
    times. Alternative: a full descriptor, or the Parquet in the take, which changes the result.

## 9. What the pinned tools cannot do exactly

43. PyAV 19.0.2 has no call that flushes the open Cluster. So a file before `close()` holds only
    whole Clusters, and the cuts of item 23 make the torn blocks.
44. The MP4 muxer gives a fragment to its output only when the fragment is complete (SFF-764). So a
    torn fragment is also made by a cut.

## 10. The requirement of each value

`links` are the same in each case, except `frames`: `take_uuid`, `camera_key`, `rotation` and
`files` are `ok`; `dimensions`, `hashes` and `calibration` are `not_checked` (no Parquet and no
TOML, SFF-872). Each take is `complete` (SFF-869), with `manifest` `present` (SFF-867), `warnings`
`[]` and one `folder_files` item (the capture info JSON, `["prerelease"]`, SFF-891).

- **G02 `take`**: each value as in `G01/take` (golden/README.md).
- **G04 `take`**: four files `finished` with `fit` true (SFF-747) and 6 rows; `player_ns` is the
  fitted time (SFF-777, SFF-781); `frames` is `ok` for `full` (four finished files with 6 rows,
  SFF-872) and `not_checked` for `player` (SFF-892).
- **G05, both cases**: `folder_warnings` `["stray_tmp"]` (SFF-790). Cameras 0 and 1 and the audio
  are `unfinished`: no `# end` line (SFF-747). Camera 2 is `damaged` with `crc_mismatch`, and
  `rows` is 9: the read stops at row 9 (SFF-746). `rows` 22, 21 and 21 count the complete rows
  (SFF-746, SFF-885). `records` has 17, 15 and 9 frames: a row and a complete block (SFF-740).
  `torn_bytes` (SFF-791): camera 0, 0 + 107; camera 1, 37 + 123 = 160; camera 2, 0 + 0 (the bad
  row and the rows after it are complete lines); audio, 0 in `audio_clean_kill` and 0 + 5,870 in
  `audio_torn_fragment` (SFF-792). `fit` false, `missing_fit` and `player_ns` = `arrival_ns` for
  each camera (SFF-781). Camera 0 has `gap` (SFF-887). For audio, `fit` false and `missing_fit`,
  and `fitted_ns` is from the fit of the reader: `t0_ns` 12344678, `period_fs` 20833356458
  (SFF-784, SFF-779). `frames` is `not_checked` in the two scopes: no file is `finished` (SFF-872).
- **G06 `repaired`**: each file `repaired`: a `# repair` line and a last `# end` line (SFF-795).
  `torn_bytes` 0 (SFF-791). `fit` true and `player_ns` from the fit lines (SFF-781, SFF-777).
  `rows` and `records` 17, 15, 9 and 21: each camera pair has equal rows and blocks (item 2).
  Camera 0 has `gap`. No `folder_warnings` (item 33). `frames` is `not_checked`: a `repaired` file
  is not in the row-count part (SFF-872).
- **G06 `interrupted_repair`**: each file `unfinished`, `fit` false, `missing_fit`, also with fit
  lines (SFF-747, SFF-798). `rows` and `records` 17, 15, 9 and 21, from the cuts of item 2.
  `player_ns` = `arrival_ns`; audio `fitted_ns` from the fit of the reader, as in G05.
  `torn_bytes`: 20 for camera 2, the torn footer line (SFF-746); 0 for each other file, because
  each media file is cut. `folder_warnings` `["stray_tmp"]`. The step order of this case is open
  (item 6).
- **G11, each case**: camera 1 is `invalid`, with `rows`, `torn_bytes`, `fit` and `records` null
  (SFF-885, item 8) and `["prerelease"]` (item 9). The reason: `leading_zero`, `plus_sign` and
  `row_integer_2_53`, `bad_metadata` (SFF-701); `rate_0_1` and `rate_2_20_plus_1`, `bad_rate`
  (SFF-750); `rotation_45`, `bad_rotation` (SFF-751); `bad_label`, `bad_label` (SFF-753), with
  `camera_label` null (SFF-885); `missing_key`, `missing_metadata` (SFF-748); `unknown_clock`,
  `bad_metadata` (SFF-772). Camera 0 and the audio are as in G1. `frames` is `not_checked` in the
  two scopes: only one camera file is `finished` (SFF-872). So the two results of a case have the
  same bytes.
- **G12 `take`**: each file `finished`, 12 rows (audio 4). Camera 0: `fit` true, `["gap",
  "prerelease"]`, `player_ns` from two segments (SFF-777). Camera 1: `fit` true, times rounded down
  (SFF-777). Camera 2: `fit` false, `missing_fit`, `player_ns` = `arrival_ns` (SFF-781, SFF-885).
  Camera 3: `["encode_skip","prerelease"]` (SFF-887); records 6 and 7 have the same `player_ns`,
  because `records` hold p and not the strict time (SFF-782). Audio: `fitted_ns` by SFF-779.
  `frames` is `ok` for `full` and `not_checked` for `player`. In `equal_fitted_times.parquet`, the
  times of rows 6 and 7 differ by 1 ns (item 45).
