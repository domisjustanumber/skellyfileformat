# Open work

This file holds the open work of the [decision log](README.md). Read the items that apply to your
task. Delete an item when its work is done. The PR that closes an item records the result.

- **Gate 2: runnable tests and golden folders.** The user accepted the items of
  [ADR-VPD9](entries/VPD9-spec-draft-v2-details.md) and
  [ADR-3D33](entries/3D33-spec-draft-v2-details-folder-files.md) at gate 1 on 2026-11-16. Write the
  runnable tests of [conformance.md](../spec/conformance.md) and the golden folders G1 to G16 of
  SPEC.md Appendix A, and stop for gate 2. G17 waits for the skellysync decisions.
  [ADR-G21H](entries/G21H-gate-2-tests-location-and-interfaces.md) gives the place of the tests, the
  names that they call and the rules of the golden files. The user reviewed G1 ([ADR-94YQ](entries/94YQ-golden-g1-review-decisions.md)): the
  other folders copy its conventions. Also do the repository changes of its item 9:
  `.gitattributes`, the golden generator in `tools/`, and the `golden/` and `tests/` rows and the
  command of the failing run in `AGENTS.md`. The golden folders also get the vectors that
  [ADR-W6HV](entries/W6HV-spec-v2-details-part-3.md) to
  [ADR-72QQ](entries/72QQ-spec-v2-details-part-8.md) add to Appendix A (G8, G9, G11, G12, G13, G15
  and G16). [ADR-0JVZ](entries/0JVZ-spec-v2-details-part-9.md) item 22 gives the layout and the
  cases, with two expected results for each case (the scopes `full` and `player`).
  [ADR-QH61](entries/QH61-spec-v2-details-part-15.md) item 46 gives the tests that this repository
  runs.
- **Complete section 18.3** ([ADR-PVG8](entries/PVG8-spec-v2-details-part-10.md) item 23).
  Exports are not in gate 2, and section 18.3 is provisional
  ([ADR-2MQE](entries/2MQE-tests-prerelease-serial-and-exports.md) item 12). G3 holds no export,
  and SFT-743 has no golden part, until the freemocap exporter is ported and these points are
  decided: one inventory
  for the tall and the wide exports; the snapshot members `revision` and `selection`;
  `float_precision` for float32; the bytes of the NPZ; the texts of the notebook and of the
  READMEs; `<file>` of `calibration_copies/`; and `exported_at` in a golden file. The entry lists
  the facts in which the freemocap code does not agree with section 18.3. Item 3 of
  [ADR-E45D](entries/E45D-spec-draft-v2-corrections-after-review.md) waits with section 18.3
  ([ADR-H2HQ](entries/H2HQ-descriptor-members-deferred-points-and-old-audio.md) item 4): the place
  of the three version members in the export inventory and in the BVH metadata JSON (the spec lists
  them first). It changes one rule of [ADR-9DV4](entries/9DV4-format-version-from-freemocap.md)
  and [ADR-VPD9](entries/VPD9-spec-draft-v2-details.md), so the [Rules](README.md#rules) can need
  an entry that supersedes them.
- **Choices of round 7 of the golden review.** The user must accept or change each choice of
  [ADR-SM53](entries/SM53-choices-for-the-decisions-of-round-7.md) (proposed): the form of version
  2.0 for an unknown `major`; the rows of the reader fit of an unfinished audio file (SFF-784 and
  SFF-792); the new members of the G5 truth files.
- **Absorb the accepted entries into the spec.** The check of 2026-11-16 absorbed 16 entries. Each
  entry of this list stays Active: no absorb document states the rule of its line, or a later entry
  (in brackets) changed the rule and no entry supersedes the old text (the [Rules](README.md#rules)).
  Write the rule in its absorb document, or supersede the entry. Then absorb the entry. Do this
  after the gate 2 review, with one consolidation entry
  ([ADR-H2HQ](entries/H2HQ-descriptor-members-deferred-points-and-old-audio.md) item 6).
  - [ADR-0001](entries/0001-decision-log-agents-md-and-private-data.md) item 2: git tracks only `.claude/skills/` of `.claude/`.
  - [ADR-2C9V](entries/2C9V-whole-take-folder-scope-and-package.md) items 4, 5 and 7: `RECORDING_CONTRACT.md`, `skellyfileformat[write]`, the frame label.
  - [ADR-5XNA](entries/5XNA-folder-layout-names-and-manifest.md) item 8: "by their fixed suffix" ([ADR-0XX2](entries/0XX2-spec-v2-details-part-5.md) item 6a: exact names); the offer of a
    new manifest.
  - [ADR-6RSB](entries/6RSB-camera-files-mjpeg-mkv-and-csv-timing.md) item 5: "only in the MKV and the CSV".
  - [ADR-92TM](entries/92TM-opus-audio-in-fragmented-mp4.md) items 1, 2 and 12: no FLAC, WAV or MCAP audio; libopus and the `av` pin;
    Lichtblick. Item 10 ([ADR-0WTH](entries/0WTH-spec-v2-details-part-12.md) item 36).
  - [ADR-9DV4](entries/9DV4-format-version-from-freemocap.md) items 3 and 9: "N for the Nth prerelease revision" ([ADR-E45D](entries/E45D-spec-draft-v2-corrections-after-review.md) item 3,
    [ADR-0JVZ](entries/0JVZ-spec-v2-details-part-9.md) item 20); the 2.x releases at the same time.
  - [ADR-CZQ9](entries/CZQ9-read-old-write-new-and-legacy-recognition.md) items 1, 3 and 4: the skellycam and freemocap rules for old recordings.
  - [ADR-G1YG](entries/G1YG-writing-crash-reading-and-repair.md) item 7: "a take that it owns" ([ADR-JB3A](entries/JB3A-repair-state-question-and-skellycam-lock.md) item 3).
  - [ADR-KW3G](entries/KW3G-reader-result-for-the-folder.md) items 7 and 8: `folder_files`; a timing sidecar alone ([ADR-Q4BK](entries/Q4BK-spec-v2-details-part-4.md) item 4).
  - [ADR-N6HS](entries/N6HS-info-jsons-and-calibration.md) items 2 and 3: the list of the homes; when a calibration changes.
  - [ADR-P76Y](entries/P76Y-tracking-parquet.md) items 4 and 8: the display rotation; the realtime warning and badge
    ([ADR-ATW0](entries/ATW0-spec-v2-details-part-6.md) item 11, [ADR-E45D](entries/E45D-spec-draft-v2-corrections-after-review.md) item 5).
  - [ADR-Q9X2](entries/Q9X2-realtime-tracking-journal.md) items 2 and 5: the journal node; the fold at start-up ([ADR-1HH0](entries/1HH0-lock-startup-repair-and-reader-model-check.md) item 2).
  - [ADR-T8PK](entries/T8PK-privacy-notice-and-no-code-in-files.md) item 3: the notice at an export or a share.
  - [ADR-VPD9](entries/VPD9-spec-draft-v2-details.md): item 2 ([ADR-E45D](entries/E45D-spec-draft-v2-corrections-after-review.md) item 3); item 6, the flag bits ([ADR-W6HV](entries/W6HV-spec-v2-details-part-3.md) item 2d); item
    12, the repair line ([ADR-ATW0](entries/ATW0-spec-v2-details-part-6.md) item 13) and the lock ([ADR-1HH0](entries/1HH0-lock-startup-repair-and-reader-model-check.md) item 1).
  - [ADR-3D33](entries/3D33-spec-draft-v2-details-folder-files.md) items 4 and 5: the TOML that the manifest names ([ADR-0XX2](entries/0XX2-spec-v2-details-part-5.md) item 6b);
    `charuco_detector:<board>` ([ADR-6VRQ](entries/6VRQ-spec-v2-details-part-13.md) item 37).
  - [ADR-G21H](entries/G21H-gate-2-tests-location-and-interfaces.md): item 2 ([ADR-0JVZ](entries/0JVZ-spec-v2-details-part-9.md) item 21); items 1, 4 to 6 and 10 wait for the gate 2 work.
  - [ADR-Q4BK](entries/Q4BK-spec-v2-details-part-4.md) item 4d: a manifest with no `take_uuid` ([ADR-PVG8](entries/PVG8-spec-v2-details-part-10.md) item 25: `bad_schema`).
  - [ADR-0XX2](entries/0XX2-spec-v2-details-part-5.md) items 6c and 8: "one part for each pair of files" ([ADR-0WTH](entries/0WTH-spec-v2-details-part-12.md) item 31); the fold
    "only after `state` is `finished`" ([ADR-1HH0](entries/1HH0-lock-startup-repair-and-reader-model-check.md) item 2).
  - [ADR-DM9S](entries/DM9S-spec-v2-details-part-7.md) item 14: the scope of the JavaScript reader ([ADR-0JVZ](entries/0JVZ-spec-v2-details-part-9.md) item 21).
  - [ADR-E68K](entries/E68K-camera-match-repair-order-and-g5-g6-files.md) item 3: "never half repaired"; [ADR-7JJJ](entries/7JJJ-audio-repair-refused-header-values-and-the-rules-of-w5ak.md) item 5:
    "only when the folder has no take" ([ADR-158N](entries/158N-details-for-the-decisions-of-round-3.md) items 12 and 13).
- **Provisional parts of spec draft v2.** Close each of them before v2.0.0:
  - SFF-752 (Q107, [ADR-2MQE](entries/2MQE-tests-prerelease-serial-and-exports.md) item 11): the
    source and the text form of `port_path` and `os_device_id` on each OS are not
    decided ([ADR-70VP](entries/70VP-camera-identity-forms-and-remembered-keys.md) item 1). They wait for these tests on Windows, Linux and macOS: a reboot, a replug
    to the same port, a move to another port, and two identical cameras. No test ran on Linux or
    macOS;
  - SFF-756, bit 1 `filled`: its meaning waits for the slot assembly of the skellycam plan, row 2.2,
    and for desk tests DT4 and DT7. A writer of version 2.0 writes 0 to it
    ([ADR-W6HV](entries/W6HV-spec-v2-details-part-3.md) item 2c);
  - SFF-757: the live byte offsets of the video sidecar wait for desk test DT5;
  - SFF-771 and the `audio_latency_ns` key: wait for the microphone latency test (A3 of the skellycam
    plan);
  - SFF-773: the `clock` values `linux_monotonic` and `macos_uptime_raw` wait for the Linux and macOS
    timing tests (T-S7);
  - SFF-788: the fsync interval waits for a measurement of its cost;
  - SFF-797: the repair of a camera file waits for desk test DT-R1 (what a killed PyAV MKV holds, and
    what Blender, FFmpeg and the player read from it);
  - SFF-846: the journal waits for the on/off load test and the kill test with real data (DT11);
  - SFF-848: the `.blend` scene contents are future freemocap work;
  - SFF-862, SFF-863 and G17: skellysync folders wait for the skellysync decisions D-Q, D-FPS,
    D-HDR, D-DRIFT and D-AUDIO;
  - G5 and G6: the stand-in for the killed camera file waits for desk tests DT-R1 and DT5
    ([ADR-G21H](entries/G21H-gate-2-tests-location-and-interfaces.md) item 6).
- **Open points of the model types of the Parquet descriptor**
  ([ADR-W5JC](entries/W5JC-nested-model-types-in-the-descriptor-part.md)). They wait for the
  freemocap `sfn26` port. The spec keeps its text until then
  ([ADR-H2HQ](entries/H2HQ-descriptor-members-deferred-points-and-old-audio.md) item 3).
  - `tracker_connections`: no code of freemocap `sfn26` checks that each name is in
    `tracker_keypoint_names` (SFF-832).
  - `tracker_connections` has the mark **v2**. `object_geometry` and `tracker_stage_path` have only
    "From `sfn26`". The three members have the same origin.
  - `segment_topology` (SFF-832): no code has this member. freemocap at c27fc299 and at `sfn26`
    refuses it. [ADR-6VRQ](entries/6VRQ-spec-v2-details-part-13.md) item 38a gives its values.
  - `joint_angle_names` of `ReconstructionSourceDefinition`: c27fc299 has exactly 3 names for each
    joint, and `sfn26` has any number. `EulerConvention.angle_names` has exactly 3 at the two commits.
  - `sequence` of `EulerConvention`: the code also accepts upper-case letters. The part says `x`,
    `y` or `z`.
  - A mapping entry of `TrackerMappingSnapshot`: the code loads an object with any members.
  - The code also accepts the absence of `tags` and `angle_names`. Their rows give no default, so
    the reader refuses a file without them ([ADR-158N](entries/158N-details-for-the-decisions-of-round-3.md) item 5).
  - freemocap `sfn26` names skellyforge and skellytracker by branch, with no commit. The `sfn26`
    form of the types has no pin.
  - No class checked a whole model with the `sfn26` and **v2** members. The example of the part has
    none of them.
  - The code gives no meaning or rule for `feature_names`, `segment_name` and `source_mesh_units` of
    `RigidObjectGeometry`, for `tracker_stage_path`, for the units of `LandmarkSnapshot.position`, or
    for the relation of `known_tracker_keypoints` to `tracker_keypoint_names`.
- **Desk tests that the decisions name.** A kill during a replace on Windows
  ([ADR-G1YG](entries/G1YG-writing-crash-reading-and-repair.md) item 10); the 2D pixel origin and
  centre convention (DT-K3; no convention was found in freemocap or skellytracker); the Blender addon
  on an MKV take (DT-B3; the addon filters `.mp4` today) and its rotation of the video planes from
  `display_rotation` (DT-B4).
- **Code changes that the spec needs (a list for the user; not applied).** skellycam: the CSV
  sidecar writer, the Opus fMP4 writer, the manifest writer, the new capture info JSON (written at the
  start and the end, whole), no glob of `*_info.json`, no `synchronized_videos_README.md`, and labels
  from `camera_key`. freemocap: `recording_id` = `<rec>` in place of the folder name
  (`parquet_writer.py:44-45`, `recording_view.py:46-47`), the descriptor v2 fields, the value columns
  and encodings, `int32` in place of `int64` for the Parquet columns `frame_number` and `run_id` (the
  reader must also accept `int64` from older files), whole-file TOML writes and a new `calibration_uuid` for each geometry change, no copy
  of the capture JSON in `<rec>_recording_info.json`, the reader through the manifest, the realtime
  journal node, and the names of `RECORDING_CONTRACT.md` and `shared/recording-contract/paths.json`.
  The Blender addon: MKV video planes, the `blender/` outputs and no pickle. freemocap and the addon:
  `format_version`, `format_prerelease` and `writer` in the export inventory and in the BVH metadata
  JSON, and `run-<N>` in the name of each file of a run other than 0
  ([ADR-E45D](entries/E45D-spec-draft-v2-corrections-after-review.md) items 3 and 4). From the
  details of 2026-11-16: skellycam takes `.processing.lock` for each write of the manifest, and
  writes the flag `repeat`, the identity string of SFF-752 and `media_cut_bytes` in a repair line.
  freemocap removes `selected_run_id` from the descriptor, writes `calibration_uuid_before` and
  `calibration_uuid_after` in `CalibrationUpdateRequest`, writes `coverage.events`, starts the fold
  only after `state` is `finished`, folds no journal and repairs no file at start-up before the user
  agrees ([ADR-1HH0](entries/1HH0-lock-startup-repair-and-reader-model-check.md)), rewrites the times of a realtime run after a repair, and writes
  `version` 5 in the export inventory. From
  [ADR-JB3A](entries/JB3A-repair-state-question-and-skellycam-lock.md): skellycam also takes
  `.processing.lock` for each write of the capture info JSON, the repair sets the manifest `state`
  to `finished`, and freemocap asks one time for the whole take, also before it folds a left-over
  journal of a finished take. From the details of parts 9 to 15: each writer writes
  `format_prerelease` 1; the repair writes the manifest again
  ([ADR-YYE3](entries/YYE3-spec-v2-details-part-11.md) item 26a); freemocap writes the summary
  values of [ADR-PVG8](entries/PVG8-spec-v2-details-part-10.md) item 24, `data_records` in the
  journal end record, the `coverage` values, the integer group time, `segment_topology`, the source
  `charuco_detector:<squares_x>x<squares_y>` and different joint angle names
  ([ADR-6VRQ](entries/6VRQ-spec-v2-details-part-13.md),
  [ADR-N6KY](entries/N6KY-spec-v2-details-part-14.md)). The readers get the `scope` argument and the
  `--records` switch ([ADR-0JVZ](entries/0JVZ-spec-v2-details-part-9.md) item 21). From
  [ADR-70VP](entries/70VP-camera-identity-forms-and-remembered-keys.md): skellycam reads the serial, the port path and the OS device identifier from the OS, not
  from the capture library. Its backend owns a store of remembered cameras: not browser storage,
  and not deleted when a camera is unplugged. skellycam asks the user with a live preview, lets
  the user name a camera, and imports remembered cameras from a take folder. freemocap binds a
  calibration by `camera_key`. From [ADR-94YQ](entries/94YQ-golden-g1-review-decisions.md) item 6: freemocap must run the calibration geometry
  check before the question about cameras that the OS cannot tell apart, and list the most likely
  candidates first. From [ADR-B6WH](entries/B6WH-repair-equal-pair-cut-and-no-normal-end.md): the
  repair of skellycam and freemocap cuts a camera pair to equal rows and blocks, cuts a sidecar at
  its first bad row, appends nothing to a media file and writes its own name as the `source` of
  `camera_gap`. From [ADR-7JJJ](entries/7JJJ-audio-repair-refused-header-values-and-the-rules-of-w5ak.md)
  item 2: the repair also cuts the audio sidecar to the blocks whose every sample is in the cut
  audio file. From [ADR-2MQE](entries/2MQE-tests-prerelease-serial-and-exports.md): skellycam
  gives an assigned key to a new camera with the key of a remembered camera. From
  [ADR-E68K](entries/E68K-camera-match-repair-order-and-g5-g6-files.md) and
  [ADR-H2HQ](entries/H2HQ-descriptor-members-deferred-points-and-old-audio.md): skellycam finds
  the candidates of a remembered camera by SFF-752; the repair does each step for the whole take;
  the legacy playback of skellycam does not correct the early audio of old recordings and shows a
  note that it can lead by up to about 74 ms.
- **Permalinks to the skellycam evidence.** The new entries cite skellycam `dom/research` files as
  plain paths. Many of them are not committed yet. Change them to full-SHA permalinks after that
  branch is committed and pushed.
- **Cross-platform test tools.** At the end of this work, draft minimal one-off scripts that a
  person runs by hand on Linux and macOS (camera identity, clocks, golden bytes, the lock, capture
  and repair). The list is in skellycam `research/CAPTURE_AND_RECORDING_PLAN.md`, section 4.1.
- **Idea for a later minor version (no decision).** A journal record type `frame`
  (`frame_number`, `processed_ns`): "the pipeline took this frame"
  ([ADR-1P4N](entries/1P4N-timing-coverage-of-a-realtime-run-and-latency-at-the-fold.md)).
- **Side note (no decision): stale input signatures.** The posthoc code of freemocap puts a
  signature of the times into the input signatures of each stage. If the fold copies that, a repair
  that rewrites the times of a realtime run leaves those signatures stale. No rule covers it.
