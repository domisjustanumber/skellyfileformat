# DM9S — Spec draft v2 details, part 7: JavaScript scope, privacy, identity, ranges, smaller points

**Status:** proposed, 2026-11-16 (agent; ambiguous points from the independent review).

## Decision

This part holds items 14 to 17 of the proposals that [ADR-W6HV](W6HV-spec-v2-details-part-3.md)
introduces (items 1 and 2, and the meaning of "Basis" and "CHOICE"). The other parts are
[ADR-Q4BK](Q4BK-spec-v2-details-part-4.md) (3 and 4), [ADR-0XX2](0XX2-spec-v2-details-part-5.md)
(5 to 8), [ADR-ATW0](ATW0-spec-v2-details-part-6.md) (9 to 13) and
[ADR-72QQ](72QQ-spec-v2-details-part-8.md) (18 and 19).

14. **JavaScript reader scope** (SFF-892; SFT-768, SFT-769). CHOICE. With the parts of item 6c, the
    JavaScript reader gives `not_checked` for `frames`, `dimensions`, `hashes` and `calibration`. It
    evaluates `take_uuid`, `camera_key`, `rotation` and `files` on the files that it reads. The
    byte-for-byte comparison leaves out a check that is `not_checked` in the JavaScript result. A
    G9 vector that is only in the TOML, the Parquet or the journal is a Python test. Basis (3).

15. **Privacy and safety** (SFF-881, SFF-883, SFF-884; SFT-766, SFT-767; G16).
    - a. `media_shows_people` is true when the take has a camera file, an audio file or a Parquet.
      The no-manifest rule of SFF-883 uses the same list. SFF-881 names only a camera file now, and
      SFF-883 names a camera file or a capture info JSON. Basis (1),
      [ADR-T8PK](T8PK-privacy-notice-and-no-code-in-files.md) item 2.
    - b. `fields` holds exactly these, when the file exists and the value is not null. Capture info
      JSON, for each camera: `user_name` (`user_entered_name`), `device/model` and `device/os_name`
      (`device_name`), `device/serial` (`serial_number`), `device/port_path` (`device_path`); and
      `/audio/device_name` (`device_name`). Each timing sidecar: `utc_offset_min` (`time_zone`).
      Manifest: `/recording_name`, and each `user_name` and `model` of the summary. TOML:
      `metadata.alignment_recording_id` (`user_entered_name`). Basis (3).
    - c. CHOICE. A reader finds a pickle by the name suffix `.pkl` or `.pickle`, in any case, in the
      root and the media folder. It lists the file in `other_files` as `invalid`, with
      `code_in_file`. For each NPY or NPZ file that the manifest lists, it reads only the NPY header.
      An object `descr` makes the `folder_files` item `invalid`, with `code_in_file`. Basis (3).

16. **Identity and ranges** (SFF-701, SFF-752, SFF-754, SFF-767; SFT-717, SFT-735; G11).
    - a. CHOICE. The identity string is `<vendor_id>:<product_id>:serial:<serial>`, or
      `<vendor_id>:<product_id>:port:<port_path>` when the device gives no serial. The four values
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
      gets both info JSONs. Appendix A lists no info JSON in G13 now. Basis (3).

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
