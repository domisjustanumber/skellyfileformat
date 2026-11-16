# 0XX2 — Spec draft v2 details, part 5: legacy result, manifest rebuild, summary and manifest lock

**Status:** accepted, 2026-11-16 (user; review of the proposed details, each item, with the
recommended option of each CHOICE).

## Decision

This part holds items 5 to 8 of the proposals that [ADR-W6HV](W6HV-spec-v2-details-part-3.md)
introduces (items 1 and 2, and the meaning of "Basis" and "CHOICE"). The other parts are
[ADR-Q4BK](Q4BK-spec-v2-details-part-4.md) (3 and 4), [ADR-ATW0](ATW0-spec-v2-details-part-6.md)
(9 to 13), [ADR-DM9S](DM9S-spec-v2-details-part-7.md) (14 to 17) and
[ADR-72QQ](72QQ-spec-v2-details-part-8.md) (18 and 19). The user accepted
each item of this part on 2026-11-16, with the recommended option of each CHOICE. The recommended
option is the text of the item.

5. **Legacy** (SFF-875 to SFF-880, SFF-885; SFT-764, SFT-765; G15).
   - a. CHOICE. A row of the era table matches when each signal of the row is present. "as X" adds
     the signals of row X. The rows that say "as" make a chain. When the matched rows are in one
     chain, the reader reports the range of the last matched row, and `ambiguous` is false. When
     they are in two chains, or no row matches, the reader reports from the lowest first release to
     the highest last release of the matched rows (v1.0.25 to v1.8.2 with no row), and `ambiguous`
     is true.
     Basis (1), [ADR-CZQ9](CZQ9-read-old-write-new-and-legacy-recognition.md) item 6, and (3).
   - b. CHOICE. A legacy folder that is not `v1` and not `pre_v1` has `family` = `unknown`,
     `release_range` null, `ambiguous` false, and empty `eras` and `warnings`. Version 2.0 does not
     recognise the layout of the development code. Basis (3).
   - c. `legacy` gets the member `calibration`: `{path, state}`, with the state `present`, `missing`
     or `ambiguous`. `path` is null when the state is not `present`. Basis (3).

6. **Manifest rebuild** (SFF-718, SFF-731, SFF-814, SFF-872; SFT-710, SFT-740; G7).
   - a. In a rebuild, a reader tests these exact names in the root, built from `<rec>`:
     `<rec>_info.json`, `<rec>_recording_info.json`, `<rec>_camera_calibration.toml`,
     `<rec>_data.parquet`, `<rec>_realtime_journal.bin` and `<rec>.blend`. It does not match a
     suffix. Basis (1),
     [ADR-5XNA](5XNA-folder-layout-names-and-manifest.md) item 3, and (3).
   - b. SFF-814 gets the exception: in a rebuild, the reader uses `<rec>_camera_calibration.toml`.
     Basis (1), [ADR-5XNA](5XNA-folder-layout-names-and-manifest.md) item 8.
   - c. A link check has one part for each pair of files that its rule compares. A part is not
     evaluated when a file that it needs is absent, is `invalid`, or is not read by that reader. The
     state is `mismatch` when an evaluated part fails, `ok` when one or more parts are evaluated and
     none fails, and `not_checked` when no part is evaluated. So, with no manifest, `calibration` is
     `not_checked`, `hashes` has only its Parquet part and `files` has only its Parquet part.
     Basis (3).

7. **Manifest summary** (SFF-728, SFF-729; SFT-708, SFT-709).
   - Each camera has `exposure_us` (a number or null) in place of "the main control values".
     `audio` is null, or `{file, sample_rate, channels, duration_s}`. Each item of `processing_runs`
     is `{run_id, origin, recorded_at}`, with the latest `recorded_at` of the stage provenances of
     the run. `summary` gets `warnings`: the codes of the manifest `warnings`, each one time, sorted.
     `nominal_fps` is `num/den`, rounded half up to 3 decimal places. Basis (1),
     [ADR-5XNA](5XNA-folder-layout-names-and-manifest.md) item 6 (exposure; warnings).
   - "A validator" is a reader. A reader gives `summary_stale` when `camera_label`,
     `display_rotation` or `nominal_fps` (after the same rounding) differs from the sidecar, or when
     `gaps` or `filled` differs from the `# end` line of a finished or repaired sidecar. Basis (3).

8. **Two writers of the manifest** (SFF-724, SFF-725, SFF-789, SFF-844; SFT-708, SFT-730). CHOICE.
   - Each writer of the manifest, also skellycam, reads it, changes it and writes it while it holds
     `.processing.lock`. Each writer keeps the members and the items of the other owner. freemocap
     starts the fold only after `state` is `finished`.
   - `.processing.lock` is an empty file. The lock is the file lock of the operating system on that
     file, not the existence of the file. A lock file that no process holds is not a lock, so no
     stale-lock rule is necessary. A reader ignores the file. Basis (2): freemocap at c27fc299,
     `freemocap/core/recording/parquet_storage/parquet_writer.py`, `recording_write_lock`, lines 28
     to 33 (`FileLock`, `timeout=0`). Confirmed in that file on 2026-11-16.

## Reason

- Each item removes a point at which two readers, or a reader and a golden result, can differ.
- The CHOICE items need the user. Each has one alternative, which is not rejected.

## Consequences

- New: the members `legacy.calibration` and `summary.warnings`, and the family `unknown`.
- skellycam must take `.processing.lock` when it writes the manifest.

## Evidence

- freemocap at c27fc299: `parquet_writer.py` (item 8).
- skellycam `dom/research` (local, not committed):
  `research/skellycam_recording/docs/legacy_release_inventory_20261115.md` section 3.

## Open work

[open-work.md](../open-work.md)
