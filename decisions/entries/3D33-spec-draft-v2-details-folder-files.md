# 3D33 — Spec draft v2 details, part 2: folder files, opening a folder, legacy and the reader result

**Status:** proposed, 2026-11-16 (agent; spec draft v2 for gate 1).

## Decision

Spec draft v2 uses these details. Gate 1 reviews them. Part 1 is
[ADR-VPD9](VPD9-spec-draft-v2-details.md).

1. **Manifest.** The members, roles, owners and `state` (`recording`, `finished`) of SPEC.md section
   5. A warning is `{code, source, camera_key, detail}`. skellycam codes: `camera_gap`,
   `control_mismatch`, `awb_not_settled`. A stale summary gives `summary_stale`.
2. **Capture info JSON.** The members of SPEC.md section 13. The key of a camera with `camera_key` 0
   is `0:<camera_label>`. The control names of SPEC.md section 13. The file is written at the start and
   the end of the take.
3. **Processing info JSON.** The header members, then the current `processed` block.
4. **Calibration TOML.** The header keys in `[metadata]`; the camera table key, `name` and `id` are
   the label; `index` is `group_position`; `controls_at_calibration` is a sub-table. A change of
   geometry (an alignment or a transform) gives a new `calibration_uuid`. Every TOML write is whole. A
   reader uses only the TOML that the manifest names.
5. **Parquet.** `value_f64` is column 10. Each channel has `dtype`. The descriptor gains
   `format_version`, `format_prerelease`, `writer` and `take_uuid`; `recording_id` is `<rec>`. A camera
   source is `camera:<camera_label>`, with `camera_key`, `camera_label`, `timing_filename` and no
   `nominal_fps`. A camera sensor group is named from the hash of its `camera_key` values. The group
   time is `mean_camera_times`. One channel for each row group. ChArUco corners are `OVERLAY_2D` rows
   of a `charuco_detector:<board>` source with names `corner_<id>`. `origin` and `coverage` are
   members of each stage provenance. `segment_topology` is an array of
   `{name, parent, proximal, distal}`.
6. **Blender.** The scenes of runs other than 0 and the 3D models are in `blender/`. A take of this
   format gets no legacy addon output. The scene contents are provisional.
7. **Annotated videos.** `annotated_videos/<rec>.<label>.annotated.mp4`: H.264, CRF 18, the
   orientation of the stored frames, no time stamp.
8. **Exports.** The notebook moves into `exports/`. The inventory is
   `<prefix>.export_inventory.json`, so that its name differs from the processing info JSON. The tall
   CSV has one `value` column. Each NPY array has the `dtype` of its channel.
9. **Logs.** `logs/<program>.log`.
10. **Opening a folder.** A device pair is found by the first line of its CSV and the magic of its
    media file. A media file or a sidecar alone gives `orphan_file`. Two takes give
    `multiple_takes`. A manifest of another take is `invalid`. In a rebuild, `<rec>` comes from the
    sidecar names. The link checks of SPEC.md section 20, with the states `ok`, `mismatch` and
    `not_checked`. A camera with key 0 gives `camera_key_zero`. A stale `parquet_sha256` gives the
    warning `stale_processing_info`, not an error.
11. **Legacy.** The era table of the research inventory is the normative recognition rule. The legacy
    warnings are `legacy_fake_confidence`, `legacy_marker_order`, `legacy_nonrigid_alignment` and
    `legacy_calibration_unverified`.
12. **Privacy.** The `privacy` object has `fields` (`file`, `field`, `kind`) and
    `media_shows_people`. The reason `code_in_file` is for a pickle or an object array.
13. **Reader result.** `result_version` 2 and the members of SPEC.md section 23. New codes:
    `manifest_missing`, `stray_tmp`, `orphan_file`, `camera_key_zero`, `stale_processing_info`,
    `summary_stale`, `calibration_mismatch`, `realtime_run`, `multiple_takes`, `bad_schema` (for a JSON,
    TOML or Parquet file) and `code_in_file`.
14. **Golden folders** G1 to G17 of SPEC.md Appendix A.

## Reason

- Each item is a detail that the spec needs and that no decision fixes. Items 2 to 5 and 8 keep the
  current freemocap and skellycam fields where a decision does not remove them.

## Evidence

skellycam `dom/research` (local, not committed):
- `research/skellycam_recording/docs/parquet_inventory_20261116.md` (freemocap c27fc299 and `sfn26`);
- `research/skellycam_recording/docs/folder_files_inventory_20261116.md` (freemocap c27fc299,
  skellycam 169caf637, addon 73e1b3e);
- `research/skellycam_recording/docs/legacy_release_inventory_20261115.md`, section 3.
