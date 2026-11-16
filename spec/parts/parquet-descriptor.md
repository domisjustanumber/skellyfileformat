# Parquet descriptor (normative part of SPEC.md section 16)

Status: **draft v2, for review at gate 1**. This part is normative. Section 16 of
[SPEC.md](../SPEC.md) cites it. It gives the descriptor that the Arrow schema metadata key
`freemocap.recording` holds, and the row rules of the tracking Parquet. The source is freemocap
`development-streaming` at c27fc299 and the freemocap `sfn26` branches, with the changes of descriptor
`schema_version` 2 ([ADR-P76Y](../../decisions/entries/P76Y-tracking-parquet.md)). A change marked
**v2** is new in schema version 2. The details that the decision entries do not fix are proposed in
[ADR-VPD9](../../decisions/entries/VPD9-spec-draft-v2-details.md).

## Conventions

- The descriptor is one JSON object (RFC 8259). A writer writes every member, also when it has its
  default value, except where a row says "omitted when empty" or "omitted when null".
- A model marked **closed** has no member other than its listed members. A reader of a known `minor`
  refuses a closed model with an unknown member. A reader of an older `minor` ignores members that
  its `minor` does not know (SPEC.md section 3).
- A map with integer keys (`runs`) has the keys as decimal strings.
- A tuple is a JSON array. An enum is its text value.
- A float is finite. NaN and infinity are not allowed.

## Root: `RecordingMetadata` (closed)

| Member | Type | Rule |
|---|---|---|
| `schema_version` | integer | 2 (**v2**; 1 in freemocap at c27fc299) |
| `format_version` | text | **v2.** SPEC.md section 3 |
| `format_prerelease` | integer | **v2.** SPEC.md section 3 |
| `writer` | text | **v2.** The writer string |
| `take_uuid` | text | **v2.** SPEC.md SFF-703 |
| `recording_id` | text | `<rec>`, 1 or more characters |
| `selected_run_id` | integer | 0 or more; a key of `runs` |
| `recording_info` | object | Free JSON. A writer writes `{}`. |
| `runs` | map of integer to `RunDescriptor` | Each key is 0 or more |

## `RunDescriptor` (closed)

| Member | Type | Default |
|---|---|---|
| `calibration_updates` | map of sensor group to `CalibrationUpdateRequest` | `{}` |
| `scale_fits` | array of `RecordingScaleFit` | `[]` |
| `camera_geometry` | map of sensor group to an array of `CameraModel` | `{}` |
| `sensor_groups` | map of text to `SensorGroup` | required |
| `sources` | map of text to `Source` | required |
| `reference_frames` | map of text to an object (section "Reference frames") | required |
| `models` | map of text to `RecordedModel` | required |
| `processing` | map of sensor group to an object (section "Processing") | required |
| `channels` | array of `Channel` | required |
| `static_channels` | array of `StaticChannel` | `[]` |
| `checkpoints` | array of `StageCheckpoint` | `[]` |

Reference rules:
- each key of `calibration_updates` and `camera_geometry` is a key of `sensor_groups`;
- `models[k].model_id` is k;
- `scale_fits` has at most one item for each (`sensor_group`, `source`). The group, source and
  reference frame of each fit exist, and `reference_frames[fit.reference_frame].units` is `fit.units`;
- camera IDs are different in each group of `camera_geometry`;
- the key (`sensor_group`, `source`, `reference_frame`, `kind`) is different for each channel of
  `channels` and `static_channels`;
- no `MODEL_SCALE`, `SEGMENT_SCALES` or `SEGMENT_LENGTHS` channel exists for a (group, source) that
  has a fit that is not null;
- the group and the source of each channel exist, and a reference frame that is not null exists;
- the (`sensor_group`, `stage`) of each checkpoint is different, and its group exists;
- when `processing[group]` has `stage_provenance`: the group exists, each `output_sources` item
  exists, and each stage has a checkpoint or a channel of that group and stage.

## `SensorGroup` (closed)

| Member | Type | Rule |
|---|---|---|
| `clock_description` | text | 1 or more characters. The writer writes `"recording-relative seconds; timing method declared per source"`. |
| `sample_count` | integer | 0 or more. Each declared (name, component) of each channel of the group has exactly this number of rows. |

The name of a camera sensor group is `camera_group:` followed by the first 6 hexadecimal characters of
the SHA-256 of the sorted `camera_key` values of its cameras, joined with `|` (**v2**: `camera_key` in
place of the camera ID).

## `Source` (closed)

| Member | Type |
|---|---|
| `kind` | `instance`, `tracker`, `camera` or `timing` |
| `definition` | an object, with the form of its kind (below) |

| Source name | Kind | Definition |
|---|---|---|
| `camera:<camera_label>` | `camera` | `CameraRecordingDefinition` |
| `timing:<sensor_group>` | `timing` | `{"method": <timing method>}` (closed) |
| `keypoint_model:<model name>` | `tracker` | The tracker configuration, as an object |
| `object_detector:<detector name>` | `tracker` | The detector configuration, as an object |
| `charuco_detector:<board name>` | `tracker` | **v2.** The board definition of SPEC.md section 15 |
| `model:<model_id>` | `instance` | `ReconstructionSourceDefinition` |

A reader splits a source name at its first `:`.

The timing methods are `recorded`, `inferred_from_fps` and `mean_camera_times`.

### `CameraRecordingDefinition` (closed)

| Member | Type | Rule |
|---|---|---|
| `camera_key` | text | **v2.** The `camera_key` of the camera (SPEC.md section 8) |
| `camera_label` | text | **v2.** The `camera_label` |
| `video_filename` | text | The name of the camera file |
| `timing_filename` | text | **v2.** The name of its timing sidecar |
| `timing_method` | timing method | `recorded` for a take of this format |
| `inferred_offset_s` | float | 0.0 |

**v2** removes `camera_id` (replaced by `camera_key` and `camera_label`) and `nominal_fps` (the
timing sidecar is its home).

### `ReconstructionSourceDefinition` (closed)

| Member | Type | Rule |
|---|---|---|
| `point_kind` | `RAW_KEYPOINTS_3D` or `KEYPOINTS_3D` | |
| `model_id` | text | 1 or more characters |
| `tracker` | text | A tracker source name |
| `scale_reference_name` | text | 1 or more characters |
| `landmark_names` | array of text | |
| `segment_origins` | map of segment to landmark | Each landmark is in `landmark_names` |
| `segment_parents` | map of segment to segment or null | Same keys as `segment_origins`; each parent is a segment |
| `joint_angle_names` | map of joint to an array of text | |

## `Channel` (closed)

| Member | Type | Rule |
|---|---|---|
| `sensor_group` | text | |
| `source` | text | |
| `reference_frame` | text or null | |
| `kind` | channel kind | |
| `names` | array of text | 1 or more; each different and not empty |
| `components` | map of component to units | 1 or more; ordered; names and units not empty |
| `stage` | processing stage | |
| `dtype` | `float32` or `float64` | **v2.** Default `float32`; `TIMESTAMPS` is `float64` |

For `ROTATIONS_LOCAL` and `ROTATIONS_WORLD`, `components` is `{"w":"1","x":"1","y":"1","z":"1"}` and
`reference_frame` is not null.

Channel kinds: `KEYPOINTS_3D`, `MAPPED_KEYPOINTS_3D`, `LANDMARKS_3D`, `SEGMENT_ORIGINS`,
`ROTATIONS_LOCAL`, `ROTATIONS_WORLD`, `DERIVED_POINTS`, `JOINT_ANGLES`, `OVERLAY_2D`, `BOXES_2D`,
`SEGMENT_LENGTHS`, `SEGMENT_SCALES`, `MODEL_SCALE`, `OVERLAY_REPROJECTIONS`, `TIMESTAMPS`,
`RAW_KEYPOINTS_3D`, `TRIANGULATION_WEIGHTS`, `REPROJECTION_ERROR`, `RECONSTRUCTION_COVERAGE`,
`RIGID_BODY_RESIDUALS`.

Processing stages, in order: `timing`, `observations`, `triangulation`, `filtering`, `scale_fit`,
`reconstruction`, `biomechanics`, `reprojection`.

Units: `rad`, `px`, `1` (no unit), `s`, `mm`.

### Channels and their contents

| Kind | Source | Reference frame | Names | Components → units | Stage |
|---|---|---|---|---|---|
| `TIMESTAMPS` (capture) | `camera:<label>` | null | `capture` | `timestamp_s` → `s` | `timing` |
| `TIMESTAMPS` (group) | `timing:<group>` | null | `synchronized` | `timestamp_s` → `s` | `timing` |
| `OVERLAY_2D` | `keypoint_model:…` | `camera:<label>:image` | `<stage>.<point>` | `x`, `y` → `px`; `visibility` → `1` | `observations` |
| `OVERLAY_2D` (ChArUco, **v2**) | `charuco_detector:<board>` | `camera:<label>:image` | `corner_<id>` | `x`, `y` → `px`; `visibility` → `1` | `observations` |
| `BOXES_2D` | `object_detector:…` | `camera:<label>:image` | detection stage names | `x1`, `y1`, `x2`, `y2` → `px`; `confidence`, `detector_ran` → `1` | `observations` |
| `REPROJECTION_ERROR` | `camera:<label>` | `camera:<label>:image` | diagnostic point names | `error` → `px` | `triangulation` |
| `RECONSTRUCTION_COVERAGE` | `camera:<label>` | `camera:<label>:image` | same | `observed`, `reconstructed` → `1` | `triangulation` |
| `TRIANGULATION_WEIGHTS` | `camera:<label>` | `camera:<label>:image` | same | `weight` → `1` | `triangulation` |
| `RAW_KEYPOINTS_3D` | tracker | `calibrated_world` or `camera_plane` | keypoint names, no stage prefix | `x`, `y`, `z` → `mm` or `px` | `triangulation` |
| `KEYPOINTS_3D` | tracker | same | same | same | `filtering` |
| `RIGID_BODY_RESIDUALS` | `model:<id>` | spatial reference | segment names | `measured_length`, `residual` → reference units | `reconstruction` |
| `MAPPED_KEYPOINTS_3D` | `model:<id>` | spatial reference | landmark names | `x`, `y`, `z` | `reconstruction` |
| `LANDMARKS_3D` | `model:<id>` | spatial reference | landmark names | `x`, `y`, `z` | `reconstruction` |
| `SEGMENT_ORIGINS` | `model:<id>` | spatial reference | segment names | `x`, `y`, `z` | `reconstruction` |
| `ROTATIONS_WORLD` | `model:<id>` | spatial reference | segment names | `w`, `x`, `y`, `z` → `1` | `reconstruction` |
| `ROTATIONS_LOCAL` | `model:<id>` | `<model_id>:segment_parents` | segment names | `w`, `x`, `y`, `z` → `1` | `reconstruction` |
| `JOINT_ANGLES` | `model:<id>` | `<model_id>:segment_parents` | the angle names of each joint | `radians` → `rad` | `reconstruction` |
| `DERIVED_POINTS` | `model:<id>` | spatial reference | `center_of_mass` | `x`, `y`, `z` | `biomechanics` |
| `MODEL_SCALE`, `SEGMENT_SCALES`, `SEGMENT_LENGTHS` | `model:<id>` | fit reference | | | `scale_fit`; static only, derived from the fit on read |

## `StaticChannel` (closed)

`channel` (a `Channel`) and `values` (a map of name to a map of component to a float). The names and
components are those of the channel. Static channels have no rows.

## `StageCheckpoint` (closed)

`sensor_group` (text), `stage` (processing stage), `signature` (text, 1 or more characters).

## Reference frames

| Name | Object |
|---|---|
| `camera:<camera_label>:image` | `{camera_key, calibration_camera, width, height}` (closed; **v2**: `camera_key` in place of `camera_id`, and `calibration_camera`, the name of the camera table of the TOML, in place of `calibration_camera_id`). `width` and `height` are the size of the stored JPEG. |
| `calibrated_world`, `camera_plane` | `{name, basis, units, alignment, additional_transform}`. `basis` is `blender_x_right_y_forward_z_up`. `units` is `px` for `camera_plane` and `mm` for `calibrated_world`. `alignment` is null or `{outcome, rotation_wxyz, translation_mm, anchor_segment}`, with `outcome` one of `preserved_reference`, `disabled`, `foot_support`, `body_reference`, `insufficient_evidence`. `additional_transform` is null or `{matrix}`: 16 floats, row-major, a rigid transform with the bottom row [0, 0, 0, 1]. |
| `<model_id>:segment_parents` | `{parents, root_reference}`: rotations relative to the parent segment; a root uses the named world frame |

## Processing

`processing[group]` is an object. Its members:

| Member | Object |
|---|---|
| `filtering` | The filter report of freemocap: `algorithm_version` (1), `config`, `sampling_rate_hz`, `filtered_runs`, `preserved_short_runs`, `gap_filling` |
| `camera_assignment` | `{status, source_to_calibration, fitness, error_units}`; `error_units` is `pixels_at_1000_pixel_image_diagonal` |
| `stage_provenance` | `StageProvenanceSet` |

### `StageProvenanceSet` (closed)

`version` (1) and `stages` (a map of processing stage to `StageProvenance`).

### `StageProvenance` (closed)

| Member | Type | Rule |
|---|---|---|
| `attempt_id` | text | 1 or more characters |
| `recorded_at` | text | An ISO 8601 date and time with a time zone |
| `effective_settings` | object | |
| `default_settings` | object or null | |
| `input_signatures` | map of text to text | 1 or more items; values not empty |
| `software` | object | 1 or more members: `python`, `packages` (name → `{version, commit}`), `core_sha256` |
| `output_sources` | array of text | 1 or more; different |
| `limitations` | array of text | Default `[]` |
| `base_run_id` | integer or null | 0 or more; given with `base_descriptor_signature` |
| `base_descriptor_signature` | text or null | |
| `origin` | `realtime` or `posthoc` | **v2** |
| `coverage` | object or null | **v2.** SPEC.md SFF-834 |

## `RecordedModel` (closed)

| Member | Type | Rule |
|---|---|---|
| `model_id` | text | 1 or more characters |
| `detector_type` | text | 1 or more characters |
| `tracker_keypoint_names` | array of text | 1 or more; different |
| `tracker_connections` | array of pairs of text | **v2** (from `sfn26`). Each name is in `tracker_keypoint_names` |
| `segment_topology` | array of `{name, parent, proximal, distal}` | **v2.** SPEC.md SFF-832 |
| `skeleton` | `SkeletonSnapshot` | |
| `rest_pose` | `RestPoseSnapshot` | |
| `mappings` | array of `TrackerMappingSnapshot` | 1 or more |
| `center_of_mass` | `CenterOfMassDefinitions` | |
| `segment_masses` | map of segment to float | Keys are the segment names of `center_of_mass`; each value is more than 0 |
| `scale_reference_name` | text | 1 or more characters |
| `anchor_segment_name` | text or null | Default null |
| `object_geometry` | `RigidObjectGeometry` or null | From `sfn26`; omitted when null |
| `tracker_stage_path` | array of text or null | From `sfn26`; omitted when null |

The nested types (`SkeletonSnapshot`, `LandmarkSnapshot`, `SegmentSnapshot`, `FrameSnapshot`,
`JointSnapshot`, `ChainSnapshot`, `RestPoseSnapshot`, `LandmarkGroup`, `LandmarkConnectionGroup`,
`CenterOfMassDefinitions`, `SegmentComDefinition`, `TrackerMappingSnapshot`, `RigidObjectGeometry`)
are listed in the research inventory of skellycam `dom/research`,
`research/skellycam_recording/docs/parquet_inventory_20261116.md`, section 2.2 (local, not
committed). (provisional: they are copied into this part at gate 1, after the review of the model
tree.)

## `CameraModel` (closed)

| Member | Type | Rule |
|---|---|---|
| `id` | text | The name of the camera table of the TOML |
| `camera_key` | text | **v2** |
| `index` | integer | |
| `image_size` | [width, height] | |
| `intrinsics` | `{fx, fy, cx, cy, k1, k2, p1, p2}` | Floats; `k1` to `p2` default 0.0 |
| `extrinsics` | `{quaternion_wxyz, translation}` | World to camera; 4 and 3 floats; millimetres |
| `world_position` | 3 floats | Millimetres; default [0, 0, 0] |
| `world_orientation` | 3 × 3 floats | Camera to world; default the identity |

## `RecordingScaleFit` (closed)

`sensor_group`, `source`, `reference_frame` (text), `units` (`px` or `mm`), `fit` (null or
`{fitted_scale, segment_scales, segment_lengths, measured_segment_names, voting_segment_names}`) and
`inputs` (`{algorithm_version, keypoint_names, points, model}`; `points` and `model` are 64-character
signatures).

## `CalibrationUpdateRequest` (closed)

`path`, `expected_mtime_ms` (float), `transformations` (1 or more of
`{operation, quaternion_wxyz, translation_mm}`, with `operation` one of `charuco`, `person`, `manual`;
X right, Y forward, Z up, millimetres) and `recording_id` (text or null).

## Row rules

1. Each row's `channel`, `name`, `component` and `units` are declared by one channel of its run:
   `name` is in `names`, `component` is a key of `components`, and `units` is
   `components[component]`.
2. Each value is finite or null. `frame_number` is 0 or more.
3. A trajectory is the rows of one (`run_id`, `sensor_group`, `source`, `reference_frame`,
   `channel`, `name`, `component`). In each trajectory, `frame_number` and `timestamp_s` strictly
   increase in file order, and the trajectory has exactly `sample_count` rows of its sensor group.
   A missing sample is a row with a null value, not an absent row.
4. The trajectories of one (`run_id`, `sensor_group`, `source`, `reference_frame`) have the same
   sequence of (`frame_number`, `timestamp_s`).
5. The four rows `w`, `x`, `y`, `z` of one (name, frame) of a rotation channel are next to each
   other. They are a unit quaternion (to 1e-5), or all four are null.
6. A `TIMESTAMPS` row has `component` `timestamp_s`, `units` `s`, a null `reference_frame`, and its
   value is its `timestamp_s`.
7. `OVERLAY_2D`: `visibility` is from 0 to 1. A point that is absent on a frame has `x` and `y` null
   and `visibility` 0. A frame that a realtime run skipped has all three null.
8. `BOXES_2D`: one box for each stage and frame. A stage with no box on a frame has all six
   components null. `detector_ran` is 1 when a detector of that stage ran on the frame, else 0.
9. The names of `OVERLAY_2D` are `<stage>.<point>`. A reader splits them at the first `.`.
