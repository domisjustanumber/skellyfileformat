# Choices made for G3 that the spec does not give

**Accepted by the user on 2026-11-16 as conventions of the golden folders**
([ADR-2MQE](../decisions/entries/2MQE-tests-prerelease-serial-and-exports.md) item 7). An item is a
rule of the format only where the spec states it. Decisions of the same day replaced items 1, 3,
19, 23 and 28 ([ADR-2MQE](../decisions/entries/2MQE-tests-prerelease-serial-and-exports.md) items
3 and 4, [ADR-XR63](../decisions/entries/XR63-reader-rules-of-the-golden-review.md)). Each of these
items gives its decision.

G3 is the processed take of [SPEC.md Appendix A](../SPEC.md#appendix-a-golden-folders): the
take of G1 with the processing info JSON, a calibration TOML and a tracking Parquet. It has one
case, `take`. The scripts are `tools/goldgen/g03.py` (the input) and
`tools/goldgen/folder_common.py` (the shared code for the folder files). The cross-checks are in
`tools/tests/test_g03.py`.

G3 copies each convention of [G01_CHOICES.md](G01_CHOICES.md)
([ADR-94YQ](../decisions/entries/94YQ-golden-g1-review-decisions.md) item 5). This list does not
repeat them. Each item gives the gap, the choice and the alternative
([ADR-G21H](../decisions/entries/G21H-gate-2-tests-location-and-interfaces.md) item 5).
Items 31 to 36 are contradictions and limits of the pinned tools.

## What the take holds

- The media files, the timing sidecars and the capture info JSON of `recording-files/golden/G01/take`, with the
  same bytes. The only exception is the sidecar of camera 1: its header has `display_rotation=90`
  (item 1).
- `g01_synthetic_take_camera_calibration.toml`: two cameras, not aligned.
- `g01_synthetic_take_data.parquet`: one posthoc run, 11 channels, 7,830 rows, 90 frames.
- `g01_synthetic_take_recording_info.json`: the processing info JSON.
- `recording_manifest.json`: the manifest of G1 with the new files, the calibration and the summary.
- No file in `exports/` and no manifest item with the role `export`
  ([ADR-PVG8](../decisions/entries/PVG8-spec-v2-details-part-10.md) item 23).

## The expected reader result: the members that G1 does not have

Each other member has the value and the requirement of G1 ([README.md](README.md)).

| Member | Value in G3 | Requirement |
|---|---|---|
| `takes[].warnings` | `[]`: `parquet_sha256` is correct, `camera_geometry` agrees with the TOML, the run is posthoc, and the summary agrees with the sidecars | SFF-874, SFF-837, SFF-835, SFF-729 |
| `takes[].may_contain_private_data` | true, as for G1. The new files add no `privacy` field: the TOML is not aligned | SFF-881, SFF-883 |
| `folder_files` (the items) | 4 items: one for each `files` item of the manifest and one for `calibration.file` | SFF-885 |
| `folder_files` (the order) | The bytes of the path: the TOML, the Parquet, the capture info JSON, the processing info JSON | SFF-890 |
| `folder_files[].role` | `tracking`, `capture_info` and `processing_info` from the manifest. `calibration` for the TOML (item 28) | SFF-723, SFF-885 |
| `folder_files[].state`, `reason` | `full`: `present`, null. `player`: the TOML and the Parquet are `not_checked`, null | SFF-885, SFF-892 |
| `folder_files[].warnings` | `full`: `["prerelease"]` for each item. `player`: `[]` for the TOML and the Parquet | SFF-891, SFF-892 |
| `links`: `take_uuid` | `ok`. `full`: the manifest, 3 sidecars, 2 info JSONs and the Parquet descriptor. `player`: without the Parquet | SFF-872, SFF-892 |
| `links`: `camera_key` | `ok`. `full`: the manifest with the video sidecars, the capture info JSON, the TOML and the Parquet. `player`: only the first two parts | SFF-872, SFF-892 |
| `links`: `frames` | `full`: `ok`. Each Parquet `frame_number` is from 0 to 89, and the 2 camera files have 90 rows each. `player`: `not_checked` | SFF-872, SFF-827, SFF-892 |
| `links`: `dimensions` | `full`: `ok`. Each image reference has 64 × 48, the size of the stored JPEG. `player`: `not_checked` | SFF-872, SFF-829, SFF-892 |
| `links`: `rotation` | `ok`: the capture info JSON has no rotation, and the summary has 0 and 90, as the sidecars | SFF-872 |
| `links`: `files` | `ok`. `full`: each path of the manifest, and the 4 file names of the Parquet camera sources in `synchronized_videos/`. `player`: only the paths of the manifest | SFF-872, SFF-826, SFF-892 |
| `links`: `hashes` | `full`: `ok`. The manifest with the TOML, and `parquet_sha256` with the Parquet. `player`: `not_checked` | SFF-872, SFF-892 |
| `links`: `calibration` | `full`: `ok`. The `calibration_uuid` of the manifest is that of the TOML. `player`: `not_checked` | SFF-872, SFF-814, SFF-892 |

The `player` result differs from the `full` result only in the two `folder_files` items and in the
four link checks of the table.

## The choices

### The take and the manifest

1. Appendix A says "G1 plus" and gives no `<rec>` and no `take_uuid` for G3. Choice: the take of G1
   itself, with the `<rec>` `g01_synthetic_take` and the `take_uuid` of G1. So each media file,
   each sidecar and the capture info JSON has the name of `recording-files/golden/G01/take`. Decision
   ([ADR-2MQE](../decisions/entries/2MQE-tests-prerelease-serial-and-exports.md) item 3): camera 1
   has `display_rotation` 90, the input of SFT-749. So the sidecar of camera 1 has the header line
   `# display_rotation=90`, and the manifest summary has 90 for camera 1. A header line has no
   CRC, so no other byte of the sidecar changes. The capture info JSON holds no rotation (SFF-800),
   so it keeps the bytes of G1. The stored frames stay 64 × 48 pixels: the TOML `size`, the image
   reference of the Parquet and the 2D values are in stored-JPEG pixels (SFF-829), so the TOML and
   the Parquet do not change. Each other file has the bytes of G1, and the manifest has the other
   changes of this list.
2. SFF-725 says that freemocap sets `writer` of the manifest to its own writer string. Choice: the
   writer string of the golden folders in each new file and in the manifest (G01_CHOICES.md item
   3). `owner` of the two new `files` items is `freemocap`. Alternative: `freemocap 2.0.0`.
3. `<case>.truth.json` (G01_CHOICES.md item 26) has no rule for a processed take. Choice: the
   members of the file of G1. Decision
   ([ADR-2MQE](../decisions/entries/2MQE-tests-prerelease-serial-and-exports.md) item 4): the file
   also has the member `parquet`, with the SHA-256 of the values that the generator gave to the
   Parquet writer. [README.md](README.md) defines the digest. SFT-747 checks each Parquet reader
   against it.
4. SFF-728 says "the latest `recorded_at`" and gives no comparison rule. Choice: each stage has
   the form `YYYY-MM-DDTHH:MM:SSZ`, so the order of the texts is the order of the times. The four
   stages have 2000-01-01T00:01:00Z to 00:01:03Z, and the summary holds the last one.
   Alternative: a parse of each text as a date.

### The calibration TOML

5. Section 15 gives no ID for a golden calibration. Choice: `calibration_uuid`
   `00000000000040008000000000000301` and `source_take_uuid` `00000000000040008000000000000302`,
   with the bits of a UUID version 4 (G01_CHOICES.md item 2). The source take is in no golden
   folder. Alternative: no `source_take_uuid` ("absent when not known"), and then a null in the
   summary.
6. The solver results are free. Choice: `reprojection_error_px` 0.25, `initial_cost` 1.5,
   `final_cost` 0.25, `n_iterations` 4, `solver_time_seconds` 0.5, `n_observations_used` 180,
   `n_observations_rejected` 0, `aligned` false and an empty `transformation_history`. The board is
   the board of the example of section 15. The TOML type of each key (integer or float) is the type
   in that example.
7. The camera geometry is free. Choice: for each camera, fx = fy = 60.0, cx = 32.0, cy = 24.0 and
   the distortions [0.01, -0.02, 0.0, 0.0, 0.0]. Each rotation is [0.0, 0.0, 0.0]. Camera 1 has
   the translation [-500.0, 0.0, 0.0], so its `world_position` is [500.0, 0.0, 0.0]. Each value is
   exact, and the generator needs no matrix code. Alternative: a camera with a rotation. Then the
   Rodrigues vector and the quaternion hold rounded values.
8. Section 15 does not say how `controls_at_calibration` holds a control with no value: TOML has
   no null. Choice: the key is absent. Camera 0 has `exposure_us` 4000 and `gain` 32. Camera 1 has
   an empty table, because its only control has the value null in the capture info JSON.
   Alternative: no table for camera 1.
9. Section 15 gives the layout of the TOML only by its example. Choice: the layout of the example.
   The keys are in the order of the tables of section 15, one empty line is before each table
   header after the first, `[<label>.controls_at_calibration]` follows its camera table, each array
   is on one line with `, `, a text is a basic string, and a float is the shortest decimal form
   that reads back as the same float64, always with a fraction (`60.0`). Alternative: inline tables.

### The Parquet file

10. SFF-818 names the encoding of `value` and `value_f64` only. Choice: `timestamp_s`,
    `frame_number` and `run_id` have the encoding `PLAIN` and no dictionary. Each string column has
    a dictionary (SFF-818 allows it). Alternative: `BYTE_STREAM_SPLIT` also for `timestamp_s`.
11. SFF-823 says "the rows of one channel". Choice: one row group for each item of `channels` of
    the descriptor (one `sensor_group`, `source`, `reference_frame` and `kind`), in the order of
    `channels`. So the file has 11 row groups. Alternative: one row group for each channel kind (4
    row groups).
12. The row rules do not give the order of the rows of one channel. Choice: the frame, then the
    name in the order of `names`, then the component in the order of `components`. This is the
    `array_order` of the processing info JSON, and it keeps the four rows of a quaternion together
    (row rule 5). Alternative: one trajectory after the other.
13. SFF-817 says "the UTF-8 JSON of the descriptor" and gives no white space and no number form.
    Choice: one line with `,` and `:` and no space, the members in the order of the tables of the
    part, no escape of a character above U+007F, and each float in the shortest form that reads
    back, always with a fraction (`1.0`, as freemocap writes it). The descriptor is not a JSON file
    of the take, so the number rule of SFF-702 does not apply to it. Alternative: the number form
    of SFF-702 (`1`).

### The descriptor

14. The part does not give the encoding or the sort order for the name of a sensor group. Choice:
    the keys in order of their bytes, joined with `|`, as UTF-8. G3 has one group,
    `camera_group:d8888d`, with `sample_count` 90.
15. The part gives no name for a synthetic tracker, and it gives the definition of a tracker source
    only as "the tracker configuration, as an object". Choice: the sources
    `keypoint_model:synthetic_stick` and `keypoint_model:synthetic_pair`, each with the definition
    `{}`. Alternative: a definition with invented settings.
16. Appendix A wants "a model with connection pairs and a model with no connection pair". Choice:
    the model `stick` is the informative example of the part, which the generator reads from the
    part, with `tracker_connections` `[["kp_a","kp_b"],["kp_b","kp_d"],["kp_d","kp_e"]]` (the pairs
    of its `landmark_connections`, as keypoint names). The model `pair` is the smallest model that
    obeys the writer rules: 2 landmarks, 1 segment, no joint, a mapping with `passthrough` true,
    and no `tracker_connections`. It also has an empty `landmark_connections`. Alternative: a copy
    of `stick` with no pairs.
17. The part does not give the place of `tracker_connections` and `segment_topology` in a model
    that the example does not show. Choice: the order of the table of `RecordedModel`: after
    `tracker_keypoint_names` and before `skeleton`.
18. The part does not say if a run needs a `model:<model_id>` source for each model. Choice: G3
    has no `model:` source, because it has no channel of the stage `reconstruction`. So no member
    of the descriptor links a tracker to a model. In G3, each tracker gives exactly the
    `tracker_keypoint_names` of the model in its name. Alternative: a
    `ReconstructionSourceDefinition` for each model, with no channel.
19. The part does not say which members of `processing[<group>]` a writer must write, and it gives
    no member types for `filtering` and `camera_assignment`. Choice: only `stage_provenance`. The
    manifest summary needs it (`origin` and `recorded_at`, SFF-728). Decision
    ([ADR-XR63](../decisions/entries/XR63-reader-rules-of-the-golden-review.md)): `filtering` and
    `camera_assignment` are open JSON objects, and a reader checks only that each is an object,
    until freemocap defines them. [ADR-H2HQ](../decisions/entries/H2HQ-descriptor-members-deferred-points-and-old-audio.md)
    item 1 makes them optional: a
    reader checks that each is an object only when it is present. So G3 keeps the choice.
20. The values of a `StageProvenance` are free. Choice: four stages (`timing`, `observations`,
    `triangulation`, `filtering`), each with `attempt_id` `g03-synthetic-attempt`,
    `effective_settings` `{}`, `default_settings` null, `input_signatures`
    `{"synthetic_input": <64 zeros>}`, `software` `{"python": "3.13.13", "packages": {},
    "core_sha256": <64 zeros>}`, `limitations` `[]`, null base members, `origin` `posthoc` and
    `coverage` null. `output_sources` holds the sources of the channels of the stage, in the order
    of `channels`. `checkpoints` is `[]`: each stage has a channel.
21. The part does not give the order of `channels`, `sources` and `reference_frames`. Choice:
    `channels` by stage, then by tracker (`stick`, `pair`), then by camera in order of
    `group_position`: 2 capture `TIMESTAMPS`, 1 group `TIMESTAMPS`, 4 `OVERLAY_2D`, 2
    `RAW_KEYPOINTS_3D`, 2 `KEYPOINTS_3D`. `sources`: the cameras, the timing source, the trackers.
    `reference_frames`: the camera images, then `calibrated_world`.
22. Row rule 9 gives no name for a tracker stage. Choice: `body`, so the `OVERLAY_2D` names are
    `body.kp_a` to `body.kp_e`, `body.p` and `body.q`.
23. `CameraModel` says "world to camera" and does not say which world: the world of the TOML or
    `calibrated_world` after the axis map of SFF-809. Choice: the world of the TOML, with no axis
    map. So `extrinsics`, `world_position` and `world_orientation` hold the values of the TOML, and
    `id` is the key of the camera table. SFF-837 compares only poses relative to camera 0, so the
    choice does not change `calibration_mismatch`. Decision
    ([ADR-XR63](../decisions/entries/XR63-reader-rules-of-the-golden-review.md)): the camera
    geometry of the descriptor is in the world of the calibration TOML, as G3 has it.
24. `calibration_camera` of the manifest and of an image reference is "the name of the camera
    table". Choice: the `camera_label`, which is the key of the table (SFF-806).

### The values of the rows

25. The 2D and 3D values are free. Choice: small formulas of the frame, the name, the camera and
    the tracker. Each 2D value is a number of quarters of a pixel inside the image, and
    `visibility` is 1, 0.875, 0.75 or 0.625. Each raw 3D value is an integer number of millimetres,
    and each filtered value is the raw value plus 0.5. So each float32 is exact. The values are not
    a triangulation: they do not agree with the calibration. No reader rule compares them.
    Alternative: points that the generator projects with the calibration.
26. SFT-748 needs a point that the tracker did not detect. Choice: `kp_e` of `stick` in camera 1
    on the frames 10 to 12: `x` and `y` are null and `visibility` is 0 (SFF-831). The
    `RAW_KEYPOINTS_3D` rows of `kp_e` are null on these frames (one view gives no 3D point), and the
    `KEYPOINTS_3D` rows have values (the filter fills the gap).
27. The cameras of G1 have even fitted times. So the sum of the two strict player times of each
    frame is even, and no group time of G3 shows the "rounded half up" of SFF-828. The strict
    player times of G3 equal its player times: no two fitted times are equal. G12 and the unit test
    `test_strict_and_group_times` cover the two rules.

### The processing info JSON and the reader result

28. SFF-885 gives each `folder_files` item a `role`, and the manifest has no role for
    `calibration.file`. Decision
    ([ADR-XR63](../decisions/entries/XR63-reader-rules-of-the-golden-review.md)): the reader gives
    the role `calibration` to the file that `calibration.file` names. Before, the results of G3 had
    null. Each result of each golden case with a TOML (G3, G7, G8, G9, `higher_minor` of G10 and
    G14) now has `calibration`.
29. Section 14 says that a `data` item has `components` and does not give its form. Choice: the
    `components` object of the descriptor channel (component to units), and `names` as in the
    channel. The `data` items are in the order of `channels`. `cameras` is in order of
    `group_position`. `selected_run_id` is 0, the only run. Alternative: `components` as an array
    of names.
30. Section 14 says "`reference_frames` (as in the descriptor)". Choice: the same JSON value. It
    holds no float in G3, so the number rule of SFF-702 changes nothing.

### Contradictions and limits of the pinned tools

31. **Not shown by a file.** The ZSTD level 3 of SFF-818 is not in the file. The generator sets it
    through pyarrow. No test of the golden file can check it.
32. **More than the spec names.** pyarrow 26.0.0 writes the Parquet format version 2.6, data pages
    of version 1, `created_by` `parquet-cpp-arrow version 26.0.0`, column statistics and a second
    key-value entry `ARROW:schema` (the Arrow schema, which keeps the nullability and the
    descriptor). Choice: keep them. The encoding list of each column also has `RLE`: it is the
    encoding of the levels and, with a dictionary, of the indices.
33. **SFT-750 and SFF-832.** SFT-750 says "each model has `tracker_connections`", and then that a
    model with no pair omits it. G3 follows SFF-832: the model `pair` has no such member.
34. **SFF-892 and the processing info JSON.** The scope `player` reads the processing info JSON,
    but not the Parquet. So its item is `present` with `prerelease` in the two results, and the
    check `take_uuid` has its part in the two results, while `hashes` is `not_checked` for `player`.
35. **`recording-files/golden/README.md`.** It said "Only G1 exists". It now lists each folder, the rotated camera
    of G3 and the digest of item 3.
36. **`tools/goldgen/common.py`.** `expected_result` gives only the result of a capture-only take,
    and `write_take` does not return the manifest. `folder_common.py` wraps the first and reads the
    manifest again from the file. `g01.build` makes the truth file inline, so `g03.py` repeats
    those lines. No fault was found in `common.py`.
