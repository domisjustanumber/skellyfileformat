# P76Y — The tracking Parquet: one file for 2D and 3D, its conventions, links, numbers and realtime runs

**Status:** superseded by [G9ER](G9ER-consolidation-of-the-pushed-entries.md),
2026-11-17 (commit to main; was accepted, 2026-11-16 (user; whole-folder grilling, 2026-11-13 to 2026-11-16)).

## Decision

1. **One file.** `<rec>_data.parquet` holds the 2D and the 3D tracking data of the take, and the
   ChArUco observations as tracking rows. freemocap writes it. skellycam writes no Parquet file:
   when freemocap makes tracking data, freemocap moves it into the Parquet.
2. **Conventions.** The spec adopts the current conventions of the file:
   - one table with one row for each value. The columns are `timestamp_s`, `sensor_group`,
     `frame_number`, `source`, `reference_frame`, `channel`, `name`, `component`, `value`,
     `value_f64`, `units` and `run_id`;
   - missing data is null, never NaN;
   - the confidence is the `visibility` channel, from 0 to 1;
   - 3D is in millimetres, in the world frame of the calibration, with Blender axes.
3. **Descriptor.** The descriptor is in the Arrow metadata of the file, under the key
   `freemocap.recording`. Its `schema_version` is 2. It has real fields for `take_uuid` and, for
   each camera source, `camera_key`, the video file name, the timing CSV file name and the timing
   method.
4. **2D pixel space.** 2D points are in the pixel space of the stored JPEG, in sensor orientation,
   before `display_rotation` ([ADR-DE9S](DE9S-rotation-in-the-video-csv-header.md)). freemocap
   rotates them for display.
5. **Skeleton definitions** are in the descriptor: the keypoint names, and `tracker_connections`,
   the edges as pairs of keypoint names (as on the freemocap `sfn26` branches). The spec also
   documents a segment topology as plain JSON (segment name, parent, proximal keypoint, distal
   keypoint), so that another program can draw the skeleton without freemocap code. There is no
   `tracker_schema.json`.
6. **Numbers.** `value` is float32 and `value_f64` is float64. Each channel declares its number
   type in the descriptor: float32 by default, float64 for times and for values that need it. A row
   uses one of the two columns, and the other is null.
7. **Encoding.** Both value columns use the `BYTE_STREAM_SPLIT` encoding and no dictionary. The
   compression is ZSTD at level 3. A writer never uses LZ4 or Brotli. The spec states the encoding,
   so that a reader knows that it must support it (parquet-format 2.8.0 or later). fastparquet
   cannot read these files. This is accepted.
8. **Realtime runs.** A run that the realtime pipeline made has `origin` = `realtime`, and a
   coverage block in the provenance of each stage: the frames in the take and the frames processed,
   the skips by reason, the journal CRC rejects, `clean_close` and the latency.
   - A skipped frame has x, y and visibility all null. "Seen but not detected" stays as today.
   - A realtime run has no posthoc checkpoints, so posthoc never continues from realtime data.
   - Posthoc adds a new run. It never replaces a realtime run.
   - A reader warns: "Realtime run: N/M frames processed, causal filters, may contain dropped and
     extrapolated frames". The UI shows a badge.
   - What posthoc does with a realtime run is freemocap's choice. The spec does not define it.
9. **Exports** of float32 values print the shortest form that reads back as the same float32
   (`0.1`, not `0.10000000149011612`). The export checks compare in float32.

## Reason

- The Parquet is the most solid and validated part of the folder today.
- float32 holds the precision of the 2D and 3D data. With `BYTE_STREAM_SPLIT`, no dictionary on
  the values and ZSTD level 3, the file is about 36% of today's size (about 1.27 GB/h instead of
  3.5 GB/h), and pyarrow, pandas, polars, DuckDB and hyparquet read it bit-exactly.
- freemocap-ui's hyparquet-compressors fails on LZ4. hyparquet decodes Brotli 3 to 4 times slower.
- A user must know that a realtime run can hold dropped and extrapolated frames.

## Evidence

skellycam `dom/research` (local, not committed):
- `research/skellycam_recording/recording_upgrade/results/parquet_dtypes/FINDINGS.md` (pyarrow
  26.0.0, polars 2.0.0, DuckDB 2.0.0, pandas 2.3.3, fastparquet 2026.9.0, hyparquet 1.25.6);
- `research/skellycam_recording/docs/parquet_float64_20261115.md`;
- `research/skellycam_recording/docs/skeleton_definition_history_20261115.md`;
- `research/skellycam_recording/docs/whole_folder_spec_plan_20261113.md`, "Grilling log": round 2
  Q7 to Q10; round 3 Q8, Q11, Q14, Q17; round 5 Q7 and the Parquet constraint; round 7 items 4 and
  5.

## Alternatives rejected

- Separate 2D and 3D files: two files with one set of links.
- One float32 `value` column: no future channel could store float64.
- Plain encoding, so that fastparquet can read the file: about 4 points more file size.
- Bring back `tracker_schema.json`: freemocap removed it, and the descriptor holds the names.

## Open work

[open-work.md](../open-work.md)
