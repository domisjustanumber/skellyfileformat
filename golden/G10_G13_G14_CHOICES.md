# Choices made for G10, G13 and G14 that the spec does not give

**Status: proposed. The user did not review this list.** An agent made each choice.

The folders are G13 (a realtime take after the fold), G14 (a calibration and its copies) and G10
(the version vectors) of [SPEC.md Appendix A](../spec/SPEC.md#appendix-a-golden-folders). The scripts
are `tools/goldgen/g13.py`, `tools/goldgen/g14.py` and `tools/goldgen/g10.py`. The cross-checks are in
`tools/tests/test_g10_g13_g14.py`. The conventions of [G01_CHOICES.md](G01_CHOICES.md), of
[G03_CHOICES.md](G03_CHOICES.md) and of [CAPTURE_VECTORS_CHOICES.md](CAPTURE_VECTORS_CHOICES.md)
apply. This list does not repeat them. Each item gives the gap, the choice and, where useful, the
alternative. Section 4 lists the spec gaps that the user must decide.

## 1. G13: the case `take`

### What the take holds

- Two cameras of 12 frames each, with the lattices of G1 and no gap. No audio.
- `recording_manifest.json`, `g13_synthetic_take_info.json` and `g13_synthetic_take_recording_info.json`.
- `g13_synthetic_take_realtime_journal.bin`: 6,167 bytes. A header record, one event record, 19
  good data records, 1 data record with a wrong CRC, a hole of 4,096 zero bytes and a torn tail of
  20 bytes. It has no end record.
- `g13_synthetic_take_data.parquet`: one run, run 0, with the origin `realtime`. It holds the
  `TIMESTAMPS` rows of the 2 cameras and of the group, and one `OVERLAY_2D` channel for each camera.
- `take.truth.json`: the offsets of the good records, of the rejected record, of the hole and of the
  torn tail, and the count and the SHA-256 digest of the check of SFF-845.

### The expected reader result

| Member | Value | Requirement |
|---|---|---|
| `takes[].state` | `complete`: 2 camera files for `group_size` 2, `audio_count` 0 | SFF-869 |
| `takes[].warnings` | `full`: `["realtime_run"]`. `player`: `[]` | SFF-835, SFF-892 |
| `folder_files` | 4 items: the Parquet, the capture info JSON, the journal, the processing info JSON | SFF-885, SFF-890 |
| journal item, `full` | `damaged`, `crc_mismatch`, `records` 21, `rejected_records` 1, `torn_bytes` 20, `["prerelease"]` | SFF-843, SFF-886, SFF-891 |
| journal item, `player` | `not_checked`, reason null, `[]`, the three integers null | SFF-885, SFF-892 |
| `links`: `calibration` | `not_checked` in the two scopes: no TOML and no manifest calibration | SFF-872 |
| `links`: `hashes` | `full`: `ok` from its Parquet part only. `player`: `not_checked` | SFF-872, SFF-892 |
| other `links` | as in G3 | SFF-872 |

### Choices

1. Appendix A gives no `<rec>` and no `take_uuid`. Choice: `g13_synthetic_take` and
   `00000000000040008000000000000013`, with the other take keys of G1.
2. Appendix A lists "2 camera files, their timing sidecars, a manifest and both info JSONs". The row
   does not name sections 9 and 10. Choice: no audio. `audio_count` is 0, and `audio` is null in
   the manifest, in its summary and in the capture info JSON. Alternative: the audio of G1.
3. "Small" has no number. Choice: 12 frames for each camera. The cameras are the cameras of
   `capture_cases.camera`: camera 0 has a serial and a driver time in each row.
4. The row does not name section 15. Choice: the take has no calibration TOML. So the realtime
   pipeline makes only raw 2D, and the journal holds only `OVERLAY_2D` (SFF-842 lists more result
   kinds). `camera_geometry` is `{}`, and `calibration_camera` of each image reference is null
   (item 46).
5. The tracker is free. Choice: the source `keypoint_model:synthetic_pair` with the definition
   `{}`, the model `pair` of G3, and the names `body.p` and `body.q`.
6. The spec does not say if the manifest lists the journal. Choice: a `files` item with the role
   `realtime_journal`, the owner `freemocap` and `sha256` null (SFF-723, SFF-725). Alternative: no
   item. The journal is then an item of `folder_files` with the role null, because it has a fixed
   name of SFF-731 (SFF-885).
7. The order of the records is free. Choice: the header, one event, then for each frame the data
   record of channel 0 and of channel 1. The pipeline skipped channel 1 on frame 4 and both channels
   on frame 9. The data record of channel 0 on frame 6 has a CRC with its bit 0 changed. The hole
   follows the records of frame 8. The torn tail is the first 20 bytes of the record of channel 1
   on frame 11. The writer wrote no end record, so `clean_close` is false.
8. The take state is the state of SFF-793 and SFF-845: skellycam finished the take, freemocap
   stopped while it wrote the journal, the user agreed to the fold of the left-over journal, and the
   fold is done. The verified delete did not occur.
9. SFF-700 says that a JSON record of the journal has LF line ends, and gives no white space rule.
   Choice: compact JSON (no space, no line end), with the members in the order of the table of
   section 17. In the header, each channel has `channel_index` first, then the members of `Channel`
   in the order of the part.
10. The spec gives no parameter names for an event. Choice: one event with `time_ns` 150000000,
    `stage` `observations`, `parameter` `min_visibility` and `value` 0.5.
11. The values are free. Choice: a number of quarters of a pixel for `x` and `y`, and 1 or 0.875 for
    `visibility`, so each float32 is exact. `body.q` of channel 0 on frame 2 was not detected: `x`
    and `y` are NaN (null in the Parquet), and `visibility` is 0 (SFF-831, SFF-841).
12. `processed_ns` is free. Choice: m + 20 ms + 1.3 ms × frame + 0.25 ms × `channel_index`, where m
    is the group time of SFF-828. So `p50` is 26.5 ms and `p99` is 34.3 ms (19 latencies).
13. The fold writes the `TIMESTAMPS` rows from the sidecars (SFF-844, SFF-828). Choice: the run has
    the 2 capture `TIMESTAMPS` channels and the group `TIMESTAMPS` channel, as in G3, and the stage
    provenances `timing` and `observations`. Each has `origin` `realtime` and a `coverage` object
    (SFF-834: "in the stage provenance of each sensor group"). Item 44 gives the coverage of
    `timing`.
14. A frame of a channel with no good data record is a skipped frame. Its `x`, `y` and `visibility`
    are null (SFF-834, row rule 7). The frame of the rejected record is such a frame.
15. The provenance values are free. Choice: the values of G3, with `attempt_id`
    `goldgen-synthetic-attempt` and `recorded_at` `2000-01-01T00:01:00Z` (`timing`) and
    `2000-01-01T00:01:01Z` (`observations`). The manifest summary has one run: `origin` `realtime`
    and the later text.
16. SFF-891 says that each file of the take except the manifest has the warning `prerelease`.
    Choice: the journal item has it, also in the state `damaged`.
17. `<case>.truth.json` has no rule for a journal. Choice: the member `journal` with `name`,
    `good_offsets`, `rejected_offsets`, `hole` ([offset, size]), `torn_tail` (the offset of its
    `magic`), `check_count` and `check_digest` (SFF-845). SFT-757 and SFT-758 need these facts.

## 2. G14: the cases `calibration_take` and `mocap_take`, and `library/`

### What the folder holds

- `calibration_take/`: `g14_calibration_take`, `take_uuid` `00000000000040008000000000001401`,
  `purpose` `calibration`. Two cameras of 10 frames, no audio. It holds its TOML, the processing
  info JSON and a Parquet with one posthoc run: 3 `TIMESTAMPS` channels and 2 ChArUco
  `OVERLAY_2D` channels.
- `mocap_take/`: `g14_mocap_take`, `take_uuid` `00000000000040008000000000001402`, `purpose`
  `motion_capture`. The same two cameras, 10 frames, no audio. It holds the capture files and a
  byte-identical copy of the TOML. It has no Parquet and no processing info JSON.
- `library/`: `g14_calibration_take_camera_calibration.toml` and
  `last_successful_camera_calibration.toml`, with the bytes of the TOML. The folder has no result
  file: it is not a case.

### Choices

18. The `calibration_uuid` is `00000000000040008000000000001403`. `source_take_uuid` is the
    `take_uuid` of the calibration take. The other TOML values are those of G3
    ([G03_CHOICES.md](G03_CHOICES.md) items 6 to 9), with `n_observations_used` 144.
19. SFF-811 says that "a take that uses a calibration" holds a copy, and SFF-813 names "the copy of
    the calibration take". Choice: the calibration take holds its TOML as
    `<rec>_camera_calibration.toml`, with the `calibration` member and the `calibration_camera`
    values of its manifest.
20. The motion-capture take holds only what the case needs: the capture files and the TOML copy.
    Its manifest gets `calibration`, `calibration_camera` and `summary.calibration`. Alternative: a
    Parquet and a processing info JSON, as in G3.
21. Appendix A says "a library TOML". SFF-812 and SFT-739 also name
    `last_successful_camera_calibration.toml`. Choice: both files.
22. The part gives the source definition of `charuco_detector` as "the board definition of SPEC.md
    section 15". Choice: the JSON object of the TOML table `[metadata.board]`, with its 5 keys in the
    order of section 15.
23. SFF-836 does not list the corner IDs of a board. Choice: the OpenCV inner corners of the board:
    (5 − 1) × (3 − 1) = 8 names, `corner_0` to `corner_7`.
24. Camera 1 does not see the board on frames 3 and 4. Choice: each corner of these frames has `x`
    and `y` null and `visibility` 0, as a point that a tracker did not detect (SFF-831). Alternative:
    all three null.
25. The run has `models` `{}` and `camera_geometry` `{}`: it has no keypoint tracker and stores no
    geometry (item 45). It has the stage provenances `timing` and `observations`, with `origin`
    `posthoc` and `coverage` null (SFF-834).
26. The expected result of `calibration_take` is the result rule of G3: each link check is `ok` in
    `full`. The result of `mocap_take` has `dimensions` `not_checked` in the two scopes, because no
    Parquet exists (SFF-872). Each other check of `full` is `ok`.

## 3. G10: the version vectors

27. `higher_minor` is the take of G3 (`g01_synthetic_take`), made again with `2.1` in each version
    field: the 3 sidecars, the manifest, both info JSONs, the TOML and the Parquet descriptor.
28. The value of each unknown field is free. Choice: `1`. The sidecars have `# x_future=1` after
    the last header key, and `x_future` before `crc32` in the column line, with the value `1` and a
    new CRC in each row. The manifest and the two info JSONs have `"x_future": 1` as their last
    member. The TOML has `x_future = 1` as the last key of `[metadata]` and of the table of camera 0.
29. Appendix A does not say which row has the flag bit 7. Choice: row 10 of camera 0, with the
    flags 128.
30. The changed files have new SHA-256 values. Choice: the manifest gets the new `sha256` of each
    info JSON and of the TOML (SFF-723). `parquet_sha256` is correct. So only the version vector
    differs from G3.
31. The descriptor gets no unknown member: Appendix A does not ask for one. The part says that a
    reader of a known `minor` refuses a closed model with an unknown member. So an unknown member of
    a closed model of a higher `minor` is a separate case (item 50).
32. The expected results of `higher_minor` have the bytes of the results of G3. The reader ignores
    each unknown field (SFF-709). Each file keeps `format_prerelease` 1 and the warning
    `prerelease`.
33. `unknown_major_sidecar` is the take `take` of G1 with `# format_version=3.0` in the sidecar of
    camera 1, as G11 changes camera 1. Its `files` item is `unsupported_version`, with `reason`,
    `rows`, `torn_bytes`, `fit` and `records` null, and the header values of `camera_key` and
    `camera_label`. Its warnings are `["prerelease"]` (CAPTURE_VECTORS_CHOICES.md item 9). The pair
    counts as a camera file, so the take is `complete` (item 10 of that file). The parts of the link
    checks that need the refused sidecar are not evaluated (item 11 of that file). So `frames` is
    `not_checked` in the two scopes: one camera file is `finished`.
34. `unknown_major_folder_file` is the take of G1 with `"format_version": "3.0"` in the capture info
    JSON. The manifest has the new `sha256` of that file. Its `folder_files` item is
    `unsupported_version`, `reason` null, `["prerelease"]`, in the two scopes. `take_uuid`,
    `camera_key` and `rotation` stay `ok` from their other parts.
35. `higher_minor_journal` is the take of G13. The journal header has `2.1`. The record of the type
    200 is the third record, after the event record. Its payload is the 8 ASCII bytes `x_future`.
    Each other file has `2.0`. The fold ignores the record, so the Parquet has the bytes of the
    Parquet of G13. The journal item has `records` 22. Each other member of the result is the member
    of G13.
36. `prerelease_0` is the take of G1 with `format_prerelease` 0 in the manifest, the 3 sidecars and
    the capture info JSON. The writer string does not change. The results are the results of G1
    with no `prerelease`.

## 4. Spec gaps, contradictions and ambiguities

The user must decide each item.

40. **`unsupported_version` and the link parts** (SFF-872). The rule says that a reader does not
    evaluate a part when a file is "absent, is `invalid`, or is a file that the scope does not
    read". It does not name `unsupported_version`. G10 treats an `unsupported_version` file as an
    `invalid` file.
41. **The header of an unknown `major`** (SFF-708, SFF-885, SFF-889). The reader puts a file in the
    `files` of its take when it can read its `take_uuid`, and it gives `camera_key` and
    `camera_label` "when their form is correct". A reader that does not know the `major` cannot know
    the form. G10 reads the header lines as in version 2.0. Alternative: the file is in
    `other_files`, and the take is `incomplete`.
42. **`reason` of `unsupported_version`** (SFF-886, SFF-887). No reason code applies. G10 gives
    null. `test_golden_files.py` asks for null for each state other than `invalid` and `damaged`.
43. **`prerelease` on a refused file** (SFF-891, Appendix A). A reader that does not know the
    `major` cannot read `format_prerelease`. G10 follows Appendix A ("each file of each case")
    and gives the warning. Alternative: `[]`.
44. **The coverage of the stage `timing`** (SFF-834, SFF-841). `frames_processed` counts the frames
    with data records of a channel of the stage. A journal has no `TIMESTAMPS` channel. So the
    literal rule gives the stage `timing` of a realtime run `frames_processed` 0, `skips`
    `{"no_record": 12}` and the latencies null. G13 follows the literal rule. Alternative: the run
    has no provenance for `timing`, or `coverage` null for it.
45. **A run with no stored geometry** (SFF-837). The rule compares the geometry of a run with the
    TOML. It does not say what a run with `camera_geometry` `{}` gives. G14 gives no
    `calibration_mismatch`.
46. **`calibration_camera` with no TOML** (parts/parquet-descriptor.md, "Reference frames"). The
    member is "the name of the camera table of the TOML", with no null rule. The manifest member of
    the same name can be null. G13 writes null.
47. **"Data records" of the coverage** (SFF-834). The rule does not say "good". G13 counts only good
    records: a rejected record is not a result.
48. **The checks of SFF-845 with two records of one frame.** G13 has no such pair. So the golden
    files do not test "only the last in file order counts". A test can make the pair at run time.
49. **SFT-703 and G10.** SFT-703 has G10 as input and says that each file has `format_version` 2.0.
    That sentence is for the output of a writer. G10 holds files with 2.1 and 3.0.
50. **Unknown members in a closed model** (parts/parquet-descriptor.md, "Conventions"). A reader of
    a known `minor` refuses a closed model with an unknown member, and a reader of an older `minor`
    ignores it. No golden folder has this vector.

## 5. Limits of this work

51. **Shared files.** `golden/README.md` still says "Only G1 exists". `folder_common.add_processing`
    always writes a TOML, so `g13.py` updates the manifest itself. The shared writers read the
    version fields from globals of `common.py`. `g10.py` changes the globals for one block. A
    parameter of the shared writers is the better fix. This work does not change these files.
52. **Not shown by a file.** The ZSTD level 3 of SFF-818 is not in the Parquet. pyarrow writes the
    same extra metadata as for G3 ([G03_CHOICES.md](G03_CHOICES.md) item 32).
