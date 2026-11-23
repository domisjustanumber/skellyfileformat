# CZQ9 — Old recordings stay readable; new programs write only this format; the spec recognises legacy folders

**Status:** superseded by [YBT1](../../../decisions/entries/YBT1-spec-only-test-adapter-and-labels.md), 2026-11-17 (commit to main; was absorbed, 2026-11-17 (commit to main; was accepted, 2026-11-16 (user; whole-folder grilling, 2026-11-13 to 2026-11-16))).

## Decision

1. New skellycam and freemocap keep reading each recording format that freemocap v1.0.25 to
   v1.8.2 and the current code write.
2. New skellycam, skellysync and freemocap write only this format: the files of
   [ADR-6RSB](6RSB-camera-files-mjpeg-mkv-and-csv-timing.md),
   [ADR-92TM](92TM-opus-audio-in-fragmented-mp4.md) and the folder files of this spec. They write
   no legacy timestamp CSV, no WAV audio and no burned-in overlay.
3. skellycam plays old H.264 recordings through a legacy `<video>` path. It also gives an explicit
   "upgrade recording" conversion, for the other old files and on request.
4. skellycam owns the converter. The converter uses `skellyspecs[write]`.
5. **Recognition.** The spec defines how a reader recognises a legacy folder and what result it
   reports. The code that reads old formats stays in skellycam and freemocap.
6. **Only v1 or later is supported.** A reader reports the family and the narrowest release range
   that the content of a v1.x folder proves, for example "v1.3.1–v1.4.7". When the files cannot
   decide, it says so ("v1.1.0–v1.1.1, ambiguous"). It does not guess.
7. **Pre-v1 folders** (v0.0.x and v0.1.0) are identified as "freemocap pre-v1 layout,
   unsupported", so that a user gets a clear message.
8. **Known-bad legacy data.** When a reader recognises a layout with a known defect, it reports a
   named warning code. Examples: the mislabelled hands and face of v1.1.0; the 2D "confidence" of
   v1.0.25, which is z × width; the non-rigid camera-0 alignment before v1.6.0; a v1.x TOML that may
   not be the calibration of the 3D data.
9. **Legacy annex.** The spec has an informative annex that describes the files, shapes, units and
   quirks of each v1.x layout, so that others can read old freemocap output. Pre-v1 layouts are not
   in the annex.
10. **Calibration lookup by glob** is used only to read v1 folders
    ([ADR-N6HS](N6HS-info-jsons-and-calibration.md)).

This entry supersedes [ADR-X1G6](X1G6-read-old-write-mcap.md) in full. Items 3 and 4 restate its
items 4 and 5. Item 1 restates its item 1, with the supported releases. Item 2 replaces its item 2
(MCAP with Opus) and adds freemocap. Item 5 replaces its items 3 and 6 (legacy outside the spec).
Items 6 to 10 are new.

## Reason

- The reasons of ADR-X1G6 stay: users keep their old recordings, and a program that writes two
  formats doubles the test work.
- A reader of the whole folder must say "this is an old take" in the same way in each program.
- No release writes its version into the folder, so the content must decide.

## Evidence

skellycam `dom/research` (local, not committed):
- `research/skellycam_recording/docs/legacy_release_inventory_20261115.md` (87 releases, three
  families, about 25 layouts, the known-bad data);
- `research/skellycam_recording/docs/legacy_sync_and_blender_addon_20261115.md`;
- `research/skellycam_recording/docs/whole_folder_spec_plan_20261113.md`, "Grilling log": round 1
  A6; round 2 Q17 to Q19; round 3 Q10.

## Alternatives rejected

- Legacy stays fully out of the spec (ADR-X1G6 item 6): each program would report old takes in its
  own way.
- Support pre-v1 layouts: the user supports only v1 or later.

## Open work

[open-work.md](../open-work.md)

_Edited 2026-11-23 (commit to main): link repair._

_Edited 2026-11-23 (commit to main): rename._
