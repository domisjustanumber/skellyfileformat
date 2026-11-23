# XR63 — Reader rules from the review of the golden folders: legacy signals, refused sidecars, roles, link checks, open descriptor members

**Status:** absorbed into
[`spec/SPEC.md#5-the-recording-manifest`](../../SPEC.md#5-the-recording-manifest),
[`spec/SPEC.md#13-capture-info-json`](../../SPEC.md#13-capture-info-json),
[`spec/SPEC.md#20-opening-a-folder`](../../SPEC.md#20-opening-a-folder),
[`spec/SPEC.md#21-legacy-folders`](../../SPEC.md#21-legacy-folders),
[`spec/SPEC.md#23-the-reader-result`](../../SPEC.md#23-the-reader-result),
[`spec/parts/parquet-descriptor.md#processing`](../../parts/parquet-descriptor.md#processing),
[`spec/parts/parquet-descriptor.md#cameramodel-closed`](../../parts/parquet-descriptor.md#cameramodel-closed),
2026-11-17 (commit to main; was accepted, 2026-11-16 (user; questions Q87 to Q93, Q95, Q106 and Q110 of the review of
the golden folders)).

## Decision

The user accepted these rules. Each item gives its question number.

1. **Legacy era signals (Q87).** The keys of SFF-878 in `recording_parameters.json` count at any
   depth. When a folder has a `pre_v1` signal and a `v1` signal, `v1` wins (SFF-877, SFF-878).
2. **A refused sidecar (Q88).** A sidecar that the reader refuses (`invalid`) is not in the
   take-level checks: it causes no `summary_stale` and no `take_fact_mismatch`. Its own state
   `invalid` is the report (SFF-729, SFF-871).
3. **The role `calibration` (Q89).** The reader reports the `role` `calibration` in `folder_files`
   for the file that the manifest member `calibration.file` names. Before, the role was null. The
   result of each golden case that has a TOML changes (section 5, SFF-885).
4. **A folder file of another take (Q90).** A folder file that holds another `take_uuid` is
   `present`, and the link check `take_uuid` is `mismatch` (SFF-889).
5. **Roles in a rebuild (Q91).** When the reader rebuilds a missing manifest, the `role` of a folder
   file comes from its fixed file name (SFF-731).
6. **The link check `dimensions` (Q92).** The check compares the image reference of the Parquet
   (SFF-829) with the camera file, and nothing else (SFF-872).
7. **A file with an unknown major version (Q93).** The reader skips its link checks, as for an
   `invalid` file. Its `reason` is null. It still gets the warning `prerelease` when the reader
   can read the field and the value is above 0 (SFF-872, SFF-886, SFF-891; [ADR-7JJJ](7JJJ-audio-repair-refused-header-values-and-the-rules-of-w5ak.md)
   item 6, corrected on 2026-11-17).
8. **Open descriptor members (Q95).** The descriptor members `filtering` and `camera_assignment`
   are optional, open JSON objects. A reader checks that each is an object only when it is
   present, until freemocap defines them ([ADR-H2HQ](H2HQ-descriptor-members-deferred-points-and-old-audio.md) item 1, Q121; corrected on 2026-11-17). The camera geometry of the descriptor is in the world of the calibration TOML
   (parts/parquet-descriptor.md, sections "Processing" and `CameraModel`).
9. **`key_origin` (Q106).** A reader checks only that `key_origin` is one of the three values. A
   reader never computes a key again from the `device` values (SFF-803).
10. **A folder with only a TOML, a Parquet or a journal (Q110).** A folder that holds only a TOML,
    a Parquet or a journal of this format has `folder_state` `unreadable` in the two scopes
    (SFF-888, SFF-892).

## Reason

The user answered "otherwise agree" to the recommendations of the review on 2026-11-16. The
user gave no reason for these items.
[ADR-W5AK](W5AK-details-for-the-decisions-q83-to-q111.md) proposes the details that the spec text
of items 5, 9 and 10 needed.

## Consequences

- The result of each golden case that has a TOML changes (item 3). This entry is the decision entry
  that `AGENTS.md` section 4 needs for that change of the golden files.
- Items 3, 4 and 10 close three open points of 2026-11-16 (open-work.md).

## Open work

See [open-work.md](../open-work.md).

_Edited 2026-11-23 (commit to main): link repair._
