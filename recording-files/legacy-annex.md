# Legacy annex: freemocap v1.x recording folders (informative)

Status: **draft v2, for review at gate 1**. This annex is informative. It describes the folders that
freemocap v1.0.25 to v1.8.2 wrote, so that other programs can read old freemocap output
([ADR-CZQ9](decisions/entries/CZQ9-read-old-write-new-and-legacy-recognition.md)). The normative
rules (recognition, the reader result and the warnings) are in [SPEC.md](SPEC.md) section 21. The
rules to read the camera files and the time files of v1 are SFF-896 to SFF-903 of
[Section 21, continued](SPEC.md#section-21-continued-the-camera-files-of-a-v1-folder), and section 9
of this annex gives their background. Pre-v1
layouts (v0.0.x and v0.1.0) are not described: they are not supported. The layout of the freemocap
development code is not described: version 2.0 of the format does not recognise it, and a reader
reports the family `unknown` for it (SPEC.md SFF-877,
[ADR-0XX2](decisions/entries/0XX2-spec-v2-details-part-5.md)).

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
| V1i | v1.8.0 to v1.8.2 | No `reprojection_filtered_*` files. Optional `raw_data/mediapipe_outlier_rejection_normalized_camera_weights.npy`. `recording_parameters.json` has `use_triangulate_outlier_rejection`, `minimum_cameras_for_triangulation`, `maximum_cameras_to_drop` and `target_reprojection_error`. v1.8.0 removed `run_reprojection_error_filtering`, and `tracking_parameters_model` stays. So a V1i folder does not match the row V1e–V1h' of SPEC.md SFF-878: only the row V1i matches ([ADR-0WTH](decisions/entries/0WTH-spec-v2-details-part-12.md) item 30a). |

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
([ADR-CZQ9](decisions/entries/CZQ9-read-old-write-new-and-legacy-recognition.md) item 1,
[ADR-H2HQ](decisions/entries/H2HQ-descriptor-members-deferred-points-and-old-audio.md) item 5,
[ADR-46NQ](../decisions/entries/46NQ-old-recordings-play-as-they-are-no-upgrade-converter.md),
[ADR-A8Y2](../decisions/entries/A8Y2-skellysync-is-the-only-converter-of-old-recordings.md)).

- New skellycam and freemocap keep reading each recording format that freemocap v1.0.25 to v1.8.2
  and the current code write.
- skellycam plays old recordings as they are. It converts no old recording, and it has no legacy
  `<video>` path for old H.264 recordings. It has no "upgrade recording" converter. Its player reads
  the camera files of a v1 folder by SPEC.md SFF-896 to SFF-903.
- skellysync is the only converter of old recordings. It is a conversion writer (SPEC.md section
  1, "writer"). skellycam converts no recording.
- The legacy playback of skellycam does not correct the early audio (9 to 74 ms) of old skellycam
  recordings. It shows a note: the audio of recordings of that era can lead by up to about 74 ms.

## 9. The camera files and the time files of v1

This section is the background of SPEC.md SFF-896 to SFF-903
([ADR-3XYN](decisions/entries/3XYN-v1-camera-file-rules-move-to-recording-files.md)). The rules of
a player, for example its decoders, its routes by codec and its user interface, are not here. For
skellycam they are in `specs/player-legacy.md` of skellycam. The sources are:

- skellycam `dom/legacy-player`, `specs/player-legacy.md`, revision 5 (commit
  c0d61ee107c3c5b9ad203be09bccd21c8dcf619b), sections 2, 3.7 and 6;
- the H.264 study of skellycam, `research/h264_study/part_a/NOTES.md` on `dom/h264-scrub-study`
  (commit 71caa2d0b7dfe576c98e31eed0fc23ed8ffc64cc), sections 11.1 and 12.1;
- the release inventory of section 1 of this annex;
- the FFmpeg 9.0 source, `libavformat/mov.c` (`mov_fix_index`, `mov_seek_stream`), read on
  2026-11-24. Nothing was built or run.

### Where the camera files come from

| Source | Camera files | Time files |
|---|---|---|
| The v1 writer (skellycam 2023.9.1086 to 2025.9.1097, freemocap v1.0.25 to v1.8.2) | `Camera_<NNN>_synchronized.mp4` | `Camera_<NNN>_synchronized_binary.npy` |
| The official FreeMoCap sample data (a 2022 recording in a v1 folder) | old names of the form `sesh_<date>_synced_Cam<N>.mp4` | none |
| The v1 "import videos" wizard (`recording_sessions/import_<name>/`) | each `.mp4` file that the user picked | none |
| v0.1.0 (pre-v1) | `Camera_<NNN>.mp4` | `Camera_<NNN>_binary.npy` |
| v2 alpha builds of freemocap and skellycam | names of the form `<rec>.id-<n>.idx-<n>.mp4` | not described |

The names of the sample data and of an import folder do not end in `_synchronized.mp4`, so the
reader result gives the family `unknown` for such a folder (SFF-877). SFF-896 still reads its camera
files. The time file name rule `<stem>_binary.npy` finds the time files of the v1 writer and of
v0.1.0. FreeMoCap v1 itself finds its videos with `*.mp4` and `*.MP4` in `synchronized_videos/`. The
owner supports only v1: a v2 alpha folder is refused, and a v0.1.0 folder is not refused but has no
support (skellycam spec question Q713, answered as Q740 of 2026-11-25).

### The camera files of the v1 writer

- The codec is MPEG-4 Part 2 (`mp4v`, `esds` object type 0x20), from OpenCV. The GOP is 12 frames,
  with no B-frames. So the decode order is the presentation order. `moov` is at the end of the file.
- The edit list has the media time 0, so M = 0 in SFF-898.
- The rotation is in the pixels. v1 writes no rotation matrix in `tkhd`.
- The frame rate in the header is the median capture rate of the camera. So the header rates of the
  cameras of one recording can differ, and SFF-902 takes their median.
- The v1 synchronizer cuts the cameras to their overlap. So the cameras of one recording have the
  same frame count. A difference comes from an import or from a damaged file (SFF-900).
- An import can be an FFmpeg re-encode to H.264 with the x264 defaults (GOP 250 with B-frames). Then
  the edit list has a media time above 0. This is not verified on a real import.

### The time files

- Each value is `time.perf_counter_ns()` of the capture: a monotonic clock of the recording machine.
  It is not Unix time. Values of two machines, or of two boots of one machine, cannot be compared.
- The cameras of one v1 recording are captured on one machine. The values of the cameras are taken
  to be on one clock. This is not verified in the skellycam v1 code.
- A float64 holds each integer up to 2^53 with no loss: about 104 days of clock time in
  nanoseconds. Above that, the values lose their last digits. The rounding of SFF-897 then gives the
  nearest value that the file holds.
- The v1 synchronizer writes a copy of a frame for a dropped frame, with a repeated time value. So a
  repeated value is a frame, and T_k can stay the same for two or more frames.
- FreeMoCap v1 takes the mean of the times over the cameras (`data_loader.py`). SFF-901 does the
  same, and makes the result never decrease.
- The `_timestamps_human_readable.csv` file holds the same values as text. SFF-897 does not use it.

### Why the frame index is the truth

The v1 synchronizer already matched the frames of the cameras: frame k of each camera is one moment.
The FreeMoCap processing uses the frames by index. So SFF-900 never chooses a frame by its time, and
the times serve only the clock, the labels and the pace. The skellycam player chooses a frame by
its time for a take of this format (`specs/player.md` of skellycam, section 7.3). For a v1 folder it
does not.

### The edit list in FFmpeg

The MP4 demuxer of FFmpeg keeps, in its index, the key frame before the edit start and the frames up
to the next key frame after the edit end. It marks each frame with a CTS outside the edit with
`AV_PKT_FLAG_DISCARD`, so that the frame is dropped after decoding. It then shifts the time stamps,
so that the first kept frame of a video track has the time stamp 0, and it sets the start time to E.
So the time stamps of FFmpeg and of the frame table can differ by a constant. The time stamp of a
MP4 index entry of FFmpeg is the DTS. So SFF-899 finds the entry of each frame by its byte offset,
leaves out the entries marked to discard, and compares the DTS after the subtraction of the DTS of
frame 0. The index of a file cut short still holds each frame, so SFF-899 compares only the frames
below n_c. PyAV 19.0.2 gives these entries as `stream.index_entries`. The skellycam study index kept each
sample and only shifted the time stamps. It did not drop the samples outside the edit. No real v1
file has an edit that cuts frames.
