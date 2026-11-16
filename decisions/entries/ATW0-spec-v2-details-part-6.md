# ATW0 — Spec draft v2 details, part 6: unfinished pairs, flags, realtime warning, calibration, footers

**Status:** absorbed into [`spec/SPEC.md#6-camera-files`](../../spec/SPEC.md#6-camera-files),
[`spec/SPEC.md#7-csv-timing-sidecars-common-rules`](../../spec/SPEC.md#7-csv-timing-sidecars-common-rules),
[`spec/SPEC.md#8-video-timing-sidecar`](../../spec/SPEC.md#8-video-timing-sidecar),
[`spec/SPEC.md#11-clocks-the-fit-and-reader-timing`](../../spec/SPEC.md#11-clocks-the-fit-and-reader-timing),
[`spec/SPEC.md#12-writing-crashed-files-and-repair`](../../spec/SPEC.md#12-writing-crashed-files-and-repair),
[`spec/SPEC.md#15-calibration-toml`](../../spec/SPEC.md#15-calibration-toml),
[`spec/SPEC.md#16-tracking-parquet`](../../spec/SPEC.md#16-tracking-parquet),
[`spec/SPEC.md#23-the-reader-result`](../../spec/SPEC.md#23-the-reader-result),
[`spec/parts/parquet-descriptor.md#calibrationupdaterequest-closed`](../../spec/parts/parquet-descriptor.md#calibrationupdaterequest-closed),
2026-11-16 (commit to main; was accepted, 2026-11-16).

## Decision

This part holds items 9 to 13 of the proposals that [ADR-W6HV](W6HV-spec-v2-details-part-3.md)
introduces (items 1 and 2, and the meaning of "Basis" and "CHOICE"). The other parts are
[ADR-Q4BK](Q4BK-spec-v2-details-part-4.md) (3 and 4), [ADR-0XX2](0XX2-spec-v2-details-part-5.md)
(5 to 8), [ADR-DM9S](DM9S-spec-v2-details-part-7.md) (14 to 17) and
[ADR-72QQ](72QQ-spec-v2-details-part-8.md) (18 and 19). The user accepted
each item of this part on 2026-11-16, with the recommended option of each CHOICE. The recommended
option is the text of the item.

9. **Unfinished video pairs** (SFF-740, SFF-746, SFF-791; SFT-714, SFT-732; G5, G6).
   - Row k belongs to the k-th complete block, in file order. A frame is usable when its row is
     usable (SFF-746) and its block is complete. A reader uses no row after the last complete block
     and no block after the last usable row. `rows` counts the CSV rows (item 3e). `records` holds
     only the usable frames.
   - `torn_bytes` of an unfinished pair is the bytes of the torn last line of the sidecar, plus the
     bytes of the media file after its last complete block or fragment. Basis (1),
     [ADR-G1YG](G1YG-writing-crash-reading-and-repair.md) item 5; (2) draft v0 SFF-451 (a reader does
     not use a frame that has no record).

10. **Flags and counts** (SFF-756, SFF-758, SFF-782, SFF-828, SFF-886, SFF-887; SFT-717, SFT-728).
    - a. `gap` is 0 in the first row, and when the row or the row before has an empty
      `source_frame_number`. Basis (2), draft v0 SFF-170.
    - b. `encode_skips` of the `# end` line is the number of rows with the flag `encode_skip`. A
      repair can then compute it from the rows. Basis (3).
    - c. A reader gives the file warning `encode_skip` when one or more usable rows have that flag.
      Each reader makes a file `invalid` with `bad_time` when a row time or a fitted time has a
      magnitude of 2^53 ns or more. Basis (1), [ADR-KW3G](KW3G-reader-result-for-the-folder.md)
      items 3 and 4.
    - d. With player times p, the strict player time is s(0) = p(0) and s(k) = the larger of p(k)
      and s(k − 1) + 1 ns. A reader gives s to freemocap, and SFF-828 uses s. `records` hold p.
      Basis (1), [ADR-6RSB](6RSB-camera-files-mjpeg-mkv-and-csv-timing.md) items 10 and 12, and (3).

11. **`realtime_run`** (SFF-835; SFT-752). A reader gives the code `realtime_run` one time when a
    run has a stage provenance with `origin` = `realtime`. The text is guidance for the program that
    shows the take. It is not in the reader result. The program shows it for each camera sensor
    group, with N and M from the `coverage` of the stage `observations`. Basis (3).

12. **Calibration** (SFF-809, SFF-810, SFF-837; parts/parquet-descriptor.md; SFT-738, SFT-754).
    - a. When `aligned` is false, the world is the OpenCV camera frame of the camera with `index` 0:
      +X right, +Y down, +Z along the optical axis. freemocap changes each TOML world to
      `calibrated_world` with one fixed axis map, the same for an aligned and an unaligned TOML. The
      names "forward, left, up" are the labels of that map. They describe the room only after an
      alignment. The map is (x, y, z) = (−Y, X, Z), confirmed on 2026-11-16 in skellyforge at
      f5404db (`coordinate_systems.yaml`, the conventions `ros` and `blender`).
      Basis (2): freemocap at c27fc299, `coordinate_conventions.py` lines 8 to 10,
      `posthoc_reconstruction.py` lines 143 to 145, and `pin_camera_zero_to_origin`
      (`anipose_calibration_helpers.py`, lines 44 to 64).
    - b. CHOICE. "Agrees" in SFF-837 means, for each camera, by `camera_key`: the image size is
      equal; `fx`, `fy`, `cx`, `cy`, `k1`, `k2`, `p1` and `p2` differ by 1e-6 or less; and the pose
      relative to the camera with `index` 0 (each rotation matrix value, and each translation value
      in mm) differs by 1e-6 or less. A rigid change of the world does not change a relative pose.
      So an alignment by `person` or `charuco` gives no `calibration_mismatch`. Basis (3).
    - c. CHOICE. `CalibrationUpdateRequest` loses `path` and `expected_mtime_ms`, and gets
      `calibration_uuid_before` and `calibration_uuid_after`. Basis (2): in freemocap at
      c27fc299, `calibration_update.py`, the two members guard a write request
      (`_require_revision`, lines 22 to 24). They are not facts of the take. (1)
      [ADR-3D33](3D33-spec-draft-v2-details-folder-files.md) item 4.

13. **Footer lines** (SFF-745, SFF-775, SFF-795, SFF-796, SFF-798; SFT-733; G6).
    - A footer line is `# <word>`, then zero or more ` <key>=<value>`, with single spaces. A writer
      writes the keys in the order of this spec. Only the value of the last key can hold a space. It
      ends at the line end. `fitter_params` is the last key of `# fit`, and `repair_writer` is the
      last key of `# repair`. A later minor version adds a key before the last key. A reader does
      not parse `fitter_params`.
    - The repair line is `# repair cut_bytes=<n> media_cut_bytes=<m> repair_writer=<writer string>`.
      `cut_bytes` is for the sidecar, and `media_cut_bytes` is for the media file. Basis (3).

## Reason

- Each item removes a point at which two readers, or a reader and a golden result, can differ.
- The CHOICE items need the user. Each has one alternative, which is not rejected.

## Consequences

- New: the footer key `media_cut_bytes`.
- The axis map of item 12a must be confirmed against skellyforge at f5404db before the text lands.

## Evidence

- freemocap at c27fc299: `coordinate_conventions.py`, `posthoc_reconstruction.py`,
  `anipose_calibration_helpers.py` and `calibration_update.py` (item 12).
- skellyfileformat at 38ad0d6, `spec/SPEC.md`: draft v0 SFF-170 and SFF-451.

## Open work

[open-work.md](../open-work.md)
