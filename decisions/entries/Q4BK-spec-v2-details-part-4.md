# Q4BK — Spec draft v2 details, part 4: reader result members and orphan files

**Status:** absorbed into
[`spec/SPEC.md#5-the-recording-manifest`](../../spec/SPEC.md#5-the-recording-manifest),
[`spec/SPEC.md#12-writing-crashed-files-and-repair`](../../spec/SPEC.md#12-writing-crashed-files-and-repair),
[`spec/SPEC.md#20-opening-a-folder`](../../spec/SPEC.md#20-opening-a-folder),
[`spec/SPEC.md#181-blender`](../../spec/SPEC.md#181-blender),
[`spec/SPEC.md#21-legacy-folders`](../../spec/SPEC.md#21-legacy-folders),
[`spec/SPEC.md#23-the-reader-result`](../../spec/SPEC.md#23-the-reader-result),
2026-11-17 (commit to main; was accepted, 2026-11-16 (user; review of the proposed details, each item, with the
recommended option of each CHOICE)).

## Decision

This part holds items 3 and 4 of the proposals that [ADR-W6HV](W6HV-spec-v2-details-part-3.md)
introduces (items 1 and 2, and the meaning of "Basis" and "CHOICE"). The other parts are
[ADR-0XX2](0XX2-spec-v2-details-part-5.md) (5 to 8), [ADR-ATW0](ATW0-spec-v2-details-part-6.md)
(9 to 13), [ADR-DM9S](DM9S-spec-v2-details-part-7.md) (14 to 17) and
[ADR-72QQ](72QQ-spec-v2-details-part-8.md) (18 and 19). The user accepted
each item of this part on 2026-11-16, with the recommended option of each CHOICE. The recommended
option is the text of the item.

3. **Reader result** (SFF-790, SFF-885, SFF-887, SFF-890; SFT-731, SFT-761, SFT-768; each
   committed result).
   - a. `fit` is true only when the sidecar holds fit lines and the reader uses them. It is false
     when the reader computes a fit (SFF-784). Basis (3).
   - b. `links` holds each check of SFF-872 one time, in the order of that table. Basis (3).
   - c. `links[].detail` is null in the canonical result. A reader can give a text outside the
     result. Basis (3).
   - d. CHOICE. `files[].name` and `other_files[].name` are paths relative to the take folder, with
     `/`. Basis (3): one rule, the same as `folder_files[].path`.
   - e. `rows` is the number of data rows that SFF-746 lets the reader use, for a camera and for
     audio. An audio item has `camera_key` and `camera_label` null. An `invalid` or
     `unsupported_version` item has `rows`, `torn_bytes` and `fit` null. Its `camera_key` and
     `camera_label` are the header values when their form is correct, else null. Basis (3).
   - f. `folder_files` has one item for each `files` item of the manifest, one for
     `calibration.file`, and one for each root file with a fixed name of item 6a that exists. An
     item is `missing` only when the manifest names a path that does not exist. A rebuild lists only
     the files that it finds. The state `ambiguous` is used only in `legacy.calibration` (item 5c).
     Basis (3).
   - g. CHOICE. In the manifest, `files[].sha256` is the SHA-256 for the roles `capture_info`,
     `processing_info`, `blend`, `blender_output` and `annotated_video`. It is null for `tracking`
     (its home is `parquet_sha256`), `export` (its home is the export inventory),
     `realtime_journal` and `log`. A reader does not check it. Basis (1),
     [ADR-N6HS](N6HS-info-jsons-and-calibration.md) item 2 (one fact, one home).
   - h. `legacy.release_range` is null, or an array of two release names, for example
     `["v1.3.1","v1.7.4"]`. `legacy.eras` is an array of the Era cells of the matched rows of
     SFF-878, in table order, with `-` in place of the dash. Basis (3).
   - i. A file whose name ends in `.tmp` or starts with `.`, and `<rec>.blend1`, is in no list. A
     code is at most one time in a `warnings` array. CHOICE: `stray_tmp` and `orphan_file` become
     folder warnings, because the file can have no take. Basis (3).

4. **Orphans and "a file of this format"** (SFF-865, SFF-869, SFF-875, SFF-887, SFF-888, SFF-889;
   SFT-761).
   - a. A file of this format is one of these: a timing sidecar with the first line of SFF-864; a
     JSON file whose `skellyfileformat` member has a value of this spec; a TOML with
     `[metadata].calibration_uuid`; a Parquet with a `freemocap.recording` descriptor of
     `schema_version` 2; a journal with a header record; a media file in a device pair. A media file
     alone has no mark of the format. It is in `other_files` as `not_in_format`.
   - b. A take exists for each `take_uuid` that one or more device pairs hold (SFF-866).
   - c. A timing sidecar alone, with a `take_uuid` that the reader can read, is in the `files` of
     its take when that take exists. Its `name` is the path of the missing media file. Its state is
     `invalid`, with the new reason code `missing_media`. It does not count as a camera file or an
     audio file in SFF-869. When no such take exists, the item is in `other_files` with the same
     state and reason.
     CHOICE: a new code cannot be avoided without a false reason.
   - d. A folder file of this format with no take is in `other_files` as `invalid`, with
     `take_fact_mismatch`. A manifest that no take uses and that holds no `take_uuid` has the reason
     `bad_schema` and gives no `orphan_file` ([ADR-PVG8](PVG8-spec-v2-details-part-10.md) item 25). The rule also
     applies in a folder with a take, to a folder file that no manifest lists and whose name has the
     `<rec>` of no take ([ADR-158N](158N-details-for-the-decisions-of-round-3.md) item 13; corrected on 2026-11-17).
   - e. Each file of a to d that is alone gives `orphan_file`. SFF-889 gets the words of
     [ADR-KW3G](KW3G-reader-result-for-the-folder.md) item 7 again ("a file of this format").
     Basis (1), [ADR-KW3G](KW3G-reader-result-for-the-folder.md) item 7 and
     [ADR-3D33](3D33-spec-draft-v2-details-folder-files.md) item 10.

## Reason

- Each item removes a point at which two readers, or a reader and a golden result, can differ.
- The CHOICE items need the user. Each has one alternative, which is not rejected.

## Consequences

- New: the reason code `missing_media`.
- `stray_tmp` and `orphan_file` move to `folder_warnings`.

## Open work

[open-work.md](../open-work.md)
