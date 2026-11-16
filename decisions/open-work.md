# Open work

This file holds the open work of the [decision log](README.md). Read the items that apply to your
task. Delete an item when its work is done. The PR that closes an item records the result.

- **Gate 2: runnable tests and golden folders.** The user accepted the items of
  [ADR-VPD9](entries/VPD9-spec-draft-v2-details.md) and
  [ADR-3D33](entries/3D33-spec-draft-v2-details-folder-files.md) at gate 1 on 2026-11-16. Write the
  runnable tests of [conformance.md](../spec/conformance.md) and the golden folders G1 to G16 of
  SPEC.md Appendix A, and stop for gate 2. G17 waits for the skellysync decisions.
- **Absorb the accepted entries into the spec.** After gate 1, when `spec/SPEC.md` or `README.md`
  states all rules of an entry, move the entry to Historical as absorbed:
  [ADR-2C9V](entries/2C9V-whole-take-folder-scope-and-package.md),
  [ADR-5XNA](entries/5XNA-folder-layout-names-and-manifest.md),
  [ADR-6RSB](entries/6RSB-camera-files-mjpeg-mkv-and-csv-timing.md),
  [ADR-92TM](entries/92TM-opus-audio-in-fragmented-mp4.md),
  [ADR-9DV4](entries/9DV4-format-version-from-freemocap.md),
  [ADR-CZQ9](entries/CZQ9-read-old-write-new-and-legacy-recognition.md) (only its items 2 and 5 to
  10: items 1, 3 and 4 are skellycam and freemocap rules),
  [ADR-DE9S](entries/DE9S-rotation-in-the-video-csv-header.md),
  [ADR-G1YG](entries/G1YG-writing-crash-reading-and-repair.md),
  [ADR-KW3G](entries/KW3G-reader-result-for-the-folder.md),
  [ADR-N6HS](entries/N6HS-info-jsons-and-calibration.md),
  [ADR-P76Y](entries/P76Y-tracking-parquet.md),
  [ADR-Q9X2](entries/Q9X2-realtime-tracking-journal.md),
  [ADR-QS7B](entries/QS7B-blender-outputs-and-exports.md) and
  [ADR-T8PK](entries/T8PK-privacy-notice-and-no-code-in-files.md).
- **Provisional parts of spec draft v2.** Close each of them before v2.0.0:
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
  - the nested model types of the Parquet descriptor (`SkeletonSnapshot` and the others) are copied
    into parts/parquet-descriptor.md at gate 1.
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
  The Blender addon: MKV video planes, the `blender/` outputs and no pickle.
- **Permalinks to the skellycam evidence.** The new entries cite skellycam `dom/research` files as
  plain paths. Many of them are not committed yet. Change them to full-SHA permalinks after that
  branch is committed and pushed.
- **S10b: correct the audio start of old recordings?** The audio of old skellycam recordings is
  9–74 ms early. The user must decide if playback corrects it
  ([ADR-CZQ9](entries/CZQ9-read-old-write-new-and-legacy-recognition.md)). skellycam does the legacy
  playback, so the result goes into a skellycam entry. Delete this item when that entry exists.
