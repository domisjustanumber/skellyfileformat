# Choices made for G15 that the spec does not give

**Accepted by the user on 2026-11-16 as conventions of the golden folders**
([ADR-2MQE](../decisions/entries/2MQE-tests-prerelease-serial-and-exports.md) item 7). An item is a
rule of the format only where the spec states it. A decision of the same day replaced choice 4 and
the contradictions 1 and 4 ([ADR-XR63](../decisions/entries/XR63-reader-rules-of-the-golden-review.md)).
Each of these items gives its decision.

G15 holds the legacy folders of [SPEC.md Appendix A](../spec/SPEC.md#appendix-a-golden-folders).
`tools/goldgen/g15.py` makes it. The conventions of [G01_CHOICES.md](G01_CHOICES.md) apply and are
not repeated here. Each case is a set of stub files: a reader recognises a legacy folder by file
names, JSON keys, CSV headers and TOML values, so no file holds media or data. Most stub files are
empty. The source of the layouts is the release inventory that
[legacy-annex.md](../spec/legacy-annex.md) names.

## The cases

"Chain" tells the rows of SFF-878 that the case matches. Each `v1` case also has the empty file
`synchronized_videos/Camera_000_synchronized.mp4`, which makes the family `v1` (SFF-877).
`<case>` in a file name is the name of the case folder.

| Case | Stub files (without the MP4 of a `v1` case) | Matched rows | `release_range`, `ambiguous` (scope `full`) |
|---|---|---|---|
| `v1a` | `output_data/recording_parameters.json` with `mediapipe_parameters_model.skip_2d_image_tracking`; `output_data/raw_data/mediapipeBodyWorld_numCams_numFrames_numTrackedPoints_XYZ.npy` | V1a | v1.0.25 to v1.0.34, false |
| `v1b_v1d` | the JSON with `mediapipe_parameters_model`, `run_3d_triangulation` and `run_reprojection_error_filtering`; `output_data/raw_data/mediapipe3dData_numCams_numFrames_numTrackedPoints_reprojectionError.npy` | V1b–V1d | v1.1.0 to v1.3.0, false |
| `v1b_v1c` | as `v1b_v1d`, and `output_data/mediapipe_skeleton_segment_lengths.json` | V1b–V1d, V1b–V1c | v1.1.0 to v1.1.1, false |
| `v1e_v1h` | the JSON with `tracking_parameters_model` and `run_reprojection_error_filtering`; `output_data/raw_data/mediapipe_2dData_numCams_numFrames_numTrackedPoints_pixelXY.npy`; `output_data/mediapipe_body_3d_xyz.csv` with the header `body_nose_x,body_nose_y,body_nose_z` | V1e–V1h' | v1.3.1 to v1.7.4, false |
| `v1f_v1h` | the JSON and the body CSV of `v1e_v1h`; `output_data/mediapipe_skeleton_3d.npy`; `<case>_by_frame.csv` | V1e–V1h', V1f–V1h' | v1.5.0 to v1.7.4, false |
| `v1g_v1h` | as `v1f_v1h`, and `<case>_camera_calibration.toml` with `cam_0.rotation` | the 3 rows to V1g–V1h' | v1.6.0 to v1.7.4, false |
| `v1h` | as `v1g_v1h`, and `cam_0.world_position` in the TOML | the 4 rows to V1h–V1h' | v1.7.0 to v1.7.4, false |
| `v1h_prime` | as `v1g_v1h`, and `metadata.groundplane_calibration` in the TOML, and the column `reprojection_error` in `<case>_by_frame.csv` | the 5 rows to V1h' | v1.7.4 to v1.7.4, false |
| `v1i` | the JSON with `tracking_parameters_model` and `use_triangulate_outlier_rejection` | V1i | v1.8.0 to v1.8.2, false |
| `two_chains` | the files of `v1b_v1d` and of `v1e_v1h` (with `mediapipe_skeleton_3d.npy`), with one JSON that has the keys of the two rows | V1b–V1d, V1e–V1h' | v1.1.0 to v1.7.4, true |
| `no_signal` | none | none | v1.0.25 to v1.8.2, true |
| `v0_0_x` | `SyncedVideos/<case>_synced_Cam1.mp4`; `<case>_config.yaml` | family `pre_v1` | null, false |
| `v0_1_0` | `synchronized_videos/Camera_000.mp4`; `synchronized_videos/timestamps/Camera_000_binary.npy` | family `pre_v1` | null, false |
| `mp4_only` | `clip_a.mp4`; `clip_b.mp4` | family `unknown` | null, false |

## The expected result

| Member | Value | Requirement |
|---|---|---|
| `result_version` | 2 | SFF-885 |
| `folder_state` | `legacy`: the folder has regular files and no file of this format | SFF-875, SFF-888 |
| `folder_warnings` | `[]`: no `.tmp` file, and no file of this format that is alone | SFF-790, SFF-865 |
| `takes` | `[]` | SFF-885 |
| `other_files` | each file of the root and of `synchronized_videos/`, as `not_in_format` with `reason` null, in order of the bytes of the path. A file of another subfolder is not listed | SFF-885, SFF-890 |
| `legacy.family` | `v1`, `pre_v1` or `unknown` | SFF-876, SFF-877 |
| `legacy.eras` | the Era cells of the matched rows, in table order, with `-` | SFF-878, SFF-885 |
| `legacy.release_range`, `legacy.ambiguous` | one chain: the range of the last matched row, false. Two chains: from the lowest first release to the highest last release, true. No row: `["v1.0.25","v1.8.2"]`, true. Not `v1`: null, false | SFF-876, SFF-877, SFF-878 |
| `legacy.warnings` | each warning whose range overlaps the reported range, sorted. Not `v1`: `[]` | SFF-879, SFF-890 |
| `legacy.calibration` | `{"path":"<case>_camera_calibration.toml","state":"present"}` when the case has that file, else `{"path":null,"state":"missing"}`. Not `v1`: null | SFF-880 |
| The scope `player` | `family`, `calibration` and `other_files` do not change. For `v1`: `release_range` `["v1.0.25","v1.8.2"]`, `ambiguous` true, `eras` `[]` and the four warnings. For `pre_v1` and `unknown`, the two results are the same bytes | SFF-892 |

The warnings of the scope `full` are: `v1a`: `legacy_calibration_unverified`,
`legacy_fake_confidence`, `legacy_nonrigid_alignment`. `v1b_v1d`, `v1b_v1c` and `two_chains`:
`legacy_calibration_unverified`, `legacy_marker_order`, `legacy_nonrigid_alignment`. `v1e_v1h` and
`v1f_v1h`: `legacy_calibration_unverified`, `legacy_nonrigid_alignment`. `v1g_v1h`, `v1h`,
`v1h_prime` and `v1i`: `legacy_calibration_unverified`. `no_signal`: the four warnings.

## Choices

1. **Stub content.** Appendix A does not say what a legacy golden folder holds. Choice: stub
   files. A file is empty (0 bytes) when no signal needs its content. Alternative: small real
   media and arrays, which no rule of section 21 reads.
2. **The case names and the rows.** "Layout and cases" gives no row for each case name. Choice:
   `v1e_v1h`, `v1f_v1h` and `v1g_v1h` are the rows V1e–V1h', V1f–V1h' and V1g–V1h'. `v1h` is the
   row V1h–V1h'. `v1h_prime` is the row V1h'. Each case of a chain has the signals of each row
   before it in the chain, because "as X" adds them (SFF-878).
3. **The file of the family `v1`.** SFF-877 gives two signals. Choice: each `v1` case has only
   `synchronized_videos/Camera_000_synchronized.mp4`, with one camera. Alternative: also
   `synchronized_videos/timestamps/Camera_000_synchronized_binary.npy`. No case tests that second
   signal alone: see item 17.
4. **Where a key of `recording_parameters.json` is.** SFF-878 says "has `<key>`" and
   "`mediapipe_parameters_model` with `<key>`". It gives no depth. Choice: each stub has the keys
   where the v1 releases wrote them. `skip_2d_image_tracking` is in `mediapipe_parameters_model`.
   `run_3d_triangulation`, `run_reprojection_error_filtering` and
   `use_triangulate_outlier_rejection` are in `anipose_triangulate_3d_parameters_model`. So a
   reader must find a key at any depth. Alternative: each key in `mediapipe_parameters_model` or
   at the top, which no release wrote. See contradiction 1. Decision (ADR-XR63): the keys of
   SFF-878 in `recording_parameters.json` count at any depth.
5. **The other content of `recording_parameters.json`.** Choice: only the signal keys.
   `mediapipe_parameters_model` and `tracking_parameters_model` are `{}`. The values are free, because a
   signal is the presence of a key: `run_3d_triangulation` is true, and each other value is false. The file has the white
   space of item 13 of G01_CHOICES.md. `mediapipe_skeleton_segment_lengths.json` holds `{}`.
6. **The folder of a file that SFF-878 names without a folder.** Choice, from the annex:
   `output_data/mediapipe_skeleton_segment_lengths.json`, `output_data/mediapipe_skeleton_3d.npy`
   and `output_data/raw_data/mediapipe_2dData_*`.
7. **The full names of the files with `*`.** Choice, from the annex:
   `mediapipeBodyWorld_numCams_numFrames_numTrackedPoints_XYZ.npy`,
   `mediapipe3dData_numCams_numFrames_numTrackedPoints_reprojectionError.npy` and
   `mediapipe_2dData_numCams_numFrames_numTrackedPoints_pixelXY.npy`.
8. **"`mediapipe_skeleton_3d.npy` or `mediapipe_2dData_*`"** (row V1e–V1h'). Choice: `v1e_v1h` has
   only the second file. Each later case of the chain, and `two_chains`, has only the first. So
   the folder tests the two parts of the "or". Alternative: the two files in each case.
9. **The body CSV.** SFF-878 gives no name. Choice, from the annex:
   `output_data/mediapipe_body_3d_xyz.csv`, with the one header line
   `body_nose_x,body_nose_y,body_nose_z`, an LF and no data row.
10. **`<name>_by_frame.csv`.** SFF-878 does not say what `<name>` is. Choice: the name of the case
    folder, in the root. A reader that tests the exact name and a reader that tests
    `*_by_frame.csv` give the same result. The header is the tidy header of the annex:
    `frame,timestamp,timestamp_by_camera,model,keypoint,x,y,z`. For `v1h_prime`,
    `reprojection_error` is the last column. The inventory does not give its position.
11. **The TOML.** Choice: `<case>_camera_calibration.toml`, the exact name of SFF-880, so the state
    is `present`. It holds only `[cam_0]` with `rotation = [ 0.0, 5e-7, -5e-7,]`. The two values
    that are not 0 test the limit 1e-6 of SFF-878 with the two signs. Alternative: three zeros; or
    a value of 1e-6, which depends on how a reader parses the limit. The TOML has no
    `path_to_recorded_videos` and no other member of a real v1 TOML.
12. **The V1h signal.** SFF-878 gives three signals with "or". Choice: `v1h` has `world_position`
    in `[cam_0]`, and `v1h_prime` has `[metadata] groundplane_calibration = false`. The value is
    `false`, because the signal is the presence of the key: a v1.7 folder with no ground-plane
    calibration also has the key. No
    case has the board `name`: see contradiction 2.
13. **The case `v1i`.** Appendix A gives its two JSON keys. Choice: no other era file. Alternative:
    also the files of the row V1e–V1h' (a real V1i folder has them), to show that the missing
    `run_reprojection_error_filtering` alone stops that row.
14. **The case `two_chains`.** Appendix A does not say which chains. Choice: the rows V1b–V1d and
    V1e–V1h'. The range v1.1.0 to v1.7.4 is not the range of `no_signal`, so the two cases test
    different rules. No release wrote such a folder: one `recording_parameters.json` has the keys
    of the two rows. Alternative: V1a and V1i, which gives v1.0.25 to v1.8.2.
15. **The pre-v1 cases.** SFF-876 gives the signals and not the full names. Choice for `v0_0_x`:
    `SyncedVideos/<case>_synced_Cam1.mp4` (git keeps no empty folder) and `<case>_config.yaml`,
    empty. Alternative: `RawVideos/`, or `sessionSettings.txt`. Choice for `v0_1_0`: the two files
    of SFF-876 with `NNN` = `000`.
16. **The case `mp4_only`.** Choice: `clip_a.mp4` and `clip_b.mp4` in the root. Alternative: MP4
    files in `synchronized_videos/` with no `_synchronized` suffix.
17. **Not in G15.** These inputs have no case, because Appendix A names none: a `v1` folder with
    only the timestamps NPY; a TOML with a rotation that is not 0 (the row V1g–V1h' does not
    match); a `v1` folder with the calibration state `ambiguous` (SFT-765 makes its own folders); a
    legacy folder with a pickle; a folder with the signals of `pre_v1` and of `v1`.

## Contradictions and gaps in the texts

1. **SFF-878, row V1b–V1d, against the v1 code.** The row says "`mediapipe_parameters_model` with
   `run_3d_triangulation` and `run_reprojection_error_filtering`". In freemocap v1.1.0 to v1.7.4,
   these two keys are in `anipose_triangulate_3d_parameters_model`
   ([ADR-0WTH](../decisions/entries/0WTH-spec-v2-details-part-12.md), Evidence, for
   `run_reprojection_error_filtering`; the inventory, for the V1a key list). If "with" means
   "inside", no real folder matches the row. The same question applies to the row V1i: the key
   `use_triangulate_outlier_rejection` is not at the top of the file. The spec must say "at any
   depth", or name the object of each key. G15 follows choice 4. Decided: "at any depth" (choice 4).
2. **SFF-878, row V1h–V1h': "a board `name`".** The TOML has no key for the board name. The name is
   in the text of `metadata.charuco_board_object` (`name='7x5 Charuco'`, annex section 4). Each
   camera table of each era has a key `name` (annex section 5). A reader that tests a TOML key
   `name` matches each era. The spec must give the exact test. G15 does not use this signal.
3. **SFF-876 against the inventory, v0.0.x.** SFF-876 says "`<name>_config.yaml` or
   `sessionSettings.txt`". The detection rule of the inventory says "and". Its era table has
   `sessionSettings.txt` only in the first v0.0.x era, and the config YAML in each era. So "or" is
   correct, and G15 uses the config YAML.
4. **SFF-876 and SFF-877: no order.** The spec does not say which family wins when a folder has
   the signals of `pre_v1` and of `v1`. No case of G15 has the two. Decision (ADR-XR63): `v1` wins.
5. **SFF-875 and SFF-888 with SFF-721.** A reader scans only the root and the media folder. The
   spec does not say if a folder whose only regular files are in other subfolders is `legacy` or
   `empty`. Each case of G15 has a file in the root or in `synchronized_videos/`.
6. **`<name>` and "a body CSV".** SFF-878 does not define them (choices 9 and 10). SFF-718 lets a
   legacy read use a glob pattern, and does not say which reads do.
7. **The inventory and the row names.** The detection table of the inventory has one row "V1e-V1h"
   and a separate signal for V1h'. SFF-878 names its rows V1e–V1h' and so on. The case names of
   Appendix A have no mark for the prime (`v1e_v1h`). The meaning is the same.
8. **The v0.1.0 names.** The inventory says that v0.1.0 also wrote
   `output_data/raw_data/mediapipe_2dData_*`, the name of the row V1e–V1h'. This is not a fault:
   the family is decided first, and the era table is only for `v1`.
