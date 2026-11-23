# Parquet descriptor (normative part of SPEC.md section 16)

Status: **draft v2, for review at gate 1**. This part is normative. Section 16 of
[SPEC.md](../SPEC.md) cites it. It gives the descriptor that the Arrow schema metadata key
`freemocap.recording` holds, and the row rules of the tracking Parquet. The source is freemocap
`development-streaming` at c27fc299 and the freemocap `sfn26` branches, with the changes of descriptor
`schema_version` 2 ([ADR-P76Y](../decisions/entries/P76Y-tracking-parquet.md)). A change marked
**v2** is new in schema version 2. The details that the decision entries do not fix are proposed in
[ADR-VPD9](../decisions/entries/VPD9-spec-draft-v2-details.md). The changes to
`selected_run_id` and to `CalibrationUpdateRequest` are from
[ADR-72QQ](../decisions/entries/72QQ-spec-v2-details-part-8.md) and
[ADR-ATW0](../decisions/entries/ATW0-spec-v2-details-part-6.md). The nested types of
`RecordedModel`, and what a reader checks in them, are from
[ADR-W5JC](../decisions/entries/W5JC-nested-model-types-in-the-descriptor-part.md). The source
names, the Parquet values and the JSON types of the structure check are from
[ADR-6VRQ](../decisions/entries/6VRQ-spec-v2-details-part-13.md). The scope of the writer rules
is from [ADR-N6KY](../decisions/entries/N6KY-spec-v2-details-part-14.md) item 40.

## Conventions

- The descriptor is one JSON object (RFC 8259). A writer writes every member, also when it has its
  default value, except where a row says "omitted when empty" or "omitted when null". In
  `RecordedModel` and its nested types, these members are omitted: `tracker_connections` when it is
  empty; `object_geometry` and `tracker_stage_path` when null; `presentation` of `SkeletonSnapshot`
  when null; and `observation_frame` of `SegmentSnapshot` when null.
- A model marked **closed** has no member other than its listed members. A reader of a known `minor`
  refuses a closed model with an unknown member. A reader of an older `minor` ignores members that
  its `minor` does not know (SPEC.md section 3).
- A map with integer keys (`runs`) has the keys as decimal strings.
- A tuple is a JSON array. An enum is its text value. The one exception is `handedness` of
  `FrameSnapshot`: it is the integer 1 or -1.
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
| `recording_info` | object | Free JSON. A writer writes `{}`. |
| `runs` | map of integer to `RunDescriptor` | Each key is 0 or more |

**v2** removes `selected_run_id`. The processing info JSON is its only home (SPEC.md section 14). A
change of the selected run then does not rewrite the Parquet.

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
| `charuco_detector:<squares_x>x<squares_y>` | `tracker` | **v2.** The board definition of SPEC.md section 15. The name holds `squares_x` and `squares_y` of the board, for example `charuco_detector:5x3`. The board has no name member (SPEC.md SFF-836) |
| `model:<model_id>` | `instance` | `ReconstructionSourceDefinition` |

A reader splits a source name at its first `:`.

The timing methods are `recorded`, `inferred_from_fps` and `mean_camera_times`.

### `CameraRecordingDefinition` (closed)

| Member | Type | Rule |
|---|---|---|
| `camera_key` | text | **v2.** The `camera_key` of the camera (SPEC.md section 8) |
| `camera_label` | text | **v2.** The `camera_label` |
| `video_filename` | text | The file name of the camera file, with no folder. The file is in the media folder |
| `timing_filename` | text | **v2.** The file name of its timing sidecar, with no folder. The file is in the media folder |
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
| `joint_angle_names` | map of joint to an array of text | No two joints of a model have an equal angle name |

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
| `OVERLAY_2D` | `keypoint_model:…` | `camera:<label>:image` | `<tracker stage>.<point>` | `x`, `y` → `px`; `visibility` → `1` | `observations` |
| `OVERLAY_2D` (ChArUco, **v2**) | `charuco_detector:<squares_x>x<squares_y>` | `camera:<label>:image` | `corner_<id>`: `<id>` is the OpenCV corner ID, in decimal | `x`, `y` → `px`; `visibility` → `1` | `observations` |
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
| `JOINT_ANGLES` | `model:<id>` | `<model_id>:segment_parents` | the names of `joint_angle_names` of the source definition: each joint in member order, each name in array order | `radians` → `rad` | `reconstruction` |
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
| `calibrated_world`, `camera_plane` | `{name, basis, units, alignment, additional_transform}`. `basis` is `blender_x_right_y_forward_z_up`. SPEC.md SFF-809 gives the axis map from the world of the calibration TOML to `calibrated_world`. `units` is `px` for `camera_plane` and `mm` for `calibrated_world`. `alignment` is null or `{outcome, rotation_wxyz, translation_mm, anchor_segment}`, with `outcome` one of `preserved_reference`, `disabled`, `foot_support`, `body_reference`, `insufficient_evidence`. `additional_transform` is null or `{matrix}`: 16 floats, row-major, a rigid transform with the bottom row [0, 0, 0, 1]. |
| `<model_id>:segment_parents` | `{parents, root_reference}`: rotations relative to the parent segment; a root uses the named world frame |

## Processing

`processing[group]` is an object. Its members:

| Member | Object |
|---|---|
| `filtering` | An open JSON object. freemocap writes its filter report: `algorithm_version` (1), `config`, `sampling_rate_hz`, `filtered_runs`, `preserved_short_runs`, `gap_filling` |
| `camera_assignment` | An open JSON object. freemocap writes `{status, source_to_calibration, fitness, error_units}`; `error_units` is `pixels_at_1000_pixel_image_diagonal` |
| `stage_provenance` | `StageProvenanceSet` |

`filtering` and `camera_assignment` are optional and open: a writer can omit each of them. A reader
checks that each is a JSON object only when it is present, until freemocap defines them
([ADR-XR63](../decisions/entries/XR63-reader-rules-of-the-golden-review.md) item 8,
[ADR-H2HQ](../decisions/entries/H2HQ-descriptor-members-deferred-points-and-old-audio.md) item 1).

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
| `origin` | `realtime` or `posthoc` | **v2.** `realtime` means that the run was folded from the realtime journal (SPEC.md section 17). Each stage of such a run is `realtime`, also `timing` ([ADR-1P4N](../decisions/entries/1P4N-timing-coverage-of-a-realtime-run-and-latency-at-the-fold.md)). A posthoc run is `posthoc` |
| `coverage` | object or null | **v2.** SPEC.md SFF-834 gives each member and its value, also the member `events`, and the values of the stage `timing`. null when `origin` is `posthoc` |

## `RecordedModel` (closed)

| Member | Type | Rule |
|---|---|---|
| `model_id` | text | 1 or more characters |
| `detector_type` | text | 1 or more characters |
| `tracker_keypoint_names` | array of text | 1 or more; different |
| `tracker_connections` | array of pairs of text | **v2** (from `sfn26`). Each name is in `tracker_keypoint_names`. Omitted when empty |
| `segment_topology` | array of `{name, parent, proximal, distal}` | **v2.** SPEC.md SFF-832. One item for each item of `skeleton.segments`, in that order. `name` is the segment name. `parent` is `rest_pose.parents[name]`. `proximal` is `frame.origin` and `distal` is `frame.primary_point`: landmark names |
| `skeleton` | `SkeletonSnapshot` | |
| `rest_pose` | `RestPoseSnapshot` | |
| `mappings` | array of `TrackerMappingSnapshot` | 1 or more |
| `center_of_mass` | `CenterOfMassDefinitions` | |
| `segment_masses` | map of segment to float | The keys are exactly the segment names that the definitions of `center_of_mass` give after the left/right expansion of a sided definition (section `SegmentComDefinition`); each value is more than 0 |
| `scale_reference_name` | text | 1 or more characters |
| `anchor_segment_name` | text or null | Default null. A segment of `skeleton`, or null |
| `object_geometry` | `RigidObjectGeometry` or null | From `sfn26`; omitted when null |
| `tracker_stage_path` | array of text or null | From `sfn26`; omitted when null |

The section "Nested types of `RecordedModel`" gives the nested types.

### Structure rules and writer rules

The rules of `RecordedModel` and of its nested types are of two kinds
([ADR-W5JC](../decisions/entries/W5JC-nested-model-types-in-the-descriptor-part.md)).

- **Structure.** Each member is present, except a member that its row lets the writer omit. The
  reader also accepts a member that is absent when its row gives a default, and the value null for
  a member that its row lets the writer omit when null. A writer still writes these members as this
  part says
  ([ADR-H2HQ](../decisions/entries/H2HQ-descriptor-members-deferred-points-and-old-audio.md)
  item 2). A member has a default only when its row gives one. So `tags` and `angle_names` stay
  required ([ADR-158N](../decisions/entries/158N-details-for-the-decisions-of-round-3.md)
  item 5). Each
  member has the JSON type of the column "Type", with the number of items that the column gives. A
  closed type has no other member. An "integer" is a JSON number with no fraction in its value: `1`
  and `1.0` pass. A "float" is each JSON number: `0` passes for `position`. A text is a JSON
  string. A reader checks the structure (SPEC.md SFF-893, [ADR-YBT1](../../decisions/entries/YBT1-spec-only-test-adapter-and-labels.md)). A structure fault makes the Parquet file `invalid` with the reason `bad_schema`.
- **Writer rules.** Each rule that is not a structure rule is a writer rule, at each place of this
  part. The column "Rule", the lists "Writer rules" and the sentences "Writer rule" are examples. A
  rule in the text of a type, for example "`weight` (float; more than 0)", is also a writer rule.
  The writer rules are the cross-reference rules, the value ranges and the enum values. A writer must obey each writer rule. A reader
  does not check the writer rules in version 2.0 ([ADR-YBT1](../../decisions/entries/YBT1-spec-only-test-adapter-and-labels.md)).

A later minor version can add an optional deep check. The deep check reports a fault of a writer rule
as a warning. It never refuses the file for such a fault. This specification gives no other rule for
the deep check.

## Nested types of `RecordedModel`

Each type of this section is closed. A writer must write each member, also when the member is null,
empty or has its default value, except where a row says "omitted when null". The sources are
skellyforge at f5404db, skellytracker at 03b9c1d, skellyforge `sfn26` at 5f0fd2d (`presentation`
and its types) and freemocap `sfn26` at ca0c17cc (`RigidObjectGeometry`). The files of skellyforge
that define the other types are the same at f5404db and at 5f0fd2d.

A name is text with 1 or more characters. In this section, "landmark" is the `name` of an item of
`skeleton.landmarks`, "segment" is the `name` of an item of `skeleton.segments` and "joint" is the
`name` of an item of `skeleton.joints`. "The model restores" means that freemocap builds its
skeleton from the descriptor with no error (`RecordedModel.to_bundle()`).

### `SkeletonSnapshot` (closed)

| Member | Type | Rule |
|---|---|---|
| `name` | text | 1 or more characters |
| `landmarks` | array of `LandmarkSnapshot` | 1 or more. Each `name` is different |
| `segments` | array of `SegmentSnapshot` | 1 or more. Each `name` is different |
| `joints` | array of `JointSnapshot` | Each `name` is different. Can be `[]` |
| `chains` | array of `ChainSnapshot` | Each `name` is different. Can be `[]` |
| `landmark_groups` | array of `LandmarkGroup` | Each `name` is different. Can be `[]` |
| `landmark_connections` | array of `LandmarkConnectionGroup` | Each `name` is different. Can be `[]` |
| `derived_quantities` | array of text | Each item is one of `inertia`, `extrapolated_center_of_mass`, `center_of_pressure`, `centroidal_moment_pivot`, `roll_resolution`. The writer sorts the items. Can be `[]` |
| `coordinate_system` | text | 1 or more characters. freemocap writes `blender` |
| `presentation` | `Presentation` | From `sfn26`. Omitted when null |

Writer rules:
- each landmark is in the `landmarks` of exactly one segment, and its `segment` is the name or an
  alias of a segment;
- no two landmarks have the same name or alias;
- each point name of each `frame` and `observation_frame` is a landmark;
- each name in `landmark_groups` and `landmark_connections` is a landmark;
- no two joints have an equal name in the `angle_names` of their `convention`. So the names of
  `JOINT_ANGLES` are different;
- when `joints` is not empty, each segment is the `child` of at most one joint, exactly one segment
  is the `child` of no joint, and the joints make no cycle;
- when `derived_quantities` contains `inertia`, no segment has a null `anatomical_segment`.

### `LandmarkSnapshot` (closed)

| Member | Type | Rule |
|---|---|---|
| `name` | text | 1 or more characters |
| `definition` | text | 1 or more characters. The anatomical description of the point |
| `position` | 3 floats | x, y, z. The rest position in the local frame of the segment `segment` |
| `segment` | text | The segment that owns the landmark |
| `aliases` | array of text | Other names of the landmark. Each is different, not empty and not `name`. Can be `[]` |

### `SegmentSnapshot` (closed)

| Member | Type | Rule |
|---|---|---|
| `name` | text | Lower-case letters and digits, in groups that one `_` joins. The first character is a letter (the pattern `[a-z][a-z0-9]*(_[a-z0-9]+)*`) |
| `landmarks` | array of text | The landmarks that the segment owns |
| `frame` | `FrameSnapshot` | The local frame of the segment. Its `primary_point` is in `landmarks` |
| `aliases` | array of text | Other names of the segment. Each is different, not empty and not `name`. Can be `[]` |
| `anatomical_segment` | text or null | The anatomical mass segment of the rigid body |
| `observation_frame` | `FrameSnapshot` | Omitted when null. When present, its `secondary_point` and `secondary_axis` are not null |

Writer rule: when the `origin` of `frame` is in `landmarks`, the `position` of that landmark is
[0, 0, 0], to 1e-9.

### `FrameSnapshot` (closed)

| Member | Type | Rule |
|---|---|---|
| `origin` | text | The landmark at the origin of the frame |
| `primary_point` | text | The landmark on the primary axis. It is not `origin` |
| `primary_axis` | [index, sign]: 2 integers | `index` is 0 (x), 1 (y) or 2 (z). `sign` is 1 or -1 |
| `secondary_point` | text or null | The landmark near the secondary axis. It is not `origin` and not `primary_point` |
| `secondary_axis` | [index, sign] or null | Its `index` is not the `index` of `primary_axis` |
| `handedness` | integer | 1 (right-handed) or -1 (left-handed) |

Writer rule: `secondary_point` and `secondary_axis` are both null or both not null.

`handedness` is an integer, not text. It is the exception to the convention "an enum is its text
value". freemocap refuses the text `RIGHT_HANDED`.

### `JointSnapshot` (closed)

| Member | Type | Rule |
|---|---|---|
| `name` | text | 1 or more characters |
| `parent` | text | A segment |
| `child` | text | A segment. It is not `parent` |
| `connect_at` | text | A landmark of the `landmarks` of the parent segment. The origin of the child is on it |
| `joint_type` | text | `ball`, `hinge`, `universal` or `fixed` |
| `convention` | `EulerConvention` | |

### `EulerConvention` (closed)

| Member | Type | Rule |
|---|---|---|
| `sequence` | text | 3 letters, each `x`, `y` or `z`. Two adjacent letters are different |
| `angle_names` | 3 texts | Each is different. One name for each letter of `sequence`, in order |
| `zero_offsets` | 3 floats | Radians. freemocap adds them after the decomposition. Default [0.0, 0.0, 0.0] |

### `ChainSnapshot` (closed)

| Member | Type | Rule |
|---|---|---|
| `name` | text | 1 or more characters |
| `segments` | array of text | 3 or more segments, proximal first |
| `joints` | array of text | Joints, in the same order. The number of items is the number of `segments` minus 1 |

### `LandmarkGroup` (closed)

| Member | Type | Rule |
|---|---|---|
| `name` | text | 1 or more characters |
| `landmark_names` | array of text | 1 or more landmarks; each different |
| `tags` | array of text | Each is different and not empty. The most specific tag is first. Can be `[]` |

### `LandmarkConnectionGroup` (closed)

| Member | Type | Rule |
|---|---|---|
| `name` | text | 1 or more characters |
| `pairs` | array of pairs of text | 1 or more. Each pair is 2 different landmarks |
| `tags` | array of text | Each is different and not empty. Can be `[]` |

### `Presentation` (closed)

From skellyforge `sfn26` (`skellyforge/core/skeleton/presentation.py`). It holds static geometry for
display only. Reconstruction and the scale fit do not use it. The lines and surfaces that freemocap
compiles from it (`AttachedLines`, `AttachedSurface`) are not in the descriptor.

| Member | Type | Rule |
|---|---|---|
| `contours` | array of `SuperquadricContours` | Default `[]` |
| `excluded_origin_edges` | array of pairs of text | Default `[]`. Each pair is 2 segments |
| `excluded_bones` | array of text | Default `[]`. Each item is a segment |
| `connection_materials` | array of `ConnectionMaterial` | Default `[]`. Each `group` is different and is the `name` of an item of `landmark_connections` |

freemocap checks the rules of `PresentationMaterial` when it loads the descriptor. It checks each
other writer rule of the presentation types only when the model restores, because it compiles the
presentation then.

### `SuperquadricContours` (closed)

| Member | Type | Rule |
|---|---|---|
| `segment` | text | A segment |
| `crown`, `chin`, `left_ear`, `right_ear`, `left_eye`, `right_eye` | text | Six members. Each is a landmark of the `landmarks` of the segment `segment` |
| `vertical_exponent` | float | Default 1.0. From 0.2 to 2 |
| `horizontal_exponent` | float | Default 0.85. From 0.2 to 2 |
| `posterior_depth` | float | Default 0.8. From 0.2 to 2 |
| `samples` | integer | Default 64. From 16 to 256 |
| `nose` | text or null | Default null. A landmark of the `landmarks` of the same segment |
| `line_material` | `PresentationMaterial` or null | Default null |
| `shell_material` | `PresentationMaterial` or null | Default null |
| `side_material` | `PresentationMaterial` or null | Default null |

The landmark positions are in the local frame of the segment: +X right, +Y anterior, +Z superior.

Writer rules (the contour must compile):
- the crown is above the chin (z);
- the mean z of the two ears is between the crown and the chin and is not equal to one of them. The
  same rule applies to the mean z of the two eyes;
- the two ears have different x;
- the mean y of the eyes is more than the mean y of the ears, and the x distance between the eyes
  fits in the volume that the ears give;
- when `nose` is not null, the nose is not on the line through the two ears, and the point midway
  between the ears is inside the volume.

### `PresentationMaterial` (closed)

| Member | Type | Rule |
|---|---|---|
| `color` | text | `#` and 6 hexadecimal digits (RGB), for example `#ff8800` |
| `opacity` | float | From 0 to 1 |

### `ConnectionMaterial` (closed)

`group` (text) and `material` (`PresentationMaterial`).

### `RestPoseSnapshot` (closed)

| Member | Type | Rule |
|---|---|---|
| `name` | text | |
| `root_segment_name` | text | A segment |
| `parents` | map of segment to segment or null | One key for each segment. Exactly one value is null: that of `root_segment_name` |
| `connect_ats` | map of segment to landmark | One key for the `child` of each joint |
| `orientations` | map of segment to `RotationQuaternion` | One key for each segment. The rotation of the segment relative to its parent |

Writer rule: for each joint, `parents[child]` is its `parent` and `connect_ats[child]` is its
`connect_at`.

### `RotationQuaternion` (closed)

`w`, `x`, `y`, `z` (floats). Writer rule: the norm is 1, to 1e-9. This tolerance is not the 1e-5 of
row rule 5: that tolerance is for the data rows. freemocap refuses a descriptor quaternion with a
larger error. A value that was rounded to float32 can fail this rule.

### `TrackerMappingSnapshot` (closed)

| Member | Type | Rule |
|---|---|---|
| `entries` | map of landmark to a mapping entry | Can be `{}` |
| `prefix` | text or null | When it is not null, freemocap adds it before each keypoint name of `entries` |
| `known_tracker_keypoints` | array of text or null | The keypoint names that the tracker can give. The writer sorts them |
| `passthrough` | boolean | When true, each tracker keypoint is a landmark of the same name |

Writer rules:
- when `passthrough` is true, `entries` is `{}` and `known_tracker_keypoints` has 1 or more items;
- when `known_tracker_keypoints` is not null, each keypoint name of `entries`, after `prefix`, is in
  it.

A mapping entry has one of four forms. For the structure, a mapping entry is text, an array of text
or an object. The form of an object is a writer rule.

| Form | JSON | Meaning |
|---|---|---|
| Name | text | The landmark is that keypoint |
| Mean | array of text, 1 or more | The landmark is the mean of the keypoints |
| Weighted sum | map of keypoint to float, 1 or more | The landmark is the weighted sum |
| Offset | an object with `form` equal to `anatomical_offset` | The landmark is off the surface (below) |

The offset form has these members:

| Member | Type | Rule |
|---|---|---|
| `form` | text | `anatomical_offset` |
| `origin` | array of text | 1 or more keypoints. Their mean is the origin of the frame |
| `frame` | map of axis name to `{from, to, kind}` | Exactly 2 axes. `from` and `to` are a keypoint or an array of 1 or more keypoints. `kind` is `exact` for one axis and `approximate` for the other |
| `offset` | map of axis name to float | 1 or more. Each value is a ratio of the reference length |
| `reference_length` | `{from, to}` | Each is a keypoint or an array of 1 or more keypoints |

### `CenterOfMassDefinitions` (closed)

`definitions` (a map of text to `SegmentComDefinition`). Writer rules: it has 1 or more items, and
each key is the `name` of its value.

### `SegmentComDefinition` (closed)

| Member | Type | Rule |
|---|---|---|
| `name` | text | The anatomical segment name, with no side |
| `proximal` | text | The landmark at the proximal end |
| `distal` | text | The landmark at the distal end |
| `weights` | array of `ComLandmarkWeight` | 1 or more. The sum of the weights is 1.0, to 1e-6 |
| `sided` | boolean | Default false |

When `sided` is false, the definition gives one segment name, `name`, and its landmark names are
used as written. When `sided` is true, the definition gives two segment names, `left_<name>` and
`right_<name>`, and each landmark name gets the same prefix (`left_` or `right_`). This is the
left/right expansion.

Writer rules:
- each landmark name that results is a landmark of the skeleton;
- the keys of `RecordedModel.segment_masses` are exactly the segment names that all definitions give
  after the left/right expansion. They are not the keys of `definitions`.

### `ComLandmarkWeight` (closed)

`landmark` (text) and `weight` (float; more than 0).

### `RigidObjectGeometry` (closed)

From freemocap `sfn26`.

| Member | Type | Rule |
|---|---|---|
| `feature_names` | array of text | |
| `segment_name` | text | |
| `source_mesh_units` | text | The units of the original mesh |
| `mesh_sha256` | text or null | The member is always present |
| `reference_unit_mm` | float | More than 0 |
| `object_to_segment_reference` | 16 floats | Row-major 4 × 4. Input: object millimetres. Output: segment reference units |
| `source_mesh_to_segment_reference` | 16 floats | Row-major 4 × 4. Input: original mesh units. Output: segment reference units |
| `segment_reference_to_source_mesh` | 16 floats | Row-major 4 × 4 |

A matrix multiplies a homogeneous column vector.

### Example of a `RecordedModel` (informative)

This example is one value of `models`, with the key `stick`. The `RecordedModel` class of freemocap
at c27fc299, with skellyforge at f5404db and skellytracker at 03b9c1d, loads it and writes the same
JSON value again, and the model restores. The example does not have the members from `sfn26`
(`tracker_connections`, `object_geometry`, `tracker_stage_path`, `presentation`) or the **v2** member
`segment_topology`: the class at c27fc299 refuses them. A descriptor of this format adds them as their rows say.
The example does not show the offset form of a mapping entry or a definition with `sided` true. The
segment `tip` has an `observation_frame`. The other segments omit it.

```json
{
 "model_id": "stick",
 "detector_type": "synthetic",
 "tracker_keypoint_names": ["kp_a", "kp_b", "kp_c", "kp_d", "kp_e"],
 "skeleton": {
  "name": "stick",
  "landmarks": [
   {"name": "a", "definition": "Base origin", "position": [0.0, 0.0, 0.0], "segment": "base", "aliases": []},
   {"name": "b", "definition": "Base end and tip origin", "position": [0.0, 0.0, 1.0], "segment": "base", "aliases": []},
   {"name": "c", "definition": "Base side point", "position": [1.0, 0.0, 0.0], "segment": "base", "aliases": ["c_alias"]},
   {"name": "d", "definition": "Tip end", "position": [0.0, 0.0, 1.0], "segment": "tip", "aliases": []},
   {"name": "e", "definition": "End point", "position": [0.0, 0.0, 1.0], "segment": "end", "aliases": []}
  ],
  "segments": [
   {"name": "base", "landmarks": ["a", "b", "c"],
    "frame": {"origin": "a", "primary_point": "b", "primary_axis": [2, 1], "secondary_point": "c", "secondary_axis": [0, 1], "handedness": 1},
    "aliases": [], "anatomical_segment": null},
   {"name": "tip", "landmarks": ["d"],
    "frame": {"origin": "b", "primary_point": "d", "primary_axis": [2, 1], "secondary_point": null, "secondary_axis": null, "handedness": 1},
    "aliases": [], "anatomical_segment": null,
    "observation_frame": {"origin": "b", "primary_point": "d", "primary_axis": [2, 1], "secondary_point": "c", "secondary_axis": [0, 1], "handedness": 1}},
   {"name": "end", "landmarks": ["e"],
    "frame": {"origin": "d", "primary_point": "e", "primary_axis": [2, 1], "secondary_point": null, "secondary_axis": null, "handedness": 1},
    "aliases": [], "anatomical_segment": null}
  ],
  "joints": [
   {"name": "base_tip", "parent": "base", "child": "tip", "connect_at": "b", "joint_type": "ball",
    "convention": {"sequence": "zyx", "angle_names": ["base_tip_z", "base_tip_y", "base_tip_x"], "zero_offsets": [0.0, 0.0, 0.0]}},
   {"name": "tip_end", "parent": "tip", "child": "end", "connect_at": "d", "joint_type": "hinge",
    "convention": {"sequence": "zyx", "angle_names": ["tip_end_z", "tip_end_y", "tip_end_x"], "zero_offsets": [0.0, 0.0, 0.0]}}
  ],
  "chains": [{"name": "stick_chain", "segments": ["base", "tip", "end"], "joints": ["base_tip", "tip_end"]}],
  "landmark_groups": [{"name": "all_points", "landmark_names": ["a", "b", "c", "d", "e"], "tags": ["stick"]}],
  "landmark_connections": [{"name": "stick_edges", "pairs": [["a", "b"], ["b", "d"], ["d", "e"]], "tags": []}],
  "derived_quantities": [],
  "coordinate_system": "blender"
 },
 "rest_pose": {
  "name": "stick_rest",
  "root_segment_name": "base",
  "parents": {"base": null, "tip": "base", "end": "tip"},
  "connect_ats": {"tip": "b", "end": "d"},
  "orientations": {
   "base": {"w": 1.0, "x": 0.0, "y": 0.0, "z": 0.0},
   "tip": {"w": 1.0, "x": 0.0, "y": 0.0, "z": 0.0},
   "end": {"w": 1.0, "x": 0.0, "y": 0.0, "z": 0.0}
  }
 },
 "mappings": [
  {"entries": {"a": "kp_a", "b": ["kp_b"], "c": {"kp_c": 1.0}, "d": "kp_d", "e": "kp_e"},
   "prefix": null,
   "known_tracker_keypoints": ["kp_a", "kp_b", "kp_c", "kp_d", "kp_e"],
   "passthrough": false}
 ],
 "center_of_mass": {
  "definitions": {
   "base": {"name": "base", "proximal": "a", "distal": "b", "weights": [{"landmark": "a", "weight": 0.5}, {"landmark": "b", "weight": 0.5}], "sided": false},
   "tip": {"name": "tip", "proximal": "b", "distal": "d", "weights": [{"landmark": "d", "weight": 1.0}], "sided": false},
   "end": {"name": "end", "proximal": "d", "distal": "e", "weights": [{"landmark": "e", "weight": 1.0}], "sided": false}
  }
 },
 "segment_masses": {"base": 0.5, "tip": 0.3, "end": 0.2},
 "scale_reference_name": "stick_length",
 "anchor_segment_name": null
}
```

## `CameraModel` (closed)

The camera geometry is in the world of the calibration TOML ([ADR-XR63](../decisions/entries/XR63-reader-rules-of-the-golden-review.md) item 8).

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

`calibration_uuid_before` and `calibration_uuid_after` (text, SPEC.md SFF-703; **v2**, in place of
`path` and `expected_mtime_ms`), `transformations` (1 or more of
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
   other. They are a unit quaternion (to 1e-5), or all four are null. The tolerance 1e-5 is for
   these data rows only. A quaternion of the rest pose in the descriptor (`RotationQuaternion`) is
   unit to 1e-9.
6. A `TIMESTAMPS` row has `component` `timestamp_s`, `units` `s`, a null `reference_frame`, and its
   value is its `timestamp_s`.
7. `OVERLAY_2D`: `visibility` is from 0 to 1. A point that is absent on a frame has `x` and `y` null
   and `visibility` 0. A frame that a realtime run skipped has all three null.
8. `BOXES_2D`: one box for each stage and frame. A stage with no box on a frame has all six
   components null. `detector_ran` is 1 when a detector of that stage ran on the frame, else 0.
9. The names of `OVERLAY_2D` of a `keypoint_model` source are `<tracker stage>.<point>`. A reader
   splits them at the first `.`. `<tracker stage>` is the name of a stage of the tracker: a text
   with 1 or more characters and no `.`. It is not a processing stage.
