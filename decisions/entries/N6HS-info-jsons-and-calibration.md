# N6HS — The two info JSONs, one fact in one home, and the calibration as a setup file

**Status:** superseded by [G9ER](G9ER-consolidation-of-the-pushed-entries.md),
2026-11-17 (commit to main; was accepted, 2026-11-16 (user; whole-folder grilling, 2026-11-13 to 2026-11-16)).

## Decision

1. **Two info JSONs, one writer each, no copied fields.** skellycam writes `<rec>_info.json` with
   the capture facts only. freemocap writes `<rec>_recording_info.json` with the processing summary
   only (its runs and the Parquet hash). freemocap does not copy the capture JSON into its file.
2. **One fact, one home.** Each fact has one authoritative home:
   - each media file's CSV header: what a reader needs to read that file alone (the format version,
     `take_uuid`, the take start times, the UTC offset, the clock, `group_size`, the group position,
     `camera_key`, `camera_label`, the nominal rate, `display_rotation`; for audio, the rate, the
     channels and the codec);
   - the MKV and the CSV only: the stored resolution, the actual rate and the frame counts, gaps
     and fills (a CSV end line counts them);
   - the info JSON `camera_configs`, keyed by `camera_key`: the device identity (`device`: model,
     OS name, vendor and product ID, serial or port path, backend, OS index at capture), the user
     name of the camera, the requested settings (`requested`: resolution, frame rate, capture
     format, exposure mode), the control values read back at the start (`controls`, with the unit in
     each name, for example `exposure_us`) and the exposure-step results; plus an `audio` block with
     the microphone name and host API;
   - the manifest: the file roles, the links from a camera to its video, CSV and calibration camera,
     `<rec>`, the take purpose and the warnings
     ([ADR-5XNA](5XNA-folder-layout-names-and-manifest.md));
   - the calibration TOML: the calibration identity and, in each camera table,
     `controls_at_calibration`. This is the setup, a different fact from the take's own controls.

   Other files hold `take_uuid` and `camera_key` only as link keys. The manifest `summary` is the one
   informative copy. The info JSON has no `videos`, `camera_timing` or `multiframe_timing` map, no
   `recording_directory`, no rotation, and no `camera_index`, `use_this_camera`, `resolution`,
   `color_channels`, `pixel_format` or `writer_fourcc`. The full timestamp object and the IANA time
   zone name are dropped. `recording_uuid` is dropped: `take_uuid` replaces it.
3. **The calibration is a setup file.** One calibration serves each take of one camera setup. It
   changes only when the setup changes: a camera moved, or a lens or focus changed. A calibration
   always comes from a take. Keeping that take is optional, and strongly advised.
4. **Calibration identity.** The `[metadata]` table of a calibration TOML holds its format version,
   its own `calibration_uuid` and, when known, `source_take_uuid`: the take that made it, also when
   that take was later deleted. A new calibration gets a new `calibration_uuid`. A take is never
   changed afterwards to point at a newer calibration.
5. **TOML camera tables** hold `camera_key`, `camera_label` and the image size, in addition to the
   geometry. New keys go inside `[metadata]` and the camera tables, because freemocap reads each
   other top-level table as a camera. The TOML holds no copy of the capture info JSON.
6. **A copy in each take.** Each take that uses a calibration holds a byte-identical copy named
   `<rec>_camera_calibration.toml`. The manifest records its `calibration_uuid` and a hash of its
   content, so that the folder stays complete when it is moved or renamed.
7. **The library.** freemocap keeps a library copy of each calibration in
   `~/freemocap_data/calibrations/`, with the same schema. A TOML outside a take is a file of this
   format. `last_successful_camera_calibration.toml` is a plain, identical copy of the newest
   library file. A take refers to a calibration only by its `calibration_uuid`, never by that name.
8. **Lookup by glob** (any `*calibration*.toml`) is used only to read v1 folders.
9. **TOML against a Parquet run.** When the TOML and the camera geometry stored in a Parquet run do
   not agree, the stored geometry wins for that run, and a reader gives a warning.

## Reason

- One writer for each file stops two programs from writing one file at the same time.
- One home for each fact removes the rules for copies that disagree.
- The user's model: a calibration belongs to a setup, not to one take.
- A copy and a hash in each take keep the take complete when the library or the calibration take is
  gone.

## Evidence

skellycam `dom/research` (local, not committed):
- `research/skellycam_recording/docs/camera_info_placement_20261115.md`, §2 (accepted in round 7);
- `research/skellycam_recording/docs/whole_folder_spec_plan_20261113.md`, "Grilling log": round 2
  Q6, Q8, Q11, Q12; round 3 Q5, Q6; round 4 Q1; round 7 item 7.

## Alternatives rejected

- One merged info JSON that both programs write: two writers of one file.
- A take refers to its calibration by name or by glob: a rename or a second TOML breaks it.

## Open work

[open-work.md](../open-work.md)
