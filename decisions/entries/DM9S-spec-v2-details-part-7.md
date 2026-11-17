# DM9S — Spec draft v2 details, part 7: JavaScript scope, privacy, identity, ranges, smaller points

**Status:** absorbed into
[`spec/SPEC.md#2-conventions`](../../spec/SPEC.md#2-conventions),
[`spec/SPEC.md#6-camera-files`](../../spec/SPEC.md#6-camera-files),
[`spec/SPEC.md#8-video-timing-sidecar`](../../spec/SPEC.md#8-video-timing-sidecar),
[`spec/SPEC.md#11-clocks-the-fit-and-reader-timing`](../../spec/SPEC.md#11-clocks-the-fit-and-reader-timing),
[`spec/SPEC.md#12-writing-crashed-files-and-repair`](../../spec/SPEC.md#12-writing-crashed-files-and-repair),
[`spec/SPEC.md#14-processing-info-json`](../../spec/SPEC.md#14-processing-info-json),
[`spec/SPEC.md#17-realtime-journal`](../../spec/SPEC.md#17-realtime-journal),
[`spec/SPEC.md#181-blender`](../../spec/SPEC.md#181-blender),
[`spec/SPEC.md#183-exports`](../../spec/SPEC.md#183-exports),
[`spec/SPEC.md#21-legacy-folders`](../../spec/SPEC.md#21-legacy-folders),
[`spec/SPEC.md#22-privacy-and-safety`](../../spec/SPEC.md#22-privacy-and-safety),
[`spec/SPEC.md#23-the-reader-result`](../../spec/SPEC.md#23-the-reader-result),
[`spec/SPEC.md#appendix-a-golden-folders`](../../spec/SPEC.md#appendix-a-golden-folders),
[`spec/SPEC.md#appendix-b-player-guidance-informative`](../../spec/SPEC.md#appendix-b-player-guidance-informative),
[`spec/conformance.md#the-reader-result-section-23`](../../spec/conformance.md#the-reader-result-section-23),
2026-11-17 (commit to main; was accepted, 2026-11-16 (user; review of the proposed details, each item, with the
recommended option of each CHOICE)).

## Decision

This part holds items 14 to 17 of the proposals that [ADR-W6HV](W6HV-spec-v2-details-part-3.md)
introduces (items 1 and 2, and the meaning of "Basis" and "CHOICE"). The other parts are
[ADR-Q4BK](Q4BK-spec-v2-details-part-4.md) (3 and 4), [ADR-0XX2](0XX2-spec-v2-details-part-5.md)
(5 to 8), [ADR-ATW0](ATW0-spec-v2-details-part-6.md) (9 to 13) and
[ADR-72QQ](72QQ-spec-v2-details-part-8.md) (18 and 19). The user accepted
each item of this part on 2026-11-16, with the recommended option of each CHOICE. The recommended
option is the text of the item.

14. **JavaScript reader scope** (SFF-892; SFT-768, SFT-769). CHOICE. The JavaScript reader gives
    the result of the scope `player`. In it, `frames`, `dimensions`, `hashes` and `calibration` are
    `not_checked`, and each other check has only the parts that need no TOML, Parquet or journal.
    The Python reader with the scope `player` gives the same bytes. A G9 vector that is only in the
    TOML, the Parquet or the journal is a test of the scope `full`. Basis (3). (corrected on 2026-11-17:
    [ADR-0JVZ](0JVZ-spec-v2-details-part-9.md) item 21 replaced the comparison that left out each check that is
    `not_checked` in the JavaScript result.)

15. **Privacy and safety** (SFF-881, SFF-883, SFF-884; SFT-766, SFT-767; G16).
    - a. `media_shows_people` is true when the take has a camera file, an audio file or a Parquet.
      The no-manifest rule of SFF-883 uses the same list. Basis (1),
      [ADR-T8PK](T8PK-privacy-notice-and-no-code-in-files.md) item 2.
    - b. `fields` holds exactly these, when the file exists and the value is not null. Capture info
      JSON, for each camera: `user_name` (`user_entered_name`), `device/model` and `device/os_name`
      (`device_name`), `device/serial` (`serial_number`), `device/port_path` (`device_path`), `device/os_device_id` (`device_path`,
      [ADR-70VP](70VP-camera-identity-forms-and-remembered-keys.md) item 1); and
      `/audio/device_name` (`device_name`). Each timing sidecar: `utc_offset_min` (`time_zone`).
      Manifest: `/recording_name` and each `user_name` of the summary (`user_entered_name`), and
      each `model` of the summary (`device_name`, [ADR-1HH0](1HH0-lock-startup-repair-and-reader-model-check.md) item 3; corrected on 2026-11-17). TOML:
      `metadata.alignment_recording_id` (`user_entered_name`). Basis (3).
    - c. CHOICE. A reader finds a pickle by the name suffix `.pkl` or `.pickle`, in any case, in the
      root and the media folder. It lists the file in `other_files` as `invalid`, with
      `code_in_file`. For each NPY or NPZ file that the manifest lists, it reads only the NPY header.
      An object `descr` makes the `folder_files` item `invalid`, with `code_in_file`. Basis (3).

16. **Identity and ranges** (SFF-701, SFF-752, SFF-754, SFF-767; SFT-717, SFT-735; G11).
    - a. CHOICE. The identity string is the first of the four forms of [ADR-70VP](70VP-camera-identity-forms-and-remembered-keys.md)
      item 1 that applies: `serial`, `port`, `device` or `assigned` (SFF-752; corrected on 2026-11-17: the
      two forms `serial` and `port` were replaced). The values
      are the texts of `device` in the capture info JSON, with `0000` for an ID that is null. The
      hash input is its UTF-8 bytes. Basis (1), [ADR-VPD9](VPD9-spec-draft-v2-details.md) item 4,
      and (3).
    - b. Each integer of a row that is not a time is from 0 to 2^53 − 1. A reader refuses another
      value (`bad_metadata`). A camera file has at most 2^31 frames. Basis (3).
    - c. "A file of this format" has the definition of item 4a.

17. **Smaller points.**
    - a. The processing info JSON keeps `channel`. Its value is the `kind` of the descriptor
      channel. Basis (2): freemocap at c27fc299, `freemocap/core/recording/recording_info.py`, line
      25; (1)
      [ADR-3D33](3D33-spec-draft-v2-details-folder-files.md) item 3.
    - b. `<route>` is `parquet_segments` or `parquet_constraints`. Basis (2): the folder files
      inventory, section 4.4.
    - c. CHOICE. In the export inventory, `version` is 5. `location` is `exports`. `format` is one
      of `tall_csv`, `static_tall_csv`, `wide_csv`, `static_wide_csv`, `npy`, `npz`, `notebook` and
      `metadata`. `snapshots` is an object with one snapshot for each `source_sha256`. `csv` is
      `{encoding, delimiter, absent, null, float_precision, column_order}`. The spec copies the
      snapshot members from the folder files inventory, section 4.1. Basis (2), that inventory.
    - d. In SFF-785, "the samples that the file holds" are the samples of the complete fragments,
      minus the pre-skip. Basis (1), [ADR-92TM](92TM-opus-audio-in-fragmented-mp4.md) items 8 and
      10.
    - e. [ADR-Q9X2](Q9X2-realtime-tracking-journal.md) item 2 (the journal writer is a node of its
      own) is a freemocap program rule. It is not in the format. SFF-787, SFF-788 and SFF-840 hold
      its file rules. [ADR-2C9V](2C9V-whole-take-folder-scope-and-package.md) item 7: SFF-737 gets
      the sentence "A take folder holds no overlay file". "The player draws the frame label" is a
      skellycam program rule.
    - f. Appendix A says that G13 is the state after the fold and before the verified delete. G13
      gets both info JSONs. Basis (3).

## Reason

- Each item removes a point at which two readers, or a reader and a golden result, can differ.
- The CHOICE items need the user. Each has one alternative, which is not rejected.

## Evidence

- skellycam at 169caf637: `skellycam/core/device_detection/detect_cameras_devices.py`, lines 44 to
  54 (the `camera_id` of today).
- freemocap at c27fc299: `recording_info.py` (item 17a).
- skellycam `dom/research` (local, not committed):
  `research/skellycam_recording/docs/folder_files_inventory_20261116.md` sections 1 and 4.

## Open work

[open-work.md](../open-work.md)
