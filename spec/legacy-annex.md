# Legacy annex: freemocap v1.x recording folders (informative)

Status: **draft v2, for review at gate 1**. This annex is informative. It describes the folders that
freemocap v1.0.25 to v1.8.2 wrote, so that other programs can read old freemocap output
([ADR-CZQ9](../decisions/entries/CZQ9-read-old-write-new-and-legacy-recognition.md)). The normative
rules (recognition, the reader result and the warnings) are in [SPEC.md](SPEC.md) section 21. Pre-v1
layouts (v0.0.x and v0.1.0) are not described: they are not supported. The layout of the freemocap
development code is not described: version 2.0 of the format does not recognise it, and a reader
reports the family `unknown` for it (SPEC.md SFF-877,
[ADR-0XX2](../decisions/entries/0XX2-spec-v2-details-part-5.md)).

The source is an inventory of the 87 freemocap releases and the pinned skellycam, skellytracker and
skellyforge versions: skellycam `dom/research`,
`research/skellycam_recording/docs/legacy_release_inventory_20261115.md` (local, not committed). A
file path in this annex is relative to the recording folder. No release writes its version number
into a recording.

## 1. Where v1 writes recordings

- The base folder is `~/freemocap_data/`. From v1.2.0, the user can change it.
- A recording is `recording_sessions/session_<YYYY-MM-DD_HH_MM_SS>/<recording name>/`. There is one
  session folder for each start of the app.
- The recording name is `recording_<HH_MM_SS>_gmt<±H>`, with `_calibration` for a calibration
  recording and `__<user tag>` for a user tag. The GMT offset is cut to whole hours, so +5:30 is
  written `gmt+5`.
- Imported videos are in `recording_sessions/import_<source folder name>/`, with no session level.
- Calibrations are also saved to `calibrations/<name>_camera_calibration.toml` and
  `logs_info_and_settings/last_successful_calibration.toml` of the base folder.

## 2. Files that skellycam wrote (all v1 releases)

| File | Content |
|---|---|
| `synchronized_videos/Camera_<NNN>_synchronized.mp4` | MPEG-4 Part 2 (`mp4v`) in MP4. BGR frames, optionally rotated at capture. The frame rate is the median rate of the camera, so cameras can differ. `<NNN>` is the position among the cameras that recorded a frame, not the OS device number. |
| `synchronized_videos/timestamps/Camera_<NNN>_synchronized_binary.npy` | 1-D float64: one `time.perf_counter_ns()` value for each written frame, on the monotonic clock of the machine (not Unix time, not relative to the start). A repeated value marks a duplicated frame. |
| `synchronized_videos/timestamps/Camera_<NNN>_synchronized_timestamps_human_readable.csv` | The same values, written by pandas with the header `,0`. |
| `synchronized_videos/timestamp_diagnostic_plots.png`, `first_and_last_frames.png` | Windows only. |

Synchronisation: the cameras are cut to their overlap, and the camera with the fewest frames is the
reference. Each other camera gets its nearest frame. Duplicated frames are written with no mask.
Neither the device ID nor the rotation setting is saved.

## 3. Files that freemocap wrote (era V1a, v1.0.25 to v1.0.34)

Era V1a also holds the tag `1.1.0` (with no `v`). That tag is v1.0.34 with one more log line. It is
not the release v1.1.0, which starts era V1b.

| File | Content |
|---|---|
| `annotated_videos/Camera_<NNN>_synchronized_mediapipe.mp4` | `mp4v`, at the source frame rate |
| `output_data/raw_data/mediapipe2dData_numCams_numFrames_numTrackedPoints_pixelXY.npy` | [camera, frame, 553, 3]. Marker order: body 33, right hand 21, left hand 21, face 478. NaN where not detected. Channel 2 is the MediaPipe z × image width, not a confidence. |
| `output_data/raw_data/mediapipeBodyWorld_numCams_numFrames_numTrackedPoints_XYZ.npy` | Pose world landmarks scaled by the pixel size. The scale has no meaning. V1a only. |
| `output_data/raw_data/mediapipe3dData_numFrames_numTrackedPoints_spatialXYZ.npy` | [frame, marker, xyz]: raw triangulation in the calibration world frame, mm |
| `output_data/raw_data/mediapipe3dData_numFrames_numTrackedPoints_reprojectionError.npy` | [frame, marker]: the mean pixel error over the cameras |
| `output_data/mediaPipeSkel_3d_body_hands_face.npy` | The raw 3D rotated to (x, z, −y), then gap-filled, Butterworth-filtered (fs 30, cutoff 7, order 4) and cleaned |
| `output_data/center_of_mass/segmentCOM_frame_joint_xyz.npy`, `total_body_center_of_mass_xyz.npy` | [frame, segment, xyz] and [frame, xyz] |
| `output_data/mediapipe_{body,right_hand,left_hand,face}_3d_xyz.npy` and `.csv` | The CSV columns are `nose_x, nose_y, nose_z, …`, `right_hand_wrist_x, …`, `left_hand_…` and `face_0000_x, …` |
| `output_data/mediapipe_skeleton_segment_lengths.json`, `mediapipe_names_and_connections_dict.json` | Segment lengths; names and connections (integer index pairs) |
| `output_data/recording_parameters.json` | The processing parameters: `mediapipe_parameters_model`, `anipose_triangulate_3d_parameters_model`, `post_processing_parameters_model` |
| `<name>_by_frame.json`, `<name>_by_trajectory.csv`, `<name>_frame_name_xyz.npy` | `by_frame.json` is `{"info": {segment_lengths, schemas}, "data_by_frame": {…}}`. `by_trajectory.csv` has `timestamp` (the mean perf_counter ns), `timestamp_by_camera` (a dict as text), then `<point>_x/_y/_z`. |
| `<recording name>_camera_calibration.toml` | See section 5 |
| `<name>.blend`, `<name>.ipynb` | Optional |

## 4. Changes by era

SPEC.md SFF-878 gives the signals of each era, the chains of the rows and the rule for the release
range that a reader reports.

| Era | Releases | Changes from the era before |
|---|---|---|
| V1b | v1.1.0 | 2D from skellytracker. No `mediapipeBodyWorld` file. New `raw_data/mediapipe3dData_numCams_numFrames_numTrackedPoints_reprojectionError.npy` [camera, frame, marker]. Optional `reprojection_filtered_*` files. `recording_parameters.json` keys `run_image_tracking`, `run_3d_triangulation`, `run_reprojection_error_filtering`. **Defect:** skellytracker orders pose, face, left hand, right hand, but freemocap splits body, right, left, face, so the hand and face outputs are mislabelled. |
| V1c | v1.1.1 | The marker order is fixed (body, right hand, left hand, face). Same files as V1b. |
| V1d | v1.2.0 to v1.3.0 | No `mediapipe_skeleton_segment_lengths.json` |
| V1e | v1.3.1 to v1.4.7 | Tracker-prefixed names: `raw_data/mediapipe_2dData_…`, `raw_data/mediapipe_3dData_…`, `output_data/mediapipe_skeleton_3d.npy`, `output_data/mediapipe_rigid_bones_3d.npy`, `center_of_mass/mediapipe_*`. The body CSV columns become `body_nose_x, …`. No `mediapipe_names_and_connections_dict.json`. `recording_parameters.json` has `tracking_parameters_model` and `tracking_model_info`. |
| V1f | v1.5.0 to v1.5.4 | New `<name>_by_frame.csv` in tidy form: `frame, timestamp, timestamp_by_camera, model, keypoint, x, y, z` |
| V1g | v1.6.0 to v1.6.3 | Calibration: all extrinsics are rotated and shifted into the frame of camera 0, so `cam_0` has rotation ≈ 0 and translation ≈ 0 (SPEC.md SFF-878 gives the limit of the signal: 1e-6 for each rotation value). Before, only the translations were shifted, which is not a rigid transform. The video paths are sorted. |
| V1h | v1.7.0 to v1.7.3 | The 90° rotation about x is applied only to single-camera data. Multi-camera outputs stay in the calibration frame. The TOML gains `world_orientation` and `world_position` for each camera and `[metadata] groundplane_calibration`. The board text has a `name`. Optional `output_data/charuco_3d_xyz.npy` [frame, corner, xyz]. |
| V1h' | v1.7.4 | `<name>_by_frame.csv` gains a `reprojection_error` column |
| V1i | v1.8.0 to v1.8.2 | No `reprojection_filtered_*` files. Optional `raw_data/mediapipe_outlier_rejection_normalized_camera_weights.npy`. `recording_parameters.json` has `use_triangulate_outlier_rejection`, `minimum_cameras_for_triangulation`, `maximum_cameras_to_drop` and `target_reprojection_error`. v1.8.0 removed `run_reprojection_error_filtering`, and `tracking_parameters_model` stays. So a V1i folder does not match the row V1e–V1h' of SPEC.md SFF-878: only the row V1i matches ([ADR-0WTH](../decisions/entries/0WTH-spec-v2-details-part-12.md) item 30a). |

Single-camera recordings (all eras) need no calibration. Their 3D is the 2D pixels projected to a z
plane, with a reprojection error of zero, then rotated.

## 5. The v1 calibration TOML

- Camera tables `[cam_<i>]` with `name` (the video stem, for example `Camera_000_synchronized`),
  `size` [width, height], `matrix`, `distortions`, `rotation` and `translation`.
- `[metadata]`: `charuco_square_size` (mm; default 39), `charuco_board_object` (the text of a
  `CharucoBoardDefinition`, with a memory address), `path_to_recorded_videos` (an absolute path) and
  `date_time_calibrated` (UTC with no zone mark). The board is 7 × 5, dictionary 4x4_250, marker length
  0.8 × the square.
- A loader sorts the camera keys as text, so `cam_10` comes before `cam_2`.
- In a motion-capture recording, the TOML can be missing, can have the name of another recording, or
  can be `last_successful_calibration.toml`. It is not certain to be the calibration that made the
  3D data. Which TOML was used is not recorded. SPEC.md SFF-880 gives the lookup rule of a reader
  and the result member `legacy.calibration`, with the state `present`, `missing` or `ambiguous`.
- Units are mm when the square size was entered in mm. A square size of 1 gives board units.

## 6. Other quirks

- Before v1.6.0, calibration and 2D tracking took the videos in the order of an unsorted file
  listing. On a file system that is not NTFS, the camera order of the calibration and of the 2D array
  can differ.
- Face: 478 slots. MediaPipe Holistic without refinement gives 468. In v1.0.25 the last 10 face
  columns are NaN. In skellytracker output they are 0.
- Calibration recordings have `_calibration` in their name and no `output_data`, except the optional
  ChArUco array of V1h and later.
- Diagnostic PNGs are written on Windows only.

## 7. Blender addon outputs (v1)

From the installed addon 2026.4.1041 only. The outputs of each pinned version are not verified.

`<name>.blend`, `output_data/joint_angles.{csv,npy}`, `saved_data/` (a README, info, NPY, CSV and
`<name>_bone_and_joint_data.csv`), `video_export/…mp4`, `video_export/render_cameras/…`,
`<name>_video_output.mp4`, and optionally `3d_models/` (FBX and BVH).

## 8. Old recordings in skellycam and freemocap

These are rules of the programs, not of the format
([ADR-CZQ9](../decisions/entries/CZQ9-read-old-write-new-and-legacy-recognition.md) items 1, 3 and
4, [ADR-H2HQ](../decisions/entries/H2HQ-descriptor-members-deferred-points-and-old-audio.md) item 5).

- New skellycam and freemocap keep reading each recording format that freemocap v1.0.25 to v1.8.2
  and the current code write.
- skellycam plays old H.264 recordings through a legacy `<video>` path. It also gives an explicit
  "upgrade recording" conversion, for the other old files and on request.
- skellycam owns the converter. The converter uses `skellyfileformat[write]`.
- The legacy playback of skellycam does not correct the early audio (9 to 74 ms) of old skellycam
  recordings. It shows a note: the audio of recordings of that era can lead by up to about 74 ms.
