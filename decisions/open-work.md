# Open work

This file holds the open work of the [decision log](README.md). Read the items that apply to your
task. Delete an item when its work is done. The PR that closes an item records the result.

- **Gate 2: runnable tests and golden folders.** The user accepted the items of
  [ADR-VPD9](entries/VPD9-spec-draft-v2-details.md) and
  [ADR-3D33](entries/3D33-spec-draft-v2-details-folder-files.md) at gate 1 on 2026-11-16. Write the
  runnable tests of [conformance.md](../spec/conformance.md) and the golden folders G1 to G16 of
  SPEC.md Appendix A, and stop for gate 2. G17 waits for the skellysync decisions.
  [ADR-G21H](entries/G21H-gate-2-tests-location-and-interfaces.md) gives the place of the tests, the
  names that they call and the rules of the golden files. Write the expected reader result of G1
  first, and stop for the approval of the user. Also do the repository changes of its item 9:
  `.gitattributes`, the golden generator in `tools/`, and the `golden/` and `tests/` rows and the
  command of the failing run in `AGENTS.md`. The golden folders also get the vectors that
  [ADR-W6HV](entries/W6HV-spec-v2-details-part-3.md) to
  [ADR-72QQ](entries/72QQ-spec-v2-details-part-8.md) add to Appendix A (G8, G9, G11, G12, G13, G15
  and G16). [ADR-0JVZ](entries/0JVZ-spec-v2-details-part-9.md) item 22 gives the layout and the
  cases, with two expected results for each case (the scopes `full` and `player`).
  [ADR-QH61](entries/QH61-spec-v2-details-part-15.md) item 46 gives the tests that this repository
  runs.
- **Choices made for G1 that the spec does not give.** [golden/G01_CHOICES.md](../golden/G01_CHOICES.md) holds the numbered list: 29 choices of the
  golden generator, and 5 points where the spec and the pinned tools do not agree. The user must
  decide each before the other golden folders copy G1. The list is not here, because this file
  has a size limit.
- **Points that the user did not decide on 2026-11-16** (the review of parts 9 to 15).
  - The value of `format_prerelease` after the user sends the draft to external review. It is 1
    until then (SFF-710, [ADR-0JVZ](entries/0JVZ-spec-v2-details-part-9.md) item 20).
- **Points that the camera identity review leaves open** ([ADR-70VP](entries/70VP-camera-identity-forms-and-remembered-keys.md)). The user must decide each.
  - The detail of a usable serial (SFF-752, provisional). The research code
    (`camera_identity.py`) proposes the placeholder list, the characters 0x21 to 0x7F with no `,`,
    and no serial of one repeated character. The user saw only the three conditions.
  - The `device` member that is the "model name from the OS": `model` or `os_name`.
  - The key of a camera whose computed key is the key of a remembered camera, when the user says
    that it is a new camera. The research proposes form 4.
  - SFT-717: `device.serial` can be not null and not usable for a reason that the file does not
    show. The test then cannot find the form of a `computed` key.
  - Does a reader check `key_origin`?
- **Complete section 18.3** ([ADR-PVG8](entries/PVG8-spec-v2-details-part-10.md) item 23). G3
  holds no export, and SFT-743 has no golden part, until these points are decided: one inventory
  for the tall and the wide exports; the snapshot members `revision` and `selection`;
  `float_precision` for float32; the bytes of the NPZ; the texts of the notebook and of the
  READMEs; `<file>` of `calibration_copies/`; and `exported_at` in a golden file. The entry lists
  the facts in which the freemocap code does not agree with section 18.3.
- **Points that the details of parts 9 to 15 leave open.** The user must decide each of them.
  - The `source` of the warning `camera_gap` that a repair adds to the manifest (SFF-727, SFF-793).
  - A folder that holds only a TOML, a Parquet or a journal of this format: for the scope `player`
    the file has no mark (SFF-892). Is `folder_state` then `unreadable`, as for `full`, or `legacy`
    (SFF-875, SFF-888)?
  - `README.md` says that `format_prerelease` is "N for the Nth prerelease revision". SFF-710 now
    says 1 for each internal draft. The README needs the same rule.
  - SFT-763 takes G5 and G6 as inputs for the row-count part of `frames`. Appendix A does not say
    which folder files G5 and G6 hold.
- **Open points of [ADR-E45D](entries/E45D-spec-draft-v2-corrections-after-review.md).**
  [ADR-72QQ](entries/72QQ-spec-v2-details-part-8.md) item 19 closed the other points. The user
  must decide each of these. The spec holds the smallest text until then.
  - Item 3: the place of the three members in the export inventory and in the BVH metadata JSON (the
    spec lists them first).
  - Item 3 changes one rule of [ADR-9DV4](entries/9DV4-format-version-from-freemocap.md) and
    [ADR-VPD9](entries/VPD9-spec-draft-v2-details.md). The [Rules](README.md#rules) can need an
    entry that supersedes them.
- **Points that the accepted details of 2026-11-16 leave open.** The user must decide each of them.
  - The `role` of the `folder_files` item of `calibration.file`: the manifest roles have no role for
    the calibration TOML.
  - The place and the reason of a timing sidecar alone whose `take_uuid` the reader cannot read.
  - The place of a folder file that the manifest lists and that holds another `take_uuid`:
    `folder_files` with a `take_uuid` mismatch, or `other_files` (SFF-889).
- **Absorb the accepted entries into the spec.** The check of 2026-11-16 absorbed 16 entries. Each
  entry of this list stays Active, because no absorb document states the rule that the line gives,
  or because a later entry changed the rule and no entry supersedes the old text
  (the [Rules](README.md#rules)). Write the rule in its absorb document, or supersede the entry.
  Then absorb the entry.
  - [ADR-0001](entries/0001-decision-log-agents-md-and-private-data.md) item 2: git tracks
    `.claude/skills/` and ignores the other files of `.claude/`.
  - [ADR-2C9V](entries/2C9V-whole-take-folder-scope-and-package.md): item 4 (`RECORDING_CONTRACT.md`
    of freemocap points to the spec), item 5 (the write layer `skellyfileformat[write]`) and item 7
    (the player draws the frame label, a skellycam rule).
  - [ADR-5XNA](entries/5XNA-folder-layout-names-and-manifest.md) item 8: the rebuild "by their
    fixed suffix". [ADR-0XX2](entries/0XX2-spec-v2-details-part-5.md) item 6a changed it to exact
    names. Also "A program can offer to write a new manifest".
  - [ADR-6RSB](entries/6RSB-camera-files-mjpeg-mkv-and-csv-timing.md) item 5: the actual
    resolution, rate and frame count are "only in the MKV and the CSV" (the rule of the homes).
  - [ADR-92TM](entries/92TM-opus-audio-in-fragmented-mp4.md): item 1 (no FLAC, WAV or MCAP audio),
    item 2 (libopus through PyAV, with the version of the `av` pin) and item 12 (Lichtblick).
    [ADR-0WTH](entries/0WTH-spec-v2-details-part-12.md) item 36 changed item 10.
  - [ADR-9DV4](entries/9DV4-format-version-from-freemocap.md): item 3 ("each file", and "N for the
    Nth prerelease revision"). [ADR-E45D](entries/E45D-spec-draft-v2-corrections-after-review.md)
    item 3 and [ADR-0JVZ](entries/0JVZ-spec-v2-details-part-9.md) item 20 changed it. Item 9 (the
    release of freemocap 2.x and skellycam 2.x at the same time) is in no absorb document.
  - [ADR-CZQ9](entries/CZQ9-read-old-write-new-and-legacy-recognition.md) items 1, 3 and 4: the
    skellycam and freemocap rules (the old formats that they read, the legacy `<video>` path, the
    "upgrade recording" conversion and the converter).
  - [ADR-G1YG](entries/G1YG-writing-crash-reading-and-repair.md) item 7: "a take that it owns".
    [ADR-JB3A](entries/JB3A-repair-state-question-and-skellycam-lock.md) item 3 changed it.
  - [ADR-KW3G](entries/KW3G-reader-result-for-the-folder.md): item 7 (a folder file is now in
    `folder_files`) and item 8 ("its files of the kind `camera`": a timing sidecar alone does not
    count). [ADR-Q4BK](entries/Q4BK-spec-v2-details-part-4.md) item 4 changed them.
  - [ADR-N6HS](entries/N6HS-info-jsons-and-calibration.md): item 2 (the list of the homes: "the
    MKV and the CSV only") and item 3 (a calibration changes only when the setup changes; to keep
    the calibration take is optional and advised).
  - [ADR-P76Y](entries/P76Y-tracking-parquet.md): item 4 ("freemocap rotates them for display")
    and item 8 (the warning text and the badge of the UI; the rule that posthoc never replaces a
    realtime run). [ADR-ATW0](entries/ATW0-spec-v2-details-part-6.md) item 11 and ADR-E45D item 5
    changed item 8.
  - [ADR-Q9X2](entries/Q9X2-realtime-tracking-journal.md): item 2 (the journal writer is a node of
    its own, a freemocap rule) and item 5 ("At start-up, freemocap folds each journal that it
    finds"). [ADR-1HH0](entries/1HH0-lock-startup-repair-and-reader-model-check.md) item 2 changed
    item 5.
  - [ADR-T8PK](entries/T8PK-privacy-notice-and-no-code-in-files.md) item 3: freemocap shows the
    notice when a user exports or shares a take.
  - [ADR-VPD9](entries/VPD9-spec-draft-v2-details.md): item 2 (ADR-E45D item 3 changed it), item 6
    (the flag bits: [ADR-W6HV](entries/W6HV-spec-v2-details-part-3.md) item 2d) and item 12 (the
    repair line: ADR-ATW0 item 13; the lock: ADR-1HH0 item 1).
  - [ADR-3D33](entries/3D33-spec-draft-v2-details-folder-files.md): item 4 ("A reader uses only the
    TOML that the manifest names": ADR-0XX2 item 6b added an exception) and item 5
    (`charuco_detector:<board>`: [ADR-6VRQ](entries/6VRQ-spec-v2-details-part-13.md) item 37).
  - [ADR-G21H](entries/G21H-gate-2-tests-location-and-interfaces.md): item 2 (ADR-0JVZ item 21
    changed the interfaces), and items 1, 4 to 6 and 10, which wait for the gate 2 work.
  - [ADR-Q4BK](entries/Q4BK-spec-v2-details-part-4.md) item 4d: a manifest with no `take_uuid` now
    has `bad_schema` ([ADR-PVG8](entries/PVG8-spec-v2-details-part-10.md) item 25).
  - [ADR-0XX2](entries/0XX2-spec-v2-details-part-5.md): item 6c ("one part for each pair of files":
    ADR-0WTH item 31) and item 8 (the fold "only after `state` is `finished`": SFF-844 has an
    exception from ADR-1HH0 item 2).
  - [ADR-DM9S](entries/DM9S-spec-v2-details-part-7.md) item 14: the scope of the JavaScript reader.
    ADR-0JVZ item 21 changed it.
- **Provisional parts of spec draft v2.** Close each of them before v2.0.0:
  - SFF-752: the source and the text form of `port_path` and `os_device_id` on each OS are not
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
  ([ADR-W5JC](entries/W5JC-nested-model-types-in-the-descriptor-part.md)). The user must decide
  each of them. The entry does not decide them.
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
  - Members that the code accepts when they are absent (`tags`, `sided`, `angle_names`,
    `zero_offsets`, `anchor_segment_name`, and each member of the presentation types that has a
    default): the part says that a writer writes them. Must the reader refuse a file without them?
  - A member that is "omitted when null": does the reader accept it with the value null? The code
    accepts null.
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
  calibration by `camera_key`.
- **Permalinks to the skellycam evidence.** The new entries cite skellycam `dom/research` files as
  plain paths. Many of them are not committed yet. Change them to full-SHA permalinks after that
  branch is committed and pushed.
- **S10b: correct the audio start of old recordings?** The audio of old skellycam recordings is
  9–74 ms early. The user must decide if playback corrects it
  ([ADR-CZQ9](entries/CZQ9-read-old-write-new-and-legacy-recognition.md)). skellycam does the legacy
  playback, so the result goes into a skellycam entry. Delete this item when that entry exists.
