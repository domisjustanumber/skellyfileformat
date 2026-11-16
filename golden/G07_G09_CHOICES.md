# Choices made for G7, G8 and G9 that the spec does not give

**Status: proposed. The user did not review this list.**

G7, G8 and G9 are copies of G3 ([SPEC.md Appendix A](../spec/SPEC.md#appendix-a-golden-folders)).
The scripts are `tools/goldgen/g07.py` (G7, and the helpers that G8 and G9 use),
`tools/goldgen/g08.py` and `tools/goldgen/g09.py`. The structure checks are in
`tools/tests/test_g07_g09.py`. No reader exists. The generator derives each expected result from
the rules of SPEC.md sections 5, 16, 20 and 23. It does not read the files to make the result.

G7, G8 and G9 copy each convention of [G01_CHOICES.md](G01_CHOICES.md)
([ADR-94YQ](../decisions/entries/94YQ-golden-g1-review-decisions.md) item 5) and each choice of
[G03_CHOICES.md](G03_CHOICES.md). This list does not repeat them. Each item gives the gap, the
choice and the alternative
([ADR-G21H](../decisions/entries/G21H-gate-2-tests-location-and-interfaces.md) item 5). Items 26 to
34 are gaps, contradictions and ambiguities of the spec. Items 35 to 37 are notes for the
supervisor.

## What the cases hold

Each case has the `<rec>` `g01_synthetic_take` and the `take_uuid` of G3. Each case has the bytes of
`golden/G03/take`, with these changes:

| Folder | Case | The change | Files with other bytes than G3 |
|---|---|---|---|
| G7 | `no_manifest` | No `recording_manifest.json` | none (one file less) |
| G7 | `other_take_manifest` | The manifest has `take_uuid` `00000000000040008000000000000701` | the manifest |
| G8 | `renamed` | The case folder is `renamed`, not `take` | none |
| G9 | `take_uuid` | The processing info JSON has `take_uuid` `00000000000040008000000000000901` | processing info, manifest |
| G9 | `camera_key` | `camera_configs` of the capture info JSON has another key for camera 1 | capture info, manifest |
| G9 | `frame_range` | The Parquet has 91 frames (`frame_number` 0 to 90). The camera files have 90 rows | Parquet, processing info, manifest |
| G9 | `row_counts` | Camera 0 has 89 rows, camera 1 has 90. Both files are `finished`. The Parquet has 89 frames | camera 0 MKV and CSV, Parquet, processing info, manifest |
| G9 | `dimensions` | The image reference of camera 1 has 128 × 96. The stored JPEG frames have 64 × 48 | Parquet, processing info, manifest |
| G9 | `rotation_in_configs` | The config of camera 1 has `"rotation": 90` | capture info, manifest |
| G9 | `unresolved_file` | The camera source of camera 1 has `video_filename` `g09_other_take.d20676.mkv` | Parquet, processing info, manifest |
| G9 | `stale_parquet_sha256` | `parquet_sha256` is the SHA-256 of a file with no bytes | processing info, manifest |
| G9 | `calibration_hash` | `calibration.sha256` of the manifest is the SHA-256 of a file with no bytes | manifest |
| G9 | `calibration_uuid` | `calibration.calibration_uuid` of the manifest is `00000000000040008000000000000902` | manifest |
| G9 | `recording_id` | The Parquet descriptor has `recording_id` `g09_other_take` | Parquet, processing info, manifest |

When a case changes a file, each hash that points at that file gets the new value: the `sha256` of
its manifest `files` item (SFF-723) and `parquet_sha256` (SFF-838). The only exceptions are the
vectors `stale_parquet_sha256` and `calibration_hash`. So each case has exactly one fault.

## The expected reader results

Each member that this section does not name has the value of the result of G3, in the same scope.

| Case | Scope `full` | Scope `player` | Requirement |
|---|---|---|---|
| `no_manifest` | `manifest` `missing`; take warning `manifest_missing`; `camera_key` and `calibration` `not_checked` | as `full`, and `files` also `not_checked` | SFF-731, SFF-867, SFF-872, SFF-892 |
| `other_take_manifest` | as `no_manifest`, but `manifest` `invalid`; `other_files` has the manifest, `invalid`, `take_fact_mismatch`; folder warning `orphan_file` | as `full`, and `files` also `not_checked` | SFF-731, SFF-867, SFF-889 |
| `renamed` | the bytes of the result of G3 | the bytes of the result of G3 | SFF-717, SFF-718, SFF-824, SFT-706 |
| `take_uuid` | `take_uuid` `mismatch` | `take_uuid` `mismatch` | SFF-872 |
| `camera_key` | `camera_key` `mismatch` | `camera_key` `mismatch` | SFF-872, SFF-803 |
| `frame_range` | `frames` `mismatch` | the result of G3 | SFF-872, SFF-827 |
| `row_counts` | `frames` `mismatch`; camera 0 has `rows` 89 and 89 `records` | camera 0 as in `full` | SFF-872, SFF-754 |
| `dimensions` | `dimensions` `mismatch` | the result of G3 | SFF-872, SFF-829 |
| `rotation_in_configs` | `rotation` `mismatch` | `rotation` `mismatch` | SFF-872, SFF-800 |
| `unresolved_file` | `files` `mismatch` | the result of G3 | SFF-872, SFF-826 |
| `stale_parquet_sha256` | `hashes` `mismatch`; take warning `stale_processing_info` | the result of G3 | SFF-872, SFF-874, SFF-892 |
| `calibration_hash` | `hashes` `mismatch` | the result of G3 | SFF-872, SFF-814 |
| `calibration_uuid` | `calibration` `mismatch` | the result of G3 | SFF-872, SFF-814 |
| `recording_id` | the Parquet item `invalid`, `take_fact_mismatch`, `["prerelease"]`; `dimensions` `not_checked` | the result of G3 | SFF-824, SFF-872, SFF-891 |

In `no_manifest` and `other_take_manifest`, the scope `full` evaluates these parts: `take_uuid`
(the 3 sidecars, the 2 info JSONs, the Parquet), `frames` (the Parquet and the row counts),
`dimensions`, `rotation` (only the capture info JSON), `files` (only the Parquet file names) and
`hashes` (only the processing info JSON with the Parquet). Each passes, so each of these checks is
`ok`.

In `recording_id`, the scope `full` does not evaluate a part that needs the Parquet. Each other
check keeps a part that passes: `take_uuid` (the manifest, the sidecars, the info JSONs), `camera_key`
(the sidecars, the capture info JSON, the TOML), `frames` (the row counts), `files` (the manifest
paths), `hashes` (the manifest with the TOML) and `calibration`. So each of them is `ok`.

## The choices

### All three folders

1. Appendix A gives no `<rec>` and no `take_uuid`. Choice: each case keeps the `<rec>` and the
   `take_uuid` of G3, which are those of G1. So each unchanged file has the bytes of G3.
   Alternative: a `<rec>` and a `take_uuid` for each folder, which changes each sidecar.
2. The README of the golden folders makes `<case>.truth.json` optional. Choice: G8 has
   `renamed.truth.json`, the truth file of G3, because G8 is a copy of G3. G7 and G9 have no truth
   file. No test of the clicks and the flashes names G7 or G9. Alternative: a truth file for each
   case.
3. The generator writes G3 with `g03.write_case` and then changes the files of the case. It writes
   a changed JSON file with the conventions of the golden folders (indent 2, one LF, the members in
   their order). Alternative: a full generator for each case.

### G7

4. The other `take_uuid` of `other_take_manifest` is free. Choice:
   `00000000000040008000000000000701`, with the bits of a UUID version 4 (G01_CHOICES.md item 2).
   It is the `take_uuid` of no device pair, so no take uses the manifest. Each other member of the
   manifest is the member of G3.
5. SFF-885 gives each `folder_files` item a `role`, and the manifest is the source of the roles. In
   a rebuild, no manifest gives a role. Choice: the role of the fixed name of SFF-731:
   `capture_info` for `<rec>_info.json`, `processing_info` for `<rec>_recording_info.json`,
   `tracking` for `<rec>_data.parquet`, and null for the TOML (G03_CHOICES.md item 28). So the
   `folder_files` of G7 are those of G3. Alternative: null for each item. **The user must decide.**
6. SFF-883 gives `may_contain_private_data` for a `missing` manifest, and not for an `invalid`
   manifest. Choice: the rule of a missing manifest, because the reader does not use an invalid
   manifest (SFF-867). The take has camera files, so the value is true. The `privacy` list of the
   invalid manifest also has items. So each reading gives true in G7.
7. Choice: the scope `player` reads the manifest of `other_take_manifest`, because it is a JSON
   file (SFF-892, the bullet on the mark of SFF-875). So `other_files` and `orphan_file` are the
   same in the two scopes.

### G8

8. Appendix A says "a folder with another name". Choice: the case folder `renamed`. The case
   folder of G3 is `take`. Each file inside it has the bytes of G3, and the three files beside it
   have the bytes of the files of G3. The generator runs `g03.build` and renames the four entries.

### G9: the files

9. Choice: the camera of each camera vector is camera 1 (`group_position` 1, label `d20676`).
   The only exception is `row_counts` (item 14).
10. **`take_uuid`.** Appendix A does not say which file holds the other `take_uuid`. A timing
    sidecar with another `take_uuid` makes a second take (SFF-866), and SFT-762 wants one take
    for each `take_uuid` of the sidecars. Choice: the processing info JSON, with
    `00000000000040008000000000000901`. Its item is in `folder_files`, `present`, because the
    manifest lists it (SFF-885). The vector is in a JSON file, so the two scopes show it.
    Alternative: the capture info JSON, or the Parquet descriptor (the scope `full` only). See
    item 26.
11. **`camera_key`.** Choice: the key of camera 1 in `camera_configs` of the capture info JSON is
    the key with its last hexadecimal character changed. The first 6 characters stay, so the
    `camera_label` of the config stays correct (SFF-720). The order of the keys stays
    ([ADR-W389](../decisions/entries/W389-format-rules-from-the-golden-conventions.md) item 4). The
    paths of the `privacy` list of the manifest get the new key (SFF-881). Alternative: a
    camera table of the TOML or a camera source of the Parquet with another key. These need a
    rule that the spec does not give (items 27 and 28).
12. **`frame_range`.** Choice: the Parquet has one frame more than the camera files: 91 frames,
    `sample_count` 91, `frame_number` 0 to 90. The time of frame 90 of each camera is the time of
    frame 89 plus the last step of that camera. Each row rule of the part stays true.
    Alternative: each `frame_number` plus 1.
13. **`dimensions`.** Choice: `width` 128 and `height` 96 (2 times the stored size) in the image
    reference `camera:d20676:image`. `camera_geometry` keeps `image_size` [64, 48], so the take has
    no `calibration_mismatch` (SFF-837). See item 29.
14. **`row_counts`.** Choice: camera 0 lost its last frame. Its camera file, its sidecar, its fit
    (`pos_last` 88) and its `# end` line have 89 rows, and the file is `finished`. Camera 1 keeps
    90 rows. Camera 1 has the last arrival, so the summary of the manifest stays correct
    (SFF-728). The Parquet has 89 frames: the multi-camera frames of SFF-754
    ([ADR-W6HV](../decisions/entries/W6HV-spec-v2-details-part-3.md) item 2). So the Parquet part
    of `frames` passes, and only the row-count part fails. Alternative: a Parquet of 90 frames,
    which also fails the Parquet part.
15. **`rotation_in_configs`.** SFF-800 forbids `rotation` in a camera config and gives no form.
    Choice: `"rotation": 90`, the last member of the config of camera 1. See item 30.
16. **`unresolved_file`.** Appendix A says "an unresolved file name". Choice: `video_filename` of
    the camera source of camera 1 is `g09_other_take.d20676.mkv`, which names no file in the media
    folder (SFF-826). `timing_filename` stays correct. The vector is in the Parquet, so the scope
    `player` does not show it. Alternative: a manifest path that names no file. Then the item is
    `missing` in `folder_files`, in the two scopes.
17. **`stale_parquet_sha256`.** Choice: `parquet_sha256` is the SHA-256 of a file with no bytes
    (`e3b0c442…b855`). The Parquet is the Parquet of G3. Alternative: the SHA-256 of an older
    Parquet, which needs a second Parquet.
18. **`calibration_hash`.** Choice: `calibration.sha256` of the manifest is the SHA-256 of a file
    with no bytes. The TOML is the TOML of G3. Alternative: a changed TOML with the old hash. Then
    the TOML needs a new `calibration_uuid` (SFF-810), and that is a second vector.
19. **`calibration_uuid`.** Choice: only `calibration.calibration_uuid` of the manifest changes, to
    `00000000000040008000000000000902`. `summary.calibration` keeps the values of the TOML
    (SFF-728). Alternative: a TOML with another `calibration_uuid`, which changes its hash and so
    the check `hashes` too.
20. **`recording_id`.** Choice: the descriptor has `recording_id` `g09_other_take`. The processing
    info JSON keeps `recording_id` `g01_synthetic_take` and has the correct `parquet_sha256` of the
    new Parquet. Only the Parquet has the fault.

### G9: the expected results

21. SFT-763 wants `mismatch` for each vector. Choice: each case changes exactly one check. The take
    warning `stale_processing_info` is the only new warning (SFF-874). A wrong calibration hash and
    a wrong `calibration_uuid` give no warning: SFF-887 names none for them.
22. Choice: the `invalid` Parquet of `recording_id` keeps the file warning `prerelease`, as the
    `invalid` sidecars of G11 do. Its descriptor has `format_prerelease` 1 (SFF-891). See item 32.
23. Choice: a vector in the TOML or the Parquet gives the `player` result of G3 (SFF-892;
    [ADR-DM9S](../decisions/entries/DM9S-spec-v2-details-part-7.md); SFT-767 "a test of the scope
    `full` only").
24. In `row_counts`, the `files` item of camera 0 has `rows` 89 and the 89 `records` of its rows.
    Its warnings stay `["prerelease"]`: camera 0 has no gap.
25. In `recording_id`, the part of `hashes` "the processing info JSON with the Parquet" is not
    evaluated, because the Parquet is `invalid` (SFF-872). The hash is correct, so the check is
    `ok` with each reading.

### Gaps, contradictions and ambiguities of the spec

26. **SFF-889, SFF-885, SFF-872: a folder file with another `take_uuid`.** SFF-889 puts "a folder
    file of this format with no take" in `other_files`, as `invalid`, with `take_fact_mismatch`.
    SFF-885 puts an item in `folder_files` for each `files` item of the manifest. The spec does not
    say which rule wins for a listed folder file whose `take_uuid` is the ID of no take. If the
    file is `invalid`, SFF-872 does not evaluate its part, and the check `take_uuid` is `ok`. That
    contradicts SFT-763 ("each vector of G9 gives `mismatch`"). The choice of item 10 (`present`,
    `mismatch`) follows SFT-763. **The user must decide.**
27. **SFF-872, `frames` and `dimensions`: the link of a Parquet camera source to its camera
    file.** The spec does not say how a reader links a camera source to its camera file: by
    `camera_key`, by `camera_label` (the source name `camera:<label>`) or by `video_filename`. G9
    avoids the question: in each case, the camera sources keep the key and the label of G3.
28. **SFF-837: a camera that the reader cannot link.** SFF-837 links the cameras of
    `camera_geometry` and of the TOML by `camera_key`. It does not say if a camera with no match
    gives `calibration_mismatch`. So G9 does not change a key in the TOML or in the Parquet.
29. **SFF-872, `dimensions`.** The rule says "the image width and height of each Parquet camera
    source". A camera source definition (SFF-826) has no size. The size is in the image reference
    `camera:<label>:image` (SFF-829) and in `image_size` of `camera_geometry`. The choice of item
    13 uses the image reference. **The user must decide** if the check also tests `image_size`.
30. **SFF-800 and SFF-887: a member that SFF-800 forbids.** The reason `bad_schema` names a file
    "without the members ... of its section". It does not name a file with a member more. SFF-709
    ignores an unknown member only for a higher `minor`. So the spec does not say if a 2.0 capture
    info JSON with `rotation` is `invalid`. If it is `invalid`, SFF-872 does not evaluate the part,
    and the check `rotation` is `not_checked`, which contradicts SFT-763. Choice: the file is
    `present`, and the part fails.
31. **SFT-710 and SFF-892.** SFT-710 says that, with no manifest, "`hashes` and `files` have only
    their Parquet parts, and they are `ok`". It names no scope. For the scope `player`, SFF-892
    gives `not_checked` for the two checks. G7 follows SFF-892.
32. **SFF-891: `prerelease` on an `invalid` file.** SFF-891 does not say if an `invalid` file keeps
    the warning `prerelease`. G11 keeps it for an `invalid` sidecar. G9 does the same for the
    Parquet (item 22).
33. **SFF-883: an `invalid` manifest.** See item 6. The spec gives the rule only for a `missing`
    manifest.
34. **Section 14: no reader rule for `recording_id` and `parquet` of the processing info JSON.**
    SFF-824 checks `recording_id` of the descriptor only. The spec gives no reader result for a
    processing info JSON with a wrong `recording_id` or `parquet`. G9 has no such vector.

### Notes for the supervisor

35. **`golden/README.md`** says "Only G1 exists" and lists only the G1 scripts. This work does not
    change that file (the task gave this agent no permission). It must list G7 to G9 and this
    file.
36. **`tools/goldgen/g03.py`.** `write_case` takes no camera input and no hook for the run. So
    `g09.py` writes the short camera 0 of `row_counts` with `common.write_take` in a temporary
    folder, copies its device pair, and writes the Parquet again with `g03.run_and_rows`. A
    parameter `cameras` of `write_case` and a hook for the run would make this shorter.
37. **The size.** G7 has about 690 kB, G8 about 350 kB and G9 about 3.8 MB, nearly all from the
    media files of G3. Appendix A asks for copies of G3, so each case holds the whole take.
    Alternative: a smaller base take for G9, which needs a second set of expected results.
