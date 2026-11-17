# 5XNA — Folder layout, fixed names and the recording manifest

**Status:** superseded by [G9ER](G9ER-consolidation-of-the-pushed-entries.md),
2026-11-17 (commit to main; was accepted, 2026-11-16 (user; whole-folder grilling, 2026-11-13 to 2026-11-16)).

## Decision

1. **The take folder** holds one take. A user can rename the take folder to any name. A user must
   not rename a file or a subfolder inside it: the names link the files.
2. **The recording name `<rec>`** is the name of the take when the writer starts it. Each file
   name that has a prefix uses `<rec>`. `<rec>` does not change when the folder is renamed. The
   manifest records it.
3. **Fixed names.** The spec fixes these names. A reader finds a folder file by its exact name. It
   does not search with a glob pattern.
   - `recording_manifest.json` at the root, with no prefix;
   - `<rec>_info.json` (skellycam), `<rec>_recording_info.json` (freemocap),
     `<rec>_camera_calibration.toml`, `<rec>_data.parquet` and `<rec>.blend` at the root;
   - the media folder `synchronized_videos/`;
   - `annotated_videos/`, `exports/`, `logs/` and `blender/` at the root.
4. **Media file names.** In `synchronized_videos/`, the files of a camera are `<rec>.<label>.mkv`
   and `<rec>.<label>.csv`. The audio files are `<rec>.audio.m4a` and `<rec>.audio.csv`. The OS
   camera index (`idx-`) is not in a name. `<label>` is the `camera_label`: the first 6 to 8
   hexadecimal digits of `camera_key`, different for each camera of the take.
5. **One sidecar for each media file.** Each media file has its own CSV timing sidecar with the same
   stem.
6. **The manifest.** `recording_manifest.json` holds:
   - the format version, `take_uuid` and `<rec>`;
   - each file of the take with its role (camera video and timing, audio and timing, calibration,
     Parquet, info JSONs, annotated videos, exports, `.blend`, Blender outputs, journal);
   - the camera links: `camera_key` to video, to timing sidecar, to calibration camera;
   - the take purpose (calibration or motion capture);
   - the calibration that the take uses (`calibration_uuid` and the hash of the take's copy,
     [ADR-N6HS](N6HS-info-jsons-and-calibration.md));
   - `warnings[]`: skellycam adds warnings at the end of the take (for example camera gaps, a
     control that reads back a different value, auto white balance that did not settle), and
     freemocap adds warnings later;
   - the `privacy` list ([ADR-T8PK](T8PK-privacy-notice-and-no-code-in-files.md));
   - a `summary` block, the human-readable overview of the take: each camera with its label, user
     name, model, resolution, rotation, frame rate, gaps and exposure, and the duration, audio,
     calibration, processing runs and warnings. The summary is informative. A reader must not
     compute from it. A validator warns when it does not agree with the files.
7. **Writers of the manifest.** skellycam writes the manifest when the take starts, so that it is
   valid from its first write, and again when the take ends. freemocap updates it when it adds
   files, while it holds `.processing.lock`. Each write replaces the whole file
   ([ADR-G1YG](G1YG-writing-crash-reading-and-repair.md)).
8. **Missing or broken manifest.** A reader rebuilds the links by a scan: it finds the media files
   by their content in `synchronized_videos/`, and the folder files by their fixed suffix, with
   exactly one match for each role. It reports the warning `manifest_missing`. A program can offer
   to write a new manifest. A reader does not write it.
9. **Where a reader looks.** A reader scans only the root and `synchronized_videos/`. It finds the
   files of the other subfolders through the manifest, or by their fixed names.
10. **No `synchronized_videos_README.md`** in new takes. The manifest `summary` replaces it.
11. **New take or legacy.** A reader decides by content, not by folder names: a folder with a
    manifest of this format, or with a media file and its timing sidecar of this format in
    `synchronized_videos/`, is a take of this format.

## Reason

- A user renames take folders. A manifest at a fixed name keeps the links when the folder name
  changes, and the `<rec>` prefix stays the same.
- Fixed names stop the glob errors of today: skellycam and freemocap both read `*_info.json`, and
  that pattern matches both info files.
- `synchronized_videos/` and `<rec>_camera_calibration.toml` are the names that skellycam,
  freemocap, the UI and the Blender addon use today.
- A crashed take must still open, so a missing manifest is a warning, not an error.
- freemocap's own legacy name list holds almost the same names as a new take. A name rule would
  call every new take legacy.

## Evidence

- skellycam `dom/research`, `research/skellycam_recording/docs/whole_folder_spec_plan_20261113.md`,
  section "Grilling log": round 1 B1, B2, B3, B6, D1; round 2 Q5 and Q6; round 3 Q3, Q4; round 5 Q10,
  Q12, Q13 (local, not committed).
- `research/skellycam_recording/docs/camera_info_placement_20261115.md` (labels, placement).

## Alternatives rejected

- `videos/synchronized/` and `<rec>_calibration.toml`, the canonical names of
  `RECORDING_CONTRACT.md`: no writer makes them.
- No manifest ([ADR-TDB5](TDB5-whole-recording-no-manifest.md) item 2): a renamed folder breaks the
  links.
- A README file for the overview: it is a second copy that goes stale. The manifest summary is the
  one overview.
- The writer chooses the file names ([ADR-25VV](25VV-whole-recording-scope-names.md) rejected the
  fixed names): this spec is now the spec of the whole folder
  ([ADR-2C9V](2C9V-whole-take-folder-scope-and-package.md)).

## Open work

[open-work.md](../open-work.md)
