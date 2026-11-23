# QS7B — Blender outputs, annotated videos and exports are files of the spec, with fixed names

**Status:** absorbed into
[`spec/SPEC.md#4-the-take-folder-layout-and-names`](../../SPEC.md#4-the-take-folder-layout-and-names),
[`spec/SPEC.md#18-blender-outputs-annotated-videos-exports-and-logs`](../../SPEC.md#18-blender-outputs-annotated-videos-exports-and-logs),
[`spec/SPEC.md#181-blender`](../../SPEC.md#181-blender),
[`spec/SPEC.md#182-annotated-videos`](../../SPEC.md#182-annotated-videos),
[`spec/SPEC.md#183-exports`](../../SPEC.md#183-exports),
[`spec/SPEC.md#184-logs`](../../SPEC.md#184-logs),
[`spec/SPEC.md#21-legacy-folders`](../../SPEC.md#21-legacy-folders),
2026-11-16 (commit to main; was accepted, 2026-11-16).

## Decision

1. **Blender outputs** of the freemocap Blender addon are files of the spec, with exact names. In a
   new take, they are in one folder that the addon owns, `blender/`, and `<rec>.blend` is at the root
   of the take.
2. **The addon pickle is dropped** ([ADR-T8PK](T8PK-privacy-notice-and-no-code-in-files.md)).
3. **Legacy addon layouts** are in the informative legacy annex
   ([ADR-CZQ9](CZQ9-read-old-write-new-and-legacy-recognition.md)).
4. **The `.blend` contents** (the scene, the camera layout, the object names) are future freemocap
   work. freemocap defines them in this spec when it writes `.blend` files.
5. **Annotated videos** (`annotated_videos/`) and **exports** (`exports/`) are files of the spec.
   For each, the spec gives the name, the container and the codec, and the content mapping
   ([ADR-2C9V](../../../decisions/entries/2C9V-whole-take-folder-scope-and-package.md) item 3). An annotated video is derived
   output. It is not a recorded overlay.
6. **Logs** (`logs/`): the spec gives only the name and the text encoding.
7. **Exports of float32 values** follow [ADR-P76Y](P76Y-tracking-parquet.md) item 9.

## Reason

- The Blender addon reads and writes files in the take. A reader of the whole folder must know them.
- One owned folder keeps the addon outputs apart from the format files.
- A pickle runs code when it is loaded.

## Evidence

- skellycam `dom/research` (local, not committed):
  `research/skellycam_recording/docs/legacy_sync_and_blender_addon_20261115.md`;
  `research/skellycam_recording/docs/whole_folder_spec_plan_20261113.md`, "Grilling log": round 2
  Q4; round 3 Q16.

## Open work

[open-work.md](../open-work.md)

_Edited 2026-11-23 (commit to main): link repair._
