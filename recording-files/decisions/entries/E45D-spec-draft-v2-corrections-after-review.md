# E45D — Spec draft v2 corrections after the independent review

**Status:** absorbed into [`README.md#versioning-normative`](../../README.md#versioning-normative),
[`spec/SPEC.md#3-versioning`](../../SPEC.md#3-versioning),
[`spec/SPEC.md#4-the-take-folder-layout-and-names`](../../SPEC.md#4-the-take-folder-layout-and-names),
[`spec/SPEC.md#11-clocks-the-fit-and-reader-timing`](../../SPEC.md#11-clocks-the-fit-and-reader-timing),
[`spec/SPEC.md#16-tracking-parquet`](../../SPEC.md#16-tracking-parquet),
[`spec/SPEC.md#17-realtime-journal`](../../SPEC.md#17-realtime-journal),
[`spec/SPEC.md#18-blender-outputs-annotated-videos-exports-and-logs`](../../SPEC.md#18-blender-outputs-annotated-videos-exports-and-logs),
[`spec/SPEC.md#181-blender`](../../SPEC.md#181-blender),
[`spec/SPEC.md#182-annotated-videos`](../../SPEC.md#182-annotated-videos),
[`spec/SPEC.md#183-exports`](../../SPEC.md#183-exports),
[`spec/SPEC.md#19-skellysync-folders`](../../SPEC.md#19-skellysync-folders),
[`spec/SPEC.md#20-opening-a-folder`](../../SPEC.md#20-opening-a-folder),
[`spec/SPEC.md#21-legacy-folders`](../../SPEC.md#21-legacy-folders),
[`spec/SPEC.md#23-the-reader-result`](../../SPEC.md#23-the-reader-result),
[`spec/SPEC.md#appendix-a-golden-folders`](../../SPEC.md#appendix-a-golden-folders),
[`spec/conformance.md#tests`](../../conformance.md#tests),
2026-11-16 (commit to main; was accepted, 2026-11-16).

## Decision

1. **Journal counts.** The `folder_files` item of the journal in the reader result holds three
   counts: the good records, the rejected records and `torn_bytes` (SFF-843, SFF-885).
2. **Folder-file states.** The states of a folder file gain `unsupported_version`, `unfinished` and
   `damaged`. A journal with a rejected record is `damaged`
   ([ADR-G1YG](G1YG-writing-crash-reading-and-repair.md) item 6) (SFF-843, SFF-885, SFF-886).
3. **Version fields.** The timing sidecar holds the format version and the writer string for its
   device pair. The media files stay standard files with no added fields. The export inventory and
   the BVH metadata JSON gain `format_version`, `format_prerelease` and `writer` (SFF-707, SFF-712,
   SFF-858). This item changes one rule of
   [ADR-9DV4](9DV4-format-version-from-freemocap.md) items 3 and 6 and of
   [ADR-VPD9](VPD9-spec-draft-v2-details.md) item 2: "each file" no longer includes the camera file
   and the audio file.
4. **Run numbers in names.** A name with no run number always means run 0. Each other run always
   has `run-<N>` in its name. No file is renamed or replaced when the selected run changes. The
   processing info JSON says which run is selected (SPEC.md section 18).
5. **Realtime times after a crash.** A repair may rewrite only the times of a realtime run:
   `timestamp_s` and the values of its `TIMESTAMPS` rows. Nothing else of a realtime run ever
   changes. The fold uses the player times that the sidecars give when it runs (SFF-833, SFF-844).
   No accepted entry states that a realtime run never changes:
   [ADR-P76Y](P76Y-tracking-parquet.md) item 8 says that posthoc never replaces a realtime run, and
   that rule stays. This item changes only the text of SFF-833.
6. **Audio fit by a reader.** With no fit line, a reader computes one exact integer fit: a straight
   line through the first and the last usable row. It has the members of the audio fit line (`n0`,
   `t0_ns`, an integer `period_fs`). `period_fs` is rounded down. Each row uses `adc_ns`, else
   `host_ns` ([ADR-VPD9](VPD9-spec-draft-v2-details.md) item 8) (SFF-784).
7. **Consistency repairs.** These changes make the spec agree with accepted entries. They change no
   decision:
   - the fit examples use `period_ps=33366700000`;
   - SFF-826 lists `camera_label`;
   - SFF-862 and SFF-863 are provisional;
   - G13 is a complete small take;
   - SFF-875: a legacy folder has no file of this format;
   - SFF-717 and SFF-868: `<rec>` comes from the names of the timing sidecar files, also for a take
     with only audio;
   - SFF-721 has "or by their fixed names" again;
   - the V1a era ends at v1.0.34, plus the tag `1.1.0`;
   - SFF-885 gives the integer types;
   - SFF-819: a reader accepts int64 in `frame_number` and `run_id`. The user agreed this when the
     writer type became int32 ([ADR-3D33](3D33-spec-draft-v2-details-folder-files.md) item 5);
   - the texts of SFT-706, SFT-710, SFT-714, SFT-725, SFT-730, SFT-733, SFT-740, SFT-741, SFT-743
     and SFT-747, and the golden folders G1, G7 and G9, are complete.

## Reason

1. SFF-843 makes a reader report the counts, and the result had no member for them.
2. SFF-708, SFF-791 and ADR-G1YG item 6 need these states for a folder file.
3. An MKV file and a fragmented MP4 file have no standard place for these fields. A standard file
   opens in other programs.
4. The spec gave two meanings to `<rec>.blend`, and the general rule did not agree with its tables.
   A file that keeps its name stays valid for each program that holds its path.
5. After a crash, the sidecars have no fit, so the fold has only the arrival times. A repair adds
   the fit. Without this exception, the run keeps the less accurate times.
6. The Python reader and the JavaScript reader must give the same result, byte for byte.
7. The spec must agree with the accepted entries.

## Open work

[open-work.md](../open-work.md)

_Edited 2026-11-23 (commit to main): link repair._
