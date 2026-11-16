# 0WTH — Spec draft v2 details, part 12: legacy era signals, link check parts, result values

**Status:** accepted, 2026-11-16 (user; review of the proposed details).

## Decision

This part holds items 30 to 36 of the proposals that
[ADR-0JVZ](0JVZ-spec-v2-details-part-9.md) introduces. The user accepted
them on 2026-11-16, with the recommended option of each CHOICE. Each alternative stays as a record.

30. **Legacy era signals** (SFF-876, SFF-878; legacy-annex.md; SFT-764; G15).
    - a. A V1i folder does not match the row V1e–V1h': v1.8.0 removed
      `run_reprojection_error_filtering`. So only the row V1i matches, and `ambiguous` is false.
      The annex says this in its row V1i. The case `v1i` of G15 has `tracking_parameters_model` and
      no `run_reprojection_error_filtering`.
    - b. "A TOML whose `cam_0` rotation is 0" means: each of the 3 values of `cam_0.rotation` has a
      magnitude of 1e-6 or less. The TOML is the one that SFF-880 gives with the state `present`.
      With another state, each TOML signal is absent.
    - c. In SFF-876, the v0.1.0 file is `synchronized_videos/timestamps/Camera_NNN_binary.npy`.

    Basis (2): the evidence below; (3) for the value 1e-6.

31. **Parts of the link checks** (SFF-872; SFT-710, SFT-763). A check has one part for each file,
    or pair of files, that its rule tests. The parts are:
    - `take_uuid`: one part for each of the manifest, each timing sidecar, each info JSON, the
      Parquet and the journal;
    - `camera_key`: the manifest with the video sidecars; with the capture info JSON; with the
      TOML; with the Parquet;
    - `frames`: the Parquet with each video sidecar; the row counts of the camera files (item 32);
    - `dimensions`: the Parquet with each camera file;
    - `rotation`: the capture info JSON alone; the manifest summary with each video sidecar;
    - `files`: the paths of the manifest; the file names of the Parquet;
    - `hashes`: the manifest with the TOML; the processing info JSON with the Parquet;
    - `calibration`: the manifest with the TOML.

    So, with no manifest, `camera_key` is `not_checked`, and `rotation` has only its capture info
    part. SFT-710 says this. Basis (1): [ADR-0XX2](0XX2-spec-v2-details-part-5.md) item 6c; (3).

32. **Row counts of the camera files** (SFF-754, SFF-872; SFT-763; G5, G6, G9). SFF-872 does not
    use the words "an unfinished take". The row-count part of `frames` compares the camera files
    with the state `finished`. A reader evaluates it when the take has two or more of them. A
    camera file that is `repaired`, `unfinished` or `damaged` is not in the comparison: a crash and
    a repair cut each file after its own last complete row. When the camera files that the reader
    reads have different values of `rows`, the multi-camera frames are the frames from 0 to the
    smallest `rows` minus 1. Basis (1): [ADR-W6HV](W6HV-spec-v2-details-part-3.md) item 2b; (3).

33. **`name` of a timing sidecar alone** (SFF-865, SFF-885; SFT-761, SFT-768). In `other_files`,
    the `name` of a timing sidecar alone is the path of the sidecar: `other_files` lists files that
    exist. In `files`, its `name` stays the path of the missing media file. Basis (3).

34. **Two values of `<rec>`** (SFF-868; SFT-710). When the sidecar names give two or more values,
    the reader uses the value of the video sidecar with the lowest `group_position`, as SFF-871
    does for a take key. A take with no video sidecar uses the audio sidecar. Basis (3).

35. **`fitted_ns` of an audio record** (SFF-779, SFF-784, SFF-885; SFT-727, SFT-729). It is the
    fitted time of the `first_sample` of the block (SFF-779), with the fit that the reader uses:
    the fit lines of a `finished` or `repaired` sidecar (item 28c), else the fit that the reader
    computes (SFF-784). It is null when the reader has no fit. This closes the open point of
    [ADR-E45D](E45D-spec-draft-v2-corrections-after-review.md) item 6. Basis (3).

36. **Pre-skip** (SFF-766; SFT-723). SFF-766 changes to: "Sample 0 of the audio is the first
    decoded sample after the pre-skip samples of `dOps`. A program that decodes the audio drops
    the pre-skip samples and applies no output gain." The Python reader of this package does not
    decode. Its `audio_details` gives the pre-skip, and SFT-723 decodes with PyAV. Basis (1):
    [ADR-G21H](G21H-gate-2-tests-location-and-interfaces.md) item 8.

## Reason

- Item 30: the era table must give one result for a V1i folder and for a TOML signal.
- Items 31 and 32: the state of each check must follow from the files that the take has.
- Items 33 to 35: each is one value of the reader result that two readers can fill differently.
- Item 36: SFF-766 told the reader to decode, and the accepted entry says that it does not.

## Evidence

- freemocap at the tags v1.7.4 and v1.8.2 (item 30a):
  `freemocap/data_layer/recording_models/post_processing_parameter_models.py`. At v1.7.4,
  `AniposeTriangulate3DParametersModel` has `run_reprojection_error_filtering` (line 16). At v1.8.2,
  no Python file has that name, and `ProcessingParameterModel` keeps `tracking_parameters_model`
  (line 41).
- skellycam `dom/research` (local, not committed):
  `research/skellycam_recording/docs/legacy_release_inventory_20261115.md`: the v0.1.0 session
  folder (item 30c), and section 3, "cam_0 rotation ≈ 0" (item 30b).

## Open work

[open-work.md](../open-work.md)
