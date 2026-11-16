# PVG8 — Spec draft v2 details, part 10: exports of G3, manifest summary, a manifest not used

**Status:** absorbed into [`spec/SPEC.md#2-conventions`](../../spec/SPEC.md#2-conventions),
[`spec/SPEC.md#5-the-recording-manifest`](../../spec/SPEC.md#5-the-recording-manifest),
[`spec/SPEC.md#20-opening-a-folder`](../../spec/SPEC.md#20-opening-a-folder),
[`spec/SPEC.md#23-the-reader-result`](../../spec/SPEC.md#23-the-reader-result),
[`spec/SPEC.md#appendix-a-golden-folders`](../../spec/SPEC.md#appendix-a-golden-folders),
[`spec/SPEC.md#layout-and-cases`](../../spec/SPEC.md#layout-and-cases),
[`spec/conformance.md#the-take-folder-and-the-manifest-sections-4-and-5`](../../spec/conformance.md#the-take-folder-and-the-manifest-sections-4-and-5),
[`spec/conformance.md#blender-outputs-annotated-videos-exports-and-logs-section-18`](../../spec/conformance.md#blender-outputs-annotated-videos-exports-and-logs-section-18),
2026-11-16 (commit to main; was accepted, 2026-11-16).

## Decision

This part holds items 23 to 25 of the proposals that
[ADR-0JVZ](0JVZ-spec-v2-details-part-9.md) introduces. The user accepted
them on 2026-11-16, with the recommended option of each CHOICE. Each alternative stays as a record.

23. **Exports of G3** (section 18.3; SFT-743, SFT-744; G3). CHOICE. G3 holds no export at gate 2:
    no file in `exports/` and no manifest item with the role `export`. Appendix A removes "and the
    exports" from G3. The golden part of SFT-743 waits. SFT-744 does not wait: the test makes its
    two hidden items, and it needs no export. `open-work.md` gets the item "Complete section 18.3".
    Its points: one inventory for the tall and the wide exports; the snapshot members `revision`
    and `selection`; `float_precision` for float32; the bytes of the NPZ; the texts of the notebook
    and of the READMEs; `<file>` of `calibration_copies/`; and `exported_at` in a golden file.
    Basis (2): the evidence below. Alternative: the generator makes the exports from the code
    facts below and guesses the other bytes.

24. **Manifest summary** (SFF-702, SFF-728, SFF-729; SFT-708, SFT-709; G1 and each later folder).
    CHOICE (item a).
    - a. SFF-702 gets a number rule. A writer writes a JSON number with an integer value with no
      fraction and no exponent (`30`). It writes each other number in the shortest decimal form
      that reads back as the same float64, as RFC 8785 gives it (`29.97`). `nominal_fps` and each
      `duration_s` are JSON numbers: an integer number of thousandths, divided by 1000.
      `nominal_fps` is ⌊(2000 × `num` + `den`) / (2 × `den`)⌋ thousandths. SFF-729 compares
      the thousandths. SFT-708 says "at most 3 decimal places".
    - b. `take_start_utc` is `take_start_utc_ns` as `YYYY-MM-DDTHH:MM:SSZ`, rounded down to the
      second.
    - c. `duration_s` of the take is the largest `arrival_ns` of the last rows of the video
      sidecars: ⌊(ns + 500,000) / 10^6⌋ thousandths. A take with no camera uses the audio value.
      `duration_s` of `audio` is `samples` / `sample_rate` of the `# end` line and the header,
      rounded half up to thousandths.
    - d. `cameras` is in order of `group_position`. `user_name` and `model` are `user_name` and
      `device.model` of the camera config. `exposure_us` is `controls.exposure_us.value` of that
      config, or null. `stored_px` is the size of the first stored JPEG. `gaps` and `filled` are
      the counts of the `# end` line.
    - e. `audio.file` is the path of the audio file. `calibration` is null, or
      `{calibration_uuid, source_take_uuid}` from the TOML. `source_take_uuid` is null when the
      TOML has none.
    - f. `processing_runs` is in order of `run_id`. `origin` is `realtime` when a stage provenance
      of the run has that origin, else `posthoc`. `recorded_at` is the unchanged text of the
      latest stage provenance.
    - g. In a manifest with `state` `recording`, each `duration_s`, `stored_px`, `gaps` and
      `filled` is null.

    Basis (1): [ADR-0XX2](0XX2-spec-v2-details-part-5.md) item 7 and
    [ADR-N6HS](N6HS-info-jsons-and-calibration.md) item 2 (the homes); (3). Alternative to item a:
    `nominal_fps` and `duration_s` are texts with exactly 3 decimal places.

25. **A manifest that the reader does not use** (SFF-731, SFF-867, SFF-885, SFF-889; SFT-710; G7).
    The take member `manifest` is `missing` only when `recording_manifest.json` does not exist. It
    is `invalid` when the file exists and the reader does not use it for the take: the file is not
    valid JSON, is not a manifest of this format, or holds another `take_uuid`. Each rebuild gives
    `manifest_missing`, also when `manifest` is `invalid`. The manifest is never an item of
    `folder_files`. A manifest that no take of the folder uses is in `other_files`, with the state
    `invalid`. Its reason is `take_fact_mismatch`, with the folder warning `orphan_file`, when it
    holds a `take_uuid` (SFF-889). Else its reason is `bad_schema`, with no `orphan_file`. So
    `other_take_manifest` of G7 has `manifest` `invalid`, `manifest_missing`, the `other_files`
    item and `orphan_file`. Basis (1): [ADR-Q4BK](Q4BK-spec-v2-details-part-4.md) item 4d; (3).

## Reason

- Item 23: no code writes the exports of section 18.3. A golden export would be a guess.
- Item 24: the summary is in the manifest of each golden folder, and SFF-729 compares its values.
- Item 25: SFF-731, SFF-867 and SFF-889 each give a part of the result. No text joins them.

## Evidence

freemocap at c27fc299, `freemocap/core/recording/exports/` (item 23). The code fixes these facts:
`filename` is relative to `exports/` (`publication.py`, lines 13 to 34); `<k>` starts at 1, and
`.rows-<k>` is before `.columns-<k>` (`wide_csv.py`, lines 260 to 262); `rows` and `columns` are the
first axis length and `[]` for an NPY, the number of tables and `[]` for the NPZ, and 0 and `[]` for
the notebook (lines 233 to 236 and 305 to 319); the `csv` values (lines 341 to 342). The code does
not agree with section 18.3 in these facts: two inventories with two snapshot forms (`wide_csv.py`,
line 168; `tall_csv.py`, lines 69 and 130 to 134); `version` 3 or 4; float64 arrays and int64 frames
(`arrays.py`, lines 175 and 188); a `run-<N>/` folder; the notebook in the take root; a deflated
NPZ; `revision` as a hash of file-system facts (`parquet_storage/recording_view.py`, lines 39 to
42); and no writer of the format `metadata`.

## Open work

[open-work.md](../open-work.md)
